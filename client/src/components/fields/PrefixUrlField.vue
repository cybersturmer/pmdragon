<template>
  <q-input
    dark
    flat
    type="text"
    @input="handleInput"
    :value="prefixUrl"
    :error="isError"
    :error-message="errorMessage"
    label="Workspace prefix"
    label-color="amber"
  />
</template>

<script>
import { fieldValidationMixin } from 'pages/mixins/field_validation'

export default {
  name: 'PrefixUrlField',
  mixins: [fieldValidationMixin],
  props: {
    value: String,
    errorMessage: String
  },
  data () {
    return {
      prefixUrl: this.value
    }
  },
  methods: {
    handleInput (value) {
      this.prefixUrl = value
      this.$emit('input', value)
    }
  },
  computed: {
    isError () {
      try {
        return this.errorMessage.length > 0
      } catch (e) {
        return false
      }
    }
  }
}
</script>
