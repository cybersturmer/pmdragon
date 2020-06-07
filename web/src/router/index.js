import Vue from 'vue';
import VueRouter from 'vue-router';

Vue.use(VueRouter);

const routes = [
  {
    path: '/',
    name: 'home',
    component: () => import('@/views/index/HomeView.vue'),
    meta: {
      title: 'Welcome screen | PmDragon',
      require_auth: false,
    },
  },
  {
    path: '/login',
    name: 'login',
    component: () => import('@/views/index/LoginView.vue'),
    meta: {
      title: 'Sign In | PmDragon',
      require_auth: false,
    },
  },
  {
    path: '/about',
    name: 'about',
    component: () => import('@/views/index/AboutView.vue'),
    meta: {
      title: 'About | PmDragon',
      require_auth: false,
    },
  },
  {
    path: '/news',
    name: 'news',
    component: () => import('@/views/index/NewsView.vue'),
    meta: {
      title: 'What\'s new | PmDragon',
      require_auth: false,
    },
  },
  {
    path: '/verify',
    name: 'verify',
    component: () => import('@/views/index/VerifyView.vue'),
    meta: {
      title: 'Verify registration | PmDragon',
      require_auth: false,
    },
  },
  {
    path: '/dash/backlog',
    name: 'backlog',
    component: () => import('@/views/dashboard/BacklogView.vue'),
    meta: {
      title: 'Backlog | PmDragon',
      require_auth: true,
    },
  },
  {
    path: '/dash/boards',
    name: 'boards',
    component: () => import('@/views/dashboard/BoardsView.vue'),
    meta: {
      title: 'Boards | PmDragon',
      require_auth: true,
    },
  },
];

const router = new VueRouter({
  mode: 'history',
  routes,
});

export default router;
