<template>
  <q-page class="flex flex-center">
        <q-card flat bordered class="my-card bg-grey-6" style="width: 320px">
          <q-card-section>
            <div class="column">
              <div class="col">
                <q-input
                  square
                  filled
                  v-model="form_data.username"
                  :error="isFieldValid('username')"
                  :error-message="form_errors.username"
                  label="Email"
                  class="q-mb-md"
                />
              </div>
              <div class="col">
                <q-input
                  square
                  filled
                  type="password"
                  v-model="form_data.password"
                  :error="isFieldValid('password')"
                  :error-message="form_errors.password"
                  label="Password"
                  @keyup.enter="login"
                />
              </div>
            </div>
          </q-card-section>
          <q-separator />
          <q-card-section>
            <q-btn
              outline
              color="grey-8"
              text-color="black"
              label="Sign In"
              @click="login"
            />
            <router-link :to="{ path: '/' }" class="float-right" style="text-decoration: none">
              <template>
              <q-btn
                flat
                size='md'
                text-color="black"
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

export default {
  name: 'Login',
  mixins: [Dialogs, fieldValidationMixin],
  data () {
    return {
      form_data: {
        username: '',
        password: ''
      },
      form_errors: {
        username: '',
        password: ''
      }
    }
  },
  methods: {
    async login () {
      try {
        await this.$store.dispatch('auth/LOGIN', this.form_data)
        this.form_data.username = ''
        this.form_data.password = ''
        await this.$router.push({ name: 'loading' })
      } catch (e) {
        const error = new ErrorHandler(e)
        this.showErrorDialog('Login was not successful', error.message)
      }
    }
  }
}
</script>

<style scoped>
  .q-field__messages {
    line-height: 1.25;
  }
</style>
