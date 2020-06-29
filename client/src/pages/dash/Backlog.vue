<template>
  <q-page class="flex q-layout-padding">
    <div class="column full-width">
      <h5>Sprints</h5>
      <div class="col">
        <q-scroll-area style="height: 100%">
          <div
            v-for="item in sprints"
            :key="item.id">
            <div class="h6">
              {{ item.title }} - {{ item.goal }} - (&nbsp;{{ item.issues.length }} issues&nbsp;)
            </div>
            <q-card
              v-for="issue in item.issues"
              :key="issue.id"
              dense
              dark
              bordered
              class="my-card bg-grey-8 text-white shadow-3 overflow-hidden no-padding">
              <q-card-section>
                {{ issue.title }}
              </q-card-section>
            </q-card>
          </div>
        </q-scroll-area>
      </div>
      <h5>Backlog (&nbsp;{{ backlogIssuesLength }} issues&nbsp;)</h5>
      <div class="col" v-if="backlogIssues">
        <q-scroll-area style="height: calc(100% - 35px)">
          <draggable
            v-model="backlogIssues"
            group="issues">
            <transition-group type="transition" :name="'flip-list'">
              <q-card
                v-for="item in backlogIssues"
                :key="item.id"
                @mouseover="showIssueMenu(item.id)"
                dense
                dark
                bordered
                class="my-card bg-grey-8 text-white shadow-3 overflow-hidden no-padding">
                <q-card-section>
                  {{ item.title }}
                  <q-btn
                    v-show="show_edit_button === item.id"
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
                          @click="editIssueModal(item)">
                          <q-item-section>Edit</q-item-section>
                        </q-item>
                        <q-item
                          clickable
                          v-close-popup
                          @click="removeIssueModal(item)">
                          <q-item-section>Remove</q-item-section>
                        </q-item>
                      </q-list>
                    </q-menu>
                  </q-btn>
                </q-card-section>
              </q-card>
            </transition-group>
          </draggable>
        </q-scroll-area>
        <q-card dark
                bordered
                square
                class="my-card bg-grey-8 text-white shadow-3 absolute-bottom card-no-padding"
        style="margin: 0.3em">
          <q-card-section>
            <q-input
              v-model="form_data.title"
              @keyup.enter="createIssue"
              dark
              dense
              square
              filled
              placeholder="Add Issue">
              <template v-slot:append>
                <q-btn @click="createIssue"
                       :disable="!isAddButtonEnabled"
                       dense
                       rounded
                       flat
                       icon="add"/>
              </template>
            </q-input>
          </q-card-section>
        </q-card>
      </div>
    </div>

  </q-page>
</template>

<script>
import draggable from 'vuedraggable'

export default {
  name: 'BacklogView',
  components: {
    draggable
  },
  data () {
    return {
      show_edit_button: Number,
      form_data: {
        workspace: null,
        title: null,
        project: null,
        type_category: null,
        state_category: null,
        ordering: null
      }
    }
  },
  computed: {
    backlogIssues: {
      get: function () {
        return this.$store.getters['issues/BACKLOG_ISSUES']
      },
      set: function (array) {
        const payload = [...array]

        payload.forEach((value, index) => {
          const _issue = Object.assign({}, value)
          _issue.ordering = index
          payload[index] = _issue
        })

        this.$store.dispatch('issues/ORDER_BACKLOG_ISSUES', payload)
      }
    },
    sprints: {
      get: function () {
        return this.$store.getters['issues/UNCOMPLETED_PROJECT_SPRINTS']
      },
      set: function (array) {
        const payload = [...array]

        payload.forEach((value, index) => {
          const _issue = Object.assign({}, value)
          _issue.ordering = index
          payload[index] = _issue
        })

        this.$store.dispatch('issues/')
      }
    },
    backlogIssuesLength: function () {
      return this.$store.getters['issues/BACKLOG_ISSUES_COUNT']
    },
    isAddButtonEnabled: function () {
      return Boolean(this.form_data.title)
    }
  },
  mounted () {
    this.$store.dispatch('issues/INIT_BACKLOGS')
      .catch((error) => {
        this.$q.dialog({
          title: 'Error - Cannot get Backlogs',
          message: 'Please check your Internet connection'
        })

        console.log(error)
      })

    this.$store.dispatch('issues/INIT_SPRINTS')
      .catch((error) => {
        this.$q.dialog({
          title: 'Error = Cannot get Sprints',
          message: 'Please check your Internet connection'
        })

        console.log(error)
      })
  },
  methods: {
    createIssue () {
      if (!this.form_data.title) return false

      this.form_data.workspace = this.$store.getters['current/WORKSPACE_ID']
      this.form_data.project = this.$store.getters['current/PROJECT']
      this.$store.dispatch('issues/ADD_ISSUE_TO_BACKLOG', this.form_data)
        .then(() => {
          this.form_data.title = ''
        })
        .catch((error) => {
          this.$q.dialog({
            title: 'Error - Cannot add issue to Backlog',
            message: 'Please check your Internet connection'
          })

          console.log(error)
        })
    },
    showIssueMenu (id) {
      this.show_edit_button = id
    },
    editIssueModal (item) {
      this.$q.dialog({
        dark: true,
        title: 'Issue information',
        message: 'Set Issue title',
        prompt: {
          model: item.title,
          type: 'text'
        },
        cancel: true,
        persistent: true
      })
        .onOk((data) => {
          const payload = {
            workspace: this.$store.getters['current/WORKSPACE_ID'],
            project: this.$store.getters['current/PROJECT'],
            id: item.id,
            title: data
          }

          this.$store.dispatch('issues/EDIT_ISSUE', payload)
            .catch((error) => {
              this.$q.dialog({
                title: 'Error - Cannot edit issue',
                message: 'Please check your Internet connection'
              })
              console.log(error)
            })
        })
    },
    removeIssueModal (item) {
      this.$q.dialog({
        dark: true,
        title: 'Confirmation',
        message: `Would you like to delete issue: ${item.title}`,
        cancel: true,
        persistent: true
      }).onOk(() => {
        this.$store.dispatch('issues/DELETE_ISSUE', item)
          .catch((error) => {
            this.$q.dialog({
              title: 'Error - Cannot delete issue',
              message: 'Please check your Internet connection'
            })

            console.log(error)
          })
      })
    }
  }
}
</script>
<style lang="scss">
  .flip-list-move {
    transition: transform 0.3s;
  }

  .my-card {
    margin-bottom: 0.75em;
  }

  h5 {
    font-size: 1.25rem;
    margin-bottom: 0.5rem;
    margin-top: 0.5rem;
  }

  .card-no-padding {
    .q-card__section--vert {
        padding: 0;
    }
  }

  .text-amber {
    color: #8b8b8b!important;
  }

</style>
