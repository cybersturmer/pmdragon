<template>
  <q-input
    dark
    flat
    type="text"
    @input="handleInput"
    :value="username"
    :error="isError"
    :error-message="errorMessage"
    label="Username"
    label-color="amber"
  />
</template>

<script>
import { fieldValidationMixin } from 'pages/mixins/field_validation'

export default {
  name: 'UsernameField',
  mixins: [fieldValidationMixin],
  props: {
    value: String,
    errorMessage: String
  },
  data () {
    return {
      username: this.value
    }
  },
  methods: {
    handleInput (value) {
      this.username = value
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
