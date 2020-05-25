import Vue from 'vue';
import VueRouter from 'vue-router';

Vue.use(VueRouter);

const routes = [
  {
    path: '/',
    name: 'home',
    component: () => import('../views/Home.vue'),
    meta: {
      title: 'Welcome screen | PmDragon',
    },
  },
  {
    path: '/login',
    name: 'login',
    component: () => import('../views/SignIn.vue'),
    meta: {
      title: 'Sign In | PmDragon',
    },
  },
  {
    path: '/about',
    name: 'about',
    component: () => import('../views/About.vue'),
    meta: {
      title: 'About | PmDragon',
    },
  },
  {
    path: '/news',
    name: 'news',
    component: () => import('../views/News.vue'),
    meta: {
      title: 'What\'s new | PmDragon',
    },
  },
  {
    path: '/verify',
    name: 'verify',
    component: () => import('../views/Verify.vue'),
    meta: {
      title: 'Verify registration | PmDragon',
    },
  },
];

const router = new VueRouter({
  mode: 'history',
  routes,
});

export default router;
