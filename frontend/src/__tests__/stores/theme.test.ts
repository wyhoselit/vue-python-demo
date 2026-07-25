import { describe, it, expect, beforeEach, vi } from 'vitest'
import { createPinia, setActivePinia } from 'pinia'
import { useThemeStore } from '@/stores/theme'

describe('Theme Store', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
    localStorage.clear()
    vi.spyOn(window, 'matchMedia').mockImplementation(() => ({
      matches: false,
      addListener: vi.fn(),
      removeListener: vi.fn(),
      addEventListener: vi.fn(),
      removeEventListener: vi.fn(),
      dispatchEvent: vi.fn(),
      media: '',
      onchange: null,
      content: '',
      listener: null,
    }))
  })

  it('initializes with light theme by default', () => {
    const store = useThemeStore()
    expect(store.isDark).toBe(false)
    expect(store.theme).toBe('light')
  })

  it('toggles theme correctly', () => {
    const store = useThemeStore()
    store.toggleTheme()
    expect(store.isDark).toBe(true)
    expect(store.theme).toBe('dark')
    store.toggleTheme()
    expect(store.isDark).toBe(false)
    expect(store.theme).toBe('light')
  })

  it('persists theme to localStorage', () => {
    const store = useThemeStore()
    store.toggleTheme()
    expect(localStorage.getItem('theme')).toBe('dark')
  })

  it('reads persisted theme on init', () => {
    localStorage.setItem('theme', 'dark')
    const store = useThemeStore()
    store.initTheme()
    expect(store.isDark).toBe(true)
  })
})