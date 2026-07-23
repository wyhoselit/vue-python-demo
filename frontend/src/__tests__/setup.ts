import { vi } from 'vitest'

// Mock CSS imports
vi.mock('vuetify/components/VApp/VApp.css', () => ({}))
vi.mock('vuetify/components/VAppBar/VAppBar.css', () => ({}))
vi.mock('vuetify/components/VCard/VCard.css', () => ({}))
vi.mock('vuetify/components/VContainer/VContainer.css', () => ({}))
vi.mock('vuetify/components/VRow/VRow.css', () => ({}))
vi.mock('vuetify/components/VCol/VCol.css', () => ({}))
vi.mock('vuetify/components/VMain/VMain.css', () => ({}))