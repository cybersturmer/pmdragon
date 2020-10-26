import { DEBUG, PROD_ENV, DEBUG_ENV } from 'src/.env'
import axios from 'axios'
import $store from 'src/store'
import $router from 'src/router'
import { HandleResponse } from 'src/services/util'

// Inspired by https://github.com/zmts/beauty-vuejs-boilerplate/blob/master/src/services/auth.service.js
export class AuthService {
  static async login (credentials) {
    /**
     * Login by sending login and password
     * @param credentials Object { username: '', password: ''}
     */
    const url = (DEBUG ? DEBUG_ENV.url : PROD_ENV.url) + '/auth/obtain/'

    const response = await axios.post(
      url,
      credentials
    )
    HandleResponse.compare(200, response.status)

    const tokens = response.data.tokens
    _setAuthData(tokens.access, tokens.refresh)

    return response
  }

  static async refresh () {
    /** Refresh access amd refresh token by sending refresh token */
    try {
      const url = (DEBUG ? DEBUG_ENV.url : PROD_ENV.url) + '/auth/refresh/'

      const response = await axios.post(
        url,
        { refresh: $store.getters['auth/REFRESH_TOKEN'] }
      )

      HandleResponse.compare(200, response.status)

      const tokens = response.data

      _setAuthData(tokens.access, tokens.refresh)

      return response
    } catch (e) {
      console.log(e)
      $router.push({ name: 'login' })
        .catch(() => {})
    }
  }

  static async logout () {
    /** Logout by removing auth data on the page
     * @returns {null}
     * */
    _resetAuthData()
  }

  static getAccessToken () {
    return $store.getters['auth/ACCESS_TOKEN']
  }

  /**
   * Get Header Text for using in axios
   * @returns {string}
   **/
  static getBearer () {
    return `Bearer ${this.getAccessToken()}`
  }

  static isAccessTokenExpired () {
    /**
     * @returns {boolean|*}
     */
    return !$store.getters['auth/IS_ACCESS_TOKEN_VALID']
  }

  static isRefreshTokenExpired () {
    /**
     * @returns {boolean|*}
     */
    return !$store.getters['auth/IS_REFRESH_TOKEN_VALID']
  }

  /**
   * Is Refresh token exists and still valid
   * @returns {boolean|*}
   */
  static isRefreshToken () {
    return Boolean($store.getters['auth/REFRESH_TOKEN']) && !this.isRefreshTokenExpired()
  }

  /**
   * If access token expired and refresh token exists and still valid
   * @returns {*|boolean}
   */
  static authNeedUpdate () {
    return Boolean(this.isAccessTokenExpired() && this.isRefreshToken())
  }
}

/**
 * Set Auth Data (to Vuex store), parsing details from it
 * @private
 * @param access
 * @param refresh
 */
function _setAuthData (access, refresh) {
  $store.commit('auth/SET_ACCESS_TOKEN', access)
  $store.commit('auth/SET_REFRESH_TOKEN', refresh)
}

/**
 * Reset auth data from Vuex store
 * @private
 */
function _resetAuthData () {
  $store.commit('auth/LOGOUT')
}
