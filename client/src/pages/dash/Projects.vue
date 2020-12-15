<template>
  <q-page class="q-pa-lg">
    <div class="row justify-center">
      <div class="col-8">
        <q-card
          dark
          class="bg-grey-9 q-ma-sm"
          bordered>
          <q-card-section>
            <q-select
              dark
              flat
              square
              dense
              v-model="formData.workspace"
              :options="workspaces"
              :option-label="(item) => item.prefix_url.toUpperCase()"
              option-value="id"
            />
            <q-input
              dark
              v-model="formData.title"
              label="Project title"
              label-color="amber"/>
            <q-input
              dark
              v-model="formData.key"
              label="Project key"
              label-color="amber"/>
          </q-card-section>
          <q-card-actions vertical class="text-center">
            <q-btn
              dark
              outline
              label="Create"/>
          </q-card-actions>
        </q-card>
      </div>
    </div>
  </q-page>
</template>

<script>

export default {
  name: 'Project',
  mixins: [],
  data () {
    return {
      formData: {
        workspace: this.$store.getters['auth/WORKSPACES']
          .find(workspace => workspace.prefix_url === this.$store.getters['current/WORKSPACE']),
        title: '',
        key: ''
      },
      formErrors: {
        workspace: '',
        title: '',
        key: ''
      }
    }
  },
  methods: {
    async createProject () {
      await this.$store.dispatch('auth/ADD_PROJECT', this.formData)
    }
  },
  computed: {
    workspaces () {
      return this.$store.getters['auth/WORKSPACES']
    }
  }
}
</script>
