import Vue from 'vue';
import Vuex from 'vuex';
import persons from '@/modules/persons';

Vue.use(Vuex);

// eslint-disable-next-line import/prefer-default-export
export const store = new Vuex.Store({
  state: {},
  mutations: {},
  actions: {},
  getters: {},
  modules: {
    persons,
  },
});
