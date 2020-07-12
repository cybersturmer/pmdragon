<template>
  <q-page class="flex q-layout-padding">
    <div class="column full-width">
      <h5>Sprints</h5>
      <div class="col">
        <q-scroll-area style="height: 100%">
            <div
              v-for="sprint in sprints"
              :key="sprint.id"
              class="q-ma-xs">
              <div class="h6 text-amber" style="margin-top: 1rem">
                {{ sprint.title }} - {{ sprint.goal }} - (&nbsp;{{ sprint.issues.length }} issues&nbsp;)
              </div>
              <draggable
                :value="getSprintIssues(sprint.id)"
                group="issues"
                class="q-card--bordered q-pa-sm"
                style="border: 1px dashed #606060; min-height: 67px;"
                @change="handleDraggableChanges($event, drag_types.SPRINT, sprint.id)">
                <transition-group type="transition" :name="'flip-list'" tag="div">
                  <q-card
                    v-for="issue in getSprintIssues(sprint.id)"
                    :key="issue.id"
                    dense
                    dark
                    bordered
                    class="my-card bg-grey-8 text-white shadow-3 overflow-hidden no-padding">
                    <q-card-section>
                      <span class="text-muted">#{{ issue.id }}</span> {{ issue.title }}
                    </q-card-section>
                  </q-card>
                </transition-group>
              </draggable>
            </div>
        </q-scroll-area>
      </div>
      <h5>Backlog (&nbsp;{{ backlogIssuesLength }} issues&nbsp;)</h5>
      <div class="col" v-if="backlogIssues">
        <q-scroll-area style="height: calc(100% - 35px)">
          <draggable
            :value="backlogIssues"
            @change="handleDraggableChanges($event, drag_types.BACKLOG, backlog.id)"
            style="border: 1px dashed #606060; padding: 10px; min-height: 67px;"
            group="issues">
            <transition-group type="transition" :name="'flip-list'" tag="div">
              <q-card
                v-for="item in backlogIssues"
                :key="item.id"
                @mouseover="showIssueMenu(item.id)"
                dense
                dark
                bordered
                class="my-card bg-grey-8 text-white shadow-3 overflow-hidden no-padding">
                <q-card-section>
                  #{{ item.id }} {{ item.title }}
                  <q-btn
                    v-show="show_edit_button === item.id"
                    dense
                    flat
                    icon-right="more_vert"
                    class="absolute-right"
                    style="margin-right: 10px">
                    <q-menu dark>
                      <q-list dense style="min-width: 100px">
                        <q-item
                          clickable
                          v-close-popup
                          @click="editIssueModal(item)">
                          <q-item-section>Edit</q-item-section>
                        </q-item>
                        <q-item
                          clickable
                          v-close-popup
                          @click="removeIssueModal(item)">
                          <q-item-section>Remove</q-item-section>
                        </q-item>
                      </q-list>
                    </q-menu>
                  </q-btn>
                </q-card-section>
              </q-card>
            </transition-group>
          </draggable>
        </q-scroll-area>
        <q-card dark
                bordered
                square
                class="my-card bg-grey-8 text-white shadow-3 absolute-bottom card-no-padding"
        style="margin: 0.3em">
          <q-card-section>
            <q-input
              v-model="form_data.title"
              @keyup.enter="createIssue"
              dark
              dense
              square
              filled
              placeholder="Add Issue">
              <template v-slot:append>
                <q-btn @click="createIssue"
                       :disable="!isAddButtonEnabled"
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
import { unWatch } from 'src/services/util'

export default {
  name: 'BacklogView',
  components: {
    draggable
  },
  data () {
    return {
      show_edit_button: Number,
      form_data: {
        workspace: null,
        title: null,
        project: null,
        type_category: null,
        state_category: null,
        ordering: null
      },
      drag_types: {
        SPRINT: 1,
        BACKLOG: 0
      }
    }
  },
  computed: {
    backlog: function () {
      return this.$store.getters['issues/BACKLOG']
    },
    backlogIssues: function () {
      return this.$store.getters['issues/BACKLOG_ISSUES']
    },
    backlogIssuesLength: function () {
      return this.$store.getters['issues/BACKLOG_ISSUES_COUNT']
    },
    sprints: function () {
      return this.$store.getters['issues/UNCOMPLETED_PROJECT_SPRINTS']
    },
    isAddButtonEnabled: function () {
      return Boolean(this.form_data.title)
    }
  },
  mounted () {
    this.$store.dispatch('issues/INIT_BACKLOGS')
      .catch((error) => {
        this.$q.dialog({
          title: 'Error - Cannot get Backlogs',
          message: 'Please check your Internet connection'
        })

        console.log(error)
      })

    this.$store.dispatch('issues/INIT_SPRINTS')
      .catch((error) => {
        this.$q.dialog({
          title: 'Error = Cannot get Sprints',
          message: 'Please check your Internet connection'
        })

        console.log(error)
      })
  },
  methods: {
    createIssue () {
      if (!this.form_data.title) return false

      this.form_data.workspace = this.$store.getters['current/WORKSPACE_ID']
      this.form_data.project = this.$store.getters['current/PROJECT']
      this.$store.dispatch('issues/ADD_ISSUE_TO_BACKLOG', this.form_data)
        .then(() => {
          this.form_data.title = ''
        })
        .catch((error) => {
          this.$q.dialog({
            title: 'Error - Cannot add issue to Backlog',
            message: 'Please check your Internet connection'
          })

          console.log(error)
        })
    },
    showIssueMenu (id) {
      this.show_edit_button = id
    },
    editIssueModal (item) {
      this.$q.dialog({
        dark: true,
        title: 'Issue information',
        message: 'Set Issue title',
        prompt: {
          model: item.title,
          type: 'text'
        },
        cancel: true,
        persistent: true
      })
        .onOk((data) => {
          const payload = {
            workspace: this.$store.getters['current/WORKSPACE_ID'],
            project: this.$store.getters['current/PROJECT'],
            id: item.id,
            title: data
          }

          this.$store.dispatch('issues/EDIT_ISSUE', payload)
            .catch((error) => {
              this.$q.dialog({
                title: 'Error - Cannot edit issue',
                message: 'Please check your Internet connection'
              })
              console.log(error)
            })
        })
    },
    removeIssueModal (item) {
      this.$q.dialog({
        dark: true,
        title: 'Confirmation',
        message: `Would you like to delete issue: ${item.title}`,
        cancel: true,
        persistent: true
      }).onOk(() => {
        this.$store.dispatch('issues/DELETE_ISSUE', item)
          .catch((error) => {
            this.$q.dialog({
              title: 'Error - Cannot delete issue',
              message: 'Please check your Internet connection'
            })

            console.log(error)
          })
      })
    },
    getSprintIssues (sprintId) {
      return this.$store.getters['issues/SPRINT_BY_ID_ISSUES'](sprintId)
    },
    handleMoving (issuesList, event) {
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
    handleSprintMoving (event, sprintId) {
      /** Handling moving inside of sprint **/
      const currentSprintIssues = this.$store.getters['issues/SPRINT_BY_ID'](sprintId).issues

      const handled = this.handleMoving(currentSprintIssues, event)

      this.$store.dispatch('issues/UPDATE_ISSUES_ORDERING', handled.ordering)
        .then(() => {
          this.$store.commit('issues/UPDATE_SPRINT_ISSUES', {
            id: sprintId,
            issues: handled.list
          })
        })
    },
    handleBacklogMoving (event, backlogId) {
      /** Handling moving inside of backlog **/
      const currentBacklogIssues = this.$store.getters['issues/BACKLOG'].issues

      const handled = this.handleMoving(currentBacklogIssues, event)

      this.$store.dispatch('issues/UPDATE_ISSUES_ORDERING', handled.ordering)
        .then(() => {
          this.$store.commit('issues/UPDATE_BACKLOG_ISSUES', {
            id: backlogId,
            issues: handled.list
          })
        })
    },
    handleAdding (issuesList, event) {
      const immutableList = unWatch(issuesList)

      immutableList
        .splice(event.added.newIndex, 0, event.added.element.id)

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
    handleSprintAdding (event, sprintId) {
      /** Handling adding inside of Sprint **/
      const currentSprintIssues = this.$store.getters['issues/SPRINT_BY_ID'](sprintId).issues

      const handled = this.handleAdding(currentSprintIssues, event)
      const compositeSprintIdsList = {
        id: sprintId,
        issues: handled.list
      }

      this.$store.dispatch('issues/UPDATE_ISSUES_IN_SPRINT', compositeSprintIdsList)
        .then(() => {
          this.$store.dispatch('issues/UPDATE_ISSUES_ORDERING', handled.ordering)
        })
    },
    handleBacklogAdding (event, backlogId) {
      /** Handling adding to Backlog **/
      const currentBacklogIssues = this.$store.getters['issues/BACKLOG'].issues

      const handled = this.handleAdding(currentBacklogIssues, event)
      const compositeBacklogIdsList = {
        id: backlogId,
        issues: handled.list
      }
      this.$store.dispatch('issues/UPDATE_ISSUES_IN_BACKLOG', compositeBacklogIdsList)
        .then(() => {
          this.$store.dispatch('issues/UPDATE_ISSUES_ORDERING', handled.ordering)
        })
    },
    handleRemoving (issuesList, event) {
      const immutableList = unWatch(issuesList)

      immutableList
        .splice(event.removed.oldIndex, 1)

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
    handleSprintRemoving (event, sprintId) {
      /** Handling removing from Sprint **/
      const currentSprintIssues = this.$store.getters['issues/SPRINT_BY_ID'](sprintId)

      const handled = this.handleRemoving(currentSprintIssues, event)
      const compositeSprintIds = {
        id: sprintId,
        issues: handled.list
      }

      this.$store.dispatch('issues/UPDATE_ISSUES_IN_SPRINT', compositeSprintIds)
        .then(() => {
          this.$store.dispatch('issues/UPDATE_ISSUES_ORDERING', handled.ordering)
        })
    },
    handleBacklogRemoving (event, backlogId) {
      /** Handling removing from Backlog **/
      const currentBacklogIssues = this.$store.getters['issues/BACKLOG'].issues

      const handled = this.handleRemoving(currentBacklogIssues, event)
      const compositeBacklogIds = {
        id: backlogId,
        issues: handled.list
      }

      this.$store.dispatch('issues/UPDATE_ISSUES_IN_BACKLOG', compositeBacklogIds)
        .then(() => {
          this.$store.dispatch('issues/UPDATE_ISSUES_ORDERING', handled.ordering)
        })
    },
    handleDraggableChanges (event, dragType, dragId) {
      const isSprintMoved = ('moved' in event) && (dragType === this.drag_types.SPRINT)
      const isBacklogMoved = ('moved' in event) && (dragType === this.drag_types.BACKLOG)

      const isSprintAdded = ('added' in event) && (dragType === this.drag_types.SPRINT)
      const isBacklogAdded = ('added' in event) && (dragType === this.drag_types.BACKLOG)

      const isSprintRemoved = ('removed' in event) && (dragType === this.drag_types.SPRINT)
      const isBacklogRemoved = ('removed' in event) && (dragType === this.drag_types.BACKLOG)

      switch (true) {
        case isSprintMoved:
          this.handleSprintMoving(event, dragId)
          break
        case isBacklogMoved:
          this.handleBacklogMoving(event, dragId)
          break
        case isSprintAdded:
          this.handleSprintAdding(event, dragId)
          break
        case isBacklogAdded:
          this.handleBacklogAdding(event, dragId)
          break
        case isSprintRemoved:
          this.handleSprintRemoving(event, dragId)
          break
        case isBacklogRemoved:
          this.handleBacklogRemoving(event, dragId)
          break
        default:
          throw new Error('This error should not occurred')
      }
    }
  }
}
</script>
<style lang="scss">
  .q-card__section--vert {
    padding: 13px;
  }

  .flip-list-move {
    transition: transform 0.3s;
  }

  .my-card:not(:last-child) {
    margin-bottom: 0.75em;
  }

  h5 {
    font-size: 1.25rem;
    margin-bottom: 0.5rem;
    margin-top: 0.5rem;
  }

  .card-no-padding {
    .q-card__section--vert {
        padding: 0;
    }
  }

  .text-amber {
    color: #8b8b8b!important;
  }

</style>
