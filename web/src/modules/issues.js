/* eslint-disable no-param-reassign */
import FetchPresets from '@/libs/FetchPresets';

const headers = {
  Accept: 'application/json',
  'Content-Type': 'application/json',
};

const state = {
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

export default {
  state,
  getters,
  mutations,
  actions,
};
