<template>
  <h5>
    {{ title }}
    <span>
      (&nbsp;{{ info }}&nbsp;)
    </span>
  </h5>
</template>

<script>
export default {
  name: 'BlockHeaderInfo',
  props: {
    title: {
      type: String,
      required: true
    },
    info: {
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
  span {
    font-size: 0.75em;
    text-transform: none;
  }
</style>
