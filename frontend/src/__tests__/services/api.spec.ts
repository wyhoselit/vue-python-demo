import { describe, it, expect, vi, beforeEach } from 'vitest'
import axios from 'axios'

vi.mock('axios')

describe('API Service', () => {
  beforeEach(() => {
    vi.clearAllMocks()
    vi.resetModules()
  })

  it('healthCheck returns status ok', async () => {
    const mockGet = vi.fn().mockResolvedValue({ data: { status: 'ok' } })
    ;(axios.create as unknown as { mockReturnValue: (val: { get: ReturnType<typeof vi.fn> }) => void }).mockReturnValue({ get: mockGet })

    const { healthCheck } = await import('../../services/api')
    const result = await healthCheck()
    expect(result).toEqual({ status: 'ok' })
    expect(mockGet).toHaveBeenCalledWith('/health')
  })

  it('getApiHealth returns status ok', async () => {
    const mockGet = vi.fn().mockResolvedValue({ data: { status: 'ok' } })
    ;(axios.create as unknown as { mockReturnValue: (val: { get: ReturnType<typeof vi.fn> }) => void }).mockReturnValue({ get: mockGet })

    const { getApiHealth } = await import('../../services/api')
    const result = await getApiHealth()
    expect(result).toEqual({ status: 'ok' })
    expect(mockGet).toHaveBeenCalledWith('/api/v1/health')
  })
})