<template>
  <div class="container">
    <IssueElement id="1" title="Purge all items to zero"/>
  </div>
</template>

<script>
import IssueElement from '@/components/dashboard/backlog/IssueElement.vue';

export default {
  name: 'Backlog',
  components: {
    IssueElement,
  },
};
</script>

<style scoped>

</style>
