export function BACKLOGS (state) {
  return state.backlogs
}

export function SPRINTS (state) {
  return state.sprints
}

export function ISSUES (state) {
  return state.issues
}

/** Issues Block **/
export function ISSUE_BY_ID (state) {
  /** Getting issue from main list by id **/
  return issueId => {
    return state.issues.filter((issue) => issue.id === issueId).pop()
  }
}

export function ISSUES_BY_IDS (state) {
  return issuesIds => {
    return state.issues
      .filter((issue) => issuesIds.indexOf(issue.id) >= 0)
      .sort((a, b) => a.ordering - b.ordering)
  }
}

/** Sprints block **/
export function SPRINTS_BY_CURRENT_PROJECT (state, getters, rootState, rootGetters) {
  return state.sprints
    .filter((sprint) => sprint.project === rootGetters['current/PROJECT'])
}

export function SPRINT_STARTED_BY_CURRENT_PROJECT (state, getters) {
  return getters.SPRINTS_BY_CURRENT_PROJECT
    .filter((sprint) => sprint.is_started === true).pop()
}

export function SPRINT_STARTED_BY_CURRENT_PROJECT_ISSUES (state, getters) {
  return getters.ISSUES_BY_IDS(getters.SPRINT_STARTED_BY_CURRENT_PROJECT.issues)
}

export function PROJECT_SPRINTS (state, getters, rootState, rootGetters) {
  try {
    return state.sprints
      .filter((sprint) => sprint.project === rootGetters['current/PROJECT'])
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

export function SPRINT_BY_ID_ISSUES (state, getters) {
  return sprintId => {
    return getters.ISSUES_BY_IDS(getters.SPRINT_BY_ID(sprintId).issues)
  }
}

/** Issue States Block **/
export function ISSUE_STATES_BY_CURRENT_PROJECT (state, getters, rootState, rootGetters) {
  return state.issue_states
    .filter((issueState) => issueState.project === rootGetters['current/PROJECT'])
}

export function ISSUE_TYPES_BY_CURRENT_PROJECT (state, getters, rootState, rootGetters) {
  return state.issue_types
    .filter((issueType) => issueType.project === rootGetters['current/PROJECT'])
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

export function BACKLOG_ISSUES (state, getters) {
  try {
    return getters.ISSUES_BY_IDS(getters.BACKLOG.issues)
  } catch (error) {
    return []
  }
}

export function BACKLOG_ISSUES_COUNT (state, getters, rootState, rootGetters) {
  try {
    return getters.BACKLOG.issues.length
  } catch (error) {
    return 0
  }
}
