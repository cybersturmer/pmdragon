<template>
    <div class="card border-dark">
        <div class="card-body">
            <h5 class="card-title text-secondary">{{ title }}</h5>
            <p class="card-text">{{ text }}</p>
            <p class="card-footer m-0 p-0 border-0 float-right">{{ date }}</p>
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
