export function IS_LOGGED_IN (state, getters) {
  return getters.USER_ID && getters.IS_ACCESS_TOKEN_VALID && getters.IS_REFRESH_TOKEN_VALID
}

export function IS_ACCESS_TOKEN_VALID (state) {
  const now = Date.now()
  return state.tokens.access.expired_at !== null &&
    now < Date.parse(state.tokens.access.expired_at)
}

export function IS_REFRESH_TOKEN_VALID (state) {
  const now = Date.now()
  return state.tokens.refresh.expired_at !== null &&
    now < Date.parse(state.tokens.refresh.expired_at)
}

export function ACCESS_TOKEN (state) {
  return state.tokens.access.data
}

export function REFRESH_TOKEN (state) {
  return state.tokens.refresh.data
}

export function PERSON_BY_ID (state, getters) {
  /** Getting person by id from current workspace **/
  return personId => {
    return getters.WORKSPACE_DATA.participants
      .filter((participant) => participant.id === personId)
      .pop()
  }
}

export function WORKSPACES (state) {
  return state.workspaces
}

export function WORKSPACE_DATA (state, getters, rootState, rootGetters) {
  return state.workspaces.find(workspace => workspace.prefix_url === rootGetters['current/WORKSPACE'])
}

export function WORKSPACE_ID (state, getters) {
  return getters.WORKSPACE_DATA.id
}

export function PROJECT_DATA (state, getters, rootState, rootGetters) {
  return getters.WORKSPACE_DATA.projects.find(project => project.id === rootGetters['current/PROJECT'])
}

export function PROJECT_NAME (state, getters) {
  try {
    return getters.PROJECT_DATA.title
  } catch (e) {
    return null
  }
}

export function FIRST_NAME (state) {
  return state.first_name
}

export function LAST_NAME (state) {
  return state.last_name
}

export function USERNAME (state) {
  return state.username
}

export function AVATAR (state) {
  return state.avatar ? state.avatar : null
}

export function USER_ID (state) {
  return state.user_id
}
