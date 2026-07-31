import api from '../api'

export const getLogs = async () => {
  const response = await api.get('/api/v1/admin/logs')
  return response.data
}