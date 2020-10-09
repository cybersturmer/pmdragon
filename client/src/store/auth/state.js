import { LocalStorage, SessionStorage } from 'quasar'

export default function () {
  return {
    user_id: LocalStorage.getItem('auth.user_id') || null,
    username: LocalStorage.getItem('auth.username') || null,
    first_name: LocalStorage.getItem('auth.first_name') || null,
    last_name: LocalStorage.getItem('auth.last_name') || null,
    tokens: {
      access: LocalStorage.getItem('auth.tokens.access') || {
        data: null,
        expired_at: null
      },
      refresh: SessionStorage.getItem('auth.tokens.refresh') || {
        data: null,
        expired_at: null
      }
    }
  }
}
