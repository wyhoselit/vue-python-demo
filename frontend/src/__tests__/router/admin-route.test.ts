import { setActivePinia, createPinia } from 'pinia'
import { useAuthStore } from '@/stores/auth'
import router from '@/router'
import { createMemoryHistory, createRouter } from 'vue-router'

describe('Router Guard - Admin Route Protection', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
    router.push('/')
  })

  afterEach(() => {
    router.push('/')
  })

  it('redirects to login when not authenticated accessing admin route', async () => {
    const authStore = useAuthStore()
    authStore.user = null
    
    await router.push('/admin')
    
    expect(router.currentRoute.value.name).toBe('Login')
  })

  it('redirects to dashboard when authenticated but not admin', async () => {
    const authStore = useAuthStore()
    authStore.user = {
      id: 1,
      email: 'user@example.com',
      roles: ['user']
    }
    
    await router.push('/admin')
    
    expect(router.currentRoute.value.name).toBe('Dashboard')
  })

  it('allows admin user to access admin route', async () => {
    const authStore = useAuthStore()
    authStore.user = {
      id: 1,
      email: 'admin@example.com',
      roles: ['admin']
    }
    
    await router.push('/admin')
    
    expect(router.currentRoute.value.name).toBe('AdminStatus')
  })

  it('allows admin user with multiple roles to access admin route', async () => {
    const authStore = useAuthStore()
    authStore.user = {
      id: 1,
      email: 'admin@example.com',
      roles: ['user', 'admin', 'moderator']
    }
    
    await router.push('/admin')
    
    expect(router.currentRoute.value.name).toBe('AdminStatus')
  })
})