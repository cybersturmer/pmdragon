import { LocalStorage } from 'quasar'

function findProjectBacklog (state, projectId) {
  return state.backlogs.findIndex((el, index, array) => {
    return el.project_id === projectId
  })
}

function findBacklogIssue (issues, issueId) {
  return issues.findIndex((el, index, array) => {
    return el.id === issueId
  })
}

function findIssueIndexes (state, projectId, issueId) {
  const backlogIndex = findProjectBacklog(state, projectId)
  const issuesIndex = findBacklogIssue(state.backlogs[backlogIndex].issues, issueId)

  return {
    backlogIndex,
    issuesIndex
  }
}

export function INIT_BACKLOGS (state, payload) {
  state.backlogs = payload
  LocalStorage.set('issues.backlogs', payload)
}

export function INIT_SPRINT_DURATIONS (state, payload) {
  state.sprint_durations = payload
  LocalStorage.set('issues.sprint_durations', payload)
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
  const indexes = findIssueIndexes(state, payload.project, payload.id)
  state.backlogs[indexes.backlogIndex].issues.splice(indexes.issuesIndex, 1, payload)
  LocalStorage.set('issues.backlogs', state.backlogs)
}

export function ORDER_BACKLOG_ISSUES (state, payload) {
  const project = payload[0].project
  const backlogIndex = findProjectBacklog(state, project)
  state.backlogs[backlogIndex].issues = payload
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
