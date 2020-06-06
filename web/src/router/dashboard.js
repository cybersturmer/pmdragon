import Vue from 'vue';
import VueRouter from 'vue-router';

Vue.use(VueRouter);

const routes = [
  {
    path: '/backlog',
    name: 'backlog',
    component: () => import('@/views/dashboard/Backlog.vue'),
    meta: {
      title: 'Backlog | PmDragon',
      require_auth: true,
    },
  },
  {
    path: '/board',
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
