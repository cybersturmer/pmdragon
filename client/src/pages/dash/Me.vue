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
            <div class="text-h6 text-center">Avatar picture</div>
            <q-uploader
              dark
              square
              flat
              :accept="avatarAllowMimes"
              max-files="1"
              :factory="uploadFileAvatar"
              auto-upload
              hide-upload-btn
              @removed="onRemoved"
              style="max-width: 180px"
            />
          </q-card-section>
        </q-card>
      </div>
    </div>
  </q-page>
</template>

<script>
import { AVATAR_ALLOW_MIMES } from 'src/services/allow'

export default {
  name: 'AccountView',
  data () {
    return {
      user_form_data: {
        firstName: this.$store.getters['auth/MY_FIRST_NAME'],
        lastName: this.$store.getters['auth/MY_LAST_NAME'],
        userName: this.$store.getters['auth/MY_USERNAME']
      },
      password_form_data: {
        oldPassword: '',
        newPassword1: '',
        newPassword2: ''
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

      this.$store.dispatch('auth/UPDATE_MY_DATA', payload)
    },
    savePassword () {
      const payload = {
        old_password: this.password_form_data.oldPassword,
        new_password1: this.password_form_data.newPassword1,
        new_password2: this.password_form_data.newPassword2
      }

      this.$store.dispatch('auth/UPDATE_MY_PASSWORD', payload)
    },
    uploadFileAvatar (files) {
      files.forEach(file => {
        return this.$store.dispatch('auth/UPDATE_MY_AVATAR', file)
      })
    },
    onRemoved (file) {
      return this.$store.dispatch('auth/DELETE_MY_AVATAR')
    }
  },
  computed: {
    avatar_url: function () {
      return this.$store.getters['auth/MY_AVATAR']
    },
    avatarAllowMimes: function () {
      return AVATAR_ALLOW_MIMES
    }
  },
  mounted () {

  }
}
</script>

<style lang="scss">
 .me_card {
   min-height: 200px;
   width: 213px;
 }

  .q-uploader__list {
    font-size: 0.5em;
    padding: 5px;
    background-color: $accent;
    overflow: hidden;
    height: 165px;
    max-height: 165px;
  }

 .q-uploader__file--img {
   min-width: initial;
   background-size: contain;
   background-repeat: space;
   height: 155px;
 }

  .q-uploader__subtitle {
   font-size: 10px;
  }

 .q-uploader__title {
   font-size: 12px!important;
 }

</style>
