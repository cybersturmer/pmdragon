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
              :error="!!isPrefixUrlValid"
              :error-message="form_errors.prefix_url"
              label="URL of your team"
            />
          </div>
          <div class="col">
            <q-input
              square
              filled
              v-model="form_data.email"
              :error="!!isEmailValid"
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

export default {
  name: 'Register',
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
    register: async function () {
      try {
        await this.$store.dispatch('auth/REGISTER', this.form_data)
        this.$q.dialog({
          dark: true,
          message: 'Registered successfully. Check your email.'
        })
      } catch (e) {
        this.$q.dialog({
          dark: true,
          message: 'Something was wrong, try another data or check your connection to internet.'
        })
      }
    }
  },
  computed: {
    isEmailValid: function () {
      return this.form_errors.email.length > 0
    },
    isPrefixUrlValid: function () {
      return this.form_errors.prefix_url.length > 0
    }
  }
}
</script>

<style>
  .q-field__bottom {
    padding: 5px 12px 0;
  }
</style>
