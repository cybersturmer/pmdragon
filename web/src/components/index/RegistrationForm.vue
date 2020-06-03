<template>
    <div>
        <div v-show="!form_show" class="text-dark">
            <p class="m-1">Thanks for registration!</p>
            <p class="m-1">Your link was sent at <strong>{{ this.form_data.email }}.</strong></p>
            <p class="m-1"> Please check it and confirm registration.</p>
        </div>
        <form v-on:submit.prevent v-show="form_show">
            <PrefixUrlField group_class="input-group input-group-sm mb-2"
                            v-model="form_data.prefix_url"
                            :error="form_errors.prefix_url"
                            append_text="pmdragon.org"
                            required autofocus/>
            <EmailField group_class="input-group input-group-sm mb-2"
                        v-model="form_data.email"
                        :error="form_errors.email"
                        required/>
            <SubmitButton group_class="input-group input-group-sm mb-1"
                          button_class="btn btn-sm btn-dark w-100"
                          text="Register" v-on:click="sendRequest()"/>
        </form>
    </div>
</template>

<script>
import EmailField from '@/components/common/EmailField.vue';
import SubmitButton from '@/components/index/SubmitButton.vue';
import PrefixUrlField from '@/components/index/PrefixUrlField.vue';

export default {
  name: 'RegistrationForm',
  components: {
    PrefixUrlField,
    SubmitButton,
    EmailField,
  },
  data() {
    return {
      form_show: true,
      form_data: {
        prefix_url: '',
        email: '',
      },

      form_errors: {
        prefix_url: '',
        email: '',
      },
    };
  },

  methods: {
    async sendRequest() {
      const url = '/api/core/registration-requests/';

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
        if (('prefix_url' in json) && (Array.isArray(json.prefix_url))) {
          this.form_errors.prefix_url = json.prefix_url.join(', ');
        }

        if (('email' in json) && (Array.isArray(json.email))) {
          this.form_errors.email = json.email.join(', ');
        }

        return;
      }

      this.form_errors = { prefix_url: '', email: '' };
      this.form_show = false;
    },
  },
};
</script>
