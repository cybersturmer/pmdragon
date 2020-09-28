<template>
  <q-btn
    dark
    outline
    color="accent"
    :size="size"
    :label="label"
    @click="recognizeAction">
  </q-btn>
</template>

<script>
export default {
  name: 'StartCompleteSprintButton',
  props: {
    sprint_id: {
      type: Number,
      required: true
    },
    is_started: {
      type: Boolean,
      required: true
    },
    size: {
      type: String,
      default: 'sm'
    }
  },
  computed: {
    label: function () {
      return this.is_started ? 'Complete sprint' : 'Start sprint'
    }
  },
  methods: {
    startSprint (sprintId) {
      /** Start not empty sprint **/
      this.$store.dispatch('issues/START_SPRINT', sprintId)
        .catch((error) => {
          console.log(error)
        })
    },
    completeSprint (sprintId) {
      /** Complete started sprint **/
      this.$store.dispatch('issues/COMPLETE_SPRINT', sprintId)
        .catch((error) => {
          console.log(error)
        })
    },
    recognizeAction () {
      this.is_started ? this.completeSprint(this.sprint_id) : this.startSprint(this.sprint_id)
    }
  }
}
</script>
