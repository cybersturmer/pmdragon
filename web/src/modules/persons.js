/* eslint-disable no-param-reassign */
const headers = {
  Accept: 'application/json',
  'Content-Type': 'application/json',
};

const state = {
  username: null,
  first_name: null,
  last_name: null,
  access_token: null,
  refresh_token: null,
};

const getters = {
  ACCESS_TOKEN: (thisState) => thisState.access_token,
  REFRESH_TOKEN: (thisState) => thisState.refresh_token,
  USERNAME: (thisState) => thisState.username,
  FIRST_NAME: (thisState) => thisState.first_name,
  LAST_NAME: (thisState) => thisState.last_name,
};

const mutations = {
  SET_ACCESS_TOKEN: (thisState, payload) => {
    thisState.access_token = payload;
  },
  SET_REFRESH_TOKEN: (thisState, payload) => {
    thisState.refresh_token = payload;
  },
  SET_USERNAME: (thisState, payload) => {
    thisState.username = payload;
  },
  SET_FIRST_NAME: (thisState, payload) => {
    thisState.first_name = payload;
  },
  SET_LAST_NAME: (thisState, payload) => {
    thisState.last_name = payload;
  },
};

const actions = {
  FETCH_TOKENS: async (context, payload) => {
    const response = await fetch('/api/token/obtain/', {
      method: 'POST',
      headers,
      body: JSON.stringify(payload),
    });

    const json = await response.json();
    context.commit('SET_ACCESS_TOKEN', json.access);
    context.commit('SET_REFRESH_TOKEN', json.refresh);
  },
};

export default {
  state,
  getters,
  mutations,
  actions,
};
