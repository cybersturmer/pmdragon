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
          color: 'amber'
        }
      })
    },
    showError (e) {
      if (!e.messageUseful) return false

      return this.showConfirmDialog(
        e.statusMessage,
        e.message
      )
    }
  }
}
