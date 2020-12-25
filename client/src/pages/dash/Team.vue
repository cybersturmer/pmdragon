<template>
  <q-page class="q-pa-lg">
    <q-table
      dark
      grid
      title="Team"
      row-key="username"
      no-data-label="Invite your team members by adding them by email."
      :data="participants"
      :columns="teamTable.columns"
      :filter="teamTable.filter">
      <template #top-left>
        <q-btn-group outline>
          <q-btn
            outline
            size="sm"
            label="Invite member"
            @click="inviteMembersDialog"
          />
          <q-btn
            outline
            size="sm"
            label="Manage team"
          />
        </q-btn-group>
      </template>
      <template #top-right>
        <q-input dark dense debounce="300" v-model="teamTable.filter" placeholder="Search">
          <template #append>
            <q-icon name="search" />
          </template>
        </q-input>
      </template>
      <template #item="props">
        <div class="q-pa-xs col-xs-12 col-sm-6 col-md-2">
          <q-card dark bordered>
            <q-card-section class="text-center" style="min-height: 150px">
              <div>
                <q-avatar
                v-if="props.row.avatar">
                  <img :src="props.row.avatar" :alt="props.row.username">
                </q-avatar>
              </div>
              <span class="text-h6">{{ props.row.first_name }} {{ props.row.last_name }}</span>
            </q-card-section>
          </q-card>
        </div>
      </template>
    </q-table>
    <q-table
      dark
      grid
      title="Invited members"
      row-key="email"
      no-data-label="Invite your team members by adding them by email."
      :data="invited"
      :columns="invitedTable.columns"
      :filter="invitedTable.filter">
      <template #item="props">
        <div class="q-pa-xs col-xs-12 col-sm-5 col-md-1">
          <q-card dark bordered>
            <q-card-section style="height: 100px">
              <p class="q-ma-sm q-pa-none"><strong>Email:</strong> {{ props.row.email }}</p>
              <p class="q-ma-sm q-pa-none"><strong>Expired:</strong> {{ props.row.expired_at | moment("from", "now") }}</p>
            </q-card-section>
          </q-card>
        </div>
      </template>
    </q-table>
  </q-page>
</template>

<script>
import InviteMemberDialog from 'components/dialogs/InviteMemberDialog'

export default {
  name: 'Team',
  data () {
    return {
      teamTable: {
        columns: [
          {
            name: 'avatar'
          },
          {
            name: 'username',
            required: true,
            label: 'Username',
            align: 'left',
            field: row => row.username,
            format: val => `${val}`,
            sortable: true
          },
          {
            name: 'name',
            required: true,
            label: 'Name',
            field: row => `${row.first_name} ${row.last_name}`,
            sortable: true
          }
        ],
        filter: ''
      },
      invitedTable: {
        columns: [
          {
            name: 'email',
            required: true,
            label: 'Email',
            align: 'left',
            field: row => row.email,
            format: val => `${val}`,
            sortable: true
          },
          {
            name: 'expired',
            required: true,
            label: 'Expired At',
            field: row => this.$moment(row.expired_at).fromNow(),
            sortable: true
          }
        ],
        filter: ''
      }
    }
  },
  computed: {
    participants () {
      try {
        return this.$store.getters['auth/WORKSPACE_DATA'].participants
      } catch (e) {
        return []
      }
    },
    invited () {
      const workspaceId = this.$store.getters['auth/WORKSPACE_ID']
      const invited = this.$store.getters['auth/INVITED']

      return invited.filter((invitation) => invitation.workspace === workspaceId)
    }
  },
  methods: {
    inviteMembersDialog () {
      this.$q.dialog({
        parent: this,
        dark: true,
        title: 'Invite Members',
        component: InviteMemberDialog
      })
    }
  }
}
</script>

<style scoped>

</style>
