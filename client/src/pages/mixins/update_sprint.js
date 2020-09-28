export const updateSprintMixin = {
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
          }
    }
}