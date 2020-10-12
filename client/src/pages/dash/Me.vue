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
            <div class="text-h6 text-center">Profile picture</div>
            <q-file
              dark
              filled
              dense
              v-model="avatar_form_data.file"
              standout="text-white bg-primary"
              label="Pick file"
              counter
              :counter-label="aboutAvatarFilesToUpload"
            >
              <template v-slot:prepend>
                <q-icon name="attach_file" />
              </template>
            </q-file>
          </q-card-section>

          <q-card-actions vertical>
            <q-btn flat @click="saveAvatar">
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
    saveAvatar () {
      this.$store.dispatch('auth/UPDATE_PERSON_AVATAR', this.avatar_form_data.file)
    },
    aboutAvatarFilesToUpload ({ totalSize }) {
      return totalSize
    }
  },
  computed: {
    avatar_url: function () {
      return this.$store.getters['auth/AVATAR']
    }
  }
}
</script>

<style scoped>
 .me_card {
   height: 200px;
   width: 213px;
 }
</style>
