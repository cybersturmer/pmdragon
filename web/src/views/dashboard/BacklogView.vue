<template>
  <div class="container-fluid h-100">
    <div class="row h-50">
    </div>
    <div class="row h-50 border-top border-dark">
      <Backlog/>
    </div>
  </div>
</template>

<script>
import Backlog from '@/components/dashboard/backlog/Backlog.vue';

export default {
  name: 'BacklogView',
  components: {
    Backlog,
  },
};
</script>

<style scoped>
hr {
  box-shadow: inset -1px 0 0 rgba(0, 0, 0, .1);
  width: 100%;
}

</style>
