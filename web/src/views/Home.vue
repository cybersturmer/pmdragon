<template>
  <div class="container">
    <div class="row justify-content-md-center">
      <div class="col-3">
        <WelcomeScreen msg="PmDragon"/>
      </div>
    </div>
    <hr>
    <div class="row justify-content-md-center">
      <div class="col-3 card">
        <div class="card-body bg-light p-3">
          <RegistrationForm/>
        </div>
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
