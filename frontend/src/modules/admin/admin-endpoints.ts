import api from '@/shared/api'

export const getSystemInfo = async () => {
  const response = await api.get('/api/v1/admin/system-info')
  return response.data
}

export const getLogs = async () => {
  const response = await api.get('/api/v1/admin/logs')
  return response.data
}

export const getSettings = async () => {
  const response = await api.get('/api/v1/admin/settings')
  return response.data
}

export const updateTracingConfig = async (enabled: boolean) => {
  const response = await api.put('/api/v1/admin/tracing/config', { enabled })
  return response.data
}

export const getTracingConfig = async () => {
  const response = await api.get('/api/v1/admin/tracing/config')
  return response.data
}
