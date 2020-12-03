<template>
  <q-page class="flex flex-center">
        <q-card dark flat bordered class="my-card" style="width: 320px">
          <q-card-section style="padding: 16px 16px 0 16px">
            <div class="column">
              <div class="col">
                <UsernameField
                  v-model="formData.username"
                  :error-message="formErrors.username"
                />
              </div>
              <div class="col">
                <PasswordField
                  v-model="formData.password"
                  :error-message="formErrors.password"
                  @keyup.enter.native="login"
                />
              </div>
            </div>
          </q-card-section>
          <q-separator dark inset/>
          <q-card-section>
            <q-btn
              outline
              text-color="white"
              label="Sign In"
              @click="login"
            />
            <router-link :to="{ path: '/' }" class="float-right" style="text-decoration: none">
              <template>
              <q-btn
                flat
                size='md'
                text-color="white"
                label="Want to register?"
                style="margin-left: 30px"/>
              </template>
            </router-link>
          </q-card-section>
        </q-card>
  </q-page>
</template>

<script>
import { fieldValidationMixin } from 'pages/mixins/field_validation'
import { ErrorHandler } from 'src/services/util'
import { Dialogs } from 'pages/mixins/dialogs'
import PasswordField from 'components/fields/PasswordField'
import UsernameField from 'components/fields/UsernameField'

export default {
  name: 'Login',
  components: { UsernameField, PasswordField },
  mixins: [Dialogs, fieldValidationMixin],
  data () {
    return {
      formData: {
        username: '',
        password: ''
      },
      formErrors: {
        username: '',
        password: ''
      }
    }
  },
  methods: {
    async login () {
      try {
        await this.$store.dispatch('current/RESET_STATE')
        await this.$store.dispatch('auth/LOGOUT')
        await this.$store.dispatch('issues/RESET')

        await this.$store.dispatch('auth/LOGIN', this.formData)
        this.formData.username = ''
        this.formData.password = ''
        await this.$router.push({ name: 'loading' })
      } catch (e) {
        const error = new ErrorHandler(e)
        this.showConfirmDialog('Login was not successful', error.message)
      }
    }
  }
}
</script>

<style>
  .q-field__messages {
    line-height: 1.25;
  }
  .q-field__bottom {
    padding: 5px 0;
  }
</style>
