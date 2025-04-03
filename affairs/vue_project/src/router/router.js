import { createRouter, createWebHistory } from 'vue-router'
import HomePage from '../pages/HomePage.vue'
import LoginPage from '../pages/LoginPage.vue'
import RegisterPage from '../pages/RegisterPage.vue'
import SettingsPage from '../pages/SettingsPage.vue'
import ConsolePage from '../pages/ConsolePage.vue'
import RoleConfigPage from '../pages/RoleConfigPage.vue'
import DeviceDetailPage from '../pages/DeviceDetailPage.vue'

const routes = [
  {
    path: '/',
    redirect: '/login'
  },
  {
    path: '/login',
    name: 'Login',
    component: LoginPage
  },
  {
    path: '/register',
    name: 'Register',
    component: RegisterPage
  },
  {
    path: '/home',
    name: 'Home',
    component: HomePage,
    meta: { requiresAuth: true }
  },
  {
    path: '/settings',
    name: 'Settings',
    component: SettingsPage,
    meta: { requiresAuth: true }
  },
  {
    path: '/console',
    name: 'Console',
    component: ConsolePage,
    meta: { requiresAuth: true }
  },
  {
    path: '/role-config/:deviceId',
    name: 'RoleConfig',
    component: RoleConfigPage,
    meta: { requiresAuth: true }
  },
  {
    path: '/device/:deviceId',
    name: 'DeviceDetail',
    component: DeviceDetailPage,
    meta: { requiresAuth: true }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 路由守卫
router.beforeEach((to, from, next) => {
  // 这里可以添加登录状态检查逻辑
  // const isAuthenticated = // 检查登录状态
  // if (to.meta.requiresAuth && !isAuthenticated) {
  //   next('/login')
  // } else {
  //   next()
  // }
  next()
})

export default router
