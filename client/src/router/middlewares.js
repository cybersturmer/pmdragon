import $store from '../store'
import { AuthService } from 'src/services/auth'

export async function initCurrentUserStateMiddleware (to, from, next) {
  if (AuthService.authNeedUpdate()) {
    try {
      await AuthService.refresh()
      next()
    } catch (e) {
      console.log(e)
    }
  } else {
    next()
  }
}

export function checkAccessMiddleware (to, from, next) {
  const currentUserId = $store.getters['auth/USER_ID']

  const isAuthRoute = to.matched.some(item => item.meta.requiredAuth)

  if (isAuthRoute && currentUserId) return next()
  if (isAuthRoute) return next({ name: 'login' })
  next()
}

export function setPageTitleMiddleware (to, from, next) {
  const pageTitle = to.matched.find(item => item.meta.title)

  if (pageTitle) window.document.title = pageTitle.meta.title
  next()
}
