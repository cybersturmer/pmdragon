<template>
  <q-page class="flex flex-center">
    <q-card dark flat bordered class="my-card" style="width: 320px; height: 120px">
      <q-card-section class="text-center">
        <transition appear enter-active-class="animated fadeIn" leave-active-class="animated fadeOut">
          <div v-if="is_success" class="text-h6">You accepted invitation to workspace.</div>
          <div v-else-if="is_error" class="text-h6">Some error occurred</div>
        </transition>
      </q-card-section>
      <q-inner-loading :showing="!is_request_sent">
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
      is_request_sent: false,
      is_verified: false
    }
  },
  computed: {
    key () {
      return this.$attrs.key
    },
    is_error () {
      return this.is_request_sent && !this.is_verified
    },
    is_success () {
      return this.is_request_sent && this.is_verified
    }
  },
  async mounted () {
    await this.verifyCollaboration()
  },
  methods: {
    async verifyCollaboration () {
      try {
        await new Api().put(`/auth/request/collaborations/${this.key}/`)
        this.is_request_sent = true
        this.is_verified = true
      } catch (e) {
        this.is_request_sent = true
        this.is_verified = false
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
