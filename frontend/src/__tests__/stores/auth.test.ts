import { describe, it, expect, beforeEach, vi } from 'vitest'
import { createPinia, setActivePinia } from 'pinia'
import { useAuthStore } from '@/stores/auth'

import * as authService from '@/modules/user/services/auth'

vi.mock('@/modules/user/services/auth')

describe('Auth Store', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
    vi.clearAllMocks()
  })

  it('initializes with null user and no token', () => {
    const store = useAuthStore()
    expect(store.user).toBeNull()
    expect(store.loading).toBe(false)
    expect(store.error).toBeNull()
    expect(store.isAuthenticated).toBe(false)
  })

  it('sets user on successful login', async () => {
    const mockUser = { id: 1, email: 'test@example.com' }
    vi.mocked(authService.login).mockResolvedValueOnce(undefined)
    vi.mocked(authService.getCurrentUser).mockResolvedValueOnce(mockUser)

    const store = useAuthStore()
    await store.login({ email: 'test@example.com', password: 'password123' })

    expect(store.user).toEqual(mockUser)
    expect(store.loading).toBe(false)
    expect(store.error).toBeNull()
    expect(store.isAuthenticated).toBe(true)
  })

  it('sets error code on failed login', async () => {
    const errorResponse = { detail: 'Invalid credentials', error_code: 'INVALID_CREDENTIALS' }
    vi.mocked(authService.login).mockImplementationOnce(() => Promise.reject(errorResponse))

    const store = useAuthStore()
    await expect(store.login({ email: 'test@example.com', password: 'wrong' })).rejects.toThrow()

    expect(store.error).toBe('Invalid credentials')
    expect(store.errorCode).toBe('INVALID_CREDENTIALS')
    expect(store.loading).toBe(false)
  })

  it('sets error code on failed registration', async () => {
    const errorResponse = { detail: 'Email already registered', error_code: 'EMAIL_ALREADY_EXISTS' }
    vi.mocked(authService.register).mockImplementationOnce(() => Promise.reject(errorResponse))

    const store = useAuthStore()
    await expect(store.register({ email: 'existing@example.com', password: 'password123' })).rejects.toThrow()

    expect(store.error).toBe('Email already registered')
    expect(store.errorCode).toBe('EMAIL_ALREADY_EXISTS')
  })

  it('clears user on logout', async () => {
    vi.mocked(authService.logout).mockResolvedValueOnce()

    const store = useAuthStore()
    store.user = { id: 1, email: 'test@example.com' }
    await store.logout()

    expect(store.user).toBeNull()
    expect(store.isAuthenticated).toBe(false)
  })

  it('fetches current user', async () => {
    const mockUser = { id: 2, email: 'current@example.com' }
    vi.mocked(authService.getCurrentUser).mockResolvedValueOnce(mockUser)

    const store = useAuthStore()
    await store.fetchCurrentUser()

    expect(store.user).toEqual(mockUser)
  })

  it('clears user when fetch fails', async () => {
    vi.mocked(authService.getCurrentUser).mockRejectedValueOnce(new Error('Not authenticated'))

    const store = useAuthStore()
    store.user = { id: 1, email: 'test@example.com' }
    await store.fetchCurrentUser()

    expect(store.user).toBeNull()
  })
})