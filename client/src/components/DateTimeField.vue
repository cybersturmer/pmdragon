<template>
  <q-input filled v-model="datetime">
    <template v-slot:prepend>
      <q-icon name="event" class="cursor-pointer">
        <q-popup-proxy transition-show="scale" transition-hide="scale">
          <q-date v-model="datetime" mask="YYYY-MM-DD HH:mm" />
        </q-popup-proxy>
      </q-icon>
    </template>

    <template v-slot:append>
      <q-icon name="access_time" class="cursor-pointer">
        <q-popup-proxy transition-show="scale" transition-hide="scale">
          <q-time v-model="datetime" mask="YYYY-MM-DD HH:mm" format24h />
        </q-popup-proxy>
      </q-icon>
    </template>
  </q-input>
</template>

<script>
export default {
  name: 'DateTimeField',
  props: {
    datetime: {
      type: String,
      required: true
    }
  }
}
</script>

<style scoped>

</style>
