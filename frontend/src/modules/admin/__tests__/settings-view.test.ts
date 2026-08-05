import { describe, it, expect, vi, beforeEach } from 'vitest'
import { mount } from '@vue/test-utils'
import SettingsView from '@/modules/admin/views/SettingsView.vue'
import api from '@/shared/api'

vi.mock('@/shared/api', () => ({
  default: {
    get: vi.fn(),
    put: vi.fn(),
  }
}))

describe('SettingsView.vue', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it('loads all settings dynamically', async () => {
    vi.mocked(api.get).mockResolvedValue({
      data: {
        'system.tracing': { type: 'boolean', value: true },
        'system.logfile_path': { type: 'string', value: '/var/log/app.log' },
        'system.new_setting': { type: 'string', value: 'test_value' }
      }
    })

    const wrapper = mount(SettingsView)
    await new Promise(resolve => setTimeout(resolve, 0))

    expect(wrapper.text()).toContain('system.tracing')
    expect(wrapper.text()).toContain('system.logfile_path')
    expect(wrapper.text()).toContain('system.new_setting')
    expect(wrapper.find('input[type="checkbox"]').exists()).toBe(true)
    expect(wrapper.find('input[type="text"]').exists()).toBe(true)
    expect(wrapper.find('input[type="number"]').exists()).toBe(false)
  })

  it('renders checkbox for boolean settings', async () => {
    vi.mocked(api.get).mockResolvedValue({
      data: { 'system.tracing': { type: 'boolean', value: true } }
    })

    const wrapper = mount(SettingsView)
    await new Promise(resolve => setTimeout(resolve, 0))

    const checkbox = wrapper.find('input[type="checkbox"]')
    expect(checkbox.exists()).toBe(true)
    expect((checkbox.element as HTMLInputElement).checked).toBe(true)
  })

  it('renders text input for string settings', async () => {
    vi.mocked(api.get).mockResolvedValue({
      data: { 'system.logfile_path': { type: 'string', value: '/var/log/app.log' } }
    })

    const wrapper = mount(SettingsView)
    await new Promise(resolve => setTimeout(resolve, 0))

    const input = wrapper.find('input[type="text"]')
    expect(input.exists()).toBe(true)
    expect((input.element as HTMLInputElement).value).toBe('/var/log/app.log')
  })

  it('renders number input for numeric settings', async () => {
    vi.mocked(api.get).mockResolvedValue({
      data: { 'system.port': { type: 'number', value: 8080 } }
    })

    const wrapper = mount(SettingsView)
    await new Promise(resolve => setTimeout(resolve, 0))

    const input = wrapper.find('input[type="number"]')
    expect(input.exists()).toBe(true)
    expect(Number((input.element as HTMLInputElement).value)).toBe(8080)
  })

  it('renders textarea for object settings', async () => {
    vi.mocked(api.get).mockResolvedValue({
      data: { 'system.complex': { type: 'object', value: { nested: { value: 'test' } } } }
    })

    const wrapper = mount(SettingsView)
    await new Promise(resolve => setTimeout(resolve, 0))

    const textarea = wrapper.find('textarea')
    expect(textarea.exists()).toBe(true)
    expect((textarea.element as HTMLTextAreaElement).value).toContain('nested')
  })

  it('updates setting on input change', async () => {
    vi.mocked(api.get).mockResolvedValue({
      data: { 'system.logfile_path': { type: 'string', value: '/var/log/app.log' } }
    })
    vi.mocked(api.put).mockResolvedValue({ data: { path: '/tmp/new.log' } })

    const wrapper = mount(SettingsView)
    await new Promise(resolve => setTimeout(resolve, 0))

    const input = wrapper.find('input[type="text"]')
    await input.setValue('/tmp/new.log')

    expect(api.put).toHaveBeenCalledWith(
      '/api/v1/system/config/system.logfile_path',
      { value: '/tmp/new.log' }
    )
  })

  it('shows loading state initially', () => {
    vi.mocked(api.get).mockImplementation(() => new Promise(() => {}))

    const wrapper = mount(SettingsView)
    expect(wrapper.text()).toContain('Loading...')
  })

  it('shows error state on load failure', async () => {
    vi.mocked(api.get).mockRejectedValue(new Error('Network error'))

    const wrapper = mount(SettingsView)
    await new Promise(resolve => setTimeout(resolve, 0))

    expect(wrapper.text()).toContain('Failed to load configuration')
  })

  it('shows error state on update failure', async () => {
    vi.mocked(api.get).mockResolvedValue({
      data: { 'system.logfile_path': { type: 'string', value: '/var/log/app.log' } }
    })
    vi.mocked(api.put).mockRejectedValue(new Error('Update failed'))

    const wrapper = mount(SettingsView)
    await new Promise(resolve => setTimeout(resolve, 0))

    const input = wrapper.find('input[type="text"]')
    await input.setValue('/tmp/new.log')
    await new Promise(resolve => setTimeout(resolve, 0))

    expect(wrapper.text()).toContain('Failed to update system.logfile_path')
  })
})