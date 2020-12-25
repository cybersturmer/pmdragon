import axios from 'axios'
import $store from 'src/store'
import { DEBUG, PROD_ENV, DEBUG_ENV } from 'src/.env'
import createAuthRefreshInterceptor from 'axios-auth-refresh'

export class Api {
  constructor (options) {
    // If we should be authorized before using method than use different flow
    this.auth = options && options.auth
      ? options.auth : false

    // If expected status given  - then we throw an exception for other statuses
    this.expectedStatus = options && options.expectedStatus
      ? options.expectedStatus : false

    /** These options are completely for axios
     * https://github.com/axios/axios#config-defaults **/
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
    /** Expect status given in constructor and give an exception else **/
    return this.expectedStatus ? status === this.expectedStatus : true
  }

  /** Access token **/
  _getAccessToken () {
    /** Give a body of access token **/
    return $store.getters['auth/ACCESS_TOKEN']
  }

  _getAccessTokenHeader () {
    /** Get a prepared Authorization header **/
    return `Bearer  ${this._getAccessToken()}`
  }

  _isAccessTokenExpired () {
    /** Expiration calculated by decoding token body **/
    return !$store.getters['auth/IS_ACCESS_TOKEN_VALID']
  }

  /** Refresh token **/
  _getRefreshToken () {
    /** Get refresh Token **/
    return $store.getters['auth/REFRESH_TOKEN']
  }

  _isRefreshTokenExpired () {
    /** Expiration calculated by decoding token body **/
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
