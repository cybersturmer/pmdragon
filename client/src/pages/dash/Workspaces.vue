<template>
  <q-page class="q-pa-lg">
    <div class="row justify-center">
      <q-table
        dark
        grid
        :data="workspaces"
        no-data-label="You are not participating in any workspace"
        :filter="workspacesTable.filter"
        :filter-method="filterByString"
      >
        <template #top-right>
          <q-input dark dense debounce="300" v-model="workspacesTable.filter" placeholder="Search">
            <template #append>
              <q-icon name="search" />
            </template>
          </q-input>
        </template>
        <template #item="props">
          <div class="q-pa-xs col-xs-12 col-sm-6 col-md-4">
            <q-card dark bordered style="min-width: 350px">
              <q-card-section class="text-center">
                <div class="text-h6 text-uppercase">{{ props.row.prefix_url }}</div>
                <div class="text-subtitle2">Participants</div>
                <SmallParticipantChipElement
                  v-for="participant in props.row.participants"
                  v-bind:key="participant.id"
                  :participant="participant"
                />
              </q-card-section>
              <q-card-actions vertical>
                <q-btn v-for="project in props.row.projects"
                       v-bind:key="project.id"
                       outline
                       @click="selectSpace(props.row.prefix_url, project.id)"
                >
                  {{ project.title }}
                </q-btn>
              </q-card-actions>
            </q-card>
          </div>
        </template>
      </q-table>
    </div>
  </q-page>
</template>

<script>
import SmallParticipantChipElement from 'components/elements/SmallParticipantChipElement.vue'

export default {
  name: 'WorkspacesView',
  components: { SmallParticipantChipElement },
  data () {
    return {
      workspacesTable: {
        filter: '',
        columns: [
          {
            name: 'workspace',
            sortable: true
          }
        ]
      }
    }
  },
  methods: {
    selectSpace (prefixUrl, projectId) {
      this.$store.dispatch('current/SELECT_WORKSPACE', prefixUrl)
      this.$store.dispatch('current/SELECT_PROJECT', projectId)
      this.$router.push({ name: 'backlog' })
    },
    filterByString (rows, terms, cols, getCellValue) {
      const regex = new RegExp(terms, 'i')

      return rows
        .filter((workspace) =>
          workspace.prefix_url.match(regex) ||
          workspace.projects.find(project => project.title.match(regex))
        )
    }
  },
  computed: {
    workspaces: function () {
      const workspaces = this.$store.getters['auth/WORKSPACES']
      return workspaces.filter(workspace => workspace.projects.length > 0)
    }
  },
  mounted () {
    this.$store.dispatch('current/RESET_WORKSPACE')
    this.$store.dispatch('current/RESET_PROJECT')
  }
}
</script>
