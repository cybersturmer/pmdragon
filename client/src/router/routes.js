
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
        path: '/verify/:key',
        props: true,
        meta: {
          title: 'Verify your registration in PmDragon'
        },
        component: () => import('pages/index/Verify.vue')
      },
      {
        name: 'loading',
        path: '/loading',
        meta: {
          title: 'Loading workspaces...'
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
          title: 'Welcome pmdragon...'
        },
        component: () => import('pages/index/Kickstart.vue')
      },
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
