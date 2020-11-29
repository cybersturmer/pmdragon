<template>
  <q-page class="flex flex-center">
    <q-card dark flat bordered class="my-card" style="width: 320px">
      <q-card-section class="text-center">
        <transition appear enter-active-class="animated fadeIn" leave-active-class="animated fadeOut">
          <q-card-section>
            <q-card-section v-if="is_success" class="text-h6">
              You accepted invitation to workspace.
            </q-card-section>
            <q-card-section v-else-if="is_error" class="text-h6">
              Collaboration request was not found.
            </q-card-section>
            <q-card-actions align="center">
              <q-btn
                dark
                flat
                label="To login page"
                to="/login"
              />
            </q-card-actions>
          </q-card-section>
        </transition>
      </q-card-section>
      <q-inner-loading :showing="!isRequestSent">
        <q-spinner-gears size="50px" color="primary" />
      </q-inner-loading>
    </q-card>
  </q-page>
</template>

<script>
import { Api } from 'src/services/api'
import { Dialogs } from 'pages/mixins/dialogs'

export default {
  name: 'VerifyCollaboration',
  mixins: [Dialogs],
  data () {
    return {
      isRequestSent: false,
      isVerified: false
    }
  },
  computed: {
    key () {
      return this.$attrs.key
    },
    is_error () {
      return this.isRequestSent && !this.isVerified
    },
    is_success () {
      return this.isRequestSent && this.isVerified
    }
  },
  async mounted () {
    await this.verifyCollaboration()
  },
  methods: {
    async verifyCollaboration () {
      const payload = {
        is_accepted: true
      }

      try {
        await new Api().put(`/auth/person-invitation-requests/${this.key}/`, payload)
        this.isRequestSent = true
        this.isVerified = true
      } catch (e) {
        this.isRequestSent = true
        this.isVerified = false
      }
    }
  }
}
</script>

<style scoped>
  .q-card__section--vert {
    padding: 13px;
  }
</style>
