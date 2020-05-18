<template>
  <div class="container">
    <div class="row justify-content-md-center">
      <div class="col-sm-10 col-md-10 col-lg-6 col-xl-4">
        <H1 msg="~[ pmdragon ]~"/>
        <Description msg="Agile tool designed for software teams"/>
      </div>
    </div>
    <div class="row justify-content-md-center">
      <div class="col-sm-10 col-md-10 col-lg-6 col-xl-4">
        <div class="card border-dark p-1 rounded shadow">
          <div class="card-body">
            <RegistrationForm/>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import H1 from '../components/H1.vue';
import RegistrationForm from '../components/RegistrationForm.vue';
import Description from '../components/Description.vue';

export default {
  name: 'Home',
  components: {
    H1,
    RegistrationForm,
    Description,
  },
};
</script>
