/* eslint-disable no-param-reassign */
const headers = {
  Accept: 'application/json',
  'Content-Type': 'application/json',
};

const state = {
  username: null,
  first_name: null,
  last_name: null,
  tokens: {
    access: {
      data: null,
      expired_at: null,
    },
    refresh: {
      data: null,
      expired_at: null,
    },
  },
};

const getters = {
  ACCESS_TOKEN: (thisState) => thisState.tokens.access,
  REFRESH_TOKEN: (thisState) => thisState.tokens.refresh,
  USERNAME: (thisState) => thisState.username,
  FIRST_NAME: (thisState) => thisState.first_name,
  LAST_NAME: (thisState) => thisState.last_name,
};

const mutations = {
  SET_ACCESS_TOKEN: (thisState, payload) => {
    thisState.tokens.access = payload;
  },
  SET_REFRESH_TOKEN: (thisState, payload) => {
    thisState.tokens.refresh = payload;
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
  INIT_TOKENS: async (context, payload) => {
    
  },
  FETCH_TOKENS: async (context, payload) => {
    const response = await fetch('/api/token/obtain/', {
      method: 'POST',
      headers,
      body: JSON.stringify(payload),
    });

    const json = await response.json();
    if (response.status !== 200) {
      throw await response.json();
    }

    context.commit('SET_ACCESS_TOKEN', json.access);
    context.commit('SET_REFRESH_TOKEN', json.refresh);
  },
  FETCH_ACCESS_TOKEN: async (context, payload) => {
    const response = await fetch('/api/token/refresh/', {
      method: 'POST',
      headers,
      body: JSON.stringify(payload),
    });
  },
};

export default {
  state,
  getters,
  mutations,
  actions,
};
