/* eslint-disable no-shadow */
/* eslint-disable no-param-reassign */
import FetchPreset from '@/helpers/FetchPresets';
import Headers from '@/helpers/Headers';
import Tokens from '@/helpers/Tokens';
import Assertion from '@/helpers/Assertions';

const headers = Headers.methods.guestHeaders();

const initState = {
  user_id: null,
  username: null,
  first_name: null,
  last_name: null,
  tokens: {
    access: {
      data: null,
      details: {
        expired_at: null,
        user_id: null,
      },
    },
    refresh: {
      data: null,
      details: {
        expired_at: null,
        user_id: null,
      },
    },
  },
};

const initTokenDetails = {
  exp: null,
  iss: null,
  jti: null,
  token_type: null,
  user_id: null,
};

const state = initState;

const getters = {
  IS_LOGGED_IN({ thisState, getters }) {
    try {
      Assertion.isTrue(thisState.user_id);
      Assertion.isTrue(getters.IS_ACCESS_TOKEN_VALID);
      Assertion.isTrue(getters.IS_REFRESH_TOKEN_VALID);
      Assertion.isTrue(thisState.user_id);
    } catch (e) {
      return false;
    }

    return true;
  },
  IS_ACCESS_TOKEN_VALID(thisState) {
    const now = Date.now();
    return thisState.tokens.access.details.expired_at !== null
           && now < Date.parse(thisState.tokens.access.details.expired_at);
  },
  IS_REFRESH_TOKEN_VALID(thisState) {
    const now = Date.now();
    return thisState.tokens.refresh.details.expired_at !== null
           && now < Date.parse(thisState.tokens.refresh.details.expired_at);
  },
  ACCESS_TOKEN(thisState) {
    return thisState.tokens.access.data;
  },
  REFRESH_TOKEN: (thisState) => thisState.tokens.refresh.data,
  USERNAME: (thisState) => thisState.username,
  FIRST_NAME: (thisState) => thisState.first_name,
  LAST_NAME: (thisState) => thisState.last_name,
};

const mutations = {
  SET_ACCESS_TOKEN: (thisState, payload) => {
    let tokenDetails = initTokenDetails;

    tokenDetails = Tokens.methods.getTokenDetails(payload);

    Assertion.isTrue(tokenDetails.iss === 'PMDragon API');
    Assertion.isTrue(tokenDetails.token_type === 'access');

    const parsedTokenDetails = {
      expired_at: new Date(tokenDetails.exp * 1000),
      user_id: tokenDetails.user_id,
    };

    thisState.tokens.access.data = payload.data;
    thisState.tokens.access.details = parsedTokenDetails;
  },
  SET_REFRESH_TOKEN: (thisState, payload) => {
    let tokenDetails = initTokenDetails;

    tokenDetails = Tokens.methods.getTokenDetails(payload);

    Assertion.isTrue(tokenDetails.iss === 'PMDragon API');
    Assertion.isTrue(tokenDetails.token_type === 'refresh');

    const parsedTokenDetails = {
      expired_at: new Date(tokenDetails.exp * 1000),
      user_id: tokenDetails.user_id,
    };

    thisState.tokens.refresh.data = payload.data;
    thisState.tokens.refresh.details = parsedTokenDetails;
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
  async LOGIN({ commit }, credentials) {
    const response = await fetch('/api/auth/obtain/', {
      method: 'POST',
      headers,
      body: JSON.stringify(credentials),
    });

    const json = await FetchPreset.handleResponse(response);

    commit('SET_ACCESS_TOKEN', json.tokens.access);
    commit('SET_REFRESH_TOKEN', json.tokens.refresh);

    commit('SET_USERNAME', json.username);
    commit('SET_FIRST_NAME', json.first_name);
    commit('SET_LAST_NAME', json.last_name);
  },

  async UPDATE_TOKEN({ commit, thisState }) {
    const response = await fetch('/api/auth/refresh', {
      method: 'POST',
      headers,
      body: JSON.stringify({ access: thisState.refresh.data }),
    });

    const json = await FetchPreset.handleResponse(response);

    commit('SET_ACCESS_TOKEN', json.access);
  },

  LOGOUT({ commit }) {
    commit('SET_ACCESS_TOKEN', {
      data: null,
      details: null,
    });

    commit('SET_REFRESH_TOKEN', {
      data: null,
      details: null,
    });

    commit('SET_USERNAME', null);
    commit('SET_FIRST_NAME', null);
    commit('SET_LAST_NAME', null);
  },
};

export default {
  state,
  getters,
  mutations,
  actions,
};
