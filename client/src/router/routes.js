const PMDRAGON_STRING = '  |  PmDragon'

const routes = [
  {
    path: '/',
    component: () => import('layouts/IndexLayout.vue'),
    children: [
      {
        name: 'register',
        path: '/',
        meta: {
          title: 'Register' + PMDRAGON_STRING
        },
        component: () => import('pages/index/Register.vue')
      },
      {
        name: 'login',
        path: '/login',
        meta: {
          title: 'Sign In' + PMDRAGON_STRING
        },
        component: () => import('pages/index/Login.vue')
      },
      {
        name: 'verify-registration',
        path: '/verify/registration/:key',
        props: true,
        meta: {
          title: 'Verify your registration' + PMDRAGON_STRING
        },
        component: () => import('pages/index/VerifyRegistration.vue')
      },
      {
        name: 'verify-collaboration',
        path: '/verify/collaboration/:key',
        props: true,
        meta: {
          title: 'Verify your participation in the new workspace' +
            PMDRAGON_STRING
        },
        component: () => import('pages/index/VerifyCollaboration.vue')
      },
      {
        name: 'verify-invitation',
        path: '/verify/invitation/:key',
        props: true,
        meta: {
          title: 'Accept invitation to new workspace' + PMDRAGON_STRING
        },
        component: () => import('pages/index/VerifyInvitation.vue')
      },
      {
        name: 'loading',
        path: '/loading',
        meta: {
          title: 'Loading workspaces...' + PMDRAGON_STRING
        },
        component: () => import('pages/index/Loading.vue')
      }
    ]
  },
  {
    path: '/dash',
    component: () => import('layouts/DashLayout.vue'),
    children: [
      {
        name: 'kickstart',
        path: 'kickstart',
        meta: {
          title: 'Welcome' + PMDRAGON_STRING
        },
        component: () => import('pages/index/Kickstart.vue')
      },
      {
        name: 'workspaces',
        path: 'workspaces',
        meta: {
          title: 'Choose Workspace' + PMDRAGON_STRING
        },
        component: () => import('pages/dash/Workspaces.vue')
      },
      {
        name: 'settings',
        path: 'settings',
        meta: {
          title: 'Settings' + PMDRAGON_STRING
        },
        component: () => import('pages/dash/Settings.vue')
      },
      {
        name: 'me',
        path: 'me',
        meta: {
          title: 'My Account' + PMDRAGON_STRING
        },
        component: () => import('pages/dash/Me.vue')
      },
      {
        name: 'backlog',
        path: 'backlog',
        meta: {
          title: 'Backlog' + PMDRAGON_STRING
        },
        component: () => import('pages/dash/Backlog.vue')
      },
      {
        name: 'board',
        path: 'board',
        meta: {
          title: 'Board' + PMDRAGON_STRING
        },
        component: () => import('pages/dash/Board.vue')
      },
      {
        name: 'team',
        path: 'team',
        meta: {
          title: 'Team' + PMDRAGON_STRING
        },
        component: () => import('pages/dash/Team.vue')
      }
    ],
    meta: {
      requiredAuth: true
    }
  }
]

// Always leave this as last one
if (process.env.MODE !== 'ssr') {
  routes.push({
    path: '*',
    component: () => import('pages/Error404.vue')
  })
}

export default routes
