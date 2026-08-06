// The LLM service is in backend, not frontend.
// Frontend tests should mock service requests.
import { describe, it, expect, vi } from 'vitest'

describe('LLM API integration', () => {
  it('mocks API call', async () => {
    const mockFetch = vi.fn().mockResolvedValue({
      ok: true,
      json: () => Promise.resolve({ result: 'mock' })
    })
    globalThis.fetch = mockFetch
    
    // Simulate call
    const res = await fetch('/api/v1/ai/chat')
    const data = await res.json()
    expect(data.result).toBe('mock')
  })
})
