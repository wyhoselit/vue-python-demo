import { describe, it, expect, beforeEach } from 'vitest'
import { mount } from '@vue/test-utils'
import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'
import { createPinia, setActivePinia } from 'pinia'
import App from '../../App.vue'

const vuetify = createVuetify({
  components,
  directives,
})

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

describe('App.vue', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
  })

  it('renders the main application layout', () => {
    const wrapper = mount(App, {
      global: {
        plugins: [vuetify, createPinia()],
        stubs: vuetifyStubs,
      },
    })
    expect(wrapper.html()).toContain('AI Platform')
  })

  it('renders the app bar title', () => {
    const wrapper = mount(App, {
      global: {
        plugins: [vuetify, createPinia()],
        stubs: vuetifyStubs,
      },
    })
    expect(wrapper.text()).toContain('AI Platform')
  })
})
