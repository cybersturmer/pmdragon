import { LocalStorage } from 'quasar'

export default function () {
  return {
    backlogs: LocalStorage.getItem('issues.backlogs') || []
  }
}
