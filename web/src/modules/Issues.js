/* eslint-disable no-param-reassign */
/* eslint-disable no-shadow */
import Headers from '@/helpers/Headers';
import FetchPresets from '@/helpers/FetchPresets';

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
  issue_types: [
    {
      id: null,
      title: null,
      is_subtask: null,
      ordering: null,
    },
  ],
  issue_states: [
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
  ISSUE_TYPES: (thisState) => thisState.issue_types,
  ISSUE_STATES: (thisState) => thisState.issue_states,
  WORKSPACE_PREFIX_URL: (thisState) => thisState.current.workspace,
  WORKSPACE: (thisState) => thisState.workspaces.filter(
    (workspace) => workspace.prefix_url === thisState.current.workspace,
  ),
  CURRENT_BACKLOG: (thisState) => thisState.backlogs.filter(
    (backlog) => backlog.project === thisState.current.project,
  ),
  CURRENT_PROJECT: (thisState) => thisState.projects.filter(
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
  INIT_ISSUE_TYPES: (thisState, payload) => {
    thisState.issue_types = payload;
  },
  INIT_ISSUE_STATES: (thisState, payload) => {
    thisState.issue_states = payload;
  },
};

const actions = {
  async GET_WORKSPACES({ commit, rootGetters }) {
    const headers = Headers.methods.userHeaders(rootGetters.ACCESS_TOKEN);
    const url = '/api/auth/workspaces/';

    const response = await fetch(url, {
      headers,
    });

    const json = await FetchPresets.methods.handleResponse(response);

    commit('INIT_WORKSPACES', json);
  },
  async GET_BACKLOGS({ commit, getters, rootGetters }) {
    const headers = Headers.methods.userHeaders(rootGetters.ACCESS_TOKEN);
    const url = `/api/core/${getters.WORKSPACE_PREFIX_URL}/backlogs/`;

    const response = await fetch(url, {
      headers,
    });

    const json = await FetchPresets.methods.handleResponse(response);

    commit('INIT_BACKLOGS', json);
  },
  async GET_PROJECTS({ commit, getters, rootGetters }) {
    const headers = Headers.methods.userHeaders(rootGetters.ACCESS_TOKEN);
    const url = `/api/core/${getters.WORKSPACE_PREFIX_URL}/projects/`;

    const response = await fetch(url, {
      headers,
    });

    const json = await FetchPresets.methods.handleResponse(response);

    commit('INIT_PROJECTS', json);
  },
  async GET_ISSUE_TYPES({ commit, getters, rootGetters }) {
    const headers = Headers.methods.userHeaders(rootGetters.ACCESS_TOKEN);
    const url = `/api/core/${getters.WORKSPACE_PREFIX_URL}/issue-types/`;

    const response = await fetch(url, {
      headers,
    });

    const json = await FetchPresets.methods.handleResponse(response);

    commit('INIT_ISSUE_TYPES', json);
  },
  async GET_ISSUE_STATES({ commit, getters, rootGetters }) {
    const headers = Headers.methods.userHeaders(rootGetters.ACCESS_TOKEN);
    const url = `/api/core/${getters.WORKSPACE_PREFIX_URL}/issue-states/`;

    const response = await fetch(url, {
      headers,
    });

    const json = await FetchPresets.methods.handleResponse(response);

    commit('INIT_ISSUE_STATES', json);
  },
};

export default {
  state,
  getters,
  mutations,
  actions,
};
