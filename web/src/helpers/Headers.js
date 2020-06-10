export default {
  methods: {
    userHeaders(accessToken) {
      return {
        Accept: 'application/json',
        'Content-Type': 'application/json',
        Authorization: `Bearer ${accessToken}`,
      };
    },
    guestHeaders() {
      return {
        Accept: 'application/json',
        'Content-Type': 'application/json',
      };
    },
  },
};
