export function BACKLOGS (state) {
  return state.backlogs
}

export function SPRINTS (state) {
  return state.sprints
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
