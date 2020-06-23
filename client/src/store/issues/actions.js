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

export async function DELETE_ISSUE ({ commit }, payload) {
  try {
    const response = await new Api({ auth: true }).delete(
      `/core/issues/${payload.id}`
    )

    HandleResponse.compare(204, response.status)
    commit('DELETE_ISSUE', payload)
  } catch (error) {
    throw new ErrorWrapper(error)
  }
}

export async function ORDER_BACKLOG_ISSUES ({ commit, rootGetters }, payload) {
  const issuesPayload = []
  const backlogId = rootGetters['issues/BACKLOG'].id

  try {
    payload.forEach((value) => {
      issuesPayload.push({
        id: value.id,
        ordering: value.ordering
      })
    })
  } catch (error) {
    console.log(error)
  }

  const payloadApi = {
    issues: issuesPayload
  }

  try {
    const response = await new Api({ auth: true }).put(
      `/core/issues/ordering/${backlogId}/`,
      payloadApi
    )

    HandleResponse.compare(200, response.status)
    commit('ORDER_BACKLOG_ISSUES', payload)
  } catch (error) {
    throw new ErrorWrapper(error)
  }
}
