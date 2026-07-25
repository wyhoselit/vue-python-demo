import { describe, it, expect, beforeEach, vi } from 'vitest'
import { mount } from '@vue/test-utils'
import Dashboard from '@/views/Dashboard.vue'
import { createVuetify } from 'vuetify'
import { createPinia } from 'pinia'
import axios from 'axios'

vi.mock('axios')

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
  'v-data-table': { template: '<div />' },
}

describe('Dashboard', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it('renders correctly', () => {
    const mockInstance = {
      get: vi.fn().mockResolvedValue({ data: { cards: [], users: [] } }),
      post: vi.fn(),
      put: vi.fn(),
      delete: vi.fn(),
      interceptors: { response: { use: vi.fn() } },
    }
    vi.mocked(axios.create).mockReturnValue(mockInstance)

    const wrapper = mount(Dashboard, {
      global: {
        plugins: [vuetify, createPinia()],
        stubs: vuetifyStubs,
      },
    })
    expect(wrapper.find('div').exists()).toBe(true)
  })

  it('displays data cards', async () => {
    const mockInstance = {
      get: vi.fn().mockResolvedValue({ data: { cards: [], users: [] } }),
      post: vi.fn(),
      put: vi.fn(),
      delete: vi.fn(),
      interceptors: { response: { use: vi.fn() } },
    }
    vi.mocked(axios.create).mockReturnValue(mockInstance)

    const wrapper = mount(Dashboard, {
      global: {
        plugins: [vuetify, createPinia()],
        stubs: vuetifyStubs,
      },
    })
    await wrapper.vm.$nextTick()
    expect(wrapper.html()).toContain('Data Table')
  })
})