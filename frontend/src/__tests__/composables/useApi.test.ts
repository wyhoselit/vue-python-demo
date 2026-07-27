import { describe, it, expect, beforeEach, vi } from 'vitest'
import { useApi } from '@/composables/useApi'
import axios from 'axios'

vi.mock('axios')

describe('useApi Composable', () => {
  const mockedAxios = vi.mocked(axios)

  beforeEach(() => {
    vi.clearAllMocks()
    vi.resetModules()
  })

  it('creates axios instance with correct config', () => {
    const mockInstance = {
      get: vi.fn(),
      post: vi.fn(),
      put: vi.fn(),
      delete: vi.fn(),
      interceptors: { response: { use: vi.fn() } },
    }
    mockedAxios.create.mockReturnValue(mockInstance)

    useApi()
    expect(mockedAxios.create).toHaveBeenCalledWith({
      baseURL: 'http://localhost:8000/api/v1',
      timeout: 10000,
      withCredentials: true,
      headers: { 'Content-Type': 'application/json' },
    })
  })

  it('get method returns data', async () => {
    const mockGet = vi.fn().mockResolvedValue({ data: { test: 'data' } })
    const mockInstance = {
      get: mockGet,
      post: vi.fn(),
      put: vi.fn(),
      delete: vi.fn(),
      interceptors: { response: { use: vi.fn() } },
    }
    mockedAxios.create.mockReturnValue(mockInstance)

    const { useApi } = await import('@/composables/useApi')
    const api = useApi()
    const result = await api.get('/test')
    expect(mockGet).toHaveBeenCalledWith('/test')
    expect(result).toEqual({ test: 'data' })
  })

  it('post method returns data', async () => {
    const mockPost = vi.fn().mockResolvedValue({ data: { id: 1 } })
    const mockInstance = {
      get: vi.fn(),
      post: mockPost,
      put: vi.fn(),
      delete: vi.fn(),
      interceptors: { response: { use: vi.fn() } },
    }
    mockedAxios.create.mockReturnValue(mockInstance)

    const { useApi } = await import('@/composables/useApi')
    const api = useApi()
    const result = await api.post('/test', { name: 'test' })
    expect(mockPost).toHaveBeenCalledWith('/test', { name: 'test' })
    expect(result).toEqual({ id: 1 })
  })
})