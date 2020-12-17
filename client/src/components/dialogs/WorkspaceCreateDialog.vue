<template>
  <q-dialog ref="dialog" @hide="onDialogHide">
    <q-card dark flat bordered class="q-dialog-plugin bg-secondary">
      <q-card-section>
        <q-input
          dark
          @input="inputPrefixUrl($event)"
          :value="formData.prefix_url"
          label="Prefix Url"
          label-color="amber"
          :error="isValid('formErrors', 'prefix_url')"
          :error-message="formErrors.prefix_url"
        />
      </q-card-section>
      <q-card-actions vertical>
        <q-btn
          outline
          color="amber"
          label="Create Workspace"
          @click="onOKClick"/>
      </q-card-actions>
    </q-card>
  </q-dialog>
</template>

<script>
import { fieldValidationMixin } from 'pages/mixins/field_validation'
import { Dialogs } from 'pages/mixins/dialogs'

export default {
  name: 'WorkspaceCreateDialog',
  mixins: [fieldValidationMixin, Dialogs],
  data () {
    return {
      formData: {
        prefix_url: ''
      },
      formErrors: {
        prefix_url: ''
      }
    }
  },
  methods: {
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
      try {
        await this.$store.dispatch('auth/ADD_WORKSPACE', this.formData)
        this.$emit('ok', this.formData)
        this.hide()
      } catch (e) {
        e.setErrors(this.formErrors)
      }
    },

    onCancelClick () {
      this.hide()
    }
  }
}
</script>
