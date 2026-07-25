import { describe, it, expect, beforeEach } from 'vitest'
import { mount } from '@vue/test-utils'
import DefaultLayout from '@/layouts/DefaultLayout.vue'
import { createVuetify } from 'vuetify'
import { createPinia, setActivePinia } from 'pinia'

const vuetify = createVuetify()

const vuetifyStubs = {
  'router-view': true,
  'router-link': true,
  'v-app': { template: '<div><slot /></div>' },
  'v-app-bar': { template: '<header><slot /></header>' },
  'v-app-bar-nav-icon': { template: '<button><slot /></button>' },
  'v-toolbar-title': { template: '<h1><slot /></h1>' },
  'v-spacer': { template: '<div />' },
  'v-btn': { template: '<button><slot /></button>' },
  'v-icon': { template: '<i><slot /></i>' },
  'v-main': { template: '<main><slot /></main>' },
  'v-navigation-drawer': { template: '<aside><slot /></aside>' },
  'v-side-navigation-drawer': { template: '<aside><slot /></aside>' },
  'v-list': { template: '<ul><slot /></ul>' },
  'v-list-item': { template: '<li><slot /></li>' },
  'v-list-item-title': { template: '<span><slot /></span>' },
}

describe('DefaultLayout', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
  })

  it('renders correctly', () => {
    const wrapper = mount(DefaultLayout, {
      global: {
        plugins: [vuetify, createPinia()],
        stubs: vuetifyStubs,
      },
    })
    expect(wrapper.find('header').exists()).toBe(true)
    expect(wrapper.html()).toContain('AI Platform')
  })

  it('renders app bar with title', () => {
    const wrapper = mount(DefaultLayout, {
      global: {
        plugins: [vuetify, createPinia()],
        stubs: vuetifyStubs,
      },
    })
    expect(wrapper.text()).toContain('AI Platform')
  })
})