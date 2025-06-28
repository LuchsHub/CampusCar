import { createRouter, createWebHistory } from 'vue-router'
import type { RouteRecordRaw } from 'vue-router'

import Login from '@/views/Auth/Login.vue';

import SignupInitial from '@/views/Auth/SignupInitial.vue';
import Signup_1_Address from '@/views/Auth/Signup_1_Address.vue';
import Signup_2_Car from '@/views/Auth/Signup_2_Car.vue';
import Signup_3_DriversLicense from '@/views/Auth/Signup_3_DriversLicense.vue';

import Home from '@/views/Home.vue';

import MyRides from '@/views/MyRides.vue';

import Profile from '@/views/Profile.vue';

import Example from '@/views/Example.vue';
import Styles from '@/views/Styles.vue';

import NotFound from '@/views/Misc/NotFound.vue';

// Middleware, which checks if the user has the required role
function requireAuthentication() {
  return async () => {
    // Import store inside the function to avoid Pinia initialization issues
    const { useAuthStore } = await import('../stores/AuthStore'); // dynamic import to prevent "no active pinia" error on application startup
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
  // Authentication
  {
    path: '/login',
    name: 'login',
    component: Login,
    meta: { hideTabBar: true }
  },
  {
    path: '/signup',
    name: 'signup',
    component: SignupInitial,
    meta: { hideTabBar: true }
  },
  {
    path: '/signup/address',
    name: 'signupAddress',
    component: Signup_1_Address,
    beforeEnter: requireAuthentication(),
    meta: { hideTabBar: true }
  },
  {
    path: '/signup/car',
    name: 'signupCar',
    component: Signup_2_Car,
    beforeEnter: requireAuthentication(),
    meta: { hideTabBar: true }
  },
  {
    path: '/signup/drivers_license',
    name: 'signupDriversLicense',
    component: Signup_3_DriversLicense,
    beforeEnter: requireAuthentication(),
    meta: { hideTabBar: true }
  },

  // Home 
  {
    path: '/home',
    name: 'home',
    component: Home,
    beforeEnter: requireAuthentication(),
  },
  
  // Meine Fahrten
  {
    path: '/my_rides',
    name: 'myRides',
    component: MyRides,
    beforeEnter: requireAuthentication(),
  },

  // Profil
  {
    path: '/profile',
    name: 'Profile',
    component: Profile,
    beforeEnter: requireAuthentication(),
  },

  // Example and styles
  {
    path: '/example',
    name: 'example',
    component: Example,
    beforeEnter: requireAuthentication(),
  },
  {
    path: '/styles',
    name: 'styles',
    component: Styles,
    beforeEnter: requireAuthentication(),
  },
  
  // Error stuff
  {
    path: "/:pathMatch(.*)*",
    name: "notFound",
    component: NotFound,
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