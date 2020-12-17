<template>
  <q-page class="q-pa-lg">
    <div class="row justify-center">
      <div class="col-xl-4 col-lg-5 col-md-6 col-sm-6">
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
              @input="updateWorkspace($event)"
              :value="getWorkspaceById(formData.workspace)"
              :options="workspaces"
              :option-label="(item) => item.prefix_url.toUpperCase()"
              option-value="id"
            />
            <q-input
              dark
              v-model="formData.title"
              label="Project title"
              :error="isFieldValid('title')"
              :error-message="formErrors.title"
              label-color="amber"/>
            <q-input
              dark
              v-model="formData.key"
              label="Project key"
              :error="isFieldValid('key')"
              :error-message="formErrors.key"
              label-color="amber"/>
          </q-card-section>
          <q-card-actions vertical class="text-center">
            <q-btn
              dark
              outline
              label="Create"
              @click="createProject"
            />
          </q-card-actions>
        </q-card>
      </div>
    </div>
  </q-page>
</template>

<script>
import { fieldValidationMixin } from 'pages/mixins/field_validation'

export default {
  name: 'Project',
  mixins: [fieldValidationMixin],
  data () {
    return {
      formData: {
        workspace: this.$store.getters['auth/WORKSPACES']
          .find(workspace => workspace.prefix_url === this.$store.getters['current/WORKSPACE']).id,
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
    updateWorkspace ($event) {
      this.formData.workspace = $event.id
    },
    getWorkspaceById (id) {
      return this.$store.getters['auth/WORKSPACES']
        .find(workspace => workspace.id === id)
    },
    async createProject () {
      const payload = {
        workspace: this.formData.workspace,
        title: this.formData.title,
        key: this.formData.key
      }

      try {
        await this.$store.dispatch('auth/ADD_PROJECT', payload)
      } catch (e) {
        await this.$router.push({ name: 'workspaces' })
      }
    }
  },
  computed: {
    workspaces () {
      return this.$store.getters['auth/WORKSPACES']
    }
  }
}
</script>
