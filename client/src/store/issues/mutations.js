import { LocalStorage } from 'quasar'

function findBacklogByProjectId (state, projectId) {
  return state.backlogs.findIndex((el, index, array) => {
    return el.project_id === projectId
  })
}

function findBacklogIssue (issues, issueId) {
  return issues.findIndex((el, index, array) => {
    return el.id === issueId
  })
}

function findIssueIndexesInBacklog (state, projectId, issueId) {
  const backlogIndex = findBacklogByProjectId(state, projectId)
  const issuesIndex = findBacklogIssue(state.backlogs[backlogIndex].issues, issueId)

  return {
    backlogIndex,
    issuesIndex
  }
}

function findSprintIndexById (state, sprintId) {
  return state.sprints.findIndex((el, index, array) => {
    return el.id === sprintId
  })
}

function findBacklogIndexById (state, backlogId) {
  return state.backlogs.findIndex((el, index, array) => {
    return el.id === backlogId
  })
}

export function INIT_BACKLOGS (state, payload) {
  state.backlogs = payload
  LocalStorage.set('issues.backlogs', payload)
}

export function INIT_SPRINTS (state, payload) {
  state.sprints = payload
  LocalStorage.set('issues.sprints', payload)
}

export function INIT_ISSUES (state, payload) {
  state.issues = payload
  LocalStorage.set('issues.issues', payload)
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
  const issueIndex = state.issues.findIndex((el, index, array) => {
    return el.id === payload.id
  })

  state.issues.splice(issueIndex, 1, payload)
  LocalStorage.set('issues.issues', state.backlogs)
}

export function ORDER_BACKLOG_ISSUES (state, payload) {
  const project = payload[0].project
  const backlogIndex = findBacklogByProjectId(state, project)
  state.backlogs[backlogIndex].issues = payload
  LocalStorage.set('issues.backlogs', state.backlogs)
}

export function UPDATE_ISSUE_STATE (state, payload) {
  /** Payload content issue object **/
  const issue = state.issues.filter((issue) => issue.id === payload.id).pop()
  issue.state_category = payload.state_category

  LocalStorage.set('issues.issues', state.issues)
}

export function UPDATE_ISSUES_ORDERING (state, payload) {
  payload.forEach((issuePayload) => {
    const issue = state.issues.filter((issue) => issue.id === issuePayload.id).pop()
    issue.ordering = issuePayload.ordering
  })

  LocalStorage.set('issues.issues', state.issues)
}

export function ADD_SPRINT_TO_PROJECT (state, payload) {
  state.sprints.push(payload)

  LocalStorage.set('issues.sprints', state.sprints)
}

export function UPDATE_SPRINT_ISSUES (state, composite) {
  /** Just update issues inside sprint
   *  We use composite data for mutation **/
  const sprintIndex = findSprintIndexById(state, composite.id)
  state.sprints[sprintIndex].issues = composite.issues
  LocalStorage.set('issues.sprints', state.sprints)
}

export function START_SPRINT (state, sprintId) {
  /** Start sprint without checking - was it started before or no **/
  const sprintIndex = findSprintIndexById(state, sprintId)
  state.sprints[sprintIndex].is_started = true
  LocalStorage.set('issues.sprints', state.sprints)
}

export function COMPLETE_SPRINT (state, sprintId) {
  /** Compete sprint without checking - was it started
   * or completed before **/
  const sprintIndex = findSprintIndexById(sprintId)
  state.sprints[sprintIndex].is_completed = true
  LocalStorage.set('issues.sprints', state.sprints)
}

export function UPDATE_BACKLOG_ISSUES (state, composite) {
  /** Just update issues inside of Backlog
   * We use composite data for mutation **/
  const backlogIndex = findBacklogIndexById(state, composite.id)
  state.backlogs[backlogIndex].issues = composite.issues
  LocalStorage.set('issues.backlogs', state.backlogs)
}

export function UPDATE_SPRINT (state, payload) {
  const sprintIndex = findSprintIndexById(state, payload.id)
  state.sprints.splice(sprintIndex, 1, payload)
  LocalStorage.set('issues.sprints', state.sprints)
}

export function UPDATE_BACKLOG (state, payload) {
  const backlogIndex = findBacklogByProjectId(state, payload.id)
  state.backlogs.splice(backlogIndex, 1, payload)
  LocalStorage.set('issues.backlogs', state.backlogs)
}

export function UPDATE_ISSUE_TYPES (state, payload) {
  state.types = payload
  LocalStorage.set('issues.issue_types', payload)
}

export function UPDATE_ISSUE_STATES (state, payload) {
  state.states = payload
  LocalStorage.set('issues.issue_states', payload)
}

export function DELETE_ISSUE (state, payload) {
  const issueIndex = state.issues.findIndex((el, index, array) => {
    return el.id === payload.id
  })

  state.issues.splice(issueIndex, 1)
  LocalStorage.set('issues.issues', state.backlogs)
}

export function UNBIND_ISSUE_FROM_BACKLOG (state, payload) {
  const indexes = findIssueIndexesInBacklog(state, payload.project, payload.id)
  state.backlogs[indexes.backlogIndex].issues.splice(indexes.issuesIndex, 1)
  LocalStorage.set('issues.backlogs', state.backlogs)
}

export function UNBIND_ISSUE_FROM_SPRINT (state, payload) {
  const indexes = state.sprints.filter((sprint) => payload.id in sprint.issues)
  console.log(indexes, 'INDEXES')
}

export function RESET (state) {
  state.backlogs = []
  state.sprints = []
  state.issue_states = []
  state.issue_types = []
  state.sprint_durations = []
}
