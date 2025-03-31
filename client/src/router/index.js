import { createRouter, createWebHistory } from 'vue-router'
import LoginPass from '../views/LoginPass.vue';
import MainVue from '@/views/MainVue.vue';
import Users from '@/views/Users.vue';

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "MainVue",
      component: MainVue
    },
    {
      path: "/login",
      name: "LoginPass",
      component: LoginPass
    },
    {
      path: "/users",
      name: "Users",
      component: Users
    },
  ],
})

export default router
