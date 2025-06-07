import { createRouter, createWebHistory } from 'vue-router'
import type { RouteRecordRaw } from 'vue-router'

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    name: 'home',
    component: () => import('../views/Home.vue')
  },
  {
    path: '/example',
    name: 'example',
    component: () => import('../views/Example.vue')
  },
  {
    path: '/styles',
    name: 'styles',
    component: () => import('../views/Styles.vue')
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router 