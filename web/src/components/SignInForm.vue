<template>
    <form v-on:submit.prevent>
        <EmailField group_class="input-group input-group-sm mb-3"
                    v-model="form_data.email"
                    :error="form_errors.email"/>
        <PasswordField group_class="input-group input-group-sm mb-3"
                       v-model="form_data.password"
                       :error="form_errors.password"/>
        <SubmitButton group_class="input-group input-group-sm mb-1"
                      button_class="btn btn-sm btn-dark w-100"
                      text="Sign In"/>
    </form>
</template>

<script>
import EmailField from './EmailField.vue';
import PasswordField from './PasswordField.vue';
import SubmitButton from './SubmitButton.vue';

export default {
  name: 'SignInForm',
  components: {
    SubmitButton,
    EmailField,
    PasswordField,
  },
  data() {
    return {
      form_data: {
        email: '',
        password: '',
      },

      form_errors: {
        email: '',
        password: '',
      },
    };
  },

  methods: {
    async sendRequest() {
      const domain = window.location.hostname;
      const currentProtocol = window.location.protocol;

      const url = `${currentProtocol}//${domain}:8000/api/auth/token/`;

      const response = await fetch(url, {
        method: 'POST',
        headers: {
          Accept: 'application/json',
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(this.form_data),
      });

      const json = await response.json();
      if (response.status !== 200) {
        if (('email' in json) && (Array.isArray(json.email))) {
          this.form_errors.email = json.email.join(', ');
        }

        if (('password' in json) && (Array.isArray(json.password))) {
          this.form_errors.password = json.password.join(', ');
        }

        return;
      }

      this.form_errors = { username: '', email: '' };
    },
  },
};
</script>

<style scoped>

</style>
