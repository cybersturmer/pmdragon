<template>
    <div :class="group_class">
        <label for="email"></label>
        <input id="email" type="email" @input="handleInput"
               placeholder="your@email.com" class="form-control"
               v-model="value" required>
        <div class="invalid-feedback d-inline-block font-weight-bold"
             v-show="error">
            {{ error }}
        </div>
    </div>
</template>

<script>
export default {
  name: 'EmailField',
  props: {
    group_class: String,
    error: String,
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
