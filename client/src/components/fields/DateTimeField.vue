<template>
  <q-input dark flat :value="rawDatetime" @input="handleInput">
    <template v-slot:prepend>
      <q-icon name="event" class="cursor-pointer">
        <q-popup-proxy transition-show="scale" transition-hide="scale">
          <q-date
            dark
            :value="rawDatetime"
            @input="handleInput($event)"
            :mask="mask" />
        </q-popup-proxy>
      </q-icon>
    </template>

    <template v-slot:append>
      <q-icon name="access_time" class="cursor-pointer">
        <q-popup-proxy transition-show="scale" transition-hide="scale">
          <q-time
            dark
            :value="rawDatetime"
            @input="handleInput($event)"
            :mask="mask"
            :minute-options="minuteOptions"
            format24h />
        </q-popup-proxy>
      </q-icon>
    </template>
  </q-input>
</template>

<script>
import { DATETIME_MASK } from 'src/services/masks'

export default {
  name: 'DateTimeField',
  props: {
    value: String
  },
  data () {
    return {
      mask: DATETIME_MASK,
      minuteOptions: [0, 15, 30, 45],
      rawDatetime: this.value
    }
  },
  computed: {
    datetime: function () {
      return this.rawDatetime
    }
  },
  methods: {
    handleInput (value) {
      this.rawDatetime = value
      this.$emit('input', value)
    }
  }
}
</script>

<style scoped>

</style>
