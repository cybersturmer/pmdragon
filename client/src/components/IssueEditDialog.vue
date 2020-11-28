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
          <q-card-section>
          <q-input
            dark
            :value="formData.issue.title"
            @input="updateIssueTitle($event)"
            :label="getIssueTitleLabel()"
            label-color="amber"
          />
          </q-card-section>
          <q-card-section>
          <div class="q-mb-sm text-subtitle2 text-amber">
            Description
          </div>
          <div
            v-show="!isDescriptionEditing"
            v-html="formData.issue.description"
            class="q-pa-md bg-accent editable_block"
            @click="updateDescriptionEditingState"
          >
          </div>
          <q-editor
            dark
            v-show="isDescriptionEditing"
            v-model="formData.issue.description"
            toolbar-toggle-color="amber"
            min-height="5rem"
          />
            <q-card-actions
              v-show="isDescriptionEditing"
              style="padding: 0"
              class="q-mt-sm"
            >
              <q-btn
              outline
              color="amber"
              size="sm"
              label="Save"
              style="width: 80px"
              @click="updateIssueDescription"
              />
              <q-btn
                flat
                color="amber"
                size="sm"
                label="Cancel"
                style="width: 80px"
                @click="cancelDescriptionEditing"
              />
            </q-card-actions>
          </q-card-section>
        </q-card-section>
        <q-separator dark vertical />
        <q-card-section class="col-4">
          <q-card-section>
            <q-select
              dark
              filled
              square
              dense
              :value="getIssueStateById(formData.issue.state_category)"
              @input="updateIssueState($event)"
              :options="issueStates"
              option-label="title"
              option-value="id"
            />
            <q-select
              dark
              filled
              square
              dense
              :value="getParticipantById(formData.issue.assignee)"
              @input="updateIssueAssignee($event)"
              :options="participants"
              :option-label="(item) => `${item.first_name} ${item.last_name}`"
              option-value="id"
            />
          </q-card-section>
          <q-card-section>
            <q-input
              dark
              filled
              square
              dense
              readonly
              :value="createdAt"
              :mask="mask"
              type="datetime"
              label="Created at"
              label-color="amber"
            />
            <q-input
              dark
              filled
              square
              dense
              readonly
              :value="updatedAt"
              :mask="mask"
              type="datetime"
              label="Updated at"
              label-color="amber"
            />
          </q-card-section>
        </q-card-section>
      </q-card-section>
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
    issueTypes: {
      type: Array,
      required: true
    },
    participants: {
      type: Array,
      required: true
    },
    $store: {
      type: Object,
      required: true
    }
  },
  data () {
    return {
      isDescriptionEditing: !this.issue.description,
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
      if (id === null) {
        return {
          id: null,
          first_name: 'Unassigned',
          last_name: ''
        }
      }

      return this.participants.find(participant => participant.id === id)
    },
    getIssueTypeTitle (id) {
      return this.issueTypes.find(type => type.id === id).title
    },
    getIssueTitleLabel () {
      const issueType = this.getIssueTypeTitle(this.formData.issue.type_category)
      return `#${this.formData.issue.id} ${issueType}`
    },
    updateDescriptionEditingState () {
      this.isDescriptionEditing = !this.isDescriptionEditing
    },
    updateIssueState (state) {
      this.formData.issue.state_category = state.id
      const payload = {
        id: this.formData.issue.id,
        state_category: this.formData.issue.state_category
      }

      this.$store.dispatch('issues/PATCH_ISSUE', payload)
      this.$emit('update_state', payload)
    },
    updateIssueAssignee (assignee) {
      this.formData.issue.assignee = assignee.id

      const payload = {
        id: this.formData.issue.id,
        assignee: assignee.id
      }

      this.$store.dispatch('issues/PATCH_ISSUE', payload)
      this.$emit('update_assignee', payload)
    },
    updateIssueTitle (title) {
      this.formData.issue.title = title

      const payload = {
        id: this.formData.issue.id,
        title: title
      }

      this.$store.dispatch('issues/PATCH_ISSUE', payload)
      this.$emit('update_title', payload)
    },
    updateIssueDescription () {
      const payload = {
        id: this.formData.issue.id,
        description: this.formData.issue.description
      }

      this.$store.dispatch('issues/PATCH_ISSUE', payload)
      this.isDescriptionEditing = false

      this.$emit('update_description', payload)
    },
    cancelDescriptionEditing () {
      this.formData.issue.description = this.issue.description
      this.isDescriptionEditing = false
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
    },
    updatedAt () {
      return date.formatDate(this.formData.issue.updated_at, DATETIME_MASK)
    }
  }
}
</script>
<style lang="scss">
  .editable_block:hover {
    background-color: $primary!important;
  }
</style>
