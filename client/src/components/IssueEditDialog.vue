<template>
  <q-dialog ref="dialog" @hide="onDialogHide">
    <q-card dark class="q-dialog-plugin bg-secondary">
      <q-card-section>
        <q-input dark v-model="formData.title"/>
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
    issueId: {
      type: Number,
      required: true
    }
  },
  data () {
    return {
      issueData: this.$store.getters['issues/ISSUE_BY_ID'](this.issueId),
      formData: {
        id: this.id,
        title: this.issueData.title
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
  },
  computed: {
    getIssueData () {
      return this.$store.getters['issues/ISSUE_BY_ID'](this.issueId)
    }
  }
}
</script>
