import { describe, it, expect, beforeEach, vi } from 'vitest'
import * as logsEndpoints from '@/modules/admin/logs-endpoints'
import api from '@/shared/api'

vi.mock('@/shared/api', () => ({
  default: {
    get: vi.fn(),
    post: vi.fn(),
    put: vi.fn(),
    delete: vi.fn(),
  }
}))

describe('Admin Endpoints - Logs', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it('getLogs calls correct endpoint', async () => {
    vi.mocked(api.get).mockResolvedValue({ data: { logs: ['log1', 'log2'] } })

    const result = await logsEndpoints.getLogs()

    expect(api.get).toHaveBeenCalledWith('/api/v1/admin/logs')
    expect(result).toEqual({ logs: ['log1', 'log2'] })
  })
})