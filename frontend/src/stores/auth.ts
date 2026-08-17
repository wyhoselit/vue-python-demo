import { defineStore } from 'pinia'
import * as authService from '@/modules/user/services/auth'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    isAuthenticated: false,
    user: null as any | null,
    loading: false,
    error: null as string | null,
    errorCode: null as string | null,
  }),
  actions: {
    async login(credentials: any) {
      this.loading = true
      try {
        await authService.login(credentials)
        this.user = await authService.getCurrentUser()
        this.isAuthenticated = true
        this.error = null
      } catch (error: any) {
        this.error = error.detail
        this.errorCode = error.error_code
        throw error
      } finally {
        this.loading = false
      }
    },
    async register(credentials: any) {
      this.loading = true
      try {
        await authService.register(credentials)
        this.error = null
      } catch (error: any) {
        this.error = error.detail
        this.errorCode = error.error_code
        throw error
      } finally {
        this.loading = false
      }
    },
    async logout() {
      await authService.logout()
      this.isAuthenticated = false
      this.user = null
    },
    async fetchCurrentUser() {
      try {
        this.user = await authService.getCurrentUser()
        this.isAuthenticated = true
      } catch (error) {
        this.user = null
        this.isAuthenticated = false
      }
    }
  }
})