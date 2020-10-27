export const fieldValidationMixin = {
  methods: {
    isFieldValid (field) {
      return this.form_errors[field].length > 0
    },
    resetFieldErrorMessage (field) {
      this.form_errors[field] = ''
    }
  }
}
