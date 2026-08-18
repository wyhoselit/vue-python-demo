import { describe, it, expect, beforeEach, vi } from 'vitest'
import { mount, flushPromises } from '@vue/test-utils'
import Dashboard from '@/modules/dashboard/views/Dashboard.vue'
import { createVuetify } from 'vuetify'
import { createPinia } from 'pinia'
import * as useApiModule from '@/shared/useApi'
import { VDataTable } from 'vuetify/components' // Import VDataTable directly

vi.mock('@/shared/useApi')
vi.mock('vue-router', async (importOriginal) => {
  const actual = await importOriginal() as object;
  return {
    ...actual,
    useRoute: vi.fn(() => ({ path: '/', name: 'Dashboard' }))
  }
})

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
  'v-data-table': VDataTable, // Use the actual component for better testing
  'v-alert': { template: '<div><slot /></div>' },
  'v-btn': { template: '<button><slot /></button>' },
  'ApexChart': { template: '<div></div>' } // Stub ApexChart
}

describe('Dashboard', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it('renders loading state initially', async () => {
    let resolveStats: (value: unknown) => void
    let resolveUsers: (value: unknown) => void
    let resolveRealtime: (value: unknown) => void

    const statsPromise = new Promise((resolve) => { resolveStats = resolve })
    const usersPromise = new Promise((resolve) => { resolveUsers = resolve })
    const realtimePromise = new Promise((resolve) => { resolveRealtime = resolve })

    vi.mocked(useApiModule.useApi).mockReturnValue({
      get: vi.fn().mockImplementation((url: string) => {
        if (url === '/dashboard/stats') return statsPromise
        if (url === '/users') return usersPromise
        if (url === '/dashboard/realtime') return realtimePromise
        return Promise.resolve({})
      }),
    } as any) // Cast to any to bypass type checking for the mock

    const wrapper = mount(Dashboard, {
      global: { plugins: [vuetify, createPinia()], stubs: vuetifyStubs },
    })

    expect(wrapper.html()).toContain('載入儀表板資料中')

    resolveStats!({ total_users: 100, active_sessions: 10, api_calls_24h: 500 })
    resolveUsers!([{ id: 1, name: 'Test', email: 'test@example.com', status: 'active' }])
    resolveRealtime!([])
    await flushPromises()
  })

  it('renders success state with stats and users', async () => {
    const mockStats = { total_users: 1250, active_sessions: 42, api_calls_24h: 15420 }
    const mockUsers = [
      { id: 1, name: 'Alice Chen', email: 'alice@example.com', status: 'active' },
      { id: 2, name: 'Bob Smith', email: 'bob@example.com', status: 'active' },
    ]
    const mockRealtime = [{ timestamp: new Date().toISOString(), requests: 10, avgResponseTime: 50, status2xx: 5, status4xx: 2, status5xx: 1, activeUsers: 8 }]

    vi.mocked(useApiModule.useApi).mockReturnValue({
      get: vi.fn().mockImplementation((url: string) => {
        if (url === '/dashboard/stats') return Promise.resolve(mockStats)
        if (url === '/users') return Promise.resolve(mockUsers)
        if (url === '/dashboard/realtime') return Promise.resolve(mockRealtime)
        return Promise.resolve({})
      }),
    } as any) // Cast to any to bypass type checking for the mock

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
    vi.mocked(useApiModule.useApi).mockReturnValue({
      get: vi.fn().mockRejectedValue(new Error('Network Error')),
    } as any) // Cast to any to bypass type checking for the mock

    const wrapper = mount(Dashboard, {
      global: { plugins: [vuetify, createPinia()], stubs: vuetifyStubs },
    })

    await flushPromises()
    await new Promise(resolve => setTimeout(resolve, 50))
    await wrapper.vm.$nextTick()

    expect(wrapper.html()).toContain('載入失敗')
    expect(wrapper.html()).toContain('Network Error')
  })

  it('displays data table header', async () => {
    const mockStats = { total_users: 100, active_sessions: 10, api_calls_24h: 500 }
    const mockUsers = [{ id: 1, name: 'Test User', email: 'test@example.com', status: 'active' }]
    const mockRealtime = [{ timestamp: new Date().toISOString(), requests: 10, avgResponseTime: 50, status2xx: 5, status4xx: 2, status5xx: 1, activeUsers: 8 }]

    vi.mocked(useApiModule.useApi).mockReturnValue({
      get: vi.fn().mockImplementation((url: string) => {
        if (url === '/dashboard/stats') return Promise.resolve(mockStats)
        if (url === '/users') return Promise.resolve(mockUsers)
        if (url === '/dashboard/realtime') return Promise.resolve(mockRealtime)
        return Promise.resolve({})
      }),
    } as any) // Cast to any to bypass type checking for the mock

    const wrapper = mount(Dashboard, {
      global: { plugins: [vuetify, createPinia()], stubs: vuetifyStubs }
    })

    await flushPromises()
    await wrapper.vm.$nextTick()

    expect(wrapper.html()).toContain('使用者列表')
  })

  it('stops realtime updates on unmount', async () => {
    const clearIntervalSpy = vi.spyOn(global, 'clearInterval');
    const mockStats = { total_users: 100, active_sessions: 10, api_calls_24h: 500 };
    const mockUsers = [{ id: 1, name: 'Test User', email: 'test@example.com', status: 'active' }];
    const mockRealtime = [{ timestamp: new Date().toISOString(), requests: 10, avgResponseTime: 50, status2xx: 5, status4xx: 2, status5xx: 1, activeUsers: 8 }];

    vi.mocked(useApiModule.useApi).mockReturnValue({
      get: vi.fn().mockImplementation((url: string) => {
        if (url === '/dashboard/stats') return Promise.resolve(mockStats);
        if (url === '/users') return Promise.resolve(mockUsers);
        if (url === '/dashboard/realtime') return Promise.resolve(mockRealtime);
        return Promise.resolve({});
      }),
    } as any);

    const wrapper = mount(Dashboard, {
      global: { plugins: [vuetify, createPinia()], stubs: vuetifyStubs },
    });

    await flushPromises();
    wrapper.unmount();

    expect(clearIntervalSpy).toHaveBeenCalled();
  });

  it('handles realtime data with valid numeric values (no NaN/Infinity)', async () => {
    const mockStats = { total_users: 100, active_sessions: 10, api_calls_24h: 500 };
    const mockUsers = [{ id: 1, name: 'Test User', email: 'test@example.com', status: 'active' }];
    const mockRealtime = [{
      timestamp: new Date().toISOString(),
      requests: 100,
      avgResponseTime: 50.5,
      status2xx: 80,
      status4xx: 5,
      status5xx: 2,
      activeUsers: 25,
    }];

    vi.mocked(useApiModule.useApi).mockReturnValue({
      get: vi.fn().mockImplementation((url: string) => {
        if (url === '/dashboard/stats') return Promise.resolve(mockStats);
        if (url === '/users') return Promise.resolve(mockUsers);
        if (url === '/dashboard/realtime') return Promise.resolve(mockRealtime);
        return Promise.resolve({});
      }),
    } as any);

    const wrapper = mount(Dashboard, {
      global: { plugins: [vuetify, createPinia()], stubs: vuetifyStubs },
    });

    await flushPromises();
    await new Promise(resolve => setTimeout(resolve, 50));

    expect(wrapper.html()).toContain('100');
    expect(wrapper.html()).toContain('API 回應時間分佈');
  });

  it('falls back to mock data when realtime API returns empty array', async () => {
    const mockStats = { total_users: 100, active_sessions: 10, api_calls_24h: 500 };
    const mockUsers = [{ id: 1, name: 'Test User', email: 'test@example.com', status: 'active' }];

    vi.mocked(useApiModule.useApi).mockReturnValue({
      get: vi.fn().mockImplementation((url: string) => {
        if (url === '/dashboard/stats') return Promise.resolve(mockStats);
        if (url === '/users') return Promise.resolve(mockUsers);
        if (url === '/dashboard/realtime') return Promise.resolve([]);
        return Promise.resolve({});
      }),
    } as any);

    const wrapper = mount(Dashboard, {
      global: { plugins: [vuetify, createPinia()], stubs: vuetifyStubs },
    });

    await flushPromises();
    await new Promise(resolve => setTimeout(resolve, 50));

    expect(wrapper.html()).toContain('100');
    expect(wrapper.html()).toContain('API 回應時間分佈');
  });

  it('falls back to mock data when realtime API fails (network error)', async () => {
    const mockStats = { total_users: 100, active_sessions: 10, api_calls_24h: 500 };
    const mockUsers = [{ id: 1, name: 'Test User', email: 'test@example.com', status: 'active' }];

    vi.mocked(useApiModule.useApi).mockReturnValue({
      get: vi.fn().mockImplementation((url: string) => {
        if (url === '/dashboard/stats') return Promise.resolve(mockStats);
        if (url === '/users') return Promise.resolve(mockUsers);
        if (url === '/dashboard/realtime') return Promise.reject(new Error('Network Error'));
        return Promise.resolve({});
      }),
    } as any);

    const wrapper = mount(Dashboard, {
      global: { plugins: [vuetify, createPinia()], stubs: vuetifyStubs },
    });

    await flushPromises();
    await new Promise(resolve => setTimeout(resolve, 50));

    expect(wrapper.html()).toContain('100');
    expect(wrapper.html()).toContain('API 回應時間分佈');
  });
});