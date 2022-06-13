import { createRouter, createWebHistory } from 'vue-router';
import IndexView from '../views/IndexView.vue';

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      name: 'index',
      path: '/index',
      component: IndexView,
      children: [
        {
          name: 'signin',
          path: '/signin',
          component: () => import('../views/SigninView.vue'),
        },
        {
          name: 'signup',
          path: '/signup',
          component: () => import('../views/SignupView.vue'),
        }
      ]
    },
    {
      name: 'home',
      path: '/home',
      component: () => import('../views/HomeView.vue'),
      children: [
        {
          name: 'search',
          path: '/search',
          component: () => import('../views/SearchShopView.vue'),
        },
        {
          name: 'shop',
          path: '/shop',
          component: () => import('../views/ShopManageView.vue'),
        }
      ]
    }
  ]
})

export default router
