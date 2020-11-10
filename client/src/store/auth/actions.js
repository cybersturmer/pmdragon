import { AuthService } from 'src/services/auth'
import { Api } from 'src/services/api'
import { ErrorHandler, HandleResponse } from 'src/services/util'

export async function REGISTER ({ commit }, credentials) {
  return await new Api().post('/auth/person-registration-requests/',
    credentials)
}

export async function LOGIN ({ commit }, credentials) {
  return await AuthService.login(credentials)
}

export async function REFRESH ({ commit }, refreshToken) {
  return await AuthService.refresh(refreshToken)
}

export async function LOGOUT ({ dispatch }) {
  await AuthService.logout()
}

export async function INIT_WORKSPACES ({ commit }) {
  try {
    const response = await new Api({ auth: true }).get('/auth/workspaces/')
    HandleResponse.compare(200, response.status)
    commit('INIT_WORKSPACES', response.data)
  } catch (e) {
    throw new ErrorHandler(e)
  }
}

export async function INIT_PERSONS ({ commit }) {
  /**
  * Collaborator is everyone who is in the same workspaces as you are
  * So by init we get all persons/participant in workspace we belong to **/

  try {
    const response = await new Api({ auth: true }).get('core/persons/')
    HandleResponse.compare(200, response.status)
    commit('INIT_PERSONS', response.data)
  } catch (e) {
    throw new ErrorHandler(e)
  }
}

export async function ADD_PROJECT ({ commit }, payload) {
  try {
    const response = await new Api({ auth: true }).post(
      '/core/projects/',
      payload
    )

    HandleResponse.compare(201, response.status)
    commit('ADD_PROJECT', response.data)
  } catch (e) {
    throw new ErrorHandler(e)
  }
}

export async function INVITE_TEAM ({ commit }, payload) {
  /**
   * Not related to Vuex store now, however gonna let it stay here **/
  try {
    const response = await new Api({ auth: true }).post(
      '/core/person-invitation-requests/',
      payload
    )

    HandleResponse.compare(201, response.status)
  } catch (e) {
    throw new ErrorHandler(e)
  }
}

export async function UPDATE_MY_DATA ({ commit }, payload) {
  try {
    const response = await new Api({ auth: true })
      .put('/auth/me/', payload)

    HandleResponse.compare(200, response.status)

    commit('SET_MY_FIRST_NAME', response.data.first_name)
    commit('SET_MY_LAST_NAME', response.data.last_name)
    commit('SET_MY_USERNAME', response.data.username)
  } catch (e) {
    throw new ErrorHandler(e)
  }
}

export async function UPDATE_MY_PASSWORD ({ commit }, payload) {
  try {
    const response = await new Api({ auth: true })
      .post('/auth/password/', payload)

    HandleResponse.compare(200, response.status)
  } catch (e) {
    throw new ErrorHandler(e)
  }
}

export async function UPDATE_MY_AVATAR ({ commit }, file) {
  const formData = new FormData()
  formData.append('image', file)

  try {
    const response = await new Api({ auth: true })
      .put('/auth/avatar/', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      })

    HandleResponse.compare(200, response.status)
    commit('SET_MY_AVATAR', response.data.avatar)

    return response.data
  } catch (e) {
    throw new ErrorHandler(e)
  }
}

export async function DELETE_MY_AVATAR ({ commit }) {
  try {
    const response = await new Api({ auth: true })
      .delete('/auth/avatar/')

    HandleResponse.compare(204, response.status)
    commit('RESET_MY_AVATAR')
  } catch (e) {
    throw new ErrorHandler(e)
  }
}
