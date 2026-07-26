import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import * as authService from '../services/auth'

export interface User {
  id: number
  email: string
}

export const useAuthStore = defineStore('auth', () => {
  const user = ref<User | null>(null)
  const loading = ref(false)
  const error = ref<string | null>(null)
  
  const isAuthenticated = computed(() => !!user.value)

  const login = async (credentials: authService.LoginCredentials) => {
    loading.value = true
    error.value = null
    try {
      await authService.login(credentials)
      user.value = await authService.getCurrentUser()
    } catch (e: any) {
      error.value = e.response?.data?.detail || 'Login failed'
      throw e
    } finally {
      loading.value = false
    }
  }

  const register = async (credentials: authService.RegisterCredentials) => {
    loading.value = true
    error.value = null
    try {
      await authService.register(credentials)
    } catch (e: any) {
      error.value = e.response?.data?.detail || 'Registration failed'
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
    isAuthenticated,
    login,
    register,
    logout,
    fetchCurrentUser
  }
})
