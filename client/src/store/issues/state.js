import { LocalStorage } from 'quasar'

export default function () {
  return {
    backlogs: LocalStorage.getItem('issues.backlogs') || [],
    sprints: LocalStorage.getItem('issues.sprints') || [],
    issue_types: LocalStorage.getItem('issues.issue_types') || [],
    issue_states: LocalStorage.getItem('issues.issue_states') || [],
    sprint_durations: LocalStorage.getItem('issues.sprint_duration') || []
  }
}
