<template>
  <q-dialog ref="dialog" @hide="onDialogHide">
    <q-card dark flat bordered class="q-dialog-plugin bg-secondary">
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
          color="amber"
          label="Create"
          @click="onOKClick"
        />
      </q-card-actions>
    </q-card>
  </q-dialog>
</template>

<script>
import { fieldValidationMixin } from 'pages/mixins/field_validation'
import { Dialogs } from 'pages/mixins/dialogs'

export default {
  name: 'ProjectCreateDialog',
  mixins: [fieldValidationMixin, Dialogs],
  props: {
    defaultWorkspace: {
      type: Number,
      required: false
    }
  },
  data () {
    return {
      formData: {
        workspace: this.defaultWorkspace || this.$store.getters['auth/WORKSPACE_FIRST_ID'],
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
    show () {
      this.$refs.dialog.show()
    },

    hide () {
      this.$refs.dialog.hide()
    },

    onDialogHide () {
      this.$emit('hide')
    },

    inputPrefixUrl ($event) {
      this.dropErrors()
      this.formData.prefix_url = $event
    },

    dropErrors () {
      this.formErrors.prefix_url = ''
    },

    async onOKClick () {
      const payload = {
        workspace: this.formData.workspace,
        title: this.formData.title,
        key: this.formData.key
      }

      try {
        const emitPayload = await this.$store.dispatch('auth/ADD_PROJECT', payload)
        this.$emit('ok', emitPayload)
        this.hide()
      } catch (e) {
        e.setErrors(this.formErrors)
      }
    },

    onCancelClick () {
      this.hide()
    }
  },
  computed: {
    workspaces () {
      return this.$store.getters['auth/WORKSPACES']
    }
  }
}
</script>
