import { describe, it, expect, beforeEach } from 'vitest'
import { setActivePinia, createPinia } from 'pinia'
import { useThemeStore } from '../../stores/theme'

describe('Theme Store', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
  })

  it('initializes with default theme', () => {
    const store = useThemeStore()
    expect(store.theme).toBe('light')
  })

  it('isDark getter returns false for light theme', () => {
    const store = useThemeStore()
    expect(store.isDark).toBe(false)
  })

  it('isDark getter returns true for dark theme', () => {
    const store = useThemeStore()
    store.setTheme('dark')
    expect(store.isDark).toBe(true)
  })

  it('can change theme', () => {
    const store = useThemeStore()
    store.setTheme('dark')
    expect(store.theme).toBe('dark')
  })

  it('can toggle theme', () => {
    const store = useThemeStore()
    store.toggleTheme()
    expect(store.theme).toBe('dark')
    store.toggleTheme()
    expect(store.theme).toBe('light')
  })
})