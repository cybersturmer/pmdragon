<template>
  <q-dialog ref="dialog" @hide="onDialogHide">
    <q-card dark flat bordered class="q-dialog-plugin bg-secondary">
      <q-card-section>
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
          <template #body-cell-email="props">
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
      </q-card-section>
      <q-card-section>
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
          <template #append>
            <q-btn dense
                   flat
                   icon="add"
                   @click="addTeamMember"
            />
          </template>
        </q-input>
      </q-card-section>
      <q-card-actions vertical>
        <q-btn
          outline
          label="Invite"
          color="amber"
          @click="onOKClick"
        />
      </q-card-actions>
    </q-card>
  </q-dialog>
</template>

<script>
import { fieldValidationMixin } from 'pages/mixins/field_validation'
import { Dialogs } from 'pages/mixins/dialogs'

export default {
  name: 'SprintEditDialog',
  mixins: [fieldValidationMixin, Dialogs],
  components: { },
  data () {
    return {
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
  methods: {
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
    cancelInvitation (email) {
      /**
       * Just remove email from the payload that we gonna send to
       * create team members **/

      this.teamTableData.data = this.teamTableData.data.filter((row) => row.email !== email)
    },
    show () {
      this.$refs.dialog.show()
    },

    hide () {
      this.$refs.dialog.hide()
    },

    onDialogHide () {
      this.$emit('hide')
    },

    async onOKClick () {
      /** Create team by sending emails on server **/
      const payload = {
        invites: []
      }

      const teamData = this.teamTableData.data

      for (const emailElement in teamData) {
        const dictPayload = {
          email: teamData[emailElement].email,
          workspace: this.$store.getters['auth/WORKSPACE_ID']
        }

        payload.invites.push(dictPayload)
      }

      await this.$store.dispatch('auth/INVITE_TEAM', payload)
      this.isTeamStepDone = true
      this.$emit('ok', payload)
      this.hide()
    },

    onCancelClick () {
      this.hide()
    }
  }
}
</script>
