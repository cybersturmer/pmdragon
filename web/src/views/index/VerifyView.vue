<template>
    <div class="container">
        <div class="row justify-content-md-center">
            <div class="col-sm-10 col-md-10 col-lg-6 col-xl-5">
                <H1 msg="Verify"/>
                <Description msg="Confirm your account and use powerful tool"/>
            </div>
        </div>
        <div class="row justify-content-md-center">
            <div class="col-sm-10 col-md-10 col-lg-6 col-xl-5">
                <div class="card border-dark p-1 rounded shadow">
                    <div class="card-body">
                        <VerifyForm/>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import H1 from '@/components/index/H1.vue';
import VerifyForm from '@/components/index/VerifyForm.vue';
import Description from '@/components/index/Description.vue';

export default {
  name: 'Verify',
  components: {
    H1,
    VerifyForm,
    Description,
  },
};
</script>
