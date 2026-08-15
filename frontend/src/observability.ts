import { WebTracerProvider } from '@opentelemetry/sdk-trace-web'
import { SimpleSpanProcessor } from '@opentelemetry/sdk-trace-base'
import { OTLPTraceExporter } from '@opentelemetry/exporter-trace-otlp-http'
import { DocumentLoadInstrumentation } from '@opentelemetry/instrumentation-document-load'
import { FetchInstrumentation } from '@opentelemetry/instrumentation-fetch'
import { UserInteractionInstrumentation } from '@opentelemetry/instrumentation-user-interaction'
import { ZoneContextManager } from '@opentelemetry/context-zone'

export const setupObservability = () => {
  const collectorUrl = import.meta.env.VITE_OTEL_COLLECTOR_URL || 'http://localhost:4318/v1/traces'

  const exporter = new OTLPTraceExporter({
    url: collectorUrl,
  })

  const provider = new WebTracerProvider()
  provider.addSpanProcessor(new SimpleSpanProcessor(exporter))
  provider.register({
    contextManager: new ZoneContextManager(),
    instrumentations: [
      new DocumentLoadInstrumentation(),
      new FetchInstrumentation(),
      new UserInteractionInstrumentation(),
    ],
  })

  console.log('Observability SDK started')
}