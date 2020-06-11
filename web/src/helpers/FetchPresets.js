export default class FetchPreset {
  static async handleResponse(response) {
    const responseClone = response.clone();
    const responseCloneJson = responseClone.json();

    if (!responseClone.ok) throw await responseCloneJson;

    return responseCloneJson;
  }
}
