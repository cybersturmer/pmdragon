export const Dialogs = {
  methods: {
    showConfirmDialog (title, message, unsafe = false) {
      return this.$q.dialog({
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
