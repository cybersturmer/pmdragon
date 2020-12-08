<template>
  <q-page class="flex q-layout-padding overflow-hidden">
    <div v-if="sprint" class="full-width row items-stretch">
      <!-- Here we gonna put information about sprint and view controls -->

      <div class="full-width row q-pa-sm">
        <div class="col">
          <span class="text-h5 q-mr-md">
            <!-- Sprint name -->
            {{ sprint.title }}
          </span>
          <span class="xs-hide sm-hide md-hide text-subtitle1 text-amber q-mr-md">
            <!-- Sprint goal -->
            ( {{ sprint.goal }} )
          </span>

        </div>
        <div class="col text-right">
          <span class="text-subtitle1 q-mr-md">
            <!-- Days till the end of sprint remaining and dates on hover -->
            <q-icon name="access_time"></q-icon>
            <span :title="sprintRange">&nbsp;{{ daysRemainingText }} </span>
          </span>
          <StartCompleteSprintButton size="sm" :sprint="sprint"/>
          <q-btn
            dark
            outline
            size="sm"
            color="amber"
            icon-right="edit"
            class="xs-hide sm-hide float-right q-ml-md"
            @click="editSprintDialog(sprint)"
          />
        </div>
        <!-- Sprint complete button -->
        <!-- Edit sprint button -->
      </div>

      <div class="row full-height full-width">
        <!-- Container for issue status columns -->
        <div
          v-for="issue_state in issueStates"
          :key="issue_state.id"
          class="col bg-primary q-ma-sm">
          <!-- Column for head of column and state column -->

          <div class="q-pa-sm text-center text-uppercase" style="border: 1px solid #343434">
            <!-- Printable HEAD of column -->
            {{ issue_state.title }}&nbsp;&nbsp;&nbsp;{{ issuesByStateAmount(issue_state.id) }}
            <q-icon v-if="issue_state.is_done"
                    name="done"
                    color="positive"
                    class="q-ml-sm"
            />

          </div>

          <!--  Block of main state info  -->
          <div class="bg-secondary full-height">

            <q-scroll-area class="fit">

              <draggable
                :value="issuesByState(issue_state.id)"
                v-bind="dragOptions"
                @change="handleIssueStateChanging($event, issue_state.id)"
                class="full-height overflow-hidden-y">

                <transition-group
                  type="transition"
                  :name="'flip-list'"
                  tag="div"
                  class="fit full-height q-pa-sm overflow-hidden-y"
                  style="min-height: calc(100vh - 190px);
                       border: 1px dashed var(--q-color-accent)">

                  <IssueBoard
                    v-for="issue in issuesByState(issue_state.id)"
                    @click.native="editIssueDialog(issue)"
                    :key="issue.id"
                    :issue="issue"
                    :assignee="getAssigneeById()"
                  />
                </transition-group>
              </draggable>
            </q-scroll-area>
          </div>
        </div>
      </div>
    </div>
    <div v-if="!sprint" class="full-width q-pa-md text-center">
      <div class="text-h5"><q-icon name="history"/>&nbsp;You have not started a sprint.</div>
      <span class="text-subtitle1">Go to
        <router-link :to="{ path: 'backlog' }" class="text-amber">
          Backlog page
        </router-link> and start a sprint to continue...</span>
    </div>
  </q-page>
</template>

<script>
import draggable from 'vuedraggable'
import { updateSprintMixin } from 'src/pages/mixins/update_sprint'
import { date } from 'quasar'
import { unWatch } from 'src/services/util'
import IssueBoard from 'src/components/IssueBoard.vue'
import { DATE_MASK, SPRINT_REMAINING_UNIT } from 'src/services/masks'
import SprintEditDialog from 'components/dialogs/SprintEditDialog.vue'
import StartCompleteSprintButton from 'src/components/StartCompleteSprintButton.vue'
import IssueEditDialog from 'components/dialogs/IssueEditDialog.vue'
import { editIssueData } from 'pages/mixins/edit_issue_data'

export default {
  name: 'BoardView',
  components: {
    StartCompleteSprintButton,
    // eslint-disable-next-line vue/no-unused-components
    IssueEditDialog,
    // eslint-disable-next-line vue/no-unused-components
    SprintEditDialog,
    IssueBoard,
    draggable
  },
  mixins: [updateSprintMixin, editIssueData],
  computed: {
    dragOptions () {
      return {
        animation: 200,
        group: 'issues',
        disabled: false,
        ghostClass: 'ghost'
      }
    },
    issueStates: function () {
      return this.$store.getters['issues/ISSUE_STATES_BY_CURRENT_PROJECT']
    },
    issueTypes: function () {
      return this.$store.getters['issues/ISSUE_TYPES_BY_CURRENT_PROJECT']
    },
    issues: function () {
      return this.$store.getters['issues/SPRINTS_BY_CURRENT_PROJECT']
    },
    sprint: function () {
      return this.$store.getters['issues/CURRENT_SPRINT']
    },
    daysAmount () {
      const startedAt = this.sprint.started_at
      const finishedAt = this.sprint.finished_at

      return date.getDateDiff(finishedAt, startedAt, SPRINT_REMAINING_UNIT)
    },
    daysRemaining: function () {
      const today = new Date()
      const finishedAt = this.sprint.finished_at

      return date.getDateDiff(finishedAt, today, SPRINT_REMAINING_UNIT)
    },
    daysRemainingText: function () {
      if (this.daysRemaining > this.daysAmount) {
        return 'Will start soon...'
      } else {
        return this.daysRemaining > 0 ? this.daysRemaining + ' days remaining' : '0 days remaining'
      }
    },
    sprintRange: function () {
      const startedAt = date.formatDate(this.sprint.started_at, DATE_MASK)
      const finishedAt = date.formatDate(this.sprint.finished_at, DATE_MASK)
      return `${startedAt} - ${finishedAt}`
    }
  },
  methods: {
    getAssigneeById: function (assigneeId) {
      return this.$store.getters['auth/PERSON_BY_ID'](assigneeId)
    },
    issuesByState: function (stateId) {
      return this.$store.getters['issues/SPRINT_STARTED_BY_CURRENT_PROJECT_ISSUES']
        .filter((issue) => issue.state_category === stateId)
    },
    issuesByStateAmount: function (stateId) {
      return this.issuesByState(stateId).length
    },
    handleIssueAdded: function (event, issueStateId) {
      /** Handling added in Issues State **/
      const updatedElement = unWatch(event.added.element)
      updatedElement.state_category = issueStateId

      this.$store.dispatch('issues/UPDATE_ISSUE_STATE', updatedElement)
    },
    handleCommonMoved: function (issuesList, event) {
      /** Handle moving - common function **/

      const immutableList = unWatch(issuesList)

      immutableList
        .splice(event.moved.newIndex, 0, immutableList
          .splice(event.moved.oldIndex, 1)[0])

      const ordering = []
      immutableList.forEach((issue, index) => {
        ordering.push(
          {
            id: issue.id,
            ordering: index
          }
        )
      })

      return { list: immutableList, ordering }
    },
    handleStateMoved (event, stateId) {
      /** Handling moving inside of state **/
      const issuesList = this.issuesByState(stateId)
      const handled = this.handleCommonMoved(issuesList, event)

      this.$store.dispatch('issues/UPDATE_ISSUES_ORDERING', handled.ordering)
    },
    handleIssueStateChanging: function (event, issueStateId) {
      /** Handling moving inside of states **/
      const isAdded = ('added' in event)
      const isRemoved = ('removed' in event)
      const isMoved = ('moved' in event)

      switch (true) {
        case isAdded:
          this.handleIssueAdded(event, issueStateId)
          break
        case isRemoved:
          break
        case isMoved:
          this.handleStateMoved(event, issueStateId)
          break
        default:
          throw new Error('This error should not occurred')
      }
    },
    editIssueDialog (item) {
      this.$q.dialog({
        parent: this,
        dark: true,
        title: 'Issue ',
        component: IssueEditDialog,
        issue: item,
        issueStates: this.issueStates,
        issueTypes: this.issueTypes,
        participants: this.participants,
        $store: this.$store
      })
    },
    editSprintDialog (item) {
      this.$q.dialog({
        dark: true,
        component: SprintEditDialog,
        id: item.id,
        title: item.title,
        goal: item.goal,
        startedAt: item.started_at,
        finishedAt: item.finished_at
      })
        .onOk((data) => {
          this.$store.dispatch('issues/EDIT_SPRINT', data)
        })
    }
  }
}
</script>
<style lang="scss">
  .flip-list-move {
    transition: transform 0.3s;
  }

  .no-move {
    transition: transform 0s;
  }

  .ghost {
    opacity: 0.5;
    background: rgba(255, 255, 255, 0.6);
  }
</style>
