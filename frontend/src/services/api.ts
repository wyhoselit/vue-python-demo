import axios from 'axios'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000',
  withCredentials: true,
})

export const healthCheck = async () => {
  const response = await api.get('/health')
  return response.data
}

export const getApiHealth = async () => {
  const response = await api.get('/api/v1/health')
  return response.data
}

export default api