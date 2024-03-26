import { createRouter, createWebHistory } from 'vue-router'
import App from '@/App.vue'
import HomeView from '@/views/HomeView.vue'
import Register  from '@/views/Register.vue'
import Login from '@/views/Login.vue'
import RenderView from '@/views/HomeView.vue'
import testing from '@/views/testing.vue'
const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path:"/register",
      name: "register",
      component: Register
    },
    {
      path:"/login",
      name: "login",
      component: Login
    },
    {
      path: '/home',
      name: 'home',
      component: HomeView
    },
    {
      path: "/home/:uuid",
      name: "render",
      component: RenderView
    },
    {
      path: "/test",
      name: "test",
      component: testing
    }
  ]
})

export default router
