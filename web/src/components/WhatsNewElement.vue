<template>
    <div class="card">
        <div class="card-body">
            <h5 class="card-title">{{ title }} - {{ date }}</h5>
            <p class="card-text">{{ text }}</p>
        </div>
    </div>
</template>

<script>
export default {
  name: 'WhatsNewElement',
  props: {
    date: String,
    title: String,
    text: String,
  },
};

</script>

<style scoped>

</style>
