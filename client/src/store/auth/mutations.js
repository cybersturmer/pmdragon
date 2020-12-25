import { LocalStorage, SessionStorage } from 'quasar'

function _parseTokenDetails (token) {
  const base64Url = token.split('.')[1]
  const base64 = base64Url
    .replace(/-/g, '+')
    .replace(/_/g, '/')

  const jsonPayload = decodeURIComponent(
    atob(base64)
      .split('')
      .map((c) => `%${(`00${c
        .charCodeAt(0)
        .toString(16)}`)
        .slice(-2)}`)
      .join('')
  )

  return JSON.parse(jsonPayload)
}

export function SET_ACCESS_TOKEN (state, payload) {
  const tokenDetails = _parseTokenDetails(payload)
  const expiredAt = new Date((tokenDetails.exp - 60) * 1000)

  const access = {
    data: payload,
    expired_at: expiredAt
  }

  state.tokens.access = access
  state.user_id = tokenDetails.user_id

  LocalStorage.set('auth.tokens.access', access)
  LocalStorage.set('auth.user_id', tokenDetails.user_id)
}

export function SET_REFRESH_TOKEN (state, payload) {
  const tokenDetails = _parseTokenDetails(payload)
  const expiredAt = new Date((tokenDetails.exp - 60) * 1000)

  const refresh = {
    data: payload,
    expired_at: expiredAt
  }

  state.tokens.refresh = refresh
  state.user_id = tokenDetails.user_id

  SessionStorage.set('auth.tokens.refresh', refresh)
  SessionStorage.set('auth.user_id', tokenDetails.user_id)
}

export function SET_MY_FIRST_NAME (state, payload) {
  const me = state.persons.find(me => me.id === state.user_id)
  me.first_name = payload
  LocalStorage.set('auth.persons', state.persons)
}

export function SET_MY_LAST_NAME (state, payload) {
  const me = state.persons.find(me => me.id === state.user_id)
  me.last_name = payload
  LocalStorage.set('auth.persons', state.persons)
}

export function SET_MY_USERNAME (state, payload) {
  const me = state.persons.find(me => me.id === state.user_id)
  me.username = payload
  LocalStorage.set('auth.persons', state.persons)
}

export function SET_MY_AVATAR (state, payload) {
  if (payload == null) return false
  const me = state.persons.find(me => me.id === state.user_id)

  me.avatar = payload
  LocalStorage.set('auth.persons', state.persons)
}

export function RESET_MY_AVATAR (state) {
  const me = state.persons.find(me => me.id === state.user_id)
  me.avatar = null
  LocalStorage.set('auth.persons', state.persons)
}

export function INIT_WORKSPACES (state, payload) {
  state.workspaces = payload
  LocalStorage.set('auth.workspaces', state.workspaces)
}

export function INIT_PERSONS (state, payload) {
  state.persons = payload
  LocalStorage.set('auth.persons', state.persons)
}

export function INIT_INVITED (state, payload) {
  state.invited = payload
  LocalStorage.set('auth.invited', state.invited)
}

export function ADD_INVITED (state, payload) {
  state.invited.push(payload)
  LocalStorage.set('auth.invited', state.invited)
}

export function REMOVE_PARTICIPANT (state, payload) {
  /** Payload
   * { workspace: workspaceId,
      participantId: personId } **/

  const workspace = state.workspaces
    .find(workspace => workspace.id === payload.workspaceId)

  workspace.participants = workspace.participants
    .filter((participant) => participant.id !== payload.participantId)
  LocalStorage.set('auth.workspaces', state.workspaces)
}

export function ADD_WORKSPACE (state, payload) {
  state.workspaces.push(payload)
  LocalStorage.set('auth.workspaces', state.workspaces)
}

export function ADD_PROJECT (state, payload) {
  const workspace = state.workspaces
    .find(workspace => workspace.id === payload.workspace)

  workspace.projects.push(payload)
  LocalStorage.set('auth.workspaces', state.workspaces)
}

export function LOGOUT (state) {
  state.user_id = null
  state.workspaces = []
  state.persons = []
  state.tokens = {
    access: {
      data: null,
      expired_at: null
    },
    refresh: {
      data: null,
      expired_at: null
    }
  }

  LocalStorage.clear()
  SessionStorage.clear()
}
