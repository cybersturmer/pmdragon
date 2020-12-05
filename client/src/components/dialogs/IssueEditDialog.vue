<template>
  <q-dialog
    ref="dialog"
    @hide="onDialogHide"
  >
    <q-card
      dark
      flat
      bordered
      class="q-dialog-plugin bg-secondary"
      style="width: 85vw; max-width: 85vw;"
    >
      <q-card-section horizontal>
        <q-card-section class="col-md-8 col-xs-12 col-sm-12">
          <!-- @todo Breadcrumbs for current issue -->
          <q-scroll-area
            dark
            style="height: 65vh; border-bottom: 1px solid #686868;">
            <!-- Title block -->
            <q-card-section>
              <!-- Title editing section -->
              <q-input
                dark
                :value="formData.issue.title"
                @input="updateIssueTitle($event)"
                :label="getIssueTitleLabel()"
                label-color="amber">
                <template v-slot:before>
                  <q-icon
                    v-if="isIssueTypeIcon"
                    :name="getIssueTypeIcon.prefix"
                    :color="getIssueTypeIcon.color"
                    :title="getIssueTypeTitle(formData.issue.type_category)"
                    size="md"
                  />
                </template>
              </q-input>
            </q-card-section>
            <!-- Description -->
            <q-card-section>
              <!-- Block with issue description -->
              <div class="q-mb-xs text-subtitle2 text-amber">
                Description
              </div>
              <q-card
                v-show="!isDescriptionEditing"
                dark
                flat
                bordered
              >
                <q-card-section
                  v-html="formData.issue.description || 'Add a description by clicking this area...'"
                  class="q-pa-md editable_block"
                  @click="startEditingDescription"
                />
              </q-card>
              <q-editor
                ref="issueDescriptionEditor"
                dark
                v-show="isDescriptionEditing"
                v-model="formData.issue.description"
                paragraph-tag="p"
                toolbar-toggle-color="amber"
                min-height="5rem"
                :toolbar="editorToolbar"
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
            <!-- Messages -->
            <q-card-section
              style="padding: 0"
            >
              <!-- Block with messages -->
              <q-card-section>
                <div class="q-mb-xs text-subtitle2 text-amber">
                  Messages
                </div>
                <q-card
                  dark
                  flat
                  bordered
                  v-show="thereAreMessages"
                >
                  <q-card-section>
                    <q-chat-message
                      v-for="message in messages"
                      v-bind:key="message.id"
                      :name="getParticipantTitleById(message.created_by)"
                      :avatar="getParticipantById(message.created_by).avatar"
                      size="6"
                      :text-sanitize="false"
                      bg-color="accent"
                      text-color="amber"
                      :sent="isItMe(message.created_by)"
                    >
                      <template #default>
                        <div v-html="message.description"/>
                        <div class="text-left q-message-stamp">
                          {{ getRelativeDatetime(message.updated_at) }}
                        </div>
                        <div class="text-right">
                          <q-btn-group
                            v-show="isItMe(message.created_by)"
                            outline
                            stretch
                            class="bottom-right">
                            <q-btn
                              flat
                              size="sm"
                              label="edit"
                              @click="startMessageEditing(message.id)"
                            />
                            <q-btn
                              flat
                              size="sm"
                              label="delete"
                              @click="removeMessage(message.id)"
                            />
                          </q-btn-group>
                        </div>
                      </template>
                    </q-chat-message>
                  </q-card-section>
                </q-card>
              </q-card-section>
            </q-card-section>
          </q-scroll-area>
            <!-- New Message Block -->
          <q-card-section style="padding: 0">
            <q-card-section>
              <!-- Section for save new message -->
                <q-card
                  v-show="!isNewMessageEditing"
                  dark
                  bordered
                  class="editable_block"
                >
                  <q-card-section
                    @click="isNewMessageEditing = !isNewMessageEditing"
                  >
                    Add new message...
                  </q-card-section>
                </q-card>
                <q-card-section
                  v-show="isNewMessageEditing"
                  style="padding: 0">
                  <q-editor
                    dark
                    v-model="formNewMessage.description"
                    :toolbar="editorToolbar"
                    paragraph-tag="p"
                    ref="issueMessageEditor"
                    max-height="15vh"
                    toolbar-toggle-color="amber"
                    min-height="5rem"
                  />
                </q-card-section>
                <q-card-actions
                  v-show="isNewMessageEditing"
                  class="q-mt-sm"
                >
                  <q-btn
                    outline
                    color="amber"
                    size="sm"
                    label="Save"
                    style="width: 80px"
                    @click="createOrUpdateMessage"
                  />
                  <q-btn
                    flat
                    color="amber"
                    size="sm"
                    label="Cancel"
                    style="width: 80px"
                    @click="cancelMessageEditing"
                  />
                </q-card-actions>
            </q-card-section>
          </q-card-section>
        </q-card-section>
        <q-separator dark vertical />
        <q-card-section class="col-md-4 xs-hide sm-hide">
        <!-- Right section, we can change issue data here -->
          <q-card-section>
            <!-- Selection for issue state -->
            <q-select
              dark
              flat
              square
              dense
              :value="getIssueStateById(formData.issue.state_category)"
              @input="updateIssueState($event)"
              :options="issueStates"
              option-label="title"
              option-value="id"
            />
            <!-- Selection for issue type -->
            <q-select
              dark
              flat
              square
              dense
              :value="getIssueTypeById(formData.issue.type_category)"
              @input="updateIssueType($event)"
              :options="issueTypes"
              option-label="title"
              option-value="id"
            />
            <!-- Selection for assignee -->
            <q-select
              dark
              flat
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
            <!-- Readonly props such as created at and updated at -->
            <q-input
              dark
              flat
              square
              readonly
              :value="createdAt"
              :mask="mask"
              type="datetime"
              label="Created at"
              label-color="amber"
            />
            <q-input
              dark
              flat
              square
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
import { HandleResponse, unWatch } from 'src/services/util'
import { Api } from 'src/services/api'

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
      editorToolbar: [
        ['bold', 'italic', 'underline', 'strike'],
        ['undo', 'redo']
      ],
      isDescriptionEditing: !this.issue.description,
      formData: {
        issue: unWatch(this.issue)
      },
      formNewMessage: {
        issue: this.issue.id,
        description: ''
      },
      isNewMessageEditing: false,
      editingMessageId: null,
      messages: [],
      mask: DATETIME_MASK
    }
  },
  async mounted () {
    await this.getMessages()
  },
  methods: {
    getRelativeDatetime (datetime) {
      /** Get relative datetime for messages **/
      return this.$moment(datetime).fromNow()
    },
    getIssueStateById (id) {
      /** Get Issue state by Id, we got Issue State from props given to component **/
      return this.issueStates.find(state => state.id === id)
    },
    getIssueTypeById (id) {
      /** Get Issue Type by Id, we got Issue Types from props given to component **/
      return this.issueTypes.find(state => state.id === id)
    },
    getParticipantById (id) {
      /** Get participant object by given id from participants list given in props
       * It also can return Unassigned if given person was not found **/
      if (id === null) {
        return {
          id: null,
          first_name: 'Unassigned',
          last_name: ''
        }
      }

      return this.participants.find(participant => participant.id === id)
    },
    isItMe (id) {
      /** Return true if given id is current user id **/
      return id === this.$store.getters['auth/MY_USER_ID']
    },
    getParticipantTitleById (id) {
      /** return title with username, first name and last name as a String **/
      const participant = this.getParticipantById(id)
      return `@${participant.username} ( ${participant.first_name} ${participant.last_name} )`
    },
    async getMessages () {
      /** get messages for current issue without paging
       * Now its not a problem, will think later **/
      const response = await new Api({ auth: true }).get(
        `/core/issue-messages/?issue=${this.formData.issue.id}`
      )

      HandleResponse.compare(200, response.status)

      this.messages = response.data
    },
    getIssueTypeTitle (id) {
      /** get Title for given issue type id **/
      return this.issueTypes.find(type => type.id === id).title
    },
    getIssueTitleLabel () {
      /** get Issue title with Type and id of Issue **/
      const issueType = this.getIssueTypeTitle(this.formData.issue.type_category)
      return `#${this.formData.issue.id} ${issueType}`
    },
    startEditingDescription () {
      /** update description state
       * We use it by clicking on the block with description of Issue
       * for make it editable **/
      this.isDescriptionEditing = true
    },
    updateIssueState (state) {
      /** update state for Issue
       * We use it in selection field **/
      this.formData.issue.state_category = state.id
      const payload = {
        id: this.formData.issue.id,
        state_category: this.formData.issue.state_category
      }

      this.$store.dispatch('issues/PATCH_ISSUE', payload)
      this.$emit('update_state', payload)
    },
    updateIssueType (state) {
      /** update Issue type
       * we use it in selection field **/
      this.formData.issue.type_category = state.id
      const payload = {
        id: this.formData.issue.id,
        type_category: this.formData.issue.type_category
      }

      this.$store.dispatch('issues/PATCH_ISSUE', payload)
      this.$emit('update_type', payload)
    },
    updateIssueAssignee (assignee) {
      /** update Issue assignee
       * we use it in selection field **/
      this.formData.issue.assignee = assignee.id

      const payload = {
        id: this.formData.issue.id,
        assignee: assignee.id
      }

      this.$store.dispatch('issues/PATCH_ISSUE', payload)
      this.$emit('update_assignee', payload)
    },
    updateIssueTitle (title) {
      /** update Issue Title
       * we use it as a handler after text in input was changed
       * and user leave field by clicking outside **/
      this.formData.issue.title = title

      const payload = {
        id: this.formData.issue.id,
        title: title
      }

      this.$store.dispatch('issues/PATCH_ISSUE', payload)
      this.$emit('update_title', payload)
    },
    updateIssueDescription () {
      /** update Issue description
       * we use it as a handler for description field changing **/
      const payload = {
        id: this.formData.issue.id,
        description: this.formData.issue.description
      }

      this.$store.dispatch('issues/PATCH_ISSUE', payload)
      this.isDescriptionEditing = false

      this.$emit('update_description', payload)
    },
    cancelDescriptionEditing () {
      /** We use this handler if user wrote something in Issue description
       * and clicked cancel then **/
      this.formData.issue.description = this.issue.description
      this.isDescriptionEditing = false
    },
    cancelMessageEditing () {
      /** We use it if user wrote a message and clicked cancel then **/
      this.isNewMessageEditing = false
      this.formNewMessage.description = ''
      this.editingMessageId = null
    },
    async _createMessage () {
      /** We use it for adding one more message **/
      const payload = this.formNewMessage
      const response = await new Api({ auth: true }).post(
        '/core/issue-messages/',
        payload
      )

      HandleResponse.compare(201, response.status)
      this.messages.push(response.data)
    },
    async _updateMessage () {
      const payload = {
        description: this.formNewMessage.description
      }

      const response = await new Api({ auth: true }).patch(
        `/core/issue-messages/${this.editingMessageId}/`,
        payload
      )

      HandleResponse.compare(200, response.status)
      const oldMessage = this.messages
        .find(message => message.id === this.editingMessageId)

      const idx = this.messages
        .indexOf(oldMessage)

      this.messages.splice(idx, 1, response.data)
    },
    async createOrUpdateMessage () {
      /** We use it for adding one more message **/
      if (this.editingMessageId !== null) {
        await this._updateMessage()
      } else {
        await this._createMessage()
      }

      this.cancelMessageEditing()
    },
    startMessageEditing (id) {
      const message = this.messages.find(message => message.id === id)

      this.formNewMessage.description = message.description
      this.editingMessageId = id
      this.isNewMessageEditing = true
    },
    async removeMessage (id) {
      const response = await new Api({ auth: true }).delete(
        `/core/issue-messages/${id}/`
      )

      HandleResponse.compare(204, response.status)
      this.messages = this.messages.filter((value) => {
        return value.id !== id
      })
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
    },
    thereAreMessages () {
      return this.messages.length > 0
    },
    isIssueTypeIcon () {
      return this.$store.getters['issues/IS_ISSUE_TYPE_HAVE_ICON'](this.issue.type_category)
    },
    getIssueTypeIcon () {
      return this.$store.getters['issues/ISSUE_TYPE_BY_ID'](this.issue.type_category).icon
    }
  }
}
</script>
<style lang="scss">
  .editable_block:hover {
    background-color: $primary!important;
  }
</style>
