<template>
    <div :class="group_class">
        <button type="submit" :class="button_class" v-on:click="handleClick">
            {{ text }}
        </button>
    </div>
</template>

<script>
export default {
  name: 'SubmitButton',
  props: {
    group_class: String,
    button_class: String,
    text: String,
  },
  methods: {
    handleClick(e) {
      this.$emit('click', e);
    },
  },
};
</script>

<style scoped>

</style>
