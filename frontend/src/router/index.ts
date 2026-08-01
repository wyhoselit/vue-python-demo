import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const routes = [
  {
    path: '/',
    name: 'Dashboard',
    component: () => import('@/modules/dashboard/views/Dashboard.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/modules/user/views/LoginForm.vue'),
    meta: { layout: 'auth' }
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('@/modules/user/views/RegistrationForm.vue'),
    meta: { layout: 'auth' }
  },
  {
    path: '/admin',
    name: 'AdminStatus',
    component: () => import('@/modules/admin/views/AdminStatus.vue'),
    meta: { requiresAuth: true, requiresAdmin: true }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()
  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    next('/login')
  } else if (to.meta.requiresAdmin && (!authStore.user || !authStore.user.roles.includes('admin'))) {
    next('/')
  } else {
    next()
  }
})

export default router

