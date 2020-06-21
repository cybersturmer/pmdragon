import axios from 'axios'
import { API_URL } from 'src/.env'
import { AuthService } from 'src/services/auth'

export class Api {
  constructor (options) {
    this.isAuth = options && options.auth ? options.auth : false
    this.instance = axios.create({
      baseURL: API_URL
    })

    return this.init()
  }

  init () {
    if (this.isAuth) {
      this.instance.interceptors.request.use(request => {
        request.headers.authorization = AuthService.getBearer()

        if (!AuthService.authNeedUpdate()) return request

        return AuthService.refresh()
          .then(() => {
            request.headers.authorization = AuthService.getBearer()
            return request
          }).catch(error => Promise.reject(error))
      }, (error) => Promise.reject(error))
    }

    return this.instance
  }
}
