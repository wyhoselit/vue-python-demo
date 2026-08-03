import { describe, it, expect, vi } from 'vitest'
import { mount } from '@vue/test-utils'
import LogsView from '@/modules/admin/views/LogsView.vue'
import api from '@/shared/api'

vi.mock('@/shared/api', () => ({
  default: { get: vi.fn() }
}))

describe('LogsView.vue', () => {
  it('loads and displays logs', async () => {
    vi.mocked(api.get).mockResolvedValue({ 
      data: { logs: '2026-08-03 10:00:00 INFO System started' } 
    })
    
    const wrapper = mount(LogsView)
    await new Promise(resolve => setTimeout(resolve, 0))
    
    expect(wrapper.text()).toContain('2026-08-03 10:00:00 INFO System started')
  })
})