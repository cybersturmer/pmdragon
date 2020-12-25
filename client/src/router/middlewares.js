import $store from '../store'

export async function initCurrentUserStateMiddleware (to, from, next) {
  try {
    if ($store.getters['auth/IS_REFRESH_TOKEN_REQUIRED']) {
      await $store.dispatch('auth/REFRESH')
    }
  } catch (e) {
    console.log(e)
  }

  next()
}

export function checkAccessMiddleware (to, from, next) {
  const currentUserId = $store.getters['auth/MY_USER_ID']

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
