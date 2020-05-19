<template>
    <form v-on:submit.prevent>
        <PasswordField group_class="input-group input-group-sm mb-3"
                       v-model="form_data.password"
                       :error="form_errors.password"/>
        <SubmitButton group_class="input-group input-group-sm mb-1"
                      button_class="btn btn-sm btn-dark w-100"
                      text="Verify"
                      v-on:click="sendRequest()"/>
    </form>
</template>

<script>
import SubmitButton from './SubmitButton.vue';
import PasswordField from './PasswordField.vue';

export default {
  name: 'VerifyForm',
  components: {
    SubmitButton,
    PasswordField,
  },
  data() {
    return {
      form_data: {
        password: '',
        key: '',
      },

      form_errors: {
        password: '',
      },
    };
  },

  methods: {
    async sendRequest() {
      this.form_data.key = this.$route.query.key;

      const url = 'http://0.0.0.0:8000/api/core/persons/';

      const response = await fetch(url, {
        method: 'POST',
        headers: {
          Accept: 'application/json',
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(this.form_data),
      });

      const json = await response.json();
      if (response.status !== 201) {
        if (('password' in json) && (Array.isArray(json.password))) {
          this.form_errors.password = json.password.join(', ');
        }

        return;
      }

      this.form_errors = { password: '' };

      // Redirect ro auth
    },
  },
};
</script>

<style scoped>

</style>
