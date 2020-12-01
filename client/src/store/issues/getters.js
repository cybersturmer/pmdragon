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
    return state.issues.find(issue => issue.id === issueId)
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

export function CURRENT_SPRINT (state, getters, rootState, rootGetters) {
  /** Get current sprint
   * For current project
   * Started
   * Not completed **/
  try {
    return state.sprints
      .filter((sprint) => sprint.project === rootGetters['current/PROJECT'] &&
        sprint.is_started === true &&
        sprint.is_completed === false)
      .pop()
  } catch (e) {
    return false
  }
}

export function SPRINT_STARTED_BY_CURRENT_PROJECT_ISSUES (state, getters) {
  try {
    return getters.ISSUES_BY_IDS(getters.CURRENT_SPRINT.issues)
  } catch (e) {
    return []
  }
}

export function PROJECT_SPRINTS (state, getters, rootState, rootGetters) {
  try {
    return state.sprints
      .filter((sprint) => sprint.project === rootGetters['current/PROJECT'])
  } catch (e) {
    return null
  }
}

export function UNCOMPLETED_PROJECT_SPRINTS (state, getters) {
  try {
    return getters.PROJECT_SPRINTS.filter((sprint) => sprint.is_completed === false)
  } catch (e) {
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

export function IS_ISSUE_STATE_DONE (state) {
  return issueStateId => {
    try {
      return state.issue_states
        .find(issueState => issueState.id === issueStateId).is_done
    } catch (e) {
      return false
    }
  }
}

export function ISSUE_TYPES_BY_CURRENT_PROJECT (state, getters, rootState, rootGetters) {
  return state.issue_types
    .filter((issueType) => issueType.project === rootGetters['current/PROJECT'])
}

export function ISSUE_TYPE_BY_ID (state) {
  return issueTypeId => {
    try {
      return state.issue_types
        .find(issueType => issueType.id === issueTypeId)
    } catch (e) {
      return null
    }
  }
}

export function IS_ISSUE_TYPE_HAVE_ICON (state) {
  return issueTypeId => {
    try {
      const issueType = state.issue_types
        .find(issueType => issueType.id === issueTypeId)

      return !!issueType.icon
    } catch (e) {
      return false
    }
  }
}

export function WORKSPACE_SPRINT_DURATION (state, getters, rootState, rootGetters) {
  return state.sprint_durations
    .filter((sprintDuration) => sprintDuration.workspace === rootGetters['current/WORKSPACE_ID'])
}

export function BACKLOG (state, getters, rootState, rootGetters) {
  try {
    return state.backlogs
      .filter((backlog) => backlog.project_id === rootGetters['current/PROJECT'])[0]
  } catch (e) {
    return null
  }
}

export function BACKLOG_ISSUES (state, getters) {
  try {
    return getters.ISSUES_BY_IDS(getters.BACKLOG.issues)
  } catch (e) {
    return []
  }
}

export function BACKLOG_ISSUES_COUNT (state, getters) {
  try {
    return getters.BACKLOG.issues.length
  } catch (e) {
    return 0
  }
}
