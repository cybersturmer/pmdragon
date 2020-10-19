<template>
  <q-card
    dense
    dark
    bordered
    class="my-card bg-grey-8 q-ma-sm overflow-hidden text-center">
    <q-card-section>
      <span class="text-muted">#{{ issue.id }} {{ issue.title }}</span>
      <q-avatar v-if="issue.assignee">
        <img :src="assignee.avatar" :alt="`${assignee.first_name} ${assignee.last_name}`">
      </q-avatar>
    </q-card-section>
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
    }
  }
}
</script>
