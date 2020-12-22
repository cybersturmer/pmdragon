<template>
  <q-page class="flex flex-center">
    <q-card dark flat bordered class="my-card" style="width: 320px">
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
          :error_message="formErrors.password"
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
  </q-page>
</template>

<script>
import { Api } from 'src/services/api'
import { ErrorHandler } from 'src/services/util'
import PasswordField from 'components/fields/PasswordField'
import { Dialogs } from 'pages/mixins/dialogs'

export default {
  name: 'VerifyInvitation',
  mixins: [Dialogs],
  components: { PasswordField },
  data () {
    return {
      infoData: {
        prefix_url: '',
        email: ''
      },
      formData: {
        key: this.$attrs.key,
        password: '',
        is_invited: true
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
    const response = await new Api({
      expectedStatus: 200
    })
      .get(`/auth/person-invitation-requests/${this.key}/`)

    this.infoData.prefix_url = response.data.workspace.prefix_url
    this.infoData.email = response.data.email
  },
  methods: {
    async completeRegistration () {
      /**
       * We have to register user first and attach him
       * to workspace where we were invited. **/

      try {
        await new Api({
          expectedStatus: 201
        })
          .post('/auth/persons/', this.formData)

        const payload = {
          is_accepted: true
        }

        await new Api({
          expectedStatus: 200
        })
          .put(`/auth/person-invitation-requests/${this.key}/`, payload)

        await this.$router.push({ name: 'login' })
      } catch (e) {
        const error = new ErrorHandler(e)
        error.setErrors(this.formErrors)
        this.showError(error)
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
