export const fieldValidationMixin = {
  methods: {
    isFieldValid (field) {
      return this.form_errors[field].length > 0
    }
  }
}
