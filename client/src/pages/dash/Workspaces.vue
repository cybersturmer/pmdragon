<template>
  <q-page class="q-pa-lg">
    <div class="row justify-center">
      <div class="col-xl-3 col-lg-3 col-md-4 col-sm-6 col-xs-12"
           style="margin-left: 1em; margin-bottom: 1em"
           v-for="workspace in workspaces"
           v-bind:key="workspace.id">
        <q-card class="my-card bordered bg-primary shadow">
          <q-card-section class="text-center">
            <div class="text-h6">{{ workspace.prefix_url }}</div>
            <div class="text-subtitle1">Participants</div>
            <q-chip
              v-for="participant in workspace.participants"
              v-bind:key="participant.id"
              outline
              square
              color="grey"
              >
              {{ participant.first_name }} {{ participant.last_name }}
            </q-chip>
          </q-card-section>
          <q-separator inset />
          <q-card-actions vertical>
            <q-btn v-for="project in workspace.projects"
              outline
              v-bind:key="project.id"
              @click="selectSpace(workspace.prefix_url, project.id)"
            >{{ project.title }}</q-btn>
          </q-card-actions>
        </q-card>
      </div>
    </div>
  </q-page>
</template>

<script>
export default {
  name: 'WorkspacesView',
  methods: {
    selectSpace (prefixUrl, projectId) {
      this.$store.dispatch('current/SELECT_WORKSPACE', prefixUrl)
      this.$store.dispatch('current/SELECT_PROJECT', projectId)
      this.$router.push({ name: 'backlog' })
    }
  },
  computed: {
    workspaces: function () {
      return this.$store.getters['auth/WORKSPACES']
    }
  },
  mounted () {
    this.$store.dispatch('current/RESET_WORKSPACE')
    this.$store.dispatch('current/RESET_PROJECT')

    this.$store.dispatch('auth/INIT_WORKSPACES')
      .catch((e) => {
        console.log(e)
        this.$q.dialog({
          title: 'Error - Cannot get Workspace list',
          message: 'Please check your Internet connection'
        })
      })
  }
}
</script>
