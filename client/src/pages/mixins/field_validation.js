export const fieldValidationMixin = {
  methods: {
    isValid (module, field) {
      try {
        return this[module][field].length > 0
      } catch (e) {
        return false
      }
    },
    isFieldValid (field) {
      return this.formErrors[field].length > 0
    },
    resetFieldErrorMessage (field) {
      this.formErrors[field] = ''
    },
    isValidEmail (emailString) {
      const emailPattern = /^(?=[a-zA-Z0-9@._%+-]{6,254}$)[a-zA-Z0-9._%+-]{1,64}@(?:[a-zA-Z0-9-]{1,63}\.){1,8}[a-zA-Z]{2,63}$/
      return emailPattern.test(emailString) || false
    }
  }
}
