<template>
  <q-page class="flex q-layout-padding">

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
    }
  }
}
</script>

<style scoped>

</style>
