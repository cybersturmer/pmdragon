export function WORKSPACES (state) {
  return state.workspaces
}

export function WORKSPACE (state) {
  return state.workspace
}

export function WORKSPACE_ID (state, getters) {
  return getters.WORKSPACE_DATA.id
}

export function IS_WORKSPACE (state) {
  return Boolean(state.workspace)
}

export function PROJECT (state) {
  return state.project
}

export function WORKSPACE_DATA (state) {
  return state.workspaces.filter((workspace) => workspace.prefix_url === state.workspace).pop()
}

export function PROJECT_DATA (state, getters) {
  return getters.WORKSPACE_DATA.projects.filter((project) => project.id === state.project).pop()
}

export function PROJECT_NAME (state, getters) {
  try {
    return getters.PROJECT_DATA.title
  } catch (e) {
    return null
  }
}

export function INTERFACE_THEME (state) {
  return state.interface_theme
}

export function PERSON_BY_ID (state, getters) {
  /** Getting person by id from current workspace **/
  return personId => {
    return getters.WORKSPACE_DATA.participants
      .filter((participant) => participant.id === personId)
      .pop()
  }
}
