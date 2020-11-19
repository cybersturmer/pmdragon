<template>
  <q-card
    dense
    dark
    bordered
    class="my-card"
    @mouseover="isEditButtonVisible = true"
    @mouseleave="isEditButtonVisible = false"
  >
    <q-card-section>
      # {{ id }} {{ title }}
      <transition name="fade">
        <q-btn
          v-show="isEditButtonVisible"
          dense
          flat
          icon-right="more_horiz"
          class="absolute-right"
          style="margin-right: 10px">
          <q-menu content-class="bg-accent text-white" fit anchor="top left" self="top right" auto-close>
            <q-list dense style="min-width: 150px">
              <q-item
                clickable
                v-close-popup
                @click="editIssueModal">
                <q-item-section>Edit Issue</q-item-section>
              </q-item>
              <q-separator />
              <q-item
                clickable
                v-close-popup
                @click="removeIssueModal">
                <q-item-section>Remove Issue</q-item-section>
              </q-item>
            </q-list>
          </q-menu>
        </q-btn>
      </transition>
    </q-card-section>
  </q-card>
</template>

<script>
export default {
  name: 'IssueBacklog',
  props: {
    id: {
      type: Number,
      required: true
    },
    title: {
      type: String,
      required: true
    }
  },
  data () {
    return {
      isEditButtonVisible: false
    }
  },
  methods: {
    editIssueModal () {
      this.$emit('edit', this.id)
    },
    removeIssueModal () {
      this.$emit('remove', this.id)
    }
  }
}
</script>xha
<style lang="scss">
  .fade-enter-active, .fade-leave-active {
    transition: opacity .25s;
  }
  .fade-enter, .fade-leave-to {
    opacity: 0;
  }
</style>
