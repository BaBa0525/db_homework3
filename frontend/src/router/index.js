import { createRouter, createWebHistory } from 'vue-router';
import IndexView from '../view/IndexView';

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      name: 'index',
      path: '/index',
      component: IndexView,
    },
    {
      name: 'home',
      path: '/home',
      component: () => import('../views/HomeView'),
    }
  ]
})

export default router
