<template>
  <q-page class="flex q-layout-padding">
    <div class="row items-stretch full-width">
      <div
        v-for="issue_state in issue_states"
        :key="issue_state.id"
        class="col bg-primary full-height q-ma-sm text-center overflow-hidden">
        <div class="q-pa-sm">
          {{ issue_state.title | capitalize }}
        </div>
        <div class="bg-secondary full-height">
          <q-scroll-area class="full-height">
            <draggable>
              <q-card
                v-for="issue in "
                dense
                dark
                bordered
                class="my-card bg-grey-8">
              </q-card>
            </draggable>
          </q-scroll-area>
        </div>
      </div>
    </div>
  </q-page>
</template>

<script>
import draggable from 'vuedraggable'

export default {
  name: 'BoardView',
  components: {
    draggable
  },
  computed: {
    issue_states: function () {
      return this.$store.getters['issues/ISSUE_STATES_BY_CURRENT_PROJECT']
    },
    issue_types: function () {
      return this.$store.getters['issues/ISSUE_TYPES_BY_CURRENT_PROJECT']
    }
  },
  filters: {
    capitalize: function (value) {
      if (!value) return ''
      value = value.toString()
      return value.toUpperCase()
    }
  },
  mounted () {
    this.$store.dispatch('issues/INIT_ISSUE_TYPES')
    this.$store.dispatch('issues/INIT_ISSUE_STATES')
  }
}
</script>
