<template>
  <q-dialog ref="dialog" @hide="onDialogHide">
    <q-card dark class="q-dialog-plugin bg-secondary">
      <q-card-section>
        <div class="text-h5 text-center">
          Complete Sprint: {{ sprint.title }}
        </div>
      </q-card-section>
      <q-card-actions align="right">
        <q-btn color="primary" label="COMPLETE" @click="onOKClick" />
        <q-btn color="primary" label="CANCEL" @click="onCancelClick" />
      </q-card-actions>
    </q-card>
  </q-dialog>
</template>

<script>

export default {
  name: 'SprintCompleteDialog',
  props: {
    sprint: {
      type: Object,
      required: true
    }
  },
  data () {
    return {
      form: {
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
