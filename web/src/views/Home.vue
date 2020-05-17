<template>
  <div class="home">
    <WelcomeScreen msg="Welcome to PmDragon"/>
  </div>
</template>

<script>
import WelcomeScreen from '../components/WelcomeScreen.vue';

export default {
  name: 'Home',
  components: {
    WelcomeScreen,
  },
};
</script>
