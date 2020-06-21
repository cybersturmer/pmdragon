import { ErrorWrapper, HandleResponse } from 'src/services/util'
import { Api } from 'src/services/api'

export async function INIT_BACKLOGS ({ rootGetters, commit }) {
  try {
    const response = await new Api({ auth: true }).get(
      '/core/backlogs/'
    )

    HandleResponse.compare(200, response.status)
    commit('INIT_BACKLOGS', response.data)
  } catch (error) {
    throw new ErrorWrapper(error)
  }
}

export async function ADD_ISSUE_TO_BACKLOG ({ commit }, payload) {
  try {
    const response = await new Api({ auth: true }).post(
      '/core/issues/',
      payload
    )

    HandleResponse.compare(201, response.status)
    commit('ADD_ISSUE_TO_BACKLOG', response.data)
  } catch (error) {
    throw new ErrorWrapper(error)
  }
}

export async function EDIT_ISSUE ({ commit }, payload) {
  try {
    const response = await new Api({ auth: true }).put(
      `/core/issues/${payload.id}/`,
      payload
    )

    HandleResponse.compare(200, response.status)
    commit('EDIT_ISSUE', response.data)
  } catch (error) {
    throw new ErrorWrapper(error)
  }
}
