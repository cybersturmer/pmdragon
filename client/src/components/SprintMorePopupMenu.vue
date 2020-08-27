<template>
  <q-btn
    dark
    outline
    size="sm"
    color="accent"
    style="margin-left: 10px;"
    icon="more_horiz">
    <q-menu content-class="bg-accent text-white" fit anchor="top left" self="top right" auto-close>
      <q-list dense style="min-width: 150px">
        <q-item
          clickable
          v-close-popup
          @click="editSprintModal">
          <q-item-section>Edit Sprint</q-item-section>
        </q-item>
        <q-separator />
        <q-item
          clickable
          v-close-popup
          @click="removeSprintModal">
          <q-item-section>Remove Sprint</q-item-section>
        </q-item>
      </q-list>
    </q-menu>
  </q-btn>
</template>

<script>
export default {
  name: 'SprintMorePopupMenu',
  props: {
    sprint_id: {
      type: Number,
      required: true
    }
  },
  methods: {
    editSprintModal () {
      console.log('editSprintModal')
      this.$emit('edit', this.sprint_id)
    },
    removeSprintModal () {
      console.log('removeSprintModal')
      this.$emit('remove', this.sprint_id)
    }
  }
}
</script>
<style lang="scss">

</style>
