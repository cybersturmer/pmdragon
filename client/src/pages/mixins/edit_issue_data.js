export const editIssueData = {
  computed: {
    issueStates () {
      return this.$store.getters['issues/ISSUE_STATES_BY_CURRENT_PROJECT']
    },
    issueTypes () {
      return this.$store.getters['issues/ISSUE_TYPES_BY_CURRENT_PROJECT']
    },
    participants () {
      return this.$store.getters['auth/WORKSPACE_DATA'].participants
    }
  }
}
