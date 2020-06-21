import axios from 'axios'

export default ({ Vue, router }) => {
  Vue.prototype.$axios = axios

  axios.interceptors.response.use((response) => {
    return response
  }, (error) => {
    if (error.response.status === 401) {
      router.push({ name: 'login' })
    }
  })
}
