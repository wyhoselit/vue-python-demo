import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'
import App from '../../App.vue'

const vuetify = createVuetify({
  components,
  directives,
})

describe('App.vue', () => {
  it('renders the main application layout', () => {
    const wrapper = mount(App, {
      global: {
        plugins: [vuetify],
      },
    })
    expect(wrapper.html()).toContain('Hello World')
    expect(wrapper.html()).toContain('Welcome to the Vuetify + FastAPI demo application.')
  })

  it('renders the app bar title', () => {
    const wrapper = mount(App, {
      global: {
        plugins: [vuetify],
      },
    })
    expect(wrapper.find('.v-app-bar-title').exists()).toBe(true)
  })
})
