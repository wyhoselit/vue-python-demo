import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import * as authService from '@/modules/user/services/auth'

export interface User {
  id: number
  email: string
  roles: string[]
}

export const useAuthStore = defineStore('auth', () => {
  const user = ref<User | null>(null)
  const loading = ref(false)
  const error = ref<string | null>(null)
  const errorCode = ref<string | null>(null)
  
  const isAuthenticated = computed(() => !!user.value)

  const login = async (credentials: authService.LoginCredentials) => {
    loading.value = true
    error.value = null
    errorCode.value = null
    try {
      await authService.login(credentials)
      user.value = await authService.getCurrentUser()
      // Redirect to chat page after successful login
      return '/chat'
    } catch (e: any) {
      console.error('Auth error:', e)
      error.value = e.detail || 'Login failed'
      errorCode.value = e.error_code || 'LOGIN_FAILED'
      throw e
    } finally {
      loading.value = false
    }
  }

  const register = async (credentials: authService.RegisterCredentials) => {
    loading.value = true
    error.value = null
    errorCode.value = null
    try {
      await authService.register(credentials)
    } catch (e: any) {
      error.value = e.detail || 'Registration failed'
      errorCode.value = e.error_code || 'REGISTRATION_FAILED'
      throw e
    } finally {
      loading.value = false
    }
  }

  const logout = async () => {
    try {
      await authService.logout()
    } finally {
      user.value = null
    }
  }

  const fetchCurrentUser = async () => {
    try {
      user.value = await authService.getCurrentUser()
    } catch (e) {
      user.value = null
    }
  }

  return {
    user,
    loading,
    error,
    errorCode,
    isAuthenticated,
    login,
    register,
    logout,
    fetchCurrentUser
  }
})