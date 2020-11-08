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
        :disable="is_user_data_filled"
        :done="is_user_data_filled"
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
        :disable="is_any_project"
        :done="is_any_project"
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
        :title="`Add people you work with in workspace ${this.workspace}`"
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
          :data="team_table_data.data"
          :columns="team_table_data.columns"
        />
        <q-input
          v-model="team_form_email"
          type="email"
          square
          dense
          dark
          filled
          label-color="amber"
          placeholder="user@mail.com">
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

export default {
  name: 'Kickstart',
  data () {
    return {
      step: this.getInitStep(),
      user_form_data: {
        first_name: this.$store.getters['auth/MY_FIRST_NAME'],
        last_name: this.$store.getters['auth/MY_LAST_NAME'],
        username: this.$store.getters['auth/MY_USERNAME']
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
      team_table_data: {
        columns: [
          {
            name: 'Email',
            required: true,
            align: 'left',
            field: row => row.email,
            format: val => `${val}`
          }
        ],
        data: []
      },
      team_form_email: null
    }
  },
  computed: {
    workspace () {
      return this.$store.getters['auth/WORKSPACE_FIRST_PREFIX']
    },
    is_user_data_filled () {
      const isFirstName = !!this.$store.getters['auth/MY_FIRST_NAME']
      const isLastName = !!this.$store.getters['auth/MY_LAST_NAME']
      const isUsername = !!this.$store.getters['auth/MY_USERNAME']

      return isFirstName && isLastName && isUsername
    },
    is_any_project () {
      return this.$store.getters['auth/IS_ANY_PROJECT']
    }
  },
  methods: {
    addTeamMember () {
      if (this.team_form_email === null) return false

      this.team_table_data.data.push({
        email: this.team_form_email
      })

      this.team_form_email = null
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
