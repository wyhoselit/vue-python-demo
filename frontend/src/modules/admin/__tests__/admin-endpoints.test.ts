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

  it('getSystemInfo calls correct endpoint', async () => {
    vi.mocked(api.get).mockResolvedValue({ 
      data: { version: '1.0.0', os: 'Linux', database: 'PostgreSQL' } 
    })

    const result = await adminEndpoints.getSystemInfo()

    expect(api.get).toHaveBeenCalledWith('/api/v1/admin/system-info')
    expect(result).toEqual({ version: '1.0.0', os: 'Linux', database: 'PostgreSQL' })
  })

  it('getLogs calls correct endpoint', async () => {
    vi.mocked(api.get).mockResolvedValue({ 
      data: { logs: '2026-08-03 10:00:00 INFO System started' } 
    })

    const result = await adminEndpoints.getLogs()

    expect(api.get).toHaveBeenCalledWith('/api/v1/admin/logs')
    expect(result).toEqual({ logs: '2026-08-03 10:00:00 INFO System started' })
  })

  it('getSettings calls correct endpoint', async () => {
    vi.mocked(api.get).mockResolvedValue({ 
      data: { emailSettings: true, notifications: false } 
    })

    const result = await adminEndpoints.getSettings()

    expect(api.get).toHaveBeenCalledWith('/api/v1/admin/settings')
    expect(result).toEqual({ emailSettings: true, notifications: false })
  })
})