<template>
  <q-dialog ref="dialog" @hide="onDialogHide">
    <q-card dark class="q-dialog-plugin bg-secondary">
      <q-card-section>
        <!-- @todo Issue title -->
        <!-- @todo Issue assignment -->
        <!-- @todo Issue description -->
        <!-- @todo Breadcrumbs for current issue -->
        <!-- @todo Issue state -->
        <!-- @todo Issue type -->
      </q-card-section>
      <q-card-actions align="right">
        <q-btn color="primary" label="UPDATE" @click="onOKClick" />
        <q-btn color="primary" label="CANCEL" @click="onCancelClick" />
      </q-card-actions>
    </q-card>
  </q-dialog>
</template>

<script>

export default {
  name: 'IssueEditDialog',
  props: {
    id: {
      type: Number,
      required: true
    },
    title: {
      type: String,
      required: true
    },
    goal: {
      type: String,
      required: true
    },
    started_at: {
      type: String
    },
    finished_at: {
      type: String
    }
  },
  data () {
    return {
      form: {
        id: this.id
      }
    }
  },
  methods: {
    show () {
      this.$refs.dialog.show()
    },

    hide () {
      this.$refs.dialog.hide()
    },

    onDialogHide () {
      this.$emit('hide')
    },

    onOKClick () {
      const payload = {
      }

      this.$emit('ok', payload)
      this.hide()
    },

    onCancelClick () {
      this.hide()
    }
  }
}
</script>
