<template>
    <form v-on:submit.prevent>
        <EmailField group_class="input-group input-group-sm mb-2"
                    v-model="form_data.username"
                    :error="form_errors.username"
                    autofocus required/>
        <PasswordField group_class="input-group input-group-sm mb-2"
                       v-model="form_data.password"
                       :error="form_errors.password"
                       required/>
        <SubmitButton group_class="input-group input-group-sm mb-1"
                      button_class="btn btn-sm btn-dark w-100"
                      text="Sign In"
                      v-on:click="logIn()"/>
    </form>
</template>

<script>
import EmailField from '@/components/common/EmailField.vue';
import PasswordField from '@/components/common/PasswordField.vue';
import SubmitButton from '@/components/index/SubmitButton.vue';
import FormError from '@/helpers/FormErrors';

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
        username: '',
        password: '',
      },

      form_errors: {
        username: null,
        password: null,
        detail: null,
      },
    };
  },

  methods: {
    logIn() {
      this.$store.dispatch('LOGIN', this.form_data)
        .then(() => this.$router.push({ path: 'backlog' }))
        .catch((error) => {
          this.form_errors = FormError.handleErrors(this.form_errors, error);
        });
    },
  },
};
</script>

<style scoped>

</style>
