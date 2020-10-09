<template>
  <q-page class="flex q-layout-padding">
    <div class="column full-width">
      <div class="row">
        <q-card dark bordered class="bg-grey-9 my-card">
          <q-card-section>
            <div class="text-h6 text-center">Main user Data</div>
            <q-input
              dark
              dense
              square
              outlined
              v-model="user_form_data.firstName"
              label="First name"
              class="q-mb-sm"
            />
            <q-input
              dark
              dense
              square
              outlined
              v-model="user_form_data.lastName"
              label="Last name"
              class="q-mb-sm"
            />
            <q-input
              dark
              dense
              square
              outlined
              v-model="user_form_data.userName"
              label="Username"
            />
          </q-card-section>

          <q-card-actions vertical>
            <q-btn flat @click="saveUserData">
              Update
            </q-btn>
          </q-card-actions>
        </q-card>
      </div>
    </div>
  </q-page>
</template>

<script>
export default {
  name: 'AccountView',
  data () {
    return {
      user_form_data: {
        firstName: this.$store.getters['auth/FIRST_NAME'],
        lastName: this.$store.getters['auth/LAST_NAME'],
        userName: this.$store.getters['auth/USERNAME']
      }
    }
  },
  methods: {
    saveUserData () {
      const payload = {
        first_name: this.user_form_data.firstName,
        last_name: this.user_form_data.lastName,
        username: this.user_form_data.userName
      }

      this.$store.dispatch('auth/USER_UPDATE', payload)
    }
  }
}
</script>

<style scoped>

</style>
