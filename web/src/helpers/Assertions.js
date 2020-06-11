export default class Assertion {
  static isTrue(condition, message) {
    const messageDef = message || 'Assertion Failed';
    if (typeof Error !== 'undefined') {
      throw new Error(messageDef);
    }

    throw message;
  }
}
