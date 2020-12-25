<template>
  <q-page class="flex q-layout-padding">
    <div class="column full-width">
      <div class="row q-pa-sm">
        <div class="col-8">
          <BlockHeader title="Sprints"/>
        </div>
        <div class="col-4">
          <q-btn
            dark
            outline
            size="sm"
            color="amber"
            label="Create Sprint"
            class="float-right"
            @click="createSprint"
          />
        </div>
      </div>
      <div class="col bg-primary">
        <q-scroll-area
          dark
          class="rounded-borders"
          style="height: 100%; padding: 1.25rem; border: 1px solid #606060;">
            <div
              v-for="(sprint, index) in sprints"
              :key="sprint.id">
              <div class="row q-pa-sm">
                <div class="col-8">
                  <div class="h6 text-amber">
                    {{ sprint.title }} - {{ sprint.goal }} - (&nbsp;{{ sprint.issues.length }} issues&nbsp;)
                  </div>
                </div>
                <div class="col-4 text-right">
                  <StartCompleteSprintButton
                    v-if="index === 0"
                    :sprint="sprint"
                  />
                  <SprintMorePopupMenu
                    :sprintId="sprint.id"
                    v-on:edit="editSprintDialog(sprint)"
                    v-on:remove="removeSprintDialog(sprint)"
                  />
                </div>
              </div>
              <div class="q-card--bordered q-pa-sm"
                   style="border: 1px dashed #606060; min-height: 67px;">
                <div v-if="!areSprintIssues(sprint.id)"
                     class="text-center text-amber q-pt-md">
                  Plan sprint by dropping issues here.
                </div>
                <draggable
                  :value="sprintIssues(sprint.id)"
                  v-bind="dragOptions"
                  @change="handleDraggableEvent($event, dragTypes.SPRINT, sprint.id)"
                >
                  <transition-group type="transition" name="flip-list" tag="div">
                    <IssueBacklog
                      v-for="issue in sprintIssues(sprint.id)"
                      :key="issue.id"
                      :issue="issue"
                      @click.native="editIssueDialog(issue)"
                    />
                  </transition-group>
                </draggable>
              </div>
            </div>
        </q-scroll-area>
      </div>
      <div class="row q-pa-sm">
        <div class="col">
          <BlockHeaderInfo title="Backlog" :info="backlogIssuesLength"/>
        </div>
      </div>
      <div class="col" v-if="backlogIssues">
        <q-scroll-area
          dark
          class="rounded-borders bg-primary q-pa-sm"
          style="height: calc(100% - 35px); border: 1px solid #606060;">
          <draggable
            :value="backlogIssues"
            v-bind="dragOptions"
            @change="handleDraggableEvent($event, dragTypes.BACKLOG, backlog.id)"
            style="padding: 10px; min-height: 67px;">
            <transition-group type="transition" name="flip-list" tag="div">
              <IssueBacklog
                v-for="issue in backlogIssues"
                :key="issue.id"
                :issue="issue"
                @click.native="editIssueDialog(issue)"
              />
            </transition-group>
          </draggable>
        </q-scroll-area>
        <q-card dark
                bordered
                square
                class="my-card text-white shadow-3 absolute-bottom card-no-padding q-pa-none"
                style="margin: 0.3em"
        >
          <q-card-section style="padding: 0">
            <q-input
              v-model="formData.title"
              @keyup.enter="createIssue"
              square
              dense
              dark
              filled
              placeholder="Add Issue">
              <template v-slot:append>
                <q-btn @click="createIssue"
                       :disable="!isCreateIssueButtonEnabled"
                       dense
                       rounded
                       flat
                       icon="add"/>
              </template>
            </q-input>
          </q-card-section>
        </q-card>
      </div>
    </div>
  </q-page>
</template>

<script>
import draggable from 'vuedraggable'
import { updateSprintMixin } from 'src/pages/mixins/update_sprint'
import { editIssueData } from 'pages/mixins/edit_issue_data'
import { unWatch } from 'src/services/util'
import IssueBacklog from 'src/components/IssueBacklog.vue'
import StartCompleteSprintButton from 'src/components/StartCompleteSprintButton.vue'
import SprintMorePopupMenu from 'src/components/SprintMorePopupMenu.vue'
import BlockHeader from 'src/components/BlockHeader.vue'
import BlockHeaderInfo from 'components/BlockHeaderInfo.vue'
import SprintEditDialog from 'components/dialogs/SprintEditDialog.vue'
import IssueEditDialog from 'components/dialogs/IssueEditDialog.vue'

export default {
  name: 'BacklogView',
  components: {
    // eslint-disable-next-line vue/no-unused-components
    IssueEditDialog,
    // eslint-disable-next-line vue/no-unused-components
    SprintEditDialog,
    BlockHeader,
    BlockHeaderInfo,
    SprintMorePopupMenu,
    StartCompleteSprintButton,
    draggable,
    IssueBacklog
  },
  mixins: [updateSprintMixin, editIssueData],
  data () {
    return {
      formData: {
        workspace: null,
        title: null,
        project: null,
        type_category: null,
        state_category: null,
        ordering: null
      },
      dragTypes: {
        SPRINT: 1,
        BACKLOG: 0
      },
      dragging: false,
      isIssueDialogOpened: false
    }
  },
  computed: {
    dragOptions () {
      return {
        animation: 200,
        group: 'issues',
        disabled: false,
        ghostClass: 'ghost'
      }
    },
    backlog: function () {
      /** Getting current backlog by chosen workspace and project **/
      return this.$store.getters['issues/BACKLOG']
    },
    backlogIssues: function () {
      /** Getting current backlog issues **/
      return this.$store.getters['issues/BACKLOG_ISSUES']
    },
    backlogIssuesLength: function () {
      /** Getting issues count **/
      return this.$store.getters['issues/BACKLOG_ISSUES_COUNT'] + ' issues'
    },
    sprints: function () {
      /** Getting all sprints **/
      return this.$store.getters['issues/UNCOMPLETED_PROJECT_SPRINTS']
    },
    isCreateIssueButtonEnabled: function () {
      return Boolean(this.formData.title)
    },
    issueStates () {
      return this.$store.getters['issues/ISSUE_STATES_BY_CURRENT_PROJECT']
    },
    issueTypes () {
      return this.$store.getters['issues/ISSUE_TYPES_BY_CURRENT_PROJECT']
    }
  },
  methods: {
    createIssue () {
      /** Create Issue, assigned to Backlog by frontend **/
      if (!this.formData.title) return false

      this.formData.workspace = this.$store.getters['auth/WORKSPACE_ID']
      this.formData.project = this.$store.getters['current/PROJECT']
      this.$store.dispatch('issues/ADD_ISSUE_TO_BACKLOG', this.formData)
        .then(() => {
          this.formData.title = ''
        })
        .catch((e) => {
          this.$q.dialog({
            title: 'Error - Cannot add issue to Backlog',
            message: 'Please check your Internet connection'
          })

          console.log(e)
        })
    },
    editSprintDialog (item) {
      this.$q.dialog({
        parent: this,
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
    },
    removeSprintDialog (item) {
      this.$q.dialog({
        dark: true,
        title: 'Confirmation',
        message: `Would you like to delete sprint: ${item.title}`,
        cancel: true,
        persistent: true
      }).onOk(() => {
        this.$store.dispatch('issues/DELETE_SPRINT', item.id)
          .catch((e) => {
            this.$q.dialog({
              title: 'Error - Cannot delete sprint',
              message: 'Please check your Internet connection'
            })

            console.log(e)
          })
      })
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
    sprintIssues (sprintId) {
      return this.$store.getters['issues/SPRINT_BY_ID_ISSUES'](sprintId)
    },
    areSprintIssues (sprintId) {
      return this.sprintIssues(sprintId).length > 0
    },
    handleCommonMoved (issuesList, event) {
      /** Handle moving - doesnt matter is it sprint or backlog **/

      const immutableList = unWatch(issuesList)

      immutableList
        .splice(event.moved.newIndex, 0, immutableList
          .splice(event.moved.oldIndex, 1)[0])

      const ordering = []
      immutableList.forEach((issueId, index) => {
        ordering.push(
          {
            id: issueId,
            ordering: index
          }
        )
      })

      return { list: immutableList, ordering }
    },
    handleSprintIssueMoved (event, sprintId) {
      /** Handling moving inside of sprint **/
      const currentSprintIssues = this.$store.getters['issues/SPRINT_BY_ID'](sprintId).issues

      const handled = this.handleCommonMoved(currentSprintIssues, event)

      this.$store.dispatch('issues/UPDATE_ISSUES_ORDERING', handled.ordering)
        .then(() => {
          this.$store.commit('issues/UPDATE_SPRINT_ISSUES', {
            id: sprintId,
            issues: handled.list
          })
        })
    },
    handleBacklogIssueMoved (event, backlogId) {
      /** Handling moving inside of backlog **/
      const currentBacklogIssues = this.$store.getters['issues/BACKLOG'].issues

      const handled = this.handleCommonMoved(currentBacklogIssues, event)

      this.$store.dispatch('issues/UPDATE_ISSUES_ORDERING', handled.ordering)
        .then(() => {
          this.$store.commit('issues/UPDATE_BACKLOG_ISSUES', {
            id: backlogId,
            issues: handled.list
          })
        })
    },
    handleCommonAdded (issuesList, event) {
      const immutableList = unWatch(issuesList)

      immutableList.splice(event.added.newIndex, 0, event.added.element.id)

      const ordering = []
      immutableList.forEach((issueId, index) => {
        ordering.push(
          {
            id: issueId,
            ordering: index
          }
        )
      })

      return { list: immutableList, ordering }
    },
    handleSprintIssueAdded (event, sprintId) {
      /** Handling adding inside of Sprint **/
      const currentSprintIssues = this.$store.getters['issues/SPRINT_BY_ID'](sprintId).issues

      const handled = this.handleCommonAdded(currentSprintIssues, event)
      const compositeSprintIdsList = {
        id: sprintId,
        issues: handled.list
      }

      this.$store.dispatch('issues/UPDATE_ISSUES_IN_SPRINT', compositeSprintIdsList)
        .then(() => {
          this.$store.dispatch('issues/UPDATE_ISSUES_ORDERING', handled.ordering)
        })
    },
    handleBacklogIssueAdded (event, backlogId) {
      /** Handling adding to Backlog **/
      const currentBacklogIssues = this.$store.getters['issues/BACKLOG'].issues

      const handled = this.handleCommonAdded(currentBacklogIssues, event)
      const compositeBacklogIdsList = {
        id: backlogId,
        issues: handled.list
      }
      this.$store.dispatch('issues/UPDATE_ISSUES_IN_BACKLOG', compositeBacklogIdsList)
        .then(() => {
          this.$store.dispatch('issues/UPDATE_ISSUES_ORDERING', handled.ordering)
        })
    },
    handleCommonRemoved (issuesList, event) {
      const list = unWatch(issuesList)

      list.splice(event.removed.oldIndex, 1)

      const ordering = []
      list.forEach((issueId, index) => {
        ordering.push(
          {
            id: issueId,
            ordering: index
          }
        )
      })

      return { list, ordering }
    },
    handleSprintIssueRemoved (event, sprintId) {
      /** Handling removing from Sprint **/
      const currentSprintIssues = this.$store.getters['issues/SPRINT_BY_ID'](sprintId).issues

      const handled = this.handleCommonRemoved(currentSprintIssues, event)
      const compositeSprintIds = {
        id: sprintId,
        issues: handled.list
      }

      this.$store.dispatch('issues/UPDATE_ISSUES_IN_SPRINT', compositeSprintIds)
        .then(() => {
          this.$store.dispatch('issues/UPDATE_ISSUES_ORDERING', handled.ordering)
        })
    },
    handleBacklogIssueRemoved (event, backlogId) {
      /** Handling removing from Backlog **/
      const currentBacklogIssues = this.$store.getters['issues/BACKLOG'].issues

      const handled = this.handleCommonRemoved(currentBacklogIssues, event)
      const compositeBacklogIds = {
        id: backlogId,
        issues: handled.list
      }

      this.$store.dispatch('issues/UPDATE_ISSUES_IN_BACKLOG', compositeBacklogIds)
        .then(() => {
          this.$store.dispatch('issues/UPDATE_ISSUES_ORDERING', handled.ordering)
        })
    },
    handleDraggableEvent (event, dragType, dragId) {
      const isSprintMoved = ('moved' in event) && (dragType === this.dragTypes.SPRINT)
      const isBacklogMoved = ('moved' in event) && (dragType === this.dragTypes.BACKLOG)

      const isSprintAdded = ('added' in event) && (dragType === this.dragTypes.SPRINT)
      const isBacklogAdded = ('added' in event) && (dragType === this.dragTypes.BACKLOG)

      const isSprintRemoved = ('removed' in event) && (dragType === this.dragTypes.SPRINT)
      const isBacklogRemoved = ('removed' in event) && (dragType === this.dragTypes.BACKLOG)

      switch (true) {
        case isSprintMoved:
          this.handleSprintIssueMoved(event, dragId)
          break
        case isBacklogMoved:
          this.handleBacklogIssueMoved(event, dragId)
          break
        case isSprintAdded:
          this.handleSprintIssueAdded(event, dragId)
          break
        case isBacklogAdded:
          this.handleBacklogIssueAdded(event, dragId)
          break
        case isSprintRemoved:
          this.handleSprintIssueRemoved(event, dragId)
          break
        case isBacklogRemoved:
          this.handleBacklogIssueRemoved(event, dragId)
          break
        default:
          throw new Error('This error should not occurred')
      }
    },
    createSprint () {
      /** Create quite empty sprint **/
      const workspace = this.$store.getters['auth/WORKSPACE_ID']
      const project = this.$store.getters['current/PROJECT']

      const payload = {
        workspace,
        project
      }

      this.$store.dispatch('issues/ADD_SPRINT_TO_PROJECT', payload)
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

  .my-card:not(:last-child) {
    margin-bottom: 0.75em;
  }

  h5 {
    font-size: 1.25rem;
    margin-bottom: 0;
    margin-top: 0;
  }
</style>
