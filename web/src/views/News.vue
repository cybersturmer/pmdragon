<template>
    <div class="container">
        <div class="row justify-content-md-center">
            <div class="col-sm-10 col-md-10 col-lg-6 col-xl-4">
                <H1 msg="What's new"/>
                <Description msg="What's new happened with our product"/>
            </div>
        </div>
        <div class="row justify-content-md-center mb-2" v-for="item in news" :key="item">
            <div class="col-sm-10 col-md-10 col-lg-6 col-xl-4 small">
                <WhatsNewElement :date="item.date"
                                 :title="item.title"
                                 :text="item.text"/>
            </div>
        </div>
    </div>
</template>
<script>
import H1 from '../components/H1.vue';
import Description from '../components/Description.vue';
import WhatsNewElement from '../components/WhatsNewElement.vue';

export default {
  components: {
    WhatsNewElement,
    Description,
    H1,
  },
  data() {
    return {
      news: [
        {
          date: '19.05.2020',
          title: 'Something went right',
          text: 'When something went right, just close your eyes',
        },
        {
          date: '18.05.2020',
          title: 'Something went good',
          text: 'Imagine how great you can become',
        },
      ],
    };
  },

};
</script>
