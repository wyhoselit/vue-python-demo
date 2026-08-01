import { describe, it, expect, beforeEach, vi } from 'vitest'
import * as adminEndpoints from '@/modules/admin/admin-endpoints'
import api from '@/shared/api'

vi.mock('@/shared/api', () => ({
  default: {
    get: vi.fn(),
    post: vi.fn(),
    put: vi.fn(),
    delete: vi.fn(),
  }
}))

describe('Admin Endpoints - Status', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it('getAdminStatus calls correct endpoint', async () => {
    vi.mocked(api.get).mockResolvedValue({ data: { status: 'ok' } })

    const result = await adminEndpoints.getAdminStatus()

    expect(api.get).toHaveBeenCalledWith('/api/v1/admin/status')
    expect(result).toEqual({ status: 'ok' })
  })
})