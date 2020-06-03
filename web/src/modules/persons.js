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
  IS_LOGGED_IN(thisState) {
    return thisState.getters.IS_ACCESS_TOKEN_VALID
           && thisState.getters.IS_REFRESH_TOKEN_VALID;
  },
  IS_ACCESS_TOKEN_VALID(thisState) {
    const now = Date.now();
    return thisState.tokens.access.expired_at !== null
           && now < Date.parse(thisState.tokens.access.expired_at);
  },
  IS_REFRESH_TOKEN_VALID(thisState) {
    const now = Date.now();
    return thisState.tokens.refresh.expired_at !== null
           && now < Date.parse(thisState.tokens.refresh.expired_at);
  },
  ACCESS_TOKEN: (thisState) => thisState.tokens.access.data,
  REFRESH_TOKEN: (thisState) => thisState.tokens.refresh.data,
  USERNAME: (thisState) => thisState.username,
  FIRST_NAME: (thisState) => thisState.first_name,
  LAST_NAME: (thisState) => thisState.last_name,
};

const mutations = {
  SET_ACCESS_TOKEN: (thisState, payload) => {
    thisState.tokens.access.data = payload.data;
    thisState.tokens.access.expired_at = payload.expired_at;
  },
  SET_REFRESH_TOKEN: (thisState, payload) => {
    thisState.tokens.refresh.data = payload.data;
    thisState.tokens.refresh.expired_at = payload.expired_at;
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
  fetchTokens2(context, credentials) {
    const fetchPromise = fetch('http://pmdragon.org:8000/api/auth/obtain/', {
      method: 'POST',
      headers,
      body: JSON.stringify(credentials),
    });


    fetchPromise.then((response) => {
      if (!response.ok) throw response.json();

      return response.json();
    })
      .then((data) => {
        // eslint-disable-next-line no-console
        console.log(data);
      });
  },

  async fetchTokens({ commit }, credentials) {
    const response = await fetch('http://pmdragon.org:8000/api/auth/obtain/', {
      method: 'POST',
      headers,
      body: JSON.stringify(credentials),
    });

    const responseClone = response.clone();
    const responseCloneJson = responseClone.json();

    if (!responseClone.ok) {
      throw await responseCloneJson;
    }

    commit('SET_ACCESS_TOKEN', responseCloneJson.access);
    commit('SET_REFRESH_TOKEN', responseCloneJson.refresh);

    commit('SET_USERNAME', responseCloneJson.username);
    commit('SET_FIRST_NAME', responseCloneJson.first_name);
    commit('SET_LAST_NAME', responseCloneJson.last_name);
  },

  async fetchAccessToken({ commit, thisState }) {
    const response = await fetch('api/auth/refresh', {
      method: 'POST',
      headers,
      body: JSON.stringify({ access: thisState.refresh.data }),
    });

    const json = await response.json();
    if (response.status !== 200) {
      throw await response.json();
    }

    commit('SET_ACCESS_TOKEN', json.access);
  },
};

export default {
  state,
  getters,
  mutations,
  actions,
};
