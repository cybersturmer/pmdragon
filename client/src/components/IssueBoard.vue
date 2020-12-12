<template>
  <q-card
    dense
    dark
    bordered
    class="my-card q-ma-sm overflow-hidden text-center issue-backlog">
    <q-card-section>
      <span :class="`text-muted ${ this.isDone ? 'text-strike': '' }`">
        #{{ issue.id }}
        <q-icon
          v-if="isIssueTypeIcon"
          :name="getIssueTypeIcon.prefix"
          :color="getIssueTypeIcon.color"
          size="xs"
          :title="getIssueTypeTitle"
        />
        {{ issue.title }}
      </span>
    </q-card-section>
    <q-card-actions horizontal align="right">
      <q-chip
              v-if="assigneeUsername"
              dark
              size="md"
              color="secondary"
              text-color="amber"
              style="border-radius: 15px"
      >
        <q-avatar v-if="isAvatar">
          <img :src="assignee.avatar" :alt="`${assignee.first_name} ${assignee.last_name}`">
        </q-avatar>
        @{{ assigneeUsername }}
      </q-chip>
    </q-card-actions>
  </q-card>
</template>

<script>
export default {
  name: 'IssueBoard',
  props: {
    issue: {
      type: Object,
      required: true
    }
  },
  computed: {
    assignee: function () {
      return this.$store.getters['auth/PERSON_BY_ID'](this.issue.assignee)
    },
    isAvatar: function () {
      try {
        return this.assignee.avatar
      } catch (e) {
        return false
      }
    },
    assigneeUsername: function () {
      return this.assignee ? this.assignee.username : false
    },
    isDone: function () {
      return this.$store.getters['issues/IS_ISSUE_STATE_DONE'](this.issue.state_category)
    },
    isIssueTypeIcon () {
      return this.$store.getters['issues/IS_ISSUE_TYPE_HAVE_ICON'](this.issue.type_category)
    },
    getIssueTypeTitle () {
      return this.$store.getters['issues/ISSUE_TYPE_BY_ID'](this.issue.type_category).title
    },
    getIssueTypeIcon () {
      return this.$store.getters['issues/ISSUE_TYPE_BY_ID'](this.issue.type_category).icon
    }
  }
}
</script>
<style lang="scss">
  .q-card__actions {
    padding: 4px;
  }

  .issue-backlog:hover {
    background-color: $primary!important;
    cursor: pointer;
  }
</style>
