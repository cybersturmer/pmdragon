<template>
  <q-page class="flex flex-center">
    <q-card dark bordered flat class="my-card" style="width: 320px">
      <q-card-section style="padding: 16px 16px 0 16px">
        <div class="column">
          <div class="col">
            <PrefixUrlField
              v-model="formData.prefix_url"
              :errorMessage="formErrors.prefix_url"
            />
          </div>
          <div class="col">
            <EmailField
              v-model="formData.email"
              :errorMessage="formErrors.email"
              @keyup.enter.native="resetFieldErrorMessage('email')"
            />
          </div>
        </div>
        </q-card-section>
        <q-separator dark inset/>
        <q-card-section>
            <q-btn outline label="Sign Up" @click="register"/>
            <router-link :to="{ path: '/login' }" class="float-right"  style="text-decoration: none">
              <template>
                <q-btn
                  flat
                  size="md"
                  text-color="white"
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
import PrefixUrlField from 'components/fields/PrefixUrlField.vue'
import EmailField from 'components/fields/EmailField.vue'

export default {
  name: 'Register',
  components: { EmailField, PrefixUrlField },
  mixins: [Dialogs, fieldValidationMixin],
  data () {
    return {
      formData: {
        prefix_url: '',
        email: ''
      },
      formErrors: {
        prefix_url: '',
        email: ''
      }
    }
  },
  methods: {
    async register () {
      try {
        await this.$store.dispatch('auth/REGISTER', this.formData)
        const dialog = [
          'Congratulations',
          "We've sent you an email." +
          '<br>Please follow the link inside of it. ' +
          '<br> Link is valid only 24 hours',
          true
        ]

        this.showConfirmDialog(...dialog)
        this.formData.prefix_url = ''
        this.formData.email = ''
      } catch (e) {
        const error = new ErrorHandler(e)
        error.setErrors(this.formErrors)
        if (error.messageUseful) this.showConfirmDialog('Registration was not successful', error.message)
      }
    }
  }
}
</script>

<style>
  .q-field__bottom {
    padding: 3px 5px;
  }

  .q-field__messages {
    line-height: 1.25;
  }
</style>
