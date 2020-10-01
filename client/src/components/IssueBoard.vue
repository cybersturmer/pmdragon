<template>
  <q-card
    dense
    dark
    bordered
    class="my-card bg-grey-8 q-ma-sm overflow-hidden text-center">
    <q-card-section>
      <span class="text-muted">{{ title }}</span>
    </q-card-section>
  </q-card>
</template>

<script>
export default {
  name: 'IssueBoard',
  props: {
    id: {
      type: Number,
      required: true
    },
    title: {
      type: String,
      required: true
    }
  }
}
</script>
