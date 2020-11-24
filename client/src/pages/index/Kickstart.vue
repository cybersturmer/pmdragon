<template>
  <q-page class="q-pa-lg">
    <q-stepper
      v-model="step"
      vertical
      ref="stepper"
      dark
      inactive-color="amber"
      active-color="amber"
      done-color="positive"
      @before-transition="makeTransition"
      animated
    >
      <q-step
        :name="1"
        :disable="isUserDataFilled"
        :done="isUserStepDone"
        done-color="positive"
        title="Some bytes about you"
        icon="face"
      >
        <q-input
          v-model="userFormData.first_name"
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
          v-model="userFormData.last_name"
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
          v-model="userFormData.username"
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
        :disable="isAnyProject"
        :done="isProjectStepDone"
        done-color="positive"
        title="Create your first project"
        icon="work"
      >
        <q-input
          v-model="projectFormData.title"
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
          v-model="projectFormData.key"
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
        :title="`Add people you work with in workspace ${this.workspace}`"
        :done="isTeamStepDone"
        done-color="positive"
        icon="supervisor_account"
      >
        <q-table
          dense
          flat
          square
          row-key="name"
          dark
          no-data-label="Invite your team members by adding them by email."
          :hide-bottom="true"
          :hide-header="true"
          :data="teamTableData.data"
          :columns="teamTableData.columns"
          :pagination="teamTableData.pagination"
        />
        <q-input
          v-model="teamFormEmail"
          type="email"
          square
          dense
          dark
          filled
          label-color="amber"
          placeholder="user@mail.com"
          @keyup.enter="addTeamMember"
        >
          <template v-slot:append>
            <q-btn dense
                   flat
                   icon="add"
                   @click="addTeamMember"
            />
          </template>
        </q-input>
      </q-step>
      <template v-slot:navigation>
        <q-stepper-navigation>
          <q-btn
            @click="continueClick($refs)"
            outline
            :label="nextLabel"
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

import { fieldValidationMixin } from 'pages/mixins/field_validation'
import { Dialogs } from 'pages/mixins/dialogs'

export default {
  name: 'Kickstart',
  mixins: [fieldValidationMixin, Dialogs],
  data () {
    return {
      step: this.getInitStep(),
      isUserStepDone: false,
      isProjectStepDone: false,
      isTeamStepDone: false,
      userFormData: {
        first_name: this.$store.getters['auth/MY_FIRST_NAME'],
        last_name: this.$store.getters['auth/MY_LAST_NAME'],
        username: this.$store.getters['auth/MY_USERNAME']
      },
      userFormErrors: {
        first_name: '',
        last_name: '',
        username: ''
      },
      projectFormData: {
        workspace: this.$store.getters['auth/WORKSPACE_FIRST_ID'],
        title: '',
        key: ''
      },
      projectFormErrors: {
        workspace: '',
        title: '',
        key: ''
      },
      teamTableData: {
        columns: [
          {
            name: 'Email',
            required: true,
            align: 'left',
            field: row => row.email,
            format: val => `${val}`
          }
        ],
        pagination: {
          rowsPerPage: 0
        },
        data: []
      },
      teamFormEmail: null
    }
  },
  computed: {
    workspace () {
      return this.$store.getters['auth/WORKSPACE_FIRST_PREFIX']
    },
    isUserDataFilled () {
      const isFirstName = !!this.$store.getters['auth/MY_FIRST_NAME']
      const isLastName = !!this.$store.getters['auth/MY_LAST_NAME']
      const isUsername = !!this.$store.getters['auth/MY_USERNAME']

      return isFirstName && isLastName && isUsername
    },
    isAnyProject () {
      return this.$store.getters['auth/IS_ANY_PROJECT']
    },
    nextLabel () {
      return this.step === 3 ? 'Finish' : 'Continue'
    }
  },
  methods: {
    makeTransition (newValue, oldValue) {
      switch (oldValue) {
        case 1:
          return this.updateUserData()
        case 2:
          return this.createProject()
        case 3:
          return this.createTeam()
      }
    },
    async updateUserData () {
      await this.$store.dispatch('auth/UPDATE_MY_DATA', this.userFormData)
      this.isUserStepDone = true
    },
    async createProject () {
      await this.$store.dispatch('auth/ADD_PROJECT', this.projectFormData)
      this.isProjectStepDone = true
    },
    async createTeam () {
      const payload = {
        invites: []
      }

      const teamData = this.teamTableData.data

      for (const emailElement in teamData) {
        const dictPayload = {
          email: teamData[emailElement].email,
          workspace: this.$store.getters['auth/WORKSPACE_FIRST_PREFIX']
        }

        payload.invites.push(dictPayload)
      }

      await this.$store.dispatch('auth/INVITE_TEAM', payload)
      this.isTeamStepDone = true

      await this.$router.push({ name: 'workspaces' })
    },
    async continueClick ($refs) {
      $refs.stepper.next()
      if (this.step === 3) {
        await this.createTeam()
        await this.$router.push({ name: 'loading' })
      }
    },
    addTeamMember () {
      if (this.teamFormEmail === null) return false

      if (!this.isValidEmail(this.teamFormEmail)) {
        this.showConfirmDialog(
          'Not a correct email',
          'Please input correct email address'
        )

        return false
      }

      this.teamTableData.data.push({
        email: this.teamFormEmail
      })

      this.teamFormEmail = null
    },
    getInitStep () {
      const isMyDataFilled = !!this.$store.getters['auth/IS_MY_DATA_FILLED']
      const isAnyProject = !!this.$store.getters['auth/IS_ANY_PROJECT']

      switch (true) {
        case isAnyProject && isMyDataFilled:
          return 3
        case isAnyProject && !isMyDataFilled:
          return 1
        case !isAnyProject && isMyDataFilled:
          return 2
        default:
          return 1
      }
    }
  }
}
</script>

<style scoped>

</style>
