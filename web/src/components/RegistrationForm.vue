<template>
    <div>
        <div v-show="!form_show" class="text-dark">
            <p class="m-1">Thanks for registration!</p>
            <p class="m-1">Your link was sent at <strong>{{ this.form_data.email }}.</strong></p>
            <p class="m-1"> Please check it and confirm registration.</p>
        </div>
        <form v-on:submit.prevent v-show="form_show">
            <div class="input-group input-group-sm mb-2">
                <label for="prefix_url"></label>
                <input id="prefix_url" type="text" v-model="form_data.prefix_url"
                       placeholder="yourname" class="form-control"
                       minlength="3" maxlength="20" required>
                <div class="input-group-append">
                    <div class="input-group-text">pmdragon.org</div>
                </div>
                <div class="invalid-feedback d-inline-block font-weight-bold"
                     v-show="form_errors.prefix_url">
                    {{ form_errors.prefix_url }}
                </div>
            </div>
            <div class="input-group input-group-sm mb-2">
                <label for="email"></label>
                    <input id="email" type="email" v-model="form_data.email"
                           placeholder="yourmail@mail.com" class="form-control" required>
                <div class="invalid-feedback d-inline-block font-weight-bold"
                     v-show="form_errors.email">
                    {{ form_errors.email }}
                </div>
            </div>
            <div class="input-group input-group-sm mb-1">
                <button type="submit" class="btn btn-sm btn-dark w-100" v-on:click="sendRequest()">
                    Register
                </button>
            </div>
        </form>
    </div>
</template>

<script>
export default {
  name: 'RegistrationForm',
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
      const url = 'http://0.0.0.0:8000/api/core/registration-requests/';

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
