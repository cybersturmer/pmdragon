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
