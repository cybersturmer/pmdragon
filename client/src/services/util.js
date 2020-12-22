function _getStatusMessage (status) {
  let message = ''
  switch (status) {
    case 200:
      message = 'Was executed successfully'
      break
    case 201:
      message = 'Was created successfully'
      break
    case 400:
      message = 'Bad request'
      break
    case 401:
      message = 'Authorization was not correct'
      break
    case 404:
      message = 'Requested resource not found'
      break
    case 503:
      message = 'Server unavailable. Please try again later'
      break
    default:
      message = 'Something was wrong.'
  }

  return message
}

function _getResponseErrorMessage (error) {
  if (error.response && error.response.data) {
    if (error.response.data.detail) return error.response.data.detail
    else return _getStatusMessage(error.response.status)
  }

  if (error.response && error.response.statusText) return error.response.statusText
  return error.message === 'Network Error' ? 'Oops ! Network error. Try again later' : error.message
}

export class ErrorHandler extends Error {
  constructor (error, message) {
    super()
    this.request = error.isAxiosError
    this.data = error.response ? error.response.data : false
    this.success = error.response ? error.response.data.success : false
    this.meta = error.response ? error.response.data.meta : false
    this.code = error.response ? error.response.data.code : false
    this.status = error.response ? error.response.status : false
    this.statusMessage = _getStatusMessage(this.status)
    this.message = message || _getResponseErrorMessage(error)
    this.messageUseful = this.data ? !!error.response.data.detail : false
  }

  setErrors (errors) {
    if (!this.request) return false
    for (const [key, value] of Object.entries(this.data)) {
      if (key in errors) {
        errors[key] = Array.isArray(value) ? value.join('\r\n') : value
      }
    }
  }
}

export function unWatch (value) {
  return JSON.parse(JSON.stringify(value))
}
