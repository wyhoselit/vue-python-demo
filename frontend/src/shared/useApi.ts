import axios, { type AxiosInstance, type AxiosResponse } from 'axios'
import { recordApiCall } from '@/modules/core/metrics/metrics';

let apiInstance: AxiosInstance | null = null

const getApiInstance = (): AxiosInstance => {
  if (!apiInstance) {
    apiInstance = axios.create({
      baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api/v1',
      timeout: 10000,
      withCredentials: true,
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
  const baseURL = api.defaults.baseURL || ''
  
  const wrapCall = <T>(method: string, url: string, promise: Promise<T>) => {
    const startTime = performance.now()
    return promise
      .then((data) => {
        const duration = performance.now() - startTime
        recordApiCall(method, baseURL + url, 200, duration)
        return data
      })
      .catch((error) => {
        const duration = performance.now() - startTime
        const statusCode = error.response?.status || 0
        recordApiCall(method, baseURL + url, statusCode, duration)
        throw error
      })
  }

  return {
    get: <T>(url: string) => wrapCall('GET', url, api.get<T>(url).then((res) => res.data)),
    post: <T>(url: string, data: unknown) =>
      wrapCall('POST', url, api.post<T>(url, data).then((res) => res.data)),
    put: <T>(url: string, data: unknown) =>
      wrapCall('PUT', url, api.put<T>(url, data).then((res) => res.data)),
    delete: <T>(url: string) =>
      wrapCall('DELETE', url, api.delete<T>(url).then((res) => res.data)),
  }
}

export default getApiInstance