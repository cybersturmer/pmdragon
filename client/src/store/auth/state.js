import { LocalStorage, SessionStorage } from 'quasar'

export default function () {
  return {
    user_id: LocalStorage.getItem('auth.user_id') || null,
    workspaces: LocalStorage.getItem('auth.workspaces') || [],
    persons: LocalStorage.getItem('auth.persons') || [],
    invited: LocalStorage.getItem('auth.invited') || [],
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
