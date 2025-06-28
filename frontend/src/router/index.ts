import { createRouter, createWebHistory } from 'vue-router'
import type { RouteRecordRaw } from 'vue-router'
import { useAuthStore } from '../stores/AuthStore';

// Middleware, which checks if the user has the required role
function requireAuthentication() {
  return () => {
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
    component: () => import('../views/Auth/Login.vue'),
    meta: { hideTabBar: true }
  },
  {
    path: '/signup',
    name: 'signup',
    component: () => import('../views/Auth/Signup_initial.vue'),
    meta: { hideTabBar: true }
  },
  {
    path: '/signup/address',
    name: 'signup_address',
    component: () => import('../views/Auth/Signup_1_Address.vue'),
    // beforeEnter: requireAuthentication(),
    meta: { hideTabBar: true }
  },
  {
    path: '/signup/car',
    name: 'signup_car',
    component: () => import('../views/Auth/Signup_1_Address.vue'),
    // beforeEnter: requireAuthentication(),
    meta: { hideTabBar: true }
  },
  {
    path: '/signup/license',
    name: 'signup_license',
    component: () => import('../views/Auth/Signup_1_Address.vue'),
    // beforeEnter: requireAuthentication(),
    meta: { hideTabBar: true }
  },

  // Home 
  {
    path: '/home',
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
    component: import('../views/Misc/404.vue'),
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