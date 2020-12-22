<template>
  <q-page class="flex flex-center">
    <q-card
      v-if="isRegistration"
      dark
      flat
      bordered
      class="my-card" style="width: 320px">
      <q-card-section>
        <div class="text-h6">Complete your registration</div>
      </q-card-section>
      <q-separator dark inset/>
      <q-card-section>
        <div class="text-subtitle2">Workspace: {{ infoData.prefix_url }}</div>
        <div class="text-subtitle2">Email: {{ infoData.email }}</div>
      </q-card-section>
      <q-separator dark inset/>
      <q-card-section>
        <PasswordField
          v-model="formData.password"
          :error-message="formErrors.password"
          @keyup.enter.native="completeRegistration"
        />
      </q-card-section>
      <q-card-actions vertical>
        <q-btn
          dark
          outline
          @click="completeRegistration"
        >
          Complete
        </q-btn>
      </q-card-actions>
    </q-card>
    <q-card
      v-else
      dark
      flat
      bordered
      class="my-card">
      <q-card-section class="text-center">
        <div class="text-h6">Your registration was not found.</div>
      </q-card-section>
    </q-card>
  </q-page>
</template>

<script>
import { Api } from 'src/services/api'
import { ErrorHandler } from 'src/services/util'
import PasswordField from 'components/fields/PasswordField'
import { Dialogs } from 'pages/mixins/dialogs'
import { fieldValidationMixin } from 'pages/mixins/field_validation'

export default {
  name: 'VerifyRegistration',
  mixins: [Dialogs, fieldValidationMixin],
  components: { PasswordField },
  data () {
    return {
      isRegistration: false,
      infoData: {
        prefix_url: '',
        email: ''
      },
      formData: {
        key: this.$attrs.key,
        password: '',
        is_invited: false
      },
      formErrors: {
        password: ''
      }
    }
  },
  computed: {
    key () {
      return this.$attrs.key
    }
  },
  async mounted () {
    try {
      const response = await new Api({
        expectedStatus: 200
      })
        .get(`/auth/person-registration-requests/${this.key}/`)

      this.infoData.prefix_url = response.data.prefix_url
      this.infoData.email = response.data.email
      this.isRegistration = true
    } catch (e) {
      console.log(e)
      return false
    }
  },
  methods: {
    async completeRegistration () {
      try {
        await new Api({
          expectedStatus: 201
        })
          .post('/auth/persons/', this.formData)

        this.showConfirmDialog(
          'You are registered successfully',
          'Congratulations! You\'ve been registered. Now you can log in.')

        await this.$router.push({ name: 'login' })
      } catch (e) {
        const error = new ErrorHandler(e)
        error.setErrors(this.formErrors)
        if (error.messageUseful) this.showConfirmDialog('Registration was not successful', error.message)
      }
    }
  }
}
</script>

<style scoped>
  .q-card__section--vert {
    padding: 13px;
  }
</style>
