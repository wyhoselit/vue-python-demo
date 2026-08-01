import { describe, it, expect, vi, beforeEach } from 'vitest'
import axios from 'axios'

vi.mock('axios', () => ({
  default: {
    create: vi.fn(() => ({
      get: vi.fn(),
      interceptors: {
        request: { use: vi.fn() },
        response: { use: vi.fn() }
      }
    }))
  }
}))

describe('API Service', () => {
  beforeEach(() => {
    vi.clearAllMocks()
    vi.resetModules()
  })

  it('healthCheck returns status ok', async () => {
    const mockGet = vi.fn().mockResolvedValue({ data: { status: 'ok' } })
    ;(axios.create as ReturnType<typeof vi.fn>).mockReturnValue({
      get: mockGet,
      interceptors: {
        request: { use: vi.fn() },
        response: { use: vi.fn() }
      }
    })

    const { healthCheck } = await import('@/shared/api')
    const result = await healthCheck()
    expect(result).toEqual({ status: 'ok' })
    expect(mockGet).toHaveBeenCalledWith('/health')
  })

  it('getApiHealth returns status ok', async () => {
    const mockGet = vi.fn().mockResolvedValue({ data: { status: 'ok' } })
    ;(axios.create as ReturnType<typeof vi.fn>).mockReturnValue({
      get: mockGet,
      interceptors: {
        request: { use: vi.fn() },
        response: { use: vi.fn() }
      }
    })

    const { getApiHealth } = await import('@/shared/api')
    const result = await getApiHealth()
    expect(result).toEqual({ status: 'ok' })
    expect(mockGet).toHaveBeenCalledWith('/api/v1/health')
  })
})
