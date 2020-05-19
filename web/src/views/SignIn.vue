<template>
    <div class="container">
        <div class="row justify-content-md-center">
            <div class="col-sm-10 col-md-10 col-lg-6 col-xl-5">
                <H1 msg="Sign In"/>
                <Description msg="Sign in with existing account"/>
            </div>
        </div>
        <div class="row justify-content-md-center">
            <div class="col-sm-10 col-md-10 col-lg-6 col-xl-5">
                <div class="card border-dark p-1 rounded shadow">
                    <div class="card-body bg-light">
                        <SignInForm/>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import H1 from '../components/H1.vue';
import SignInForm from '../components/SignInForm.vue';
import Description from '../components/Description.vue';

export default {
  name: 'SignIn',
  components: {
    H1,
    SignInForm,
    Description,
  },
};
</script>
