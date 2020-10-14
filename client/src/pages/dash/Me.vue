<template>
  <q-page class="flex q-layout-padding">
    <div class="column full-width">
      <div class="row">
        <!-- Main user Data card -->
        <!-- @todo Better to move it to separate component -->
        <q-card dark bordered class="bg-grey-9 q-ma-sm">
          <q-card-section class="me_card">
            <div class="text-h6 text-center">Main user Data</div>
            <q-input
              dark
              dense
              square
              outlined
              type="text"
              v-model="user_form_data.firstName"
              label="First name"
              class="q-mb-sm"
              standout="text-white bg-primary"
            />
            <q-input
              dark
              dense
              square
              outlined
              type="text"
              v-model="user_form_data.lastName"
              label="Last name"
              class="q-mb-sm"
              standout="text-white bg-primary"
            />
            <q-input
              dark
              dense
              square
              outlined
              type="text"
              v-model="user_form_data.userName"
              label="Username"
              standout="text-white bg-primary"
            />
          </q-card-section>

          <q-card-actions vertical>
            <q-btn flat @click="saveUserData">
              Update
            </q-btn>
          </q-card-actions>
        </q-card>

        <!-- Password card -->
        <!-- @todo Better to move it to separate component -->
        <q-card dark bordered class="bg-grey-9 q-ma-sm">
          <q-card-section class="me_card">
            <div class="text-h6 text-center">Password</div>
            <q-input
              dark
              dense
              square
              outlined
              type="password"
              label="Old password"
              v-model="password_form_data.oldPassword"
              class="q-mb-sm"
              standout="text-white bg-primary"
            />
            <q-input
              dark
              dense
              square
              outlined
              type="password"
              label="Password"
              v-model="password_form_data.newPassword1"
              class="q-mb-sm"
              standout="text-white bg-primary"
            />
            <q-input
              dark
              dense
              square
              outlined
              type="password"
              label="Password confirmation"
              v-model="password_form_data.newPassword2"
              class="q-mb-sm"
              standout="text-white bg-primary"
            />
          </q-card-section>

          <q-card-actions vertical>
            <q-btn flat @click="savePassword">
              Update
            </q-btn>
          </q-card-actions>
        </q-card>

        <!-- Avatar card -->
        <!-- @todo Better to move it to separate component -->
        <q-card dark bordered class="bg-grey-9 q-ma-sm">
          <q-card-section class="me_card">
            <q-uploader
              dark
              color="primary"
              square
              flat
              no-thumbnails
              label="Avatar picture"
              :factory="uploadFileAvatar"
              auto-upload
              hide-upload-btn
              style="max-width: 180px"
            />
          </q-card-section>
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
      },
      password_form_data: {
        oldPassword: '',
        newPassword1: '',
        newPassword2: ''
      },
      avatar_form_data: {
        file: null
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

      this.$store.dispatch('auth/UPDATE_USER_DATA', payload)
    },
    savePassword () {
      const payload = {
        old_password: this.password_form_data.oldPassword,
        new_password1: this.password_form_data.newPassword1,
        new_password2: this.password_form_data.newPassword2
      }

      this.$store.dispatch('auth/UPDATE_USER_PASSWORD', payload)
    },
    uploadFileAvatar (files) {
      files.forEach(file => {
        return this.$store.dispatch('auth/UPDATE_PERSON_AVATAR', file)
      })
    }
  },
  computed: {
    avatar_url: function () {
      return this.$store.getters['auth/AVATAR']
    }
  }
}
</script>

<style>
 .me_card {
   height: 200px;
   width: 213px;
 }

  .q-uploader__list {
    font-size: 0.5em;
  }

  .q-uploader__subtitle {
   font-size: 10px;
  }

 .q-uploader__title {
   font-size: 12px!important;
 }

</style>
