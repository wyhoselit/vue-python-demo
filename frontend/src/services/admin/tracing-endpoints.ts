import api from '../api'

export const updateTracingConfig = async (enabled: boolean) => {
  const response = await api.put('/api/v1/admin/tracing/config', { enabled })
  return response.data
}

export const getTracingConfig = async () => {
  const response = await api.get('/api/v1/admin/tracing/config')
  return response.data
}