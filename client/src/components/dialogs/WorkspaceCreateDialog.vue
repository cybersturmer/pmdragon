<template>
  <q-dialog ref="dialog" @hide="onDialogHide">
    <q-card dark flat bordered class="q-dialog-plugin bg-secondary">
      <q-card-section>
        <q-input
          dark
          @input="inputPrefixUrl($event)"
          :value="formData.prefix_url"
          :rules="[workspacePrefixUrlLength]"
          maxlength="20"
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

    workspacePrefixUrlLength ($value) {
      return ($value.length >= 3 && $value.length <= 20) || 'From 3 to 20 letters and numbers are allowed'
    },

    onDialogHide () {
      this.$emit('hide')
    },

    inputPrefixUrl ($event) {
      this.dropErrors()
      this.formData.prefix_url = $event.toUpperCase()
    },

    dropErrors () {
      this.formErrors.prefix_url = ''
    },

    async onOKClick () {
      try {
        const payload = await this.$store.dispatch('auth/ADD_WORKSPACE', this.formData)
        this.$emit('ok', payload)
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
