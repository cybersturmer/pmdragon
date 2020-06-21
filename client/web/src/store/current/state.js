import { LocalStorage } from 'quasar'

export default function () {
  return {
    workspaces: LocalStorage.getItem('current.workspaces') || [],
    workspace: LocalStorage.getItem('current.workspace') || null,
    project: LocalStorage.getItem('current.project') || null
  }
}
