export default class FormError {
  static handleErrors(errorsState, errorsResult) {
    const result = {};
    Object.keys(errorsState).forEach((key) => {
      if (key in errorsResult) {
        const isArray = Array.isArray(errorsResult[key]);
        if (isArray) result[key] = errorsResult[key].join(' ');
        else result[key] = errorsResult[key];
      }
    });

    return result;
  }
}
