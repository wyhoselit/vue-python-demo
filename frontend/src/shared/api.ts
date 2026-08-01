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

api.interceptors.request.use((config) => {
  config.metadata = { startTime: new Date() }
  return config
})

api.interceptors.response.use(
  (response) => {
    const duration = new Date().getTime() - response.config.metadata.startTime.getTime()
    console.log(`Request to ${response.config.url} took ${duration}ms`)
    return response
  },
  (error) => {
    if (error.config && error.config.metadata) {
      const duration = new Date().getTime() - error.config.metadata.startTime.getTime()
      console.error(`Request to ${error.config.url} failed after ${duration}ms`)
    }
    return Promise.reject(error)
  }
)

export default api