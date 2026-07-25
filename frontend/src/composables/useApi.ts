import axios, { type AxiosInstance, type AxiosResponse } from 'axios'

let apiInstance: AxiosInstance | null = null

const getApiInstance = (): AxiosInstance => {
  if (!apiInstance) {
    apiInstance = axios.create({
      baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api/v1',
      timeout: 10000,
      headers: {
        'Content-Type': 'application/json',
      },
    })

    apiInstance.interceptors.response.use(
      (response: AxiosResponse) => response,
      (error) => {
        if (error.response?.status === 401) {
          console.error('Unauthorized access')
        }
        return Promise.reject(error)
      }
    )
  }
  return apiInstance
}

export const useApi = () => {
  const api = getApiInstance()
  return {
    get: <T>(url: string) => api.get<T>(url).then((res) => res.data),
    post: <T>(url: string, data: unknown) =>
      api.post<T>(url, data).then((res) => res.data),
    put: <T>(url: string, data: unknown) =>
      api.put<T>(url, data).then((res) => res.data),
    delete: <T>(url: string) => api.delete<T>(url).then((res) => res.data),
  }
}

export default getApiInstance