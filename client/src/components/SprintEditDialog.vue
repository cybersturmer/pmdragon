<template>
  <q-dialog ref="dialog" @hide="onDialogHide">
    <q-card dark class="q-dialog-plugin bg-secondary">
      <q-card-section>
        <q-input dark v-model="form.title"/>
        <q-input dark v-model="form.goal"/>
        <DateTimeField v-model="form.started_at"/>
        <DateTimeField v-model="form.finished_at"/>
      </q-card-section>
      <q-card-actions align="right">
        <q-btn color="primary" label="UPDATE" @click="onOKClick" />
        <q-btn color="primary" label="CANCEL" @click="onCancelClick" />
      </q-card-actions>
    </q-card>
  </q-dialog>
</template>

<script>
import DateTimeField from 'components/DateTimeField.vue'
import { date } from 'quasar'
import { DATETIME } from 'src/services/masks'

export default {
  name: 'SprintEditDialog',
  components: { DateTimeField },
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
        id: this.id,
        title: this.title,
        goal: this.goal,
        started_at: date.formatDate(this.started_at, DATETIME),
        finished_at: date.formatDate(this.finished_at, DATETIME)
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
        id: this.form.id,
        title: this.form.title,
        goal: this.form.goal,
        started_at: date.formatDate(this.form.started_at),
        finished_at: date.formatDate(this.form.finished_at)
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
