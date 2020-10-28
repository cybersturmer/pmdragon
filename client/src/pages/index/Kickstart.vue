<template>
  <q-page class="q-pa-lg">
    <q-stepper
      v-model="step"
      vertical
      ref="stepper"
      dark
      inactive-color="accent"
      active-color="amber"
      done-color="positive"
      animated
    >
      <q-step
        :name="1"
        title="Some bytes about you"
        icon="face"
      >
        <q-input
          value="Wladimir"
          dark
          dense
          square
          filled
          type="text"
          label="First name"
          class="q-mb-sm"
          standout="text-white bg-primary"
        />
        <q-input
          value="Sturmer"
          dark
          dense
          square
          filled
          type="text"
          label="Last name"
          class="q-mb-sm"
          standout="text-white bg-primary"
        />
        <q-input
          value="cybersturmer"
          dark
          dense
          square
          filled
          type="text"
          label="Username"
          standout="text-white bg-primary"
        />
      </q-step>
      <q-step
        :name="2"
        title="Create your first project"
        icon="work"
      >
        <q-input
          value="aether leaps"
          dark
          dense
          square
          filled
          type="text"
          label="Project title"
          class="q-mb-sm"
          standout="text-white bg-primary"
        />
        <q-input
          value="alps"
          dark
          dense
          square
          filled
          type="text"
          label="Project short key"
          class="q-mb-sm"
          standout="text-white bg-primary"
        />
      </q-step>
      <q-step
        :name="3"
        title="Add people you work with"
        icon="supervisor_account"
      >
        Add your team
      </q-step>
      <template v-slot:navigation>
        <q-stepper-navigation>
          <q-btn
            @click="$refs.stepper.next()"
            outline
            :label="step === 3 ? 'Finish' : 'Continue'"
          />
          <q-btn
            v-if="step > 1"
            flat
            @click="$refs.stepper.previous()"
            label="Back" />
        </q-stepper-navigation>
      </template>
    </q-stepper>
  </q-page>
</template>

<script>
export default {
  name: 'Kickstart',
  data () {
    return {
      step: 1
    }
  }
}
</script>

<style scoped>

</style>
