<template>
  <q-page class="flex q-layout-padding">
    <div class="column full-width">
      <div class="row">First name {{ firstName }}</div>
      <div class="row">Last name {{ lastName }}</div>
      <div class="row">User name {{ userName }}</div>
    </div>
  </q-page>
</template>

<script>
export default {
  name: 'AccountView',
  computed: {
    firstName: {
      get: function () {
        return this.$store.getters['auth/FIRST_NAME']
      },
      set: function () {
        /** @todo Add mutation and action */
      }
    },
    lastName: {
      get: function () {
        return this.$store.getters['auth/LAST_NAME']
      },
      set: function () {
        /** @todo Add mutation and action */
      }
    },
    userName: {
      get: function () {
        return this.$store.getters['auth/USERNAME']
      },
      set: function () {
        /** @todo Add mutation and action */
      }
    }
  }
}
</script>

<style scoped>

</style>
