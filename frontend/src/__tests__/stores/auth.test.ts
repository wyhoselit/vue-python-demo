import { describe, it, expect, beforeEach } from 'vitest'
import { createPinia, setActivePinia } from 'pinia'
import { useAuthStore } from '@/stores/auth'

describe('Auth Store', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
    localStorage.clear()
  })

  it('initializes with null user and no token', () => {
    const store = useAuthStore()
    expect(store.user).toBeNull()
    expect(store.token).toBeNull()
    expect(store.isAuthenticated).toBe(false)
  })

  it('sets auth correctly', () => {
    const store = useAuthStore()
    const user = {
      id: '1',
      email: 'test@example.com',
      name: 'Test User',
      roles: ['user'],
    }
    store.setAuth('test-token', user)
    expect(store.token).toBe('test-token')
    expect(store.user).toEqual(user)
    expect(store.isAuthenticated).toBe(true)
  })

  it('persists token to localStorage', () => {
    const store = useAuthStore()
    const user = {
      id: '1',
      email: 'test@example.com',
      name: 'Test User',
      roles: ['user'],
    }
    store.setAuth('test-token', user)
    expect(localStorage.getItem('auth_token')).toBe('test-token')
  })

  it('clears auth on logout', () => {
    const store = useAuthStore()
    store.setAuth('test-token', {
      id: '1',
      email: 'test@example.com',
      name: 'Test User',
      roles: ['user'],
    })
    store.logout()
    expect(store.token).toBeNull()
    expect(store.user).toBeNull()
    expect(store.isAuthenticated).toBe(false)
    expect(localStorage.getItem('auth_token')).toBeNull()
  })
})