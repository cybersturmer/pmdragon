<template>
  <q-page class="flex flex-center">
    <q-card flat bordered class="my-card bg-grey-6" style="width: 320px">
      <q-card-section>
        <div class="column">
          <div class="col">
            <q-input filled v-model="prefix_url" label="URL of your team" />
          </div>
          <div class="col">
            <q-input filled v-model="email" label="Your email" />
          </div>
        </div>
        </q-card-section>
        <q-separator />
        <q-card-section>
            <q-btn outline color="grey-8" text-color="black" label="Register"/>
            <router-link :to="{ path: '/login' }">
              <q-btn flat color="white" text-color="black" label="Already a member?" style="margin-left: 30px"/>
            </router-link>
        </q-card-section>
    </q-card>
  </q-page>
</template>

<script>
export default {
  name: 'Register',
  data () {
    return {
      prefix_url: '',
      email: ''
    }
  }
}
</script>
<style lang="scss">
  .q-btn {
    text-transform: none;
  }
</style>
