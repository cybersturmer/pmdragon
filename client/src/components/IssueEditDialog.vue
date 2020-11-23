<template>
  <q-dialog
    ref="dialog"
    @hide="onDialogHide"
  >
    <q-card
      dark
      class="q-dialog-plugin bg-secondary"
      style="width: 85vw; max-width: 85vw;"
    >
      <q-card-section horizontal>
        <q-card-section class="col-8">
          <!-- @todo Breadcrumbs for current issue -->
          <q-input
            dark
            dense
            v-model="formData.issue.title"
          />
          <q-editor
            dark
            v-model="formData.issue.description"
            toolbar-toggle-color="amber"
            min-height="5rem"
          />
          <!-- @todo Issue description -->
        </q-card-section>
        <q-separator dark vertical />
        <q-card-section class="col-4">
          <q-select
            dark
            dense
            :value="getIssueStateById(formData.issue.state_category)"
            @input="updateIssueState($event)"
            :options="issueStates"
            option-label="title"
            option-value="id"
          />
          <q-select
            dark
            dense
            :value="getParticipantById(formData.issue.assignee)"
            @input="updateParticipant($event)"
            :options="participants"
            :option-label="(item) => `${item.first_name} ${item.last_name}`"
            option-value="id"
          />
          <q-input
            dark
            dense
            readonly
            :value="createdAt"
            :mask="mask"
            type="datetime"
          />
          <!-- @todo Issue assignment -->
          <!-- @todo Issue state -->
          <!-- @todo Issue type -->
        </q-card-section>
      </q-card-section>
      <q-card-actions align="right">
        <q-btn color="primary" label="UPDATE" @click="onOKClick" />
        <q-btn color="primary" label="CANCEL" @click="onCancelClick" />
      </q-card-actions>
    </q-card>
  </q-dialog>
</template>

<script>
import { DATETIME_MASK } from 'src/services/masks'
import { date } from 'quasar'
import { unWatch } from 'src/services/util'

export default {
  name: 'IssueEditDialog',
  props: {
    issue: {
      type: Object,
      required: true
    },
    issueStates: {
      type: Array,
      required: true
    },
    participants: {
      type: Array,
      required: true
    }
  },
  data () {
    return {
      issueData: this.issue,
      formData: {
        issue: unWatch(this.issue)
      },
      mask: DATETIME_MASK
    }
  },
  methods: {
    getIssueStateById (id) {
      return this.issueStates.find(state => state.id === id)
    },
    getParticipantById (id) {
      return this.participants.find(participant => participant.id === id)
    },
    updateIssueState (state) {
      this.formData.issue.state_category = state.id
    },
    updateParticipant (participant) {
      this.formData.issue.assignee = participant.id
    },
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
  },
  computed: {
    createdAt () {
      return date.formatDate(this.formData.issue.created_at, DATETIME_MASK)
    }
  }
}
</script>
