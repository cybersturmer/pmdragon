<template>
  <q-page class="flex flex-center">
    <q-card
      v-if="is_registration"
      dark
      flat
      bordered
      class="my-card" style="width: 320px">
      <q-card-section>
        <div class="text-h6">Complete your registration</div>
      </q-card-section>
      <q-separator dark inset/>
      <q-card-section>
        <div class="text-subtitle2">Workspace: {{ info_data.prefix_url }}</div>
        <div class="text-subtitle2">Email: {{ info_data.email }}</div>
      </q-card-section>
      <q-separator dark inset/>
      <q-card-section>
        <PasswordField
          v-model="form_data.password"
          :error_message="form_errors.password"
          @keyup.enter="completeRegistration"
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
import { ErrorHandler, HandleResponse } from 'src/services/util'
import PasswordField from 'components/PasswordField'
import { Dialogs } from 'pages/mixins/dialogs'

export default {
  name: 'VerifyRegistration',
  mixins: [Dialogs],
  components: { PasswordField },
  data () {
    return {
      is_registration: false,
      info_data: {
        prefix_url: '',
        email: ''
      },
      form_data: {
        key: this.$attrs.key,
        password: '',
        is_invited: false
      },
      form_errors: {
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
      const response = await new Api().get(`/auth/person-registration-requests/${this.key}/`)

      HandleResponse.compare(200, response.status)

      this.info_data.prefix_url = response.data.prefix_url
      this.info_data.email = response.data.email
      this.is_registration = true
    } catch (e) {
      console.log(e)
      return false
    }
  },
  methods: {
    async completeRegistration () {
      try {
        const response = await new Api()
          .post('/auth/persons/', this.form_data)

        HandleResponse.compare(201, response.status)
        await this.$router.push({ name: 'register' })
        this.showConfirmDialog(
          'You are registered successfully',
          'Congratulations! You\'ve been registered')
          .onOk(() => {
            return this.$router.push({ name: 'register' })
          })
      } catch (e) {
        const error = new ErrorHandler(e)
        error.setErrors(this.form_errors)
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
