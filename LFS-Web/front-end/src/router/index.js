import { createRouter, createWebHistory } from 'vue-router'
import Home from '../pages/Home.vue'
import TimeManagement from '../pages/TimeManagement.vue'
import Schedule from '../pages/Schedule.vue'
import LearningPath from '../pages/LearningPath.vue'
import About from '../pages/About.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/time',
    name: 'TimeManagement',
    component: TimeManagement
  },
  {
    path: '/schedule',
    name: 'Schedule',
    component: Schedule
  },
  {
    path: '/learning',
    name: 'LearningPath',
    component: LearningPath
  },
  {
    path: '/about',
    name: 'About',
    component: About
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router 