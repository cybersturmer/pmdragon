<template>
  <q-dialog ref="dialog" @hide="onDialogHide">
    <q-card dark class="q-dialog-plugin bg-secondary">
      <q-card-section>
        <q-input dark v-model="form.title"/>
        <q-input dark v-model="form.goal"/>
        <DateTimeField v-model="form.startedAt"/>
        <DateTimeField v-model="form.finishedAt"/>
      </q-card-section>
      <q-card-actions align="right">
        <q-btn color="primary" label="UPDATE" @click="onOKClick" />
        <q-btn color="primary" label="CANCEL" @click="onCancelClick" />
      </q-card-actions>
    </q-card>
  </q-dialog>
</template>

<script>
import DateTimeField from 'components/fields/DateTimeField.vue'
import { date } from 'quasar'
import { DATETIME_MASK } from 'src/services/masks'

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
    startedAt: {
      type: String
    },
    finishedAt: {
      type: String
    }
  },
  data () {
    return {
      form: {
        id: this.id,
        title: this.title,
        goal: this.goal,
        startedAt: date.formatDate(this.startedAt, DATETIME_MASK),
        finishedAt: date.formatDate(this.finishedAt, DATETIME_MASK)
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
        startedAt: date.formatDate(this.form.startedAt),
        finishedAt: date.formatDate(this.form.finishedAt)
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
