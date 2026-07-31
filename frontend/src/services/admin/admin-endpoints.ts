import api from '../api'

export const getAdminStatus = async () => {
  const response = await api.get('/api/v1/admin/status')
  return response.data
}