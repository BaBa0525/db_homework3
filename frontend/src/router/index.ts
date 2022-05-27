import { createRouter, createWebHistory } from "vue-router";
import LoginView from "@/views/LoginView.vue";
import SignInPage from "@/components/SignInPage.vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      name: "login",
      path: "/login",
      component: LoginView,
      children: [
        {
          name: "signin",
          path: "/signin",
          component: SignInPage,
        },
        {
          name: "signup",
          path: "/signup",
          component: () => import("@/components/SignUpPage.vue"),
        },
      ],
    },
    {
      name: "home",
      path: "/home",
      component: () => import("@/views/HomeView.vue"),
    },
  ],
});

export default router;
