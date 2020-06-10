/* eslint-disable no-param-reassign */
import Headers from '@/helpers/Headers';

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
  WORKSPACE_PREFIX_URL: (thisState) => thisState.current.workspace,
  WORKSPACE: (thisState) => thisState.workspaces.filter(
    (workspace) => workspace.prefix_url === thisState.current.workspace,
  ),
  BACKLOG: (thisState) => thisState.backlogs.filter(
    (backlog) => backlog.project === thisState.current.project,
  ),
  PROJECT: (thisState) => thisState.projects.filter(
    (project) => project.id === thisState.current.project,
  ),
};

const mutations = {
  INIT_WORKSPACES: (thisState, payload) => {
    thisState.workspaces = payload;
  },
  SET_CURRENT_WORKSPACE: (thisState, payload) => {
    thisState.current.workspace = payload;
  },
  INIT_PROJECTS: (thisState, payload) => {
    thisState.projects = payload;
  },
  SET_CURRENT_PROJECT: (thisState, payload) => {
    thisState.current.project = payload;
  },
  INIT_BACKLOGS: (thisState, payload) => {
    thisState.backlogs = payload;
  },
};

const actions = {
  async fetchBacklogs({ commit }) {
    const response = await fetch('/')
  },
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
