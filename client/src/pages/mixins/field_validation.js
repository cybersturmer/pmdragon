export const fieldValidationMixin = {
  methods: {
    isFieldValid (field) {
      return this.form_errors[field].length > 0
    },
    resetFieldErrorMessage (field) {
      this.form_errors[field] = ''
    },
    isValidEmail (emailString) {
      const emailPattern = /^(?=[a-zA-Z0-9@._%+-]{6,254}$)[a-zA-Z0-9._%+-]{1,64}@(?:[a-zA-Z0-9-]{1,63}\.){1,8}[a-zA-Z]{2,63}$/
      return emailPattern.test(emailString) || false
    }
  }
}
