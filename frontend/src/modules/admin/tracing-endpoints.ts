import api from '@/shared/api'

export const updateTracingConfig = async (enabled: boolean) => {
  const response = await api.put('/api/v1/system/config/tracing.admin', { enabled })
  return response.data
}

export const getTracingConfig = async () => {
  const response = await api.get('/api/v1/system/config/tracing.admin')
  return response.data
}