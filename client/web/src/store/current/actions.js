import { Api } from 'src/services/api'
import { ErrorWrapper, HandleResponse } from 'src/services/util'

export async function INIT_WORKSPACES ({ commit }) {
  try {
    const response = await new Api({ auth: true }).get('/auth/workspaces/')
    HandleResponse.compare(200, response.status)
    commit('INIT_WORKSPACES', response.data)
  } catch (error) {
    throw new ErrorWrapper(error)
  }
}

export function SELECT_WORKSPACE ({ commit }, payload) {
  commit('SELECT_WORKSPACE', payload)
}

export function SELECT_PROJECT ({ commit }, payload) {
  commit('SELECT_PROJECT', payload)
}

export function RESET_STATE ({ commit }) {
  commit('RESET')
}

export function RESET_WORKSPACE ({ commit }) {
  commit('RESET_WORKSPACE')
}

export function RESET_PROJECT ({ commit }) {
  commit('RESET_PROJECT')
}
