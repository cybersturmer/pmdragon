<template>
  <q-page class="flex q-layout-padding">
    <div class="row items-stretch full-width">
      <div
        v-for="issue_state in issue_states"
        :key="issue_state.id"
        class="col bg-primary full-height q-ma-sm text-center overflow-hidden">
        <div class="q-pa-sm">
          {{ issue_state.title | capitalize }}
        </div>
        <div class="bg-secondary full-height">
          <q-scroll-area class="full-height">
            <draggable
              :value="issues_by_state(issue_state.id)"
              @change="handleIssueStateChanging($event, issue_state.id)"
              style="border: 1px dashed #606060; padding: 10px; min-height: 200px"
              group="issues">
              <q-card
                v-for="issue in issues_by_state(issue_state.id)"
                :key="issue.id"
                dense
                dark
                bordered
                class="my-card bg-grey-8 q-ma-sm q-pa-sm">
                {{ issue.title }}
              </q-card>
            </draggable>
          </q-scroll-area>
        </div>
      </div>
    </div>
  </q-page>
</template>

<script>
import draggable from 'vuedraggable'

export default {
  name: 'BoardView',
  components: {
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
    }
  },
  methods: {
    issues_by_state: function (stateId) {
      return this.$store.getters['issues/SPRINT_STARTED_BY_CURRENT_PROJECT_ISSUES']
        .filter((issue) => issue.state_category === stateId)
    },
    handleIssueAdded: function (event, issueStateId) {
      /** Handling added in Issues State **/
      this.$store.dispatch('issues/UPDATE_ISSUE_STATE', event.added.element)
    },
    handleIssueStateChanging: function (event, issueStateId) {
      /** Handling moving inside of states **/
      const isAdded = ('added' in event)
      const isRemoved = ('removed' in event)

      switch (true) {
        case isAdded:
          this.handleIssueAdded(event, issueStateId)
          break
        case isRemoved:
          break
        default:
          throw new Error('This error should not occurred')
      }

      console.log(event, 'EVENT')
      console.log(issueStateId, 'issueStateId')
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
