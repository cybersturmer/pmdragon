<template>
  <q-card
    dense
    dark
    bordered
    class="my-card issue-backlog"
  >
    <q-card-section>
      # {{ id }} {{ title }}
    </q-card-section>
  </q-card>
</template>

<script>
export default {
  name: 'IssueBacklog',
  props: {
    id: {
      type: Number,
      required: true
    },
    title: {
      type: String,
      required: true
    }
  },
  computed: {
    isIssueTypeIcon () {
      return this.$store.getters['issues/IS_ISSUE_TYPE_HAVE_ICON'](this.issue.type_category)
    },
    getIssueTypeIcon () {
      return this.$store.getters['issues/ISSUE_TYPE_BY_ID'](this.issue.type_category).icon
    }
  }
}
</script>
<style lang="scss">
  .fade-enter-active, .fade-leave-active {
    transition: opacity .25s;
  }

  .fade-enter, .fade-leave-to {
    opacity: 0;
  }

  .issue-backlog:hover {
    background-color: $primary!important;
    cursor: pointer;
  }
</style>
