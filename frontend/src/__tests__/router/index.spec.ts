import { describe, it, expect, beforeEach } from 'vitest'
import { setActivePinia, createPinia } from 'pinia'
import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: { template: '<div>Home</div>' },
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: { template: '<div>Not Found</div>' },
  },
]

describe('Router', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
  })

  it('has correct routes defined', () => {
    const router = createRouter({
      history: createWebHistory(),
      routes,
    })
    expect(router.getRoutes()).toHaveLength(2)
  })

  it('has home route at path /', () => {
    const router = createRouter({
      history: createWebHistory(),
      routes,
    })
    const homeRoute = router.getRoutes().find(r => r.name === 'Home')
    expect(homeRoute).toBeDefined()
    expect(homeRoute?.path).toBe('/')
  })

  it('has catch-all route for unknown paths', () => {
    const router = createRouter({
      history: createWebHistory(),
      routes,
    })
    const notFoundRoute = router.getRoutes().find(r => r.name === 'NotFound')
    expect(notFoundRoute).toBeDefined()
  })
})