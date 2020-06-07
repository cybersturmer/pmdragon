import Vue from 'vue';
import VueRouter from 'vue-router';

Vue.use(VueRouter);

const routes = [
  {
    path: '/',
    name: 'home',
    component: () => import('@/views/index/Home.vue'),
    meta: {
      title: 'Welcome screen | PmDragon',
      require_auth: false,
    },
  },
  {
    path: '/login',
    name: 'login',
    component: () => import('@/views/index/SignIn.vue'),
    meta: {
      title: 'Sign In | PmDragon',
      require_auth: false,
    },
  },
  {
    path: '/about',
    name: 'about',
    component: () => import('@/views/index/About.vue'),
    meta: {
      title: 'About | PmDragon',
      require_auth: false,
    },
  },
  {
    path: '/news',
    name: 'news',
    component: () => import('@/views/index/News.vue'),
    meta: {
      title: 'What\'s new | PmDragon',
      require_auth: false,
    },
  },
  {
    path: '/verify',
    name: 'verify',
    component: () => import('@/views/index/Verify.vue'),
    meta: {
      title: 'Verify registration | PmDragon',
      require_auth: false,
    },
  },
  {
    path: '/dash/backlog',
    name: 'backlog',
    component: () => import('@/views/dashboard/Backlog.vue'),
    meta: {
      title: 'Backlog | PmDragon',
      require_auth: true,
    },
  },
  {
    path: '/dash/board',
    name: 'board',
    component: () => import('@/views/dashboard/Board.vue'),
    meta: {
      title: 'Board | PmDragon',
      require_auth: true,
    },
  },
];

const router = new VueRouter({
  mode: 'history',
  routes,
});

export default router;
