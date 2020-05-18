<template>
    <div class="news">
        <H1 msg="What's new"/>
        <WhatsNewElement date="18.05.2020" title="Something went right"
                         text="When something went right, just close your eyes"/>
    </div>
</template>
<script>
import WhatsNewElement from '../components/WhatsNewElement.vue';
// @todo Make it render from json
// const news = [
//   {
//     date: '18.05.2020',
//     title: 'Something went right',
//     text: 'When something went right, just close your eyes',
//   },
// ];
export default {
  components: { WhatsNewElement },
};
</script>
