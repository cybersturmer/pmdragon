import Vuex from 'vuex';

const store = new Vuex.Store({
  state: {
    loading: false,
    accessToken: null,
    refreshToken: null,
    noInternet: false,
  },
  mutations: {
    SET_ACCESS_TOKEN(state, accessToken) {
      state.accessToken = accessToken;
    },
    SET_REFRESH_TOKEN(state, refreshToken) {
      state.refreshToken = refreshToken;
    },
  },
  actions: {
    async fetchTokens(credentials) {
      const response = await fetch('/api/token/obtain/', {
        method: 'POST',
        headers: {
          Accept: 'application/json',
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(credentials),
      });

      const json = await response.json();
      // todo ? Credentials was not correct
      // todo ? Token invalid error
      // todo ? Internet connection error

      this.$store.commit('SET_ACCESS_TOKEN', json.access);
      this.$store.commit('SET_REFRESH_TOKEN', json.refresh);
    },
  },
  getters: {
  },
});
