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

export function FIRST_NAME (state) {
  return state.first_name
}

export function LAST_NAME (state) {
  return state.last_name
}

export function USERNAME (state) {
  return state.username
}

export function USER_ID (state) {
  return state.user_id
}
