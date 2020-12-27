import { ErrorHandler } from 'src/services/util'
import { Api } from 'src/services/api'

export async function INIT_BACKLOGS ({ rootGetters, commit }) {
  try {
    const response = await new Api({
      auth: true,
      expectedStatus: 200
    })
      .get(
        '/core/backlogs/'
      )

    commit('INIT_BACKLOGS', response.data)
  } catch (e) {
    throw new ErrorHandler(e)
  }
}

export async function INIT_SPRINTS ({ rootGetters, commit }) {
  try {
    const response = await new Api({
      auth: true,
      expectedStatus: 200
    })
      .get(
        '/core/sprints/'
      )

    commit('INIT_SPRINTS', response.data)
  } catch (e) {
    throw new ErrorHandler(e)
  }
}

export async function INIT_ISSUES ({ commit }) {
  try {
    const response = await new Api({
      auth: true,
      expectedStatus: 200
    })
      .get(
        '/core/issues/'
      )

    commit('INIT_ISSUES', response.data)
  } catch (e) {
    throw new ErrorHandler(e)
  }
}

export async function INIT_SPRINT_DURATIONS ({ commit }) {
  try {
    const response = await new Api({
      auth: true,
      expectedStatus: 200
    })
      .get(
        '/core/sprint-durations/'
      )

    commit('INIT_SPRINT_DURATIONS', response.data)
  } catch (e) {
    throw new ErrorHandler(e)
  }
}

export async function INIT_ISSUE_STATES ({ commit }) {
  try {
    const response = await new Api({
      auth: true,
      expectedStatus: 200
    })
      .get(
        '/core/issue-states/'
      )

    commit('UPDATE_ISSUE_STATES', response.data)
  } catch (e) {
    throw new ErrorHandler(e)
  }
}

export async function INIT_ISSUE_TYPES ({ commit }) {
  try {
    const response = await new Api({
      auth: true,
      expectedStatus: 200
    })
      .get(
        '/core/issue-types/'
      )

    commit('UPDATE_ISSUE_TYPES', response.data)
  } catch (e) {
    throw new ErrorHandler(e)
  }
}

export async function INIT_ISSUE_ESTIMATIONS ({ commit }) {
  try {
    const response = await new Api({
      auth: true,
      expectedStatus: 200
    })
      .get(
        '/core/issue-estimations/'
      )

    commit('UPDATE_ISSUE_ESTIMATIONS', response.data)
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
    const response = await new Api({
      auth: true,
      expectedStatus: 200
    })
      .patch(
      `/core/issues/${payload.id}/`,
      payload
      )

    commit('UPDATE_ISSUE', response.data)
  } catch (e) {
    throw new ErrorHandler(e)
  }
}

export async function UPDATE_ISSUE_STATE ({ commit }, payload) {
  try {
    await new Api({
      auth: true,
      expectedStatus: 200
    })
      .patch(
      `/core/issues/${payload.id}/`,
      { state_category: payload.state_category }
      )

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
    await new Api({
      auth: true,
      expectedStatus: 200
    })
      .patch(
      `/core/sprints/${composite.id}/`,
      sendPayload
      )

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
    await new Api({
      auth: true,
      expectedStatus: 200
    })
      .patch(
      `/core/backlogs/${composite.id}/`,
      sendPayload
      )

    commit('UPDATE_BACKLOG_ISSUES', composite)
  } catch (e) {
    throw new ErrorHandler(e)
  }
}

export async function ADD_ISSUE_TO_BACKLOG ({ commit }, payload) {
  try {
    const response = await new Api({
      auth: true,
      expectedStatus: 201
    })
      .post(
        '/core/issues/',
        payload
      )

    commit('ADD_ISSUE_TO_BACKLOG', response.data)
    commit('ADD_ISSUE_TO_ISSUES', response.data)
  } catch (e) {
    throw new ErrorHandler(e)
  }
}

export async function ADD_SPRINT_TO_PROJECT ({ commit }, payload) {
  try {
    const response = await new Api({
      auth: true,
      expectedStatus: 201
    })
      .post(
        '/core/sprints/',
        payload
      )

    commit('ADD_SPRINT_TO_PROJECT', response.data)
  } catch (e) {
    throw new ErrorHandler(e)
  }
}

export async function START_SPRINT ({ commit }, sprintId) {
  try {
    await new Api({
      auth: true,
      expectedStatus: 200
    })
      .patch(
      `/core/sprints/${sprintId}/`,
      { is_started: true }
      )

    commit('START_SPRINT', sprintId)
  } catch (e) {
    throw new ErrorHandler(e)
  }
}

export async function COMPLETE_SPRINT ({ commit }, sprintId) {
  try {
    await new Api({ auth: true }).patch(
      `/core/sprints/${sprintId}/`,
      { is_completed: true }
    )

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
    const response = await new Api({
      auth: true,
      expectedStatus: 200
    })
      .patch(
      `/core/sprints/${payload.id}/`,
      sendPayload
      )

    commit('UPDATE_SPRINT', response.data)
  } catch (e) {
    throw new ErrorHandler(e)
  }
}

export async function DELETE_SPRINT ({ commit }, sprintId) {
  try {
    await new Api({
      auth: true,
      expectedStatus: 204
    })
      .delete(
      `/core/sprints/${sprintId}`
      )

    commit('DELETE_SPRINT', sprintId)
  } catch (e) {
    throw new ErrorHandler(e)
  }
}

export async function EDIT_ISSUE ({ commit }, payload) {
  try {
    const response = await new Api({
      auth: true,
      expectedStatus: 200
    })
      .put(
      `/core/issues/${payload.id}/`,
      payload
      )

    commit('EDIT_ISSUE', response.data)
  } catch (e) {
    throw new ErrorHandler(e)
  }
}

export async function DELETE_ISSUE ({ commit }, payload) {
  try {
    await new Api({
      auth: true,
      expectedStatus: 204
    })
      .delete(
      `/core/issues/${payload.id}`
      )

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
    await new Api({
      auth: true,
      expectedStatus: 200
    })
      .put(
        '/core/issue/ordering/',
        issuesPayload
      )

    commit('ORDER_BACKLOG_ISSUES', payload)
  } catch (e) {
    throw new ErrorHandler(e)
  }
}

export async function UPDATE_ISSUES_ORDERING ({ commit }, payload) {
  try {
    await new Api({
      auth: true,
      expectedStatus: 200
    })
      .put(
        '/core/issue/ordering/',
        payload
      )

    commit('UPDATE_ISSUES_ORDERING', payload)
  } catch (e) {
    throw new ErrorHandler(e)
  }
}

export function RESET ({ commit }) {
  commit('RESET')
}
