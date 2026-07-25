import { defineStore } from 'pinia'
import { ref } from 'vue'

export interface User {
  id: string
  email: string
  name: string
  roles: string[]
}

export const useAuthStore = defineStore('auth', () => {
  const user = ref<User | null>(null)
  const token = ref<string | null>(localStorage.getItem('auth_token'))
  const isAuthenticated = computed(() => !!token.value && !!user.value)

  const setAuth = (newToken: string, userData: User) => {
    token.value = newToken
    user.value = userData
    localStorage.setItem('auth_token', newToken)
  }

  const logout = () => {
    token.value = null
    user.value = null
    localStorage.removeItem('auth_token')
  }

  return {
    user,
    token,
    isAuthenticated,
    setAuth,
    logout,
  }
})

import { computed } from 'vue'