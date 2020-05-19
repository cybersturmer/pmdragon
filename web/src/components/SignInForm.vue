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
};
</script>

<style scoped>

</style>
