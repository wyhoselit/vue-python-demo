import { describe, it, expect, beforeEach, vi } from 'vitest'
import { mount, flushPromises } from '@vue/test-utils'
import Dashboard from '@/views/Dashboard.vue'
import { createVuetify } from 'vuetify'
import { createPinia } from 'pinia'
import { useApi } from '@/composables/useApi'

vi.mock('@/composables/useApi')

const vuetify = createVuetify()

const vuetifyStubs = {
  'router-view': true,
  'router-link': true,
  'v-container': { template: '<div><slot /></div>' },
  'v-row': { template: '<div><slot /></div>' },
  'v-col': { template: '<div><slot /></div>' },
  'v-card': { template: '<div><slot /></div>' },
  'v-card-title': { template: '<div><slot /></div>' },
  'v-card-text': { template: '<div><slot /></div>' },
  'v-progress-linear': { template: '<div />' },
  'v-progress-circular': { template: '<div />' },
  'v-data-table': { template: '<div />' },
  'v-alert': { template: '<div><slot /></div>' },
  'v-btn': { template: '<button><slot /></button>' },
}

describe('Dashboard', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it('renders loading state initially', async () => {
    let resolveStats: (value: unknown) => void
    let resolveUsers: (value: unknown) => void

    const statsPromise = new Promise((resolve) => { resolveStats = resolve })
    const usersPromise = new Promise((resolve) => { resolveUsers = resolve })

    vi.mocked(useApi).mockReturnValue({
      get: vi.fn().mockImplementation((url: string) => {
        if (url === '/dashboard/stats') return statsPromise
        if (url === '/users') return usersPromise
        return Promise.resolve({})
      }),
    })

    const wrapper = mount(Dashboard, {
      global: { plugins: [vuetify, createPinia()], stubs: vuetifyStubs },
    })

    expect(wrapper.html()).toContain('載入儀表板資料中')

    resolveStats!({ total_users: 100, active_sessions: 10, api_calls_24h: 500 })
    resolveUsers!([{ id: 1, name: 'Test', email: 'test@example.com', status: 'active' }])
    await flushPromises()
  })

  it('renders success state with stats and users', async () => {
    const mockStats = { total_users: 1250, active_sessions: 42, api_calls_24h: 15420 }
    const mockUsers = [
      { id: 1, name: 'Alice Chen', email: 'alice@example.com', status: 'active' },
      { id: 2, name: 'Bob Smith', email: 'bob@example.com', status: 'active' },
    ]

    vi.mocked(useApi).mockReturnValue({
      get: vi.fn().mockImplementation((url: string) => {
        if (url === '/dashboard/stats') return Promise.resolve(mockStats)
        if (url === '/users') return Promise.resolve(mockUsers)
        return Promise.resolve({})
      }),
    })

    const wrapper = mount(Dashboard, {
      global: { plugins: [vuetify, createPinia()], stubs: vuetifyStubs },
    })

    // Wait for onMounted to complete and all promises to resolve
    await flushPromises()
    await new Promise(resolve => setTimeout(resolve, 50))

    // Check stats are rendered in HTML
    expect(wrapper.html()).toContain('1,250')
    expect(wrapper.html()).toContain('42')
    expect(wrapper.html()).toContain('15,420')
    // v-data-table is stubbed, so user names won't appear in HTML
    // but we can verify the component made the API calls
  })

  it('renders error state when API fails', async () => {
    vi.mocked(useApi).mockReturnValue({
      get: vi.fn().mockRejectedValue(new Error('Network Error')),
    })

    const wrapper = mount(Dashboard, {
      global: { plugins: [vuetify, createPinia()], stubs: vuetifyStubs },
    })

    await flushPromises()
    await wrapper.vm.$nextTick()

    expect(wrapper.html()).toContain('載入失敗')
    expect(wrapper.html()).toContain('Network Error')
  })

  it('displays data table header', async () => {
    const mockStats = { total_users: 100, active_sessions: 10, api_calls_24h: 500 }
    const mockUsers = [{ id: 1, name: 'Test User', email: 'test@example.com', status: 'active' }]

    vi.mocked(useApi).mockReturnValue({
      get: vi.fn().mockImplementation((url: string) => {
        if (url === '/dashboard/stats') return Promise.resolve(mockStats)
        if (url === '/users') return Promise.resolve(mockUsers)
        return Promise.resolve({})
      }),
    })

    const wrapper = mount(Dashboard, {
      global: { plugins: [vuetify, createPinia()], stubs: vuetifyStubs },
    )

    await flushPromises()
    await wrapper.vm.$nextTick()

    expect(wrapper.html()).toContain('使用者列表')
  })
})