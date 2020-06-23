export function BACKLOGS (state) {
  return state.backlogs
}

export function BACKLOG (state, getters, rootState, rootGetters) {
  try {
    return state.backlogs.filter((backlog) => backlog.project_id === rootGetters['current/PROJECT'])[0]
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
