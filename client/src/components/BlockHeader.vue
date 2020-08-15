<template>
  <h5>{{ title }}</h5>
</template>

<script>
export default {
  name: 'BlockHeader',
  props: {
    title: {
      type: String,
      required: true
    }
  }
}
</script>

<style scoped>
  h5 {
    text-transform: uppercase;
  }
</style>
