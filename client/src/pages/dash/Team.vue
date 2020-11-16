<template>
  <q-page class="q-pa-lg">
    <q-table
      dark
      grid
      title="Team"
      row-key="username"
      no-data-label="Invite your team members by adding them by email."
      :data="participants"
      :columns="team_table.columns"
      :filter="team_table.filter"
    >
      <template v-slot:top-right>
        <q-input dark dense debounce="300" v-model="team_table.filter" placeholder="Search">
          <template v-slot:append>
            <q-icon name="search" />
          </template>
        </q-input>
      </template>
      <template v-slot:item="props">
        <div class="q-pa-xs col-xs-12 col-sm-6 col-md-2">
          <q-card dark bordered>
            <q-card-section class="text-center" style="min-height: 114px">
              <div>
                <q-avatar
                v-if="props.row.avatar">
                  <img :src="props.row.avatar" :alt="props.row.username">
                </q-avatar>
              </div>

              <span class="q-ml-md text-h6">{{ props.row.first_name }} {{ props.row.last_name }}</span>
            </q-card-section>
          </q-card>
        </div>
      </template>
    </q-table>
  </q-page>
</template>

<script>
export default {
  name: 'Team',
  data () {
    return {
      team_table: {
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
      }
    }
  },
  computed: {
    participants () {
      return this.$store.getters['auth/WORKSPACE_DATA'].participants
    }
  }
}
</script>

<style scoped>

</style>
