import { LocalStorage } from 'quasar'

function findIssueIndexes (state, projectId, issueId) {
  const backlogIndex = state.backlogs.findIndex((el, index, array) => {
    return el.project_id === projectId
  })

  const issuesIndex = state.backlogs[backlogIndex].issues.findIndex((el, index, array) => {
    return el.id === issueId
  })

  return {
    backlogIndex,
    issuesIndex
  }
}

export function INIT_BACKLOGS (state, payload) {
  state.backlogs = payload
  LocalStorage.set('issues.backlogs', payload)
}

export function ADD_ISSUE_TO_BACKLOG (state, payload) {
  state.backlogs
    .filter((backlog) => backlog.workspace.id === payload.workspace && backlog.project_id === payload.project)
    .pop().issues
    .push(payload)

  LocalStorage.set('issues.backlogs', state.backlogs)
}

export function EDIT_ISSUE (state, payload) {
  /**
   * Payload should contain at least workspace, project, id, field
   * It helps us to put it in the right place */

  const backlogIndex = state.backlogs.findIndex(function (el, index, array) {
    return el.project_id === payload.project
  })

  const issuesIndex = state.backlogs[backlogIndex].issues.findIndex(function (el, index, array) {
    return el.id === payload.id
  })

  state.backlogs[backlogIndex].issues.splice(issuesIndex, 1, payload)
  LocalStorage.set('issues.backlogs', state.backlogs)
}

export function DELETE_ISSUE (state, payload) {
  const indexes = findIssueIndexes(state, payload.project, payload.id)
  state.backlogs[indexes.backlogIndex].issues.splice(indexes.issuesIndex, 1)
  LocalStorage.set('issues.backlogs', state.backlogs)
}

export function RESET (state) {
  state.backlogs = []
}
