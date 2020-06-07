<template>
 <div class="card border-dark bg-secondary text-light shadow mt-2">
   <div class="card-body">
     <p class="card-text">
       {{ id }} {{ title }}
     </p>
   </div>
 </div>
</template>

<script>
export default {
  name: 'BacklogElement',
  props: {
    id: Number,
    title: String,
  },
};
</script>

<style scoped>

</style>
