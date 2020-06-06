<template>
 <div class="card border-dark">
   <div class="card-body">
     <p class="card-text">
       {{ type }} {{ title }}
     </p>
   </div>
 </div>
</template>

<script>
export default {
  name: 'IssueElement.vue',
  props: {
    id: Number,
    title: String,
  },
};
</script>

<style scoped>

</style>
