<template>
  <q-input
    dark
    filled
    type="password"
    @input="handleInput"
    :value="password"
    :error="isError"
    :error-message="error_message"
    label-color="amber"
    label="Password"/>
</template>

<script>
import { fieldValidationMixin } from 'pages/mixins/field_validation'

export default {
  name: 'PasswordField',
  mixins: [fieldValidationMixin],
  props: {
    value: String,
    error_message: String
  },
  data () {
    return {
      password: this.value
    }
  },
  methods: {
    handleInput (value) {
      this.password = value
      this.$emit('input', value)
    }
  },
  computed: {
    isError () {
      return this.error_message.length > 0
    }
  }
}
</script>
