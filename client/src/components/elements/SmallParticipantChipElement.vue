<template>
  <q-chip
    v-bind:key="participant.id"
    dark
    size="md"
    color="secondary"
    text-color="amber"
    style="border-radius: 15px"
  >
    <q-avatar v-if="participant.avatar">
      <img
        :src="participant.avatar"
        :alt="`${participant.first_name} ${participant.last_name}`">
    </q-avatar>
    {{ participant.first_name }} {{ participant.last_name }}
  </q-chip>
</template>

<script>
export default {
  name: 'SmallParticipantChipElement',
  props: {
    participant: {
      type: Object,
      required: true
    }
  }
}
</script>
