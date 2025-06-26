import { createRouter, createWebHistory } from 'vue-router'
import type { RouteRecordRaw, RouteLocationNormalized } from 'vue-router'
import { useAuthStore } from '../stores/AuthStore';

// Middleware, which checks if the user has the required role
function requireAuthentication() {
  return (_to: RouteLocationNormalized, _from: RouteLocationNormalized) => {
    const authStore = useAuthStore();
    const isAuthenticated = authStore.userAuthenticated;

    console.log("accessToken: " + authStore.accessToken)
    console.log("User authenticated: " + isAuthenticated)

    if (isAuthenticated) {
      return true;
    } else {
      return { name: "login" };
    }
  };
}

const routes: RouteRecordRaw[] = [
  // Authentication
  {
    path: '/login',
    name: 'login',
    component: () => import('../views/Login.vue'),
    meta: { hideTabBar: true }
  },
  {
    path: '/signup',
    name: 'signup',
    component: () => import('../views/Signup.vue'),
    meta: { hideTabBar: true }
  },

  // Home 
  {
    path: '/',
    name: 'home',
    component: () => import('../views/Home.vue'),
    beforeEnter: requireAuthentication(),
  },
  {
    path: '/example',
    name: 'example',
    component: () => import('../views/Example.vue'),
    beforeEnter: requireAuthentication(),
  },
  {
    path: '/styles',
    name: 'styles',
    component: () => import('../views/Styles.vue'),
    beforeEnter: requireAuthentication(),
  },
  
  // Error stuff
  {
    path: "/:pathMatch(.*)*",
    name: "notFound",
    component: import('../views/404.vue'),
    meta: {
      title: "404 - Not Found",
      hideTabBar: true
    },
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router 