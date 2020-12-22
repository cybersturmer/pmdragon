import axios from 'axios'
import $store from 'src/store'
import { DEBUG, PROD_ENV, DEBUG_ENV } from 'src/.env'
import createAuthRefreshInterceptor from 'axios-auth-refresh'

export class Api {
  constructor (options) {
    this.auth = options && options.auth
      ? options.auth : false

    this.expectedStatus = options && options.expectedStatus
      ? options.expectedStatus : false

    this.axiosOptions = {
      baseURL: DEBUG ? DEBUG_ENV.url : PROD_ENV.url,
      withCredentials: false,
      timeout: 1000,
      validateStatus: (data) => this._expectStatus(data)
    }

    if (this.auth) {
      this.axiosOptions.headers = {
        Authorization: this._getAccessTokenHeader()
      }
    }

    const refreshAuthLogic = (failedRequest) => this._refreshTokens()
      .then((tokenRefreshResponse) => {
        failedRequest.response.config.headers.Authorization =
          this._getAccessTokenHeader()

        return Promise.resolve()
      })

    this.instance = axios.create(this.axiosOptions)

    createAuthRefreshInterceptor(this.instance, refreshAuthLogic)

    return this.instance
  }

  _expectStatus (status) {
    return this.expectedStatus ? status === this.expectedStatus : true
  }

  /** Access token **/
  _getAccessToken () {
    return $store.getters['auth/ACCESS_TOKEN']
  }

  _getAccessTokenHeader () {
    return `Bearer  ${this._getAccessToken()}`
  }

  _isAccessTokenExpired () {
    return !$store.getters['auth/IS_ACCESS_TOKEN_VALID']
  }

  /** Refresh token **/
  _getRefreshToken () {
    return $store.getters['auth/REFRESH_TOKEN']
  }

  _isRefreshTokenExpired () {
    return $store.getters['auth/IS_REFRESH_TOKEN_VALID']
  }

  /** Common tokens **/
  _setAccessToken (accessToken) {
    $store.commit('auth/SET_ACCESS_TOKEN', accessToken)
  }

  _setRefreshToken (refreshToken) {
    $store.commit('auth/SET_REFRESH_TOKEN', refreshToken)
  }

  _refreshTokens () {
    return $store.dispatch('auth/REFRESH')
  }

  _isTokensRefreshRequired () {
    return $store.getters['auth/IS_REFRESH_TOKEN_REQUIRED']
  }
}
