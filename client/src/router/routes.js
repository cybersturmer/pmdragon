
const routes = [
  {
    path: '/',
    component: () => import('layouts/IndexLayout.vue'),
    children: [
      {
        name: 'register',
        path: '/',
        meta: {
          title: 'Register im PmDragon'
        },
        component: () => import('pages/index/Register.vue')
      },
      {
        name: 'login',
        path: '/login',
        meta: {
          title: 'Sign In in PmDragon'
        },
        component: () => import('pages/index/Login.vue')
      },
      {
        name: 'verify',
        path: '/verify',
        meta: {
          title: 'Verify your registration in PmDragon'
        },
        component: () => import('pages/index/Verify.vue')
      }
    ]
  },
  {
    path: '/dash',
    component: () => import('layouts/DashLayout.vue'),
    children: [
      {
        name: 'workspaces',
        path: 'workspaces',
        meta: {
          title: 'Choose Workspace'
        },
        component: () => import('pages/dash/Workspaces.vue')
      },
      {
        name: 'settings',
        path: 'settings',
        meta: {
          title: 'Settings'
        },
        component: () => import('pages/dash/Settings.vue')
      },
      {
        name: 'me',
        path: 'me',
        meta: {
          title: 'My Account'
        },
        component: () => import('pages/dash/Me.vue')
      },
      {
        name: 'backlog',
        path: 'backlog',
        meta: {
          title: 'Backlog'
        },
        component: () => import('pages/dash/Backlog.vue')
      },
      {
        name: 'board',
        path: 'board',
        meta: {
          title: 'Board'
        },
        component: () => import('pages/dash/Board.vue')
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
