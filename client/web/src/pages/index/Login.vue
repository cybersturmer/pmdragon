<template>
  <q-page class="flex flex-center">
        <q-card flat bordered class="my-card bg-grey-6" style="width: 320px">
          <q-card-section>
            <div class="column">
              <div class="col">
                <q-input filled v-model="form_data.username" label="Email" />
              </div>
              <div class="col">
                <q-input
                  type="password"
                  filled
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
            <router-link :to="{ path: '/' }">
              <q-btn
                flat
                size='md'
                color="white"
                text-color="black"
                label="Want to register?"
                style="margin-left: 30px"/>
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
    async login () {
      try {
        await this.$store.dispatch('auth/LOGIN', this.form_data)

        this.form_data.username = ''
        this.form_data.password = ''

        await this.$router.push({ path: '/dash/workspaces' })
      } catch (error) {
        this.$q.dialog({
          title: 'Error - Cannot login',
          message: 'Check your login / password'
        })

        this.form_data.password = ''
      }
    }
  }
}
</script>

<style scoped>
  .q-btn {
    text-transform: none;
  }
</style>
