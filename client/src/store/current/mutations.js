import { LocalStorage } from 'quasar'

export function INIT_WORKSPACES (state, payload) {
  state.workspaces = payload
  LocalStorage.set('current.workspaces', payload)
}

export function SELECT_WORKSPACE (state, payload) {
  state.workspace = payload
  // todo Do we really need to store data in LC?
  LocalStorage.set('current.workspace', payload)
}

export function RESET_WORKSPACE (state) {
  state.workspace = null
  LocalStorage.remove('current.workspace')
}

export function RESET_PROJECT (state) {
  state.project = null
  LocalStorage.remove('current.project')
}

export function SELECT_PROJECT (state, payload) {
  state.project = payload
  LocalStorage.set('current.project', payload)
}

export function RESET (state) {
  state.workspaces = []
  state.workspace = null
  state.projects = []
  state.project = null
}
