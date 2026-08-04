import { describe, it, expect, beforeEach, vi } from 'vitest'
import * as tracingEndpoints from '@/modules/admin/tracing-endpoints'
import * as configEndpoints from '@/modules/admin/config-endpoints'
import api from '@/shared/api'

vi.mock('@/shared/api', () => ({
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

    expect(api.get).toHaveBeenCalledWith('/api/v1/system/config/tracing.admin')
    expect(result).toEqual({ enabled: true })
  })

  it('updateTracingConfig set false calls correct endpoint', async () => {
    vi.mocked(api.put).mockResolvedValue({ data: { enabled: false } })

    const result = await tracingEndpoints.updateTracingConfig(false)

    expect(api.put).toHaveBeenCalledWith('/api/v1/system/config/tracing.admin', { enabled: false })
    expect(result).toEqual({ enabled: false })
  })

  it('updateTracingConfig set true calls correct endpoint', async () => {
    vi.mocked(api.put).mockResolvedValue({ data: { enabled: true } })

    const result = await tracingEndpoints.updateTracingConfig(true)

    expect(api.put).toHaveBeenCalledWith('/api/v1/system/config/tracing.admin', { enabled: true })
    expect(result).toEqual({ enabled: true })
  })
})

describe('Admin Endpoints - Config', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it('getSystemConfig calls correct endpoint', async () => {
    vi.mocked(api.get).mockResolvedValue({ data: { path: '/var/log/app.log' } })

    const result = await configEndpoints.getSystemConfig('system.logfile_path')

    expect(api.get).toHaveBeenCalledWith('/api/v1/system/config/system.logfile_path')
    expect(result).toEqual({ path: '/var/log/app.log' })
  })

  it('updateSystemConfig calls correct endpoint', async () => {
    vi.mocked(api.put).mockResolvedValue({ data: { path: '/tmp/new.log' } })

    const result = await configEndpoints.updateSystemConfig('system.logfile_path', { path: '/tmp/new.log' })

    expect(api.put).toHaveBeenCalledWith('/api/v1/system/config/system.logfile_path', { path: '/tmp/new.log' })
    expect(result).toEqual({ path: '/tmp/new.log' })
  })
})