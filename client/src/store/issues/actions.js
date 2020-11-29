import { ErrorHandler, HandleResponse } from 'src/services/util'
import { Api } from 'src/services/api'

export async function INIT_BACKLOGS ({ rootGetters, commit }) {
  try {
    const response = await new Api({ auth: true }).get(
      '/core/backlogs/'
    )

    HandleResponse.compare(200, response.status)
    commit('INIT_BACKLOGS', response.data)
  } catch (e) {
    throw new ErrorHandler(e)
  }
}

export async function INIT_SPRINTS ({ rootGetters, commit }) {
  try {
    const response = await new Api({ auth: true }).get(
      '/core/sprints/'
    )

    HandleResponse.compare(200, response.status)
    commit('INIT_SPRINTS', response.data)
  } catch (e) {
    throw new ErrorHandler(e)
  }
}

export async function INIT_ISSUES ({ commit }) {
  try {
    const response = await new Api({ auth: true }).get(
      '/core/issues/'
    )

    HandleResponse.compare(200, response.status)
    commit('INIT_ISSUES', response.data)
  } catch (e) {
    throw new ErrorHandler(e)
  }
}

export async function INIT_SPRINT_DURATIONS ({ commit }) {
  try {
    const response = await new Api({ auth: true }).get(
      '/core/sprint-durations/'
    )

    HandleResponse.compare(200, response.status)
    commit('INIT_SPRINT_DURATIONS', response.data)
  } catch (e) {
    throw new ErrorHandler(e)
  }
}

export async function INIT_ISSUE_STATES ({ commit }) {
  try {
    const response = await new Api({ auth: true }).get(
      '/core/issue-states/'
    )

    HandleResponse.compare(200, response.status)
    commit('UPDATE_ISSUE_STATES', response.data)
  } catch (e) {
    throw new ErrorHandler(e)
  }
}

export async function INIT_ISSUE_TYPES ({ commit }) {
  try {
    const response = await new Api({ auth: true }).get(
      '/core/issue-types/'
    )

    HandleResponse.compare(200, response.status)
    commit('UPDATE_ISSUE_TYPES', response.data)
  } catch (e) {
    throw new ErrorHandler(e)
  }
}

export async function PATCH_ISSUE ({ commit }, payload) {
  /** At least id and one more param must be provided
   * For example: {
   *   id: 1,
   *   issue_state: 2
   * }
   * **/

  try {
    const response = await new Api({ auth: true }).patch(
      `/core/issues/${payload.id}/`,
      payload
    )

    HandleResponse.compare(200, response.status)
    commit('UPDATE_ISSUE', response.data)
  } catch (e) {
    throw new ErrorHandler(e)
  }
}

export async function UPDATE_ISSUE_STATE ({ commit }, payload) {
  try {
    const response = await new Api({ auth: true }).patch(
      `/core/issues/${payload.id}/`,
      { state_category: payload.state_category }
    )

    HandleResponse.compare(200, response.status)
    commit('UPDATE_ISSUE_STATE', payload)
  } catch (e) {
    throw new ErrorHandler(e)
  }
}

export async function UPDATE_ISSUES_IN_SPRINT ({ commit }, composite) {
  const sendPayload = {
    issues: composite.issues
  }

  try {
    const response = await new Api({ auth: true }).patch(
      `/core/sprints/${composite.id}/`,
      sendPayload
    )

    HandleResponse.compare(200, response.status)
    commit('UPDATE_SPRINT_ISSUES', composite)
  } catch (e) {
    throw new ErrorHandler(e)
  }
}

export async function UPDATE_ISSUES_IN_BACKLOG ({ commit }, composite) {
  const sendPayload = {
    issues: composite.issues
  }

  try {
    const response = await new Api({ auth: true }).patch(
      `/core/backlogs/${composite.id}/`,
      sendPayload
    )

    HandleResponse.compare(200, response.status)
    commit('UPDATE_BACKLOG_ISSUES', composite)
  } catch (e) {
    throw new ErrorHandler(e)
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
    commit('ADD_ISSUE_TO_ISSUES', response.data)
  } catch (e) {
    throw new ErrorHandler(e)
  }
}

export async function ADD_SPRINT_TO_PROJECT ({ commit }, payload) {
  try {
    const response = await new Api({ auth: true }).post(
      '/core/sprints/',
      payload
    )

    HandleResponse.compare(201, response.status)
    commit('ADD_SPRINT_TO_PROJECT', response.data)
  } catch (e) {
    throw new ErrorHandler(e)
  }
}

export async function START_SPRINT ({ commit }, sprintId) {
  try {
    const response = await new Api({ auth: true }).patch(
      `/core/sprints/${sprintId}/`,
      { is_started: true }
    )

    HandleResponse.compare(200, response.status)
    commit('START_SPRINT', sprintId)
  } catch (e) {
    throw new ErrorHandler(e)
  }
}

export async function COMPLETE_SPRINT ({ commit }, sprintId) {
  try {
    const response = await new Api({ auth: true }).patch(
      `/core/sprints/${sprintId}/`,
      { is_completed: true }
    )

    HandleResponse.compare(200, response.status)
    commit('COMPLETE_SPRINT', sprintId)
  } catch (e) {
    throw new ErrorHandler(e)
  }
}

export async function EDIT_SPRINT ({ commit }, payload) {
  const sendPayload = {
    title: payload.title,
    goal: payload.goal,
    started_at: payload.startedAt,
    finished_at: payload.finishedAt
  }

  try {
    const response = await new Api({ auth: true }).patch(
      `/core/sprints/${payload.id}/`,
      sendPayload
    )

    HandleResponse.compare(200, response.status)
    commit('UPDATE_SPRINT', response.data)
  } catch (e) {
    throw new ErrorHandler(e)
  }
}

export async function DELETE_SPRINT ({ commit }, sprintId) {
  try {
    const response = await new Api({ auth: true }).delete(
      `/core/sprints/${sprintId}`
    )

    HandleResponse.compare(204, response.status)
    commit('DELETE_SPRINT', sprintId)
  } catch (e) {
    throw new ErrorHandler(e)
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
  } catch (e) {
    throw new ErrorHandler(e)
  }
}

export async function DELETE_ISSUE ({ commit }, payload) {
  try {
    const response = await new Api({ auth: true }).delete(
      `/core/issues/${payload.id}`
    )

    HandleResponse.compare(204, response.status)
    commit('DELETE_ISSUE', payload)
  } catch (e) {
    throw new ErrorHandler(e)
  }
}

export async function ORDER_BACKLOG_ISSUES ({ commit, rootGetters }, payload) {
  const issuesPayload = []

  try {
    payload.forEach((value) => {
      issuesPayload.push({
        id: value.id,
        ordering: value.ordering
      })
    })
  } catch (e) {
    console.log(e)
  }

  try {
    const response = await new Api({ auth: true }).put(
      '/core/issue/ordering/',
      issuesPayload
    )

    HandleResponse.compare(200, response.status)
    commit('ORDER_BACKLOG_ISSUES', payload)
  } catch (e) {
    throw new ErrorHandler(e)
  }
}

export async function UPDATE_ISSUES_ORDERING ({ commit }, payload) {
  try {
    const response = await new Api({ auth: true }).put(
      '/core/issue/ordering/',
      payload
    )

    HandleResponse.compare(200, response.status)
    commit('UPDATE_ISSUES_ORDERING', payload)
  } catch (e) {
    throw new ErrorHandler(e)
  }
}

export function RESET ({ commit }) {
  commit('RESET')
}
