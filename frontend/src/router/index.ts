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
    redirect: '/admin/info',
    meta: { requiresAuth: true, requiresAdmin: true }
  },
  {
    path: '/admin',
    component: () => import('@/modules/admin/views/AdminLayout.vue'),
    meta: { requiresAuth: true, requiresAdmin: true },
    children: [
      {
        path: 'info',
        name: 'AdminInfo',
        component: () => import('@/modules/admin/views/SystemInfo.vue')
      },
      {
        path: 'logs',
        name: 'AdminLogs',
        component: () => import('@/modules/admin/views/LogsView.vue')
      },
      {
        path: 'settings',
        name: 'AdminSettings',
        component: () => import('@/modules/admin/views/SettingsView.vue')
      }
    ]
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