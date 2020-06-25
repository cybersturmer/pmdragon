import { LocalStorage } from 'quasar'

export default function () {
  return {
    backlogs: LocalStorage.getItem('issues.backlogs') || [],
    sprint_durations: LocalStorage.getItem('issues.sprint_duration') || []
  }
}
