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
    sprint: {
      type: Object,
      required: true
    },
    size: {
      type: String,
      default: 'sm'
    }
  },
  computed: {
    label: function () {
      return this.sprint.is_started ? 'Complete sprint' : 'Start sprint'
    }
  },
  methods: {
    startSprint (sprintId) {
      /** Start not empty sprint **/
      if (!this.sprint.started_at || !this.sprint.finished_at) {
        this.$q.dialog({
          dark: true,
          title: 'Unable to start sprint',
          message: 'Cant start sprint without start and end date. Set started at and finished at dates first.',
          ok: {
            label: 'OK',
            color: 'accent'
          }
        })
      } else {
        this.$store.dispatch('issues/START_SPRINT', sprintId)
          .catch((error) => {
            console.log(error)
          })
      }
    },
    completeSprint (sprintId) {
      /** Complete started sprint **/
      this.$q.dialog({
        dark: true,
        title: 'Complete sprint?',
        message: 'Would you like to complete Sprint',
        ok: {
          label: 'Complete',
          color: 'accent'
        },
        cancel: {
          flat: true,
          label: 'Cancel',
          color: 'primary'
        }
      })
        .onOk(() => {
          this.$store.dispatch('issues/COMPLETE_SPRINT', sprintId)
            .catch((error) => {
              console.log(error)
            })
        })
    },
    recognizeAction () {
      this.sprint.is_started ? this.completeSprint(this.sprint.id) : this.startSprint(this.sprint.id)
    }
  }
}
</script>
