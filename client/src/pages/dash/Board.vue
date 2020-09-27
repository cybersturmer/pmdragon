<template>
  <q-page class="flex q-layout-padding">
    <div class="full-width row items-stretch">
      <!-- Here we gonna put information about sprint and view controls -->

      <div class="full-width row q-pa-sm items-center">
        <div class="text-h5 col-auto q-mr-md">
          <!-- Sprint name -->
          {{ sprint.title }}
        </div>
        <div class="text-h6 col-auto">
          <!-- Days till the end of sprint remaining and dates on hover -->
          <q-icon name="av_timer"></q-icon>
          <span>&nbsp;{{ days_remaining }} days remaining</span>
        </div>
        <div class="col-auto">
          <q-btn size="sm"></q-btn>
        </div>
        <!-- Sprint complete button -->
        <!-- Edit sprint button -->
      </div>

      <div
        v-for="issue_state in issue_states"
        :key="issue_state.id"
        class="col bg-primary full-height q-ma-sm text-center overflow-hidden">
        <!-- Column for head of column and state column -->

        <div class="q-pa-sm">
          <!-- Printable HEAD of column -->
          {{ issue_state.title | capitalize }}
        </div>

        <!--  Block of main state info  -->
        <div class="bg-secondary full-height">

          <q-scroll-area class="fit full-height">

            <draggable
              :value="issuesByState(issue_state.id)"
              @change="handleIssueStateChanging($event, issue_state.id)"
              class="full-height overflow-hidden-y"
              group="issues">

              <transition-group
                type="transition"
                :name="'flip-list'"
                tag="div"
                class="fit full-height q-pa-sm overflow-hidden-y"
                style="min-height: calc(100vh - 160px);
                       border: 1px dashed var(--q-color-accent)">

                <IssueBoard
                  v-for="issue in issuesByState(issue_state.id)"
                  :key="issue.id"
                  :id="issue.id"
                  :title="issue.title"/>

              </transition-group>

            </draggable>

          </q-scroll-area>

        </div>
      </div>
    </div>
  </q-page>
</template>

<script>
import draggable from 'vuedraggable'
import { date } from 'quasar'
import { unWatch } from 'src/services/util'
import IssueBoard from 'src/components/IssueBoard.vue'
import { SPRINT_REMAINING_UNIT } from 'src/services/masks'

export default {
  name: 'BoardView',
  components: {
    IssueBoard,
    draggable
  },
  computed: {
    issue_states: function () {
      return this.$store.getters['issues/ISSUE_STATES_BY_CURRENT_PROJECT']
    },
    issue_types: function () {
      return this.$store.getters['issues/ISSUE_TYPES_BY_CURRENT_PROJECT']
    },
    issues: function () {
      return this.$store.getters['issues/SPRINTS_BY_CURRENT_PROJECT']
    },
    sprint: function () {
      return this.$store.getters['issues/SPRINT_STARTED_BY_CURRENT_PROJECT']
    },
    days_remaining: function () {
      const startedAt = this.sprint.started_at
      const finishedAt = this.sprint.finished_at

      return date.getDateDiff(startedAt, finishedAt, SPRINT_REMAINING_UNIT)
    }
  },
  methods: {
    issuesByState: function (stateId) {
      return this.$store.getters['issues/SPRINT_STARTED_BY_CURRENT_PROJECT_ISSUES']
        .filter((issue) => issue.state_category === stateId)
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
    }
  },
  filters: {
    capitalize: function (value) {
      if (!value) return ''
      value = value.toString()
      return value.toUpperCase()
    }
  },
  mounted () {
    this.$store.dispatch('issues/INIT_ISSUE_TYPES')
    this.$store.dispatch('issues/INIT_ISSUE_STATES')
    this.$store.dispatch('issues/INIT_SPRINTS')
    this.$store.dispatch('issues/INIT_ISSUES')
  }
}
</script>
<style lang="scss">
  .flip-list-move {
    transition: transform 0.3s;
  }
</style>
