import axios from 'axios'
import { DEBUG, PROD_ENV, DEBUG_ENV } from 'src/.env'
import { AuthService } from 'src/services/auth'
import $store from 'src/store'
import $router from 'src/router'
import createAuthRefreshInterceptor from 'axios-auth-refresh'

export class Api {
  constructor (options) {
    this.isAuth = options && options.auth ? options.auth : false
    this.baseURL = DEBUG ? DEBUG_ENV.url : PROD_ENV.url
    this.instance = axios.create({
      baseURL: this.baseURL
    })

    return this.init()
  }

  init () {
    if (this.isAuth) {
      if (AuthService.isRefreshTokenExpired()) {
        $router.push({ name: 'login' })
      }

      this.instance.interceptors.request.use(
        (request) => {
          request.headers.Authorization = AuthService.getBearer()
          return request
        })

      const refreshAuthLogic = failedRequest =>
        AuthService.refresh()
          .then(
            tokens => {
              $store.commit('auth/SET_ACCESS_TOKEN', tokens.data.access)
              $store.commit('auth/SET_REFRESH_TOKEN', tokens.data.refresh)
              failedRequest.response.config.headers.Authorization =
                AuthService.getBearer()

              return Promise.resolve()
            }
          )

      createAuthRefreshInterceptor(this.instance, refreshAuthLogic)
    }

    return this.instance
  }
}
