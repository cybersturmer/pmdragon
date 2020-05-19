<template>
    <div :class="group_class">
        <label for="prefix_url"></label>
        <input id="prefix_url" type="text" @input="handleInput"
               placeholder="yourname" class="form-control"
               v-model="value" minlength="3" maxlength="20" required>
        <div class="input-group-append">
            <div class="input-group-text">{{ append_text }}</div>
        </div>
        <div class="invalid-feedback d-inline-block font-weight-bold"
             v-show="error">
            {{ error }}
        </div>
    </div>
</template>

<script>
export default {
  name: 'PrefixUrlField',
  props: {
    group_class: String,
    error: String,
    append_text: String,
  },
  data() {
    return {
      value: '',
    };
  },
  methods: {
    handleInput() {
      this.$emit('input', this.value);
    },
  },
};
</script>
