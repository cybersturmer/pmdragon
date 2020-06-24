<template>
  <q-page class="flex q-layout-padding">
    <div class="full-width">
      <q-card
        dark
        square>
        <q-tabs
          class="bg-grey-9"
          v-model="tab"
          dense
          align="justify"
          narrow-indicator
        >
          <q-tab name="interface" icon="fact_check" label="Interface"/>
          <q-tab name="issue_types" icon="view_agenda" label="Issue Types" />
          <q-tab name="issue_states" icon="view_column" label="Issue States" />
          <q-tab name="server" icon="sync" label="Server" />
        </q-tabs>
        <q-separator />
        <q-tab-panels class="bg-grey-8" v-model="tab" animated>
          <q-tab-panel name="interface">
            <q-select
              dark
              filled
              dense
              square
              options-dense
              v-model="interface_theme"
              :options="interface_data.interface_options"
            />
            <q-separator/>
            <q-select
              dark
              dense
              square
              options-dense
              v-model="language"
              filled
              :options="interface_data.language_options"
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

          <q-tab-panel name="server">
            <q-input
              v-model="server_form_data.server"
              dark
              square
              dense
              filled
              placeholder="Server for connection"
              />
            <q-separator/>
            <q-input
              v-model="server_form_data.port"
              dark
              square
              dense
              filled
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
      interface_data: {
        interface_options: [
          {
            label: 'Dark interface',
            value: 'dark-interface'
          },
          {
            label: 'Light interface',
            value: 'light-interface'
          }
        ],
        language_options: [
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
      server_form_data: {
        server: 'localhost',
        port: 8080
      }
    }
  },
  computed: {
    interface_theme: {
      get: function () {
        return this.$store.getters['current/INTERFACE_THEME']
      },
      set: function (payload) {
        this.$store.dispatch('current/SELECT_INTERFACE_THEME', payload)
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
  }
}
</script>
