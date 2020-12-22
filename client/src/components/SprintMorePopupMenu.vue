<template>
  <q-btn
    dark
    outline
    size="sm"
    color="amber"
    style="margin-left: 10px;"
    icon="more_horiz">
    <q-menu content-class="bg-secondary text-white" fit anchor="top left" self="top right" auto-close>
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
    sprintId: {
      type: Number,
      required: true
    }
  },
  methods: {
    editSprintModal () {
      this.$emit('edit', this.sprintId)
    },
    removeSprintModal () {
      this.$emit('remove', this.sprintId)
    }
  }
}
</script>
<style lang="scss">

</style>
