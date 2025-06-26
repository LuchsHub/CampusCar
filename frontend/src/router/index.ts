import { createRouter, createWebHistory } from 'vue-router'
import type { RouteRecordRaw, RouteLocationNormalized } from 'vue-router'
import { useAuthStore } from '../stores/AuthStore';

// Middleware, which checks if the user has the required role
function requireAuthentication() {
  return (_to: RouteLocationNormalized, _from: RouteLocationNormalized) => {
    const authStore = useAuthStore();
    const isAuthenticated = authStore.userAuthenticated;

    if (isAuthenticated) {
      return true;
    } else {
      return { name: "login" };
    }
  };
}

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    name: 'home',
    component: () => import('../views/Home.vue'),
    beforeEnter: requireAuthentication(),
  },
  {
    path: '/login',
    name: 'login',
    component: () => import('../views/Login.vue'),
    meta: { hideTabBar: true }
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