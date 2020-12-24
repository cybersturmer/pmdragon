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
      animated
    >
      <q-step
        :name="1"
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
          :error="isValid('userFormErrors', 'first_name')"
          :error-message="userFormErrors.first_name"
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
          :error="isValid('userFormErrors', 'last_name')"
          :error-message="userFormErrors.last_name"
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
          :error="isValid('userFormErrors', 'username')"
          :error-message="userFormErrors.username"
          hint="Better to use short username, not email"
          standout="text-white bg-primary"
        />
      </q-step>
      <q-step
        :name="2"
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
          flat
          square
          dark
          dense
          bordered
          ref="table"
          row-key="email"
          no-data-label="Invite your team members by adding them by email."
          :hide-bottom="true"
          :hide-header="true"
          :data="teamTableData.data"
          :columns="teamTableData.columns"
          :pagination="teamTableData.pagination"
        >
          <template v-slot:body-cell-email="props">
            <q-td :props="props">
              {{ props.row.email }}
              <q-btn
                dark
                flat
                dense
                icon="person_remove"
                size="sm"
                class="float-right"
                @click="cancelInvitation(props.row.email)"
              />
            </q-td>
          </template>
        </q-table>
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
      <q-step
        :name="4"
        title="Congratulations"
        done-color="positive"
        icon="thumb_up"
      >
        <q-card dark flat>
          Hello there
        </q-card>
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
      steps: [1, 2, 3, 4],
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
            name: 'email',
            required: true,
            align: 'left',
            field: row => row.email,
            format: val => `${val}`,
            sortable: true
          }
        ],
        pagination: {
          rowsPerPage: 0
        },
        data: []
      },
      teamFormErrors: {},
      teamFormEmail: null
    }
  },
  computed: {
    workspace () {
      return this.$store.getters['auth/WORKSPACE_FIRST_PREFIX']
    },
    isUserDataFilled () {
      /** If user data filled we return true **/
      const isFirstName = !!this.$store.getters['auth/MY_FIRST_NAME']
      const isLastName = !!this.$store.getters['auth/MY_LAST_NAME']
      const isUsername = !!this.$store.getters['auth/MY_USERNAME']

      return isFirstName && isLastName && isUsername
    },
    isAnyProject () {
      /** We have to check it to understand do current user
       * have at least one project **/
      return this.$store.getters['auth/IS_ANY_PROJECT']
    },
    nextLabel () {
      return this.step === 4 ? 'Finish' : 'Continue'
    }
  },
  methods: {
    async continueClick ($refs) {
      try {
        switch (this.step) {
          case 1:
            await this.updateUserData()
            break
          case 2:
            await this.createProject()
            break
          case 3:
            await this.createTeam()
            break
          case 4:
            await this.$router.push({ name: 'loading' })
            break
        }

        /** If everything was fine - we move further **/
        await $refs.stepper.next()
      } catch (error) {
        switch (this.step) {
          case 1:
            error.setErrors(this.userFormErrors)
            break
          case 2:
            error.setErrors(this.projectFormErrors)
            break
        }

        this.showError(error)
      }
    },
    cancelInvitation (email) {
      /**
       * Just remove email from the payload that we gonna send to
       * create team members **/

      this.teamTableData.data = this.teamTableData.data.filter((row) => row.email !== email)
    },
    async updateUserData () {
      /** Update user data on server and mark step as done **/
      await this.$store.dispatch('auth/UPDATE_MY_DATA', this.userFormData)
      this.isUserStepDone = true
    },
    async createProject () {
      /** Create project on server and mark step as done **/
      await this.$store.dispatch('auth/ADD_PROJECT', this.projectFormData)
      this.isProjectStepDone = true
    },
    async createTeam () {
      /** Create team by sending emails on server **/
      const payload = {
        invites: []
      }

      const teamData = this.teamTableData.data

      for (const emailElement in teamData) {
        const dictPayload = {
          email: teamData[emailElement].email,
          workspace: this.$store.getters['auth/WORKSPACE_FIRST_ID']
        }

        payload.invites.push(dictPayload)
      }

      await this.$store.dispatch('auth/INVITE_TEAM', payload)
      this.isTeamStepDone = true
    },
    addTeamMember () {
      /** Just add a team member to temp var **/
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
      /**
       * This method checks if user already filled his/her name and last name
       * created project or have more than one team member except of self
       * so that we define step we need to complete before continue **/

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
