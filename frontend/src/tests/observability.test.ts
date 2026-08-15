import { describe, it, expect, vi, beforeEach } from 'vitest'
import { setupObservability } from '../observability'

// Mock the OTel SDK modules
vi.mock('@opentelemetry/sdk-trace-web', () => {
  const mockProvider = {
    addSpanProcessor: vi.fn(),
    register: vi.fn(),
  }
  return {
    WebTracerProvider: vi.fn(() => mockProvider),
    SimpleSpanProcessor: vi.fn(),
    TraceSDK: vi.fn().mockImplementation(() => ({
      start: vi.fn(),
    })),
  }
})

vi.mock('@opentelemetry/exporter-trace-otlp-http', () => ({
  OTLPTraceExporter: vi.fn(),
}))

vi.mock('@opentelemetry/instrumentation-document-load', () => ({
  DocumentLoadInstrumentation: vi.fn(),
}))

vi.mock('@opentelemetry/instrumentation-fetch', () => ({
  FetchInstrumentation: vi.fn(),
}))

vi.mock('@opentelemetry/instrumentation-user-interaction', () => ({
  UserInteractionInstrumentation: vi.fn(),
}))

vi.mock('@opentelemetry/context-zone', () => ({
  ZoneContextManager: vi.fn(),
}))

describe('Frontend Observability', () => {
  beforeEach(() => {
    vi.resetModules()
    vi.clearAllMocks()
    // Reset env var
    delete import.meta.env.VITE_OTEL_COLLECTOR_URL
  })

  it('should initialize the OTel SDK with default collector URL', async () => {
    const { WebTracerProvider } = await import('@opentelemetry/sdk-trace-web')
    const { setupObservability } = await import('../observability')

    setupObservability()

    expect(WebTracerProvider).toHaveBeenCalled()
  })

  it('should use custom collector URL from env var', async () => {
    import.meta.env.VITE_OTEL_COLLECTOR_URL = 'http://custom-collector:4318/v1/traces'

    const { OTLPTraceExporter } = await import('@opentelemetry/exporter-trace-otlp-http')
    const { setupObservability } = await import('../observability')

    setupObservability()

    expect(OTLPTraceExporter).toHaveBeenCalledWith(
      expect.objectContaining({
        url: 'http://custom-collector:4318/v1/traces',
      })
    )
  })
})
