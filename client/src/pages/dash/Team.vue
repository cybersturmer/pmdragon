<template>
  <q-page class="q-pa-lg">
    <q-table
      dense
      flat
      square
      row-key="username"
      dark
      no-data-label="Invite your team members by adding them by email."
      :data="participants"
      :columns="columns"
    >
    </q-table>
  </q-page>
</template>

<script>
export default {
  name: 'Team',
  data () {
    return {
      columns: [
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
          align: 'left',
          field: row => `${row.first_name} ${row.last_name}`,
          sortable: true
        }
      ]
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
