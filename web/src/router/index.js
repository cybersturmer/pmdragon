import Vue from 'vue';
import VueRouter from 'vue-router';
import Home from '../views/Home.vue';

Vue.use(VueRouter);

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home,
    meta: {
      title: 'PmDragon | Welcome screen',
    },
  },
  {
    path: '/auth',
    name: 'Sign In',
    component: () => import('../views/SignIn.vue'),
    meta: {
      title: 'PmDragon | Sign in',
    },
  },
  {
    path: '/about',
    name: 'About',
    component: () => import('../views/About.vue'),
    meta: {
      title: 'PmDragon | About',
    },
  },
  {
    path: '/news',
    name: 'What\'s new',
    component: () => import('../views/News'),
    meta: {
      title: 'PmDragon | What\'s new',
    },
  },
];

const router = new VueRouter({
  routes,
  mode: 'history',
});

export default router;
