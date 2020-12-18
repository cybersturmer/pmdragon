<template>
  <q-layout view="lHh Lpr lFf" class="bg-grey-9 text-white">
    <q-header elevated class="bg-primary">
      <q-toolbar>
        <q-btn
          v-if="isWorkspaceSelected"
          flat
          dense
          round
          icon="menu"
          aria-label="Menu"
          @click="leftDrawerOpen = !leftDrawerOpen"
        />
        <q-toolbar-title>
          {{ toolbarText }}
        </q-toolbar-title>
        <q-btn
          flat
          round
          dense
          icon="swap_horiz"
          class="q-mr-xs"
          @click="goToWorkspaces"
        />
        <!-- @todo I Need to remove this hack when settings ready -->
        <q-btn
          v-if="isWorkspaceSelected && 1 === 0"
          flat
          round
          dense
          icon="settings"
          class="q-mr-xs"
          @click="goToSettings"
        />
        <q-btn
          v-if="isWorkspaceSelected"
          flat
          round
          dense
          icon="account_circle"
          class="q-mr-xs"
          @click="goToAccount"
        />
        <q-btn
          flat
          round
          dense
          icon="exit_to_app"
          class="q-mr-xs"
          @click="logout"
        />
      </q-toolbar>
    </q-header>

    <q-drawer
      v-if="isWorkspaceSelected"
      v-model="leftDrawerOpen"
      show-if-above
      :width="175"
      :breakpoint="600"
      content-class="bg-grey-8"
      bordered
    >
      <q-scroll-area style="height: calc(100% - 150px); margin-top: 150px;">
        <q-list dark class="q-pa-md">
          <q-item clickable v-ripple to="/dash/backlog">
            <q-item-section avatar>
              <q-icon name="toc" />
            </q-item-section>

            <q-item-section>
              Backlog
            </q-item-section>
          </q-item>

          <q-item clickable v-ripple to="/dash/board">
            <q-item-section avatar>
              <q-icon name="dashboard" />
            </q-item-section>

            <q-item-section>
              Board
            </q-item-section>
          </q-item>

          <q-item clickable v-ripple to="/dash/team">
            <q-item-section avatar>
              <q-icon name="people" />
            </q-item-section>

            <q-item-section>
              Team
            </q-item-section>
          </q-item>

        </q-list>
      </q-scroll-area>

      <q-card square flat class="absolute-top bg-grey-8" style="height: 150px;">
        <div class="absolute-bottom text-center bg-grey-8" style="margin-bottom: 1em;">
          <q-avatar v-if="avatarUrl" size="65px" class="q-mb-sm">
            <img :src="avatarUrl">
          </q-avatar>
          <div class="text-h6">{{ firstName }} {{ lastName }}</div>
          <div><q-badge outline color="amber" :label="`@${username}`" /></div>
        </div>
      </q-card>
    </q-drawer>

    <q-page-container>
      <keep-alive>
        <router-view />
      </keep-alive>
    </q-page-container>
  </q-layout>
</template>

<script>

export default {
  name: 'DashLayout',

  components: {
  },

  data () {
    return {
      leftDrawerOpen: false
    }
  },
  methods: {
    logout () {
      this.$store.dispatch('auth/LOGOUT')
        .then(() => {
          this.$store.dispatch('current/RESET_STATE')
          this.$store.dispatch('issues/RESET')
          this.$router.push({ name: 'login' })
        })
        .catch((e) => {
          this.$q.dialog({
            title: 'Error - Cannot LogOut',
            message: e
          })
        })
    },
    goToAccount () {
      if (this.$router.currentRoute.name === 'me') return false
      this.$router.push({ name: 'me' })
    },
    goToWorkspaces () {
      if (this.$router.currentRoute.name === 'workspaces') return false
      this.$store.dispatch('current/RESET_WORKSPACE')
      this.$store.dispatch('current/RESET_PROJECT')
      this.$router.push({ name: 'workspaces' })
    }
  },
  computed: {
    toolbarText: function () {
      const workspaceName = this.$store.getters['current/WORKSPACE']
      const project = this.$store.getters['current/PROJECT']

      if (workspaceName && project) {
        const projectName = this.$store.getters['auth/PROJECT_NAME']
        return `${workspaceName} - [ ${projectName} ]`
      }

      return '  PmDragon Community Edition'
    },
    firstName: function () {
      return this.$store.getters['auth/MY_FIRST_NAME']
    },
    lastName: function () {
      return this.$store.getters['auth/MY_LAST_NAME']
    },
    username: function () {
      return this.$store.getters['auth/MY_USERNAME']
    },
    avatarUrl: function () {
      return this.$store.getters['auth/MY_AVATAR']
    },
    isWorkspaceSelected: function () {
      return this.$store.getters['current/WORKSPACE']
    }
  }
}
</script>

<style lang="scss">
  .q-toolbar__title {
    font-size: 18px;
  }
  .q-toolbar__title:first-child {
    padding-left: 1em;
  }

  .q-drawer--left.q-drawer--bordered {
    border-color: #0f0f0f;
  }

  .text-h6 {
    font-size: 0.9rem;
  }
  .header-image {
    height: 100%;
    z-index: -1;
    opacity: 0.1;
    filter: grayscale(100%);
  }

  .q-img__content > div {
    padding: 0.5rem;
  }

  .q-field--dark .q-field__native,
  .q-field--dark .q-field__prefix,
  .q-field--dark .q-field__suffix,
  .q-field--dark .q-field__input {
    font-weight: bold;
  }
</style>
