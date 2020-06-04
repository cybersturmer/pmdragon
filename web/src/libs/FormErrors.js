export default {
  methods: {
    handleErrors(errorsState, errorsResult) {
      const result = {};
      Object.keys(errorsState).forEach((key) => {
        if (key in errorsResult) result[key] = errorsResult[key].join(' ');
      });

      return result;
    },
  },
};
