import { describe, it, expect, vi } from 'vitest'
import { mount } from '@vue/test-utils'
import SystemInfo from '@/modules/admin/views/SystemInfo.vue'
import api from '@/shared/api'

vi.mock('@/shared/api', () => ({
  default: { get: vi.fn() }
}))

describe('SystemInfo.vue', () => {
  it('loads and displays system info', async () => {
    vi.mocked(api.get).mockResolvedValue({ 
      data: { version: '1.0.0', os: 'Linux', database: 'PostgreSQL' } 
    })
    
    const wrapper = mount(SystemInfo)
    await new Promise(resolve => setTimeout(resolve, 0))
    
    expect(wrapper.text()).toContain('Version: 1.0.0')
    expect(wrapper.text()).toContain('OS: Linux')
    expect(wrapper.text()).toContain('Database: PostgreSQL')
  })
})