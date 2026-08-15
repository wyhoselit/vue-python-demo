import { describe, it, expect, afterEach, beforeEach, vi } from 'vitest';
import { createRouter, createWebHistory } from 'vue-router';
import { createPinia, defineStore, setActivePinia } from 'pinia';
import { createApp } from 'vue';
import axios from 'axios';
import { SpanStatusCode } from '@opentelemetry/api';
import { tracer } from '@/modules/core/observability';

describe('OpenTelemetry Frontend Instrumentation', () => {
  let router;
  let pinia;
  let routerTeardown;
  let startSpanSpy;
  let originalAdapter;

  beforeEach(() => {
    originalAdapter = axios.defaults.adapter;
  });

  afterEach(() => {
    vi.restoreAllMocks();
    if (routerTeardown) {
      routerTeardown();
    }
    axios.interceptors.request.clear();
    axios.interceptors.response.clear();
    axios.defaults.adapter = originalAdapter;
  });

  it('should create a span for route navigation', async () => {
    startSpanSpy = vi.spyOn(tracer, 'startSpan').mockReturnValue({
      setAttribute: vi.fn(),
      end: vi.fn(),
      recordException: vi.fn(),
      setStatus: vi.fn(),
      spanContext: vi.fn(() => ({ traceId: 'mock-trace-id' })),
    } as any);

    const { instrumentRouter } = await import('@/modules/core/router-observability');
    
    router = createRouter({
      history: createWebHistory(),
      routes: [
        { path: '/', name: 'Home', component: { template: '<div>Home</div>' } },
        { path: '/test', name: 'Test', component: { template: '<div>Test</div>' } },
      ],
    });
    routerTeardown = instrumentRouter(router);

    await router.push('/test');
    await router.isReady();

    expect(startSpanSpy).toHaveBeenCalledWith('Navigation to Test');
    expect(startSpanSpy.mock.results[0].value.setAttribute).toHaveBeenCalledWith('to', '/test');
    expect(startSpanSpy.mock.results[0].value.end).toHaveBeenCalled();
  });

  it('should create a span for pinia actions', async () => {
    startSpanSpy = vi.spyOn(tracer, 'startSpan').mockReturnValue({
      setAttribute: vi.fn(),
      end: vi.fn(),
      recordException: vi.fn(),
      setStatus: vi.fn(),
      spanContext: vi.fn(() => ({ traceId: 'mock-trace-id' })),
    } as any);

    const { piniaPlugin } = await import('@/plugins/pinia-instrumentation');
    
    pinia = createPinia();
    pinia.use(piniaPlugin);
    
    const app = createApp({});
    app.use(pinia);
    setActivePinia(pinia);

    const useTestStore = defineStore('test', {
      actions: {
        testAction() {},
      },
    });
    const testStore = useTestStore();

    testStore.testAction();

    expect(startSpanSpy).toHaveBeenCalledWith('Pinia Action: testAction');
    expect(startSpanSpy.mock.results[0].value.setAttribute).toHaveBeenCalledWith('store', 'test');
    expect(startSpanSpy.mock.results[0].value.end).toHaveBeenCalled();
  });

  it('should create a span for axios requests and handle success', async () => {
    startSpanSpy = vi.spyOn(tracer, 'startSpan').mockReturnValue({
      setAttribute: vi.fn(),
      end: vi.fn(),
      recordException: vi.fn(),
      setStatus: vi.fn(),
      spanContext: vi.fn(() => ({ traceId: 'mock-trace-id' })),
    } as any);

    const { axiosInstrumentation } = await import('@/plugins/axios-instrumentation');
    
    axiosInstrumentation();
    
    axios.defaults.adapter = vi.fn().mockImplementation((config) => {
      return Promise.resolve({
        data: 'success',
        status: 200,
        statusText: 'OK',
        headers: {},
        config,
      });
    });

    await axios.get('/api/test');

    expect(startSpanSpy).toHaveBeenCalledWith('http: GET /api/test');
    expect(startSpanSpy.mock.results[0].value.setStatus).toHaveBeenCalledWith({ code: SpanStatusCode.OK });
    expect(startSpanSpy.mock.results[0].value.end).toHaveBeenCalled();
  });

  it('should create a span for axios requests and handle error', async () => {
    startSpanSpy = vi.spyOn(tracer, 'startSpan').mockReturnValue({
      setAttribute: vi.fn(),
      end: vi.fn(),
      recordException: vi.fn(),
      setStatus: vi.fn(),
      spanContext: vi.fn(() => ({ traceId: 'mock-trace-id' })),
    } as any);
    
    const { axiosInstrumentation } = await import('@/plugins/axios-instrumentation');
    
    axiosInstrumentation();
    const errorMessage = 'Network Error';
    
    axios.defaults.adapter = vi.fn().mockImplementation((config) => {
      const error = new Error(errorMessage);
      (error as any).config = config;
      return Promise.reject(error);
    });

    await expect(axios.get('/api/error')).rejects.toThrow(errorMessage);

    expect(startSpanSpy).toHaveBeenCalledWith('http: GET /api/error');
    expect(startSpanSpy.mock.results[0].value.recordException).toHaveBeenCalledWith(new Error(errorMessage));
    expect(startSpanSpy.mock.results[0].value.setStatus).toHaveBeenCalledWith({ code: SpanStatusCode.ERROR, message: errorMessage });
    expect(startSpanSpy.mock.results[0].value.end).toHaveBeenCalled();
  });
});