export const Dialogs = {
  methods: {
    showErrorDialog (title, message) {
      this.$q.dialog({
        dark: true,
        title: title,
        message: message,
        ok: {
          label: 'OK',
          color: 'accent'
        }
      })
    }
  }
}
