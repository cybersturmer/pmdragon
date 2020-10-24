<template>
  <q-card
    dense
    dark
    bordered
    class="my-card bg-grey-8 q-ma-sm overflow-hidden text-center">
    <q-card-section>
      <span :class="`text-muted ${ this.isDone ? 'text-strike': '' }`">
        #{{ issue.id }} {{ issue.title }}
      </span>
    </q-card-section>
    <q-card-actions horizontal align="right">
      <q-chip dark
              size="md"
              color="secondary"
              text-color="amber"
              style="border-radius: 15px"
      >
        <q-avatar v-if="isAvatar">
          <img :src="assignee.avatar" :alt="`${assignee.first_name} ${assignee.last_name}`">
        </q-avatar>
        {{ assigneeUsername }}
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
      return this.assignee ? this.assignee.username : 'unassigned'
    },
    isDone: function () {
      return this.$store.getters['issues/IS_ISSUE_STATE_DONE'](this.issue.state_category)
    }
  }
}
</script>
<style scoped>
  .q-card__actions {
    padding: 4px;
  }
</style>
