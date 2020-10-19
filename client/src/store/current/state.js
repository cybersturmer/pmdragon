import { LocalStorage } from 'quasar'

export default function () {
  return {
    workspace: LocalStorage.getItem('current.workspace') || null,
    project: LocalStorage.getItem('current.project') || null,
    interface_theme: LocalStorage.getItem('current.interface_theme') || []
  }
}
