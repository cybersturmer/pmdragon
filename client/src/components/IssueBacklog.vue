<template>
  <q-card
    dense
    dark
    bordered
    class="my-card"
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
  methods: {
    editIssueModal () {
      this.$emit('edit', this.id)
    },
    removeIssueModal () {
      this.$emit('remove', this.id)
    }
  }
}
</script>xha
<style lang="scss">
  .fade-enter-active, .fade-leave-active {
    transition: opacity .25s;
  }
  .fade-enter, .fade-leave-to {
    opacity: 0;
  }
</style>
