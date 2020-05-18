<template>
  <div class="container">
    <div class="row justify-content-md-center">
      <div class="col col-lg-6">
        <WelcomeScreen msg="Welcome to PmDragon"/>
      </div>
      <div class="col col-lg-6">
        <RegistrationForm/>
      </div>
    </div>
  </div>
</template>

<script>
import WelcomeScreen from '../components/WelcomeScreen.vue';
import RegistrationForm from '../components/RegistrationForm.vue';

export default {
  name: 'Home',
  components: {
    WelcomeScreen,
    RegistrationForm,
  },
};
</script>
