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

export function SET_FIRST_NAME (state, payload) {
  state.first_name = payload
  LocalStorage.set('auth.first_name', payload)
}

export function SET_LAST_NAME (state, payload) {
  state.last_name = payload
  LocalStorage.set('auth.last_name', payload)
}

export function SET_USERNAME (state, payload) {
  state.username = payload
  LocalStorage.set('auth.username', payload)
}

export function SET_AVATAR (state, payload) {
  if (payload === null) return false

  state.avatar = payload
  LocalStorage.set('auth.avatar', payload)
}

export function LOGOUT (state) {
  state.user_id = null
  state.username = null
  state.avatar = null
  state.first_name = null
  state.last_name = null
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
