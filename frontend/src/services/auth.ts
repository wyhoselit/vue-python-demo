import api from './api'

export interface LoginCredentials {
  email: string
  password: string
}

export interface RegisterCredentials {
  email: string
  password: string
}

export interface User {
  id: number
  email: string
}

export interface AuthError {
  detail: string
  error_code: string
}

export const login = async (credentials: LoginCredentials): Promise<User> => {
  try {
    const response = await api.post('/api/v1/auth/login', credentials)
    return response.data
  } catch (error: any) {
    console.error('Service Login Error:', error)
    if (error.response && error.response.data) {
      throw error.response.data
    }
    throw { detail: 'Network error', error_code: 'NETWORK_ERROR' }
  }
}

export const register = async (credentials: RegisterCredentials): Promise<User> => {
  try {
    const response = await api.post('/api/v1/auth/register', credentials)
    return response.data
  } catch (error: any) {
    console.error('Service Register Error:', error)
    if (error.response && error.response.data) {
      throw error.response.data
    }
    throw { detail: 'Network error', error_code: 'NETWORK_ERROR' }
  }
}

export const logout = async (): Promise<void> => {
  await api.post('/api/v1/auth/logout')
}

export const getCurrentUser = async (): Promise<User> => {
  const response = await api.get('/api/v1/users/me')
  return response.data
}