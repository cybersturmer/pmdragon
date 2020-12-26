<template>
  <q-page class="q-pa-lg">
    <q-table
      dark
      grid
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
            color="amber"
            @click="inviteMembersDialog"
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
        <div class="q-pa-xs col-xs-6 col-sm-4 col-md-3 col-lg-2 col-xl-2" >
          <q-card dark bordered>
            <q-card-section horizontal>
              <!-- Avatar block -->
              <q-card-section class="col-4">
                <q-avatar
                  v-if="props.row.avatar">
                  <img :src="props.row.avatar" :alt="props.row.username">
                </q-avatar>
              </q-card-section>
              <!-- Name block -->
              <q-card-section class="col-8">
                <div class="row items-center no-wrap full-width">
                  <div class="col-10 text-center">
                    <p class="text-h6 q-pa-none q-ma-none" style="line-height: 1.5rem">{{ props.row.first_name }}</p>
                    <p class="text-h6 q-pa-none q-ma-none" style="line-height: 1.5rem">{{ props.row.last_name }}</p>
                  </div>
                  <div class="col-2 items-center">
                    <q-btn
                      v-show="!isMe(props.row.id)"
                      flat
                      dense
                      color="amber"
                      icon="more_vert">
                      <q-menu dark fit anchor="top left" self="top left" auto-close>
                        <q-list>
                          <q-item clickable
                                  @click="removeMemberDialog(props.row.id)">
                            <q-item-section>Remove from Workspace</q-item-section>
                          </q-item>
                        </q-list>
                      </q-menu>
                    </q-btn>
                  </div>
                </div>
              </q-card-section>
            </q-card-section>
          </q-card>
        </div>
      </template>
    </q-table>
    <q-table
      dark
      grid
      :title="`Invited - ( ${invited.length} email )`"
      row-key="email"
      no-data-label="Invite your team members by adding them by email."
      :data="invited"
      :columns="invitedTable.columns"
      :filter="invitedTable.filter"
      :pagination="invitedTable.pagination">
      <template #item="props">
        <div class="q-pa-xs col-xs-12 col-sm-5 col-md-4 col-lg-2 col-xl-2">
          <q-card dark bordered>
            <q-card-section style="height: 90px">
              <p class="q-ma-sm q-pa-none">
                <strong>Email:</strong>
                {{ props.row.email }}
              </p>
              <p class="q-ma-sm q-pa-none" :title="props.row.expired_at">
                <strong>Expired:</strong> {{ props.row.expired_at | moment("from", "now") }}
              </p>
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
        pagination: {
          rowsPerPage: 8
        },
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
    },
    myId () {
      return this.$store.getters['auth/MY_USER_ID']
    }
  },
  methods: {
    isMe (personId) {
      return this.$store.getters['auth/MY_USER_ID'] === personId
    },
    inviteMembersDialog () {
      this.$q.dialog({
        parent: this,
        dark: true,
        title: 'Invite Members',
        component: InviteMemberDialog
      })
    },
    removeMemberDialog (personId) {
      const participant = this.$store.getters['auth/PERSON_BY_ID'](personId)
      this.$q.dialog({
        dark: true,
        title: 'Confirmation',
        message: `Would you like to remove participant: ${participant.first_name} ${participant.last_name}`,
        cancel: true,
        persistent: true
      })
        .onOk(() => {
          this.$store.dispatch('auth/REMOVE_TEAM_MEMBER', personId)
        })
    }
  }
}
</script>

<style scoped>

</style>
