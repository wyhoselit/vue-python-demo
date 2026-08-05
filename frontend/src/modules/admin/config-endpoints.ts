import api from '@/shared/api'

export const getSystemConfig = async (key: string) => {
  const response = await api.get(`/api/v1/system/config/${key}`)
  return response.data
}

export const updateSystemConfig = async (key: string, value: any) => {
  const response = await api.put(`/api/v1/system/config/${key}`, { value })
  return response.data
}

export const getAllConfig = async () => {
  const response = await api.get('/api/v1/system/config/')
  return response.data
}