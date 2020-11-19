<template>
  <q-input
    dark
    filled
    type="password"
    @input="handleInput"
    :value="password"
    :error="isError"
    :error-message="errorMessage"
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
    errorMessage: String
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
      return this.errorMessage.length > 0
    }
  }
}
</script>
