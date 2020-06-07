<template>
  <div class="card bg-dark border-dark h-100 w-100">
  <h5 class="text-secondary mb-0 pl-1">Backlog</h5>
  <draggable v-model="backlog">
    <transition-group>
      <div v-for="item in backlog" v-bind:key="item.id">
        <BacklogElement :id="item.id"
                        :title="item.title"/>
      </div>
    </transition-group>
  </draggable>
  </div>
</template>

<script>
import BacklogElement from '@/components/dashboard/backlog/BacklogElement.vue';
import draggable from 'vuedraggable';

export default {
  name: 'Backlog',
  components: {
    draggable,
    BacklogElement,
  },
  data() {
    return {
      backlog: [
        {
          id: 1,
          title: 'Some interesting task',
        },
        {
          id: 2,
          title: 'Even more interesting task',
        },
        {
          id: 3,
          title: 'The most interesting task ever',
        },
      ],
    };
  },
};
</script>

<style scoped>

</style>
