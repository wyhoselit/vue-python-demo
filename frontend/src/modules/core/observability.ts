import { OTLPTraceExporter } from '@opentelemetry/exporter-trace-otlp-http';
import { WebTracerProvider, BatchSpanProcessor } from '@opentelemetry/sdk-trace-web';
import { ZoneContextManager } from '@opentelemetry/context-zone';
import { Resource } from '@opentelemetry/resources';
import { SemanticResourceAttributes } from '@opentelemetry/semantic-conventions';

const VITE_OTEL_COLLECTOR_URL = import.meta.env.VITE_OTEL_COLLECTOR_URL;

const exporter = new OTLPTraceExporter({
  url: VITE_OTEL_COLLECTOR_URL,
});

const provider = new WebTracerProvider({
  resource: new Resource({
    [SemanticResourceAttributes.SERVICE_NAME]: 'vue-frontend',
  }),
});

provider.addSpanProcessor(new BatchSpanProcessor(exporter));
provider.register({
  contextManager: new ZoneContextManager(),
});

export const tracer = provider.getTracer('vue-frontend-tracer');
