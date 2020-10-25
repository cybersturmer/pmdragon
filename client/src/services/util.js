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
  if (error.response && error.response.data) return error.response.data.message
  if (error.response && error.response.statusText) return error.response.statusText
  return error.message === 'Network Error' ? 'Oops ! Network error. Try again later' : error.message
}

export class ResponseWrapper {
  constructor (response) {
    this.data = response.data
    this.success = response.response ? response.data.success : false
    this.status = response.status
    this.statusMessage = _getStatusMessage(this.status)
  }

  setErrors (errors) {
    for (const [key, value] of Object.entries(this.data)) {
      if (key in errors) {
        errors[key] = value
      }
    }
  }
}

export class ErrorWrapper extends Error {
  constructor (error, message) {
    super()
    this.success = error.response ? error.response.data.success : false
    this.meta = error.response ? error.response.data.meta : false
    this.code = error.response ? error.response.data.code : false
    this.status = error.response ? error.response.status : false
    this.statusMessage = _getStatusMessage(this.status)
    this.message = message || _getResponseErrorMessage(error)
  }
}

export class HandleResponse {
  static compare (codeExpectation = 200, codeReality) {
    if (codeExpectation !== codeReality) {
      throw new ErrorWrapper(Error('Expectation code mismatch'), _getStatusMessage(codeReality))
    }
  }
}

export function unWatch (value) {
  return JSON.parse(JSON.stringify(value))
}
