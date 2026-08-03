import { describe, it, expect, vi } from 'vitest'
import { mount } from '@vue/test-utils'
import SettingsView from '@/modules/admin/views/SettingsView.vue'
import api from '@/shared/api'

vi.mock('@/shared/api', () => ({
  default: { get: vi.fn() }
}))

describe('SettingsView.vue', () => {
  it('loads and displays settings', async () => {
    vi.mocked(api.get).mockResolvedValue({ 
      data: { enabled: true } 
    })
    
    const wrapper = mount(SettingsView)
    await new Promise(resolve => setTimeout(resolve, 0))
    
    expect(wrapper.text()).toContain('Enable Tracing')
    expect(wrapper.text()).toContain('Current status: Enabled')
  })
})