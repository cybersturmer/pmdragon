export function SELECT_WORKSPACE ({ commit }, payload) {
  commit('SELECT_WORKSPACE', payload)
}

export function SELECT_PROJECT ({ commit }, payload) {
  commit('SELECT_PROJECT', payload)
}

export function SELECT_INTERFACE_THEME ({ commit }, payload) {
  commit('SELECT_INTERFACE_THEME', payload)
}

export function RESET_STATE ({ commit }) {
  commit('RESET')
}

export function RESET_WORKSPACE ({ commit }) {
  commit('RESET_WORKSPACE')
}

export function RESET_PROJECT ({ commit }) {
  commit('RESET_PROJECT')
}
