export const Dialogs = {
  methods: {
    showConfirmDialog (title, message, unsafe = false) {
      this.$q.dialog({
        dark: true,
        html: unsafe,
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
