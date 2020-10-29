<template>
  <q-page class="q-pa-lg">
    <q-stepper
      v-model="step"
      vertical
      ref="stepper"
      dark
      inactive-color="accent"
      active-color="amber"
      done-color="positive"
      animated
    >
      <q-step
        :name="1"
        title="Some bytes about you"
        icon="face"
      >
        <q-input
          v-model="user_form_data.first_name"
          dark
          dense
          square
          filled
          type="text"
          label="First name"
          class="q-mb-sm"
          standout="text-white bg-primary"
        />
        <q-input
          v-model="user_form_data.last_name"
          dark
          dense
          square
          filled
          type="text"
          label="Last name"
          class="q-mb-sm"
          standout="text-white bg-primary"
        />
        <q-input
          v-model="user_form_data.username"
          dark
          dense
          square
          filled
          type="text"
          label="Username"
          standout="text-white bg-primary"
        />
      </q-step>
      <q-step
        :name="2"
        title="Create your first project"
        icon="work"
      >
        <q-input
          v-model="project_form_data.title"
          dark
          dense
          square
          filled
          type="text"
          label="Project title"
          class="q-mb-sm"
          standout="text-white bg-primary"
        />
        <q-input
          v-model="project_form_data.key"
          dark
          dense
          square
          filled
          type="text"
          label="Project short key"
          class="q-mb-sm"
          standout="text-white bg-primary"
        />
      </q-step>
      <q-step
        :name="3"
        title="Add people you work with"
        icon="supervisor_account"
      >
        Add your team
      </q-step>
      <template v-slot:navigation>
        <q-stepper-navigation>
          <q-btn
            @click="$refs.stepper.next()"
            outline
            :label="step === 3 ? 'Finish' : 'Continue'"
          />
          <q-btn
            v-if="step > 1"
            flat
            @click="$refs.stepper.previous()"
            label="Back" />
        </q-stepper-navigation>
      </template>
    </q-stepper>
  </q-page>
</template>

<script>
import { Api } from 'src/services/api'

export default {
  name: 'Kickstart',
  data () {
    return {
      step: 1,
      user_form_data: {
        first_name: '',
        last_name: '',
        username: ''
      },
      user_form_errors: {
        first_name: '',
        last_name: '',
        username: ''
      },
      project_form_data: {
        workspace: this.$store.getters['auth/WORKSPACE_FIRST_ID'],
        title: '',
        key: ''
      },
      project_form_errors: {
        workspace: '',
        title: '',
        key: ''
      },
      team_form_data: []
    }
  },
  methods: {
    async addTeamMember (email) {
      /** Invite team member **/
      const response = new Api({ auth: true }).get()
      console.log(response)
    }
  }
}
</script>

<style scoped>

</style>
