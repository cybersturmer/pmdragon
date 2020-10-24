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
                  label="Email" />
              </div>
              <div class="col">
                <q-input
                  square
                  filled
                  type="password"
                  v-model="form_data.password"
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
export default {
  name: 'Login',
  data () {
    return {
      form_data: {
        username: '',
        password: ''
      }
    }
  },
  methods: {
    login () {
      this.$store.dispatch('auth/LOGIN', this.form_data)
        .then(() => {
          this.form_data.username = ''
          this.form_data.password = ''
        })
        .then(() => this.$router.push({ name: 'loading' }))
        .catch((e) => {
          console.log(e)

          this.$q.dialog({
            title: 'Error - Cannot login',
            message: 'Check your login / password'
          })
          this.form_data.password = ''
        })
    }
  }
}
</script>
