import axios from 'axios'
import { DEBUG, PROD_ENV, DEBUG_ENV } from 'src/.env'
import { AuthService } from 'src/services/auth'
import $router from 'src/router'

export class Api {
  constructor (options) {
    this.isAuth = options && options.auth ? options.auth : false
    this.instance = axios.create({
      baseURL: DEBUG ? DEBUG_ENV.url : PROD_ENV.url
    })

    return this.init()
  }

  init () {
    if (this.isAuth) {
      this.instance.interceptors.request.use(
        (request) => {
          console.log('Interceptor')
          console.log(request)
          request.headers.authorization = AuthService.getBearer()

          if (!AuthService.authNeedUpdate()) return request

          return AuthService.refresh()
            .then(() => {
              request.headers.authorization = AuthService.getBearer()
              return request
            })
            .catch(error => Promise.reject(error))
        },
        (error) => {
          console.log('API code')
          console.log(error)
          if (error.response.status !== 401) return Promise.reject(error)

          /** We dont have valid refresh token, so force user to login page **/
          if (!AuthService.isRefreshToken()) $router.push({ name: 'login' })

          console.log('Refresh token is valid, we gonna refresh it')
          AuthService.refresh()
            .then(() => {
              error.headers.authorization = AuthService.getBearer()
              return error
            })
        })
    }

    return this.instance
  }
}
