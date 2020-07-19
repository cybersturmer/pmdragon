<template>
  <q-card
    dense
    dark
    bordered
    class="my-card bg-accent"
    @mouseover="is_edit_button_visible = true"
    @mouseleave="is_edit_button_visible = false"
  >
    <q-card-section>
      # {{ id }} {{ title }}
      <q-btn
        v-show="is_edit_button_visible"
        dense
        flat
        icon-right="more_vert"
        class="absolute-right"
        style="margin-right: 10px">
        <q-menu dark>
          <q-list dense style="min-width: 100px">
            <q-item
              clickable
              v-close-popup
              @click="editIssueModal">
              <q-item-section>Edit</q-item-section>
            </q-item>
            <q-item
              clickable
              v-close-popup
              @click="removeIssueModal">
              <q-item-section>Remove</q-item-section>
            </q-item>
          </q-list>
        </q-menu>
      </q-btn>
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
      is_edit_button_visible: false
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
</script>
