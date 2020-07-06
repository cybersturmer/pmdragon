export function BACKLOGS (state) {
  return state.backlogs
}

export function SPRINTS (state) {
  return state.sprints
}

export function ISSUE_STATES_BY_CURRENT_PROJECT (state, getters, rootState, rootGetters) {
  return state.issue_states
    .filter((issueState) => issueState.project === rootGetters['current/PROJECT'])
}

export function ISSUE_TYPES_BY_CURRENT_PROJECT (state, getters, rootState, rootGetters) {
  return state.issue_types
    .filter((issueType) => issueType.project === rootGetters['current/PROJECT'])
}

export function SPRINTS_BY_CURRENT_PROJECT (state, getters, rootState, rootGetters) {
  return state.sprints
    .filter((sprint) => sprint.project.id === rootGetters['current/PROJECT'])
}

export function SPRINT_STARTED_BY_CURRENT_PROJECT (state, getters, rootState, rootGetters) {
  return getters.SPRINTS_BY_CURRENT_PROJECT
    .filter((sprint) => sprint.is_started === true).pop()
}

export function WORKSPACE_SPRINT_DURATION (state, getters, rootState, rootGetters) {
  return state.sprint_durations
    .filter((sprintDuration) => sprintDuration.workspace === rootGetters['current/WORKSPACE_ID'])
}

export function BACKLOG (state, getters, rootState, rootGetters) {
  try {
    return state.backlogs
      .filter((backlog) => backlog.project_id === rootGetters['current/PROJECT'])[0]
  } catch (error) {
    return null
  }
}

export function PROJECT_SPRINTS (state, getters, rootState, rootGetters) {
  try {
    return state.sprints
      .filter((sprint) => sprint.project.id === rootGetters['current/PROJECT'])
  } catch (error) {
    return null
  }
}

export function UNCOMPLETED_PROJECT_SPRINTS (state, getters) {
  try {
    return getters.PROJECT_SPRINTS.filter((sprint) => sprint.is_completed === false)
  } catch (error) {
    return null
  }
}

export function SPRINT_BY_ID (state) {
  return sprintId => state.sprints.filter((sprint) => sprint.id === sprintId).pop()
}

export function SPRINT_BY_ID_ISSUES (state) {
  return sprintId => state.sprints.filter((sprint) => sprint.id === sprintId).pop().issues
}

export function BACKLOG_ISSUES (state, getters) {
  try {
    return getters.BACKLOG.issues
  } catch (e) {
    return []
  }
}

export function BACKLOG_ISSUES_COUNT (state, getters, rootState, rootGetters) {
  try {
    return state.backlogs
      .filter((backlog) => backlog.project_id === rootGetters['current/PROJECT'])
      .pop().issues.length
  } catch (e) {
    return 0
  }
}
