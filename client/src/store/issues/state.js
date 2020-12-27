import { LocalStorage } from 'quasar'

export default function () {
  return {
    backlogs: LocalStorage.getItem('issues.backlogs') || [],
    sprints: LocalStorage.getItem('issues.sprints') || [],
    issues: LocalStorage.getItem('issues.issues') || [],
    issue_types: LocalStorage.getItem('issues.issue_types') || [],
    issue_states: LocalStorage.getItem('issues.issue_states') || [],
    issue_estimations: LocalStorage.getItem('issues.issue_estimations') || [],
    sprint_durations: LocalStorage.getItem('issues.sprint_duration') || []
  }
}
