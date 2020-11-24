<template>
  <q-page class="flex q-layout-padding">
    <div class="full-width">
      <q-card
        dark
        bordered
        square>
        <q-tabs
          class="bg-secondary"
          v-model="tab"
          dense
          align="justify"
          narrow-indicator
        >
          <q-tab name="interface" icon="fact_check" label="Interface"/>
          <q-tab name="issue_types" icon="view_agenda" label="Issue Types" />
          <q-tab name="issue_states" icon="view_column" label="Issue States" />
          <q-tab name="sprint_duration" icon="history_toggle_off" label="Sprint Duration" />
          <q-tab name="server" icon="sync" label="Server" />
        </q-tabs>
        <q-separator />
        <q-tab-panels class="bg-amber" v-model="tab" animated>
          <q-tab-panel name="interface">
            <q-select
              v-model="interfaceTheme"
              :options="interfaceData.interfaceOptions"
              dark
              dense
              square
              outlined
              options-dense
            />
            <q-select
              v-model="language"
              :options="interfaceData.languageOptions"
              dark
              dense
              square
              outlined
              options-dense
            />

          </q-tab-panel>

          <q-tab-panel name="issue_types">
            <div class="text-h6">Issue Types</div>
            Lorem ipsum dolor sit amet consectetur adipisicing elit.
          </q-tab-panel>

          <q-tab-panel name="issue_states">
            <div class="text-h6">Issue States</div>
            Lorem ipsum dolor sit amet consectetur adipisicing elit.
          </q-tab-panel>

          <q-tab-panel name="sprint_duration">
            <div
              v-for="sprint_duration in sprintDurations"
              :key="sprint_duration.id"
              class="row">
              <div class="col-8">
                <q-input
                  dark
                  dense
                  square
                  outlined
                  placeholder="Title (for example: 2 week sprint)"
                  :value="sprint_duration.title"
                >
                  <template v-slot:append>
                    <q-icon name="short_text"/>
                  </template>
                </q-input>
              </div>
              <div class="col-4">
                <q-input
                  dark
                  dense
                  square
                  outlined
                  placeholder="Duration (for example: 14d)"
                  :value="sprint_duration.duration"
                >
                  <template v-slot:append>
                    <q-icon name="timelapse"/>
                  </template>
                </q-input>
              </div>
            </div>

          </q-tab-panel>

          <q-tab-panel name="server">
            <q-input
              v-model="serverFormData.server"
              dark
              square
              dense
              outlined
              placeholder="Server for connection"
              />
            <q-input
              v-model="serverFormData.port"
              dark
              square
              dense
              outlined
              placeholder="Port for connection"
            />
          </q-tab-panel>
        </q-tab-panels>
      </q-card>
    </div>
  </q-page>
</template>

<script>
export default {
  name: 'SettingsView',
  data () {
    return {
      tab: 'interface',
      interfaceData: {
        interfaceOptions: [
          {
            label: 'Dark interface',
            value: 'dark-interface'
          },
          {
            label: 'Light interface',
            value: 'light-interface'
          }
        ],
        languageOptions: [
          {
            label: 'English',
            value: 'en'
          },
          {
            label: 'Russian',
            value: 'ru'
          }
        ]
      },
      serverFormData: {
        server: 'localhost',
        port: 8080
      }
    }
  },
  computed: {
    interfaceTheme: {
      get: function () {
        return this.$store.getters['current/INTERFACE_THEME']
      },
      set: function (payload) {
        this.$store.dispatch('current/SELECT_INTERFACE_THEME', payload)
      }
    },
    sprintDurations: {
      get: function () {
        return this.$store.getters['issues/WORKSPACE_SPRINT_DURATION']
      },
      set: function (payload) {
        this.$store.dispatch('issues/INIT_SPRINT_DURATIONS', payload)
          .catch((e) => {
            console.log(e)
          })
      }
    },
    language: {
      get: function () {
        return 'English'
      },
      set: function (value) {
        console.log(value)
      }
    }
  },
  mounted () {
    this.$store.dispatch('issues/INIT_SPRINT_DURATIONS')
      .catch((e) => {
        console.log(e)
      })
  }
}
</script>
