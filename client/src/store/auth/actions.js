import { AuthService } from 'src/services/auth'
import { Api } from 'src/services/api'
import { ErrorWrapper, HandleResponse } from 'src/services/util'

export async function LOGIN ({ commit }, credentials) {
  return await AuthService.login(credentials)
}

export async function REFRESH ({ commit }, refreshToken) {
  return await AuthService.refresh(refreshToken)
}

export async function LOGOUT ({ dispatch }) {
  await AuthService.logout()
}

export async function UPDATE_USER_DATA ({ commit }, payload) {
  try {
    const response = await new Api({ auth: true })
      .put('/auth/me/', payload)

    HandleResponse.compare(200, response.status)

    commit('SET_FIRST_NAME', response.data.first_name)
    commit('SET_LAST_NAME', response.data.last_name)
    commit('SET_USERNAME', response.data.username)
  } catch (error) {
    throw new ErrorWrapper(error)
  }
}

export async function UPDATE_USER_PASSWORD ({ commit }, payload) {
  try {
    const response = await new Api({ auth: true })
      .post('/auth/password/', payload)

    HandleResponse.compare(200, response.status)
  } catch (error) {
    throw new ErrorWrapper(error)
  }
}

export async function UPDATE_PERSON_AVATAR ({ commit }, file) {
  console.log(file)
  const formData = new FormData()
  formData.append('image', file)

  try {
    // @todo change filename to something really uniq
    const response = await new Api({ auth: true })
      .put(`/auth/avatar/${file.name}/`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      })

    HandleResponse.compare(204, response.status)
  } catch (error) {
    throw new ErrorWrapper(error)
  }
}
