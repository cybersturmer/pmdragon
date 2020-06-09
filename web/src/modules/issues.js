/* eslint-disable no-param-reassign */

const headers = {
  Accept: 'application/json',
  'Content-Type': 'application/json',
};

const state = {
  current: {
    workspace: null,
    project: null,
  },
  workspaces: [
    {
      prefix_url: null,
      participants: [],
      created_at: null,
    },
  ],
  projects: [
    {
      id: null,
      title: null,
      key: null,
      created_at: null,
    },
  ],
  issue_type_categories: [
    {
      id: null,
      title: null,
      is_subtask: null,
      ordering: null,
    },
  ],
  issue_state_categories: [
    {
      id: null,
      title: null,
      ordering: null,
    },
  ],
  backlogs: [
    {
      id: null,
      project: null,
      issues: [],
    },
  ],
  sprint_durations: [
    {
      id: null,
      title: null,
      duration: null,
    },
  ],
  sprints: [
    {
      id: null,
      project: null,
      title: null,
      goal: null,
      duration: null,
      issues: [],
      started_at: null,
      finished_at: null,
    },
  ],
};

const getters = {
  WORKSPACES: (thisState) => thisState.workspaces,
  BACKLOG: (thisState) => thisState.backlogs.filter(
    (backlog) => backlog.project === thisState.current.project,
  ),
  PROJECT: (thisState) => thisState.projects.filter(
    (project) => project.id === thisState.current.project,
  ),
};

const mutations = {
// Init Workspaces
// Choose Workspace
// Init Projects
// Choose Project
// Init Backlogs
};

const actions = {
//  Get Workspaces
// Get Projects
// Get Backlogs
};

export default {
  state,
  getters,
  mutations,
  actions,
};
