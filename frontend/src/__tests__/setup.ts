import { vi } from 'vitest'

const localStorageMock = (() => {
  let store: Record<string, string> = {}
  return {
    getItem: (key: string) => store[key] || null,
    setItem: (key: string, value: string) => { store[key] = value },
    removeItem: (key: string) => { delete store[key] },
    clear: () => { store = {} },
  }
})()

Object.defineProperty(globalThis, 'localStorage', { value: localStorageMock })

vi.mock('vuetify/components/VApp/VApp.css', () => ({}))
vi.mock('vuetify/components/VAppBar/VAppBar.css', () => ({}))
vi.mock('vuetify/components/VCard/VCard.css', () => ({}))
vi.mock('vuetify/components/VContainer/VContainer.css', () => ({}))
vi.mock('vuetify/components/VRow/VRow.css', () => ({}))
vi.mock('vuetify/components/VCol/VCol.css', () => ({}))
vi.mock('vuetify/components/VMain/VMain.css', () => ({}))
vi.mock('vuetify/components/VNavigationDrawer/VNavigationDrawer.css', () => ({}))
vi.mock('vuetify/components/VToolbar/VToolbar.css', () => ({}))
vi.mock('vuetify/components/VBtn/VBtn.css', () => ({}))
vi.mock('vuetify/components/VIcon/VIcon.css', () => ({}))
vi.mock('vuetify/components/VDataTable/VDataTable.css', () => ({}))
vi.mock('vuetify/components/VPagination/VPagination.css', () => ({}))
vi.mock('vuetify/components/VProgressLinear/VProgressLinear.css', () => ({}))

if (typeof (globalThis as any).document !== 'undefined') {
  ;(globalThis as any).document.documentElement.setAttribute('data-theme', 'light')
}