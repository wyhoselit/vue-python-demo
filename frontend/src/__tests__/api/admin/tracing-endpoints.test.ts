import { describe, it, expect, beforeEach, vi } from 'vitest'
import * as tracingEndpoints from '@/services/admin/tracing-endpoints'
import api from '@/services/api'

vi.mock('@/services/api', () => ({
  default: {
    get: vi.fn(),
    post: vi.fn(),
    put: vi.fn(),
    delete: vi.fn(),
  }
}))

describe('Admin Endpoints - Tracing', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it('getTracingConfig calls correct endpoint', async () => {
    vi.mocked(api.get).mockResolvedValue({ data: { enabled: true } })

    const result = await tracingEndpoints.getTracingConfig()

    expect(api.get).toHaveBeenCalledWith('/api/v1/admin/tracing/config')
    expect(result).toEqual({ enabled: true })
  })

  it('updateTracingConfig set false calls correct endpoint', async () => {
    vi.mocked(api.put).mockResolvedValue({ data: { enabled: false } })

    const result = await tracingEndpoints.updateTracingConfig(false)

    expect(api.put).toHaveBeenCalledWith('/api/v1/admin/tracing/config', { enabled: false })
    expect(result).toEqual({ enabled: false })
  })

  it('updateTracingConfig set true calls correct endpoint', async () => {
    vi.mocked(api.put).mockResolvedValue({ data: { enabled: true } })

    const result = await tracingEndpoints.updateTracingConfig(true)

    expect(api.put).toHaveBeenCalledWith('/api/v1/admin/tracing/config', { enabled: true })
    expect(result).toEqual({ enabled: true })
  })
})