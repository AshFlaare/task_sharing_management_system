import { createRouter, createWebHistory } from 'vue-router'
import LoginPass from '../views/LoginPass.vue';
import MainVue from '@/views/MainVue.vue';
import Users from '@/views/Users.vue';
import CreateSheetAndTasks from '@/views/CreateSheetAndTasks.vue';
import Sheets from '@/views/Sheets.vue';
import Sheet from '@/views/Sheet.vue';
import SheetsArchive from '@/views/SheetsArchive.vue';
import SheetsExecutor from '@/views/SheetsExecutor.vue';


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
    {
      path: "/task-sheets/create",
      name: "CreateSheetAndTasks",
      component: CreateSheetAndTasks
    },
    {
      path: "/sheets/review",
      name: "Sheets",
      component: Sheets
    },
    {
      path: '/sheets/review/:id',
      name: 'SheetReview',
      component: Sheet
    },
    {
      path: '/sheets-archive/review',
      name: 'SheetsArchive',
      component: SheetsArchive
    },
    {
      path: '/my-sheets/review',
      name: 'SheetsExecutor',
      component: SheetsExecutor
    }
  ],
})

export default router
