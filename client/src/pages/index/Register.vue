<template>
  <q-page class="flex flex-center">
    <q-card flat bordered class="my-card bg-grey-6" style="width: 320px">
      <q-card-section style="padding: 16px 16px 0 16px">
        <div class="column">
          <div class="col">
            <q-input
              square
              filled
              v-model="form_data.prefix_url"
              @input="resetFieldErrorMessage('prefix_url')"
              :error="isFieldValid('prefix_url')"
              :error-message="form_errors.prefix_url"
              label="Workspace prefix"
            />
          </div>
          <div class="col">
            <q-input
              square
              filled
              v-model="form_data.email"
              @change="resetFieldErrorMessage('email')"
              :error="isFieldValid('email')"
              :error-message="form_errors.email"
              label="Your email"
            />
          </div>
        </div>
        </q-card-section>
        <q-separator />
        <q-card-section>
            <q-btn outline color="grey-8" text-color="black" label="Register" @click="register"/>
            <router-link :to="{ path: '/login' }" class="float-right"  style="text-decoration: none">
              <template>
                <q-btn
                  flat
                  size="md"
                  text-color="black"
                  label="Already a member?"/>
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
  name: 'Register',
  mixins: [Dialogs, fieldValidationMixin],
  data () {
    return {
      form_data: {
        prefix_url: '',
        email: ''
      },
      form_errors: {
        prefix_url: '',
        email: ''
      }
    }
  },
  methods: {
    check_prefix: function () {
      console.log('Checked')
    },
    async register () {
      try {
        await this.$store.dispatch('auth/REGISTER', this.form_data)
        const dialog = [
          'Congratulations',
          "We've sent you an email." +
          '<br>Please follow the link inside of it. ' +
          '<br> Link is valid only 24 hours',
          true
        ]

        this.showConfirmDialog(...dialog)
      } catch (e) {
        const error = new ErrorHandler(e)
        error.setErrors(this.form_errors)
        if (error.messageUseful) this.showConfirmDialog('Registration was not successful', error.message)
      }
    }
  }
}
</script>

<style>
  .q-field__bottom {
    padding: 5px 0;
  }

  .q-field__messages {
    line-height: 1.25;
  }
</style>
