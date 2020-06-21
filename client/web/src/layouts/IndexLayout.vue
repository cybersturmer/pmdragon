<template>
  <q-layout view="lHh Lpr lFf" class="bg-grey-9 text-white">
    <q-page-container>
      <keep-alive>
        <router-view />
      </keep-alive>
    </q-page-container>
  </q-layout>
</template>

<script>
export default {
  name: 'IndexLayout'
}
</script>

<style scoped>

</style>
