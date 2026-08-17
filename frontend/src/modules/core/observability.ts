import { WebTracerProvider, SimpleSpanProcessor } from '@opentelemetry/sdk-trace-web';
import { OTLPTraceExporter } from '@opentelemetry/exporter-trace-otlp-http';
import { DocumentLoadInstrumentation } from '@opentelemetry/instrumentation-document-load';
import { FetchInstrumentation } from '@opentelemetry/instrumentation-fetch';
import { UserInteractionInstrumentation } from '@opentelemetry/instrumentation-user-interaction';
import { ZoneContextManager } from '@opentelemetry/context-zone';
import { MeterProvider, PeriodicExportingMetricReader } from '@opentelemetry/sdk-metrics';
import { OTLPMetricExporter } from '@opentelemetry/exporter-metrics-otlp-http';
import { metrics, trace, diag, DiagConsoleLogger, DiagLogLevel } from '@opentelemetry/api';
import { logs } from '@opentelemetry/api-logs';
import { LoggerProvider, SimpleLogRecordProcessor } from '@opentelemetry/sdk-logs';
import { OTLPLogExporter } from '@opentelemetry/exporter-logs-otlp-http';
import { Resource } from '@opentelemetry/resources';
import { SemanticResourceAttributes } from '@opentelemetry/semantic-conventions';

export const tracer = trace.getTracer('vue-frontend-tracer');

export const setupObservability = () => {
  diag.setLogger(new DiagConsoleLogger(), DiagLogLevel.INFO);
  const collectorUrl = import.meta.env.VITE_OTEL_COLLECTOR_URL || 'http://localhost:4318/v1/traces';
  const metricsEnabled = import.meta.env.VITE_OTEL_METRICS_ENABLED !== 'false';
  const metricsCollectorUrl = import.meta.env.VITE_OTEL_COLLECTOR_METRICS_URL || 'http://localhost:4318/v1/metrics';
  const logsCollectorUrl = import.meta.env.VITE_OTEL_COLLECTOR_LOGS_URL || 'http://localhost:4318/v1/logs';

  const resource = new Resource({
    [SemanticResourceAttributes.SERVICE_NAME]: import.meta.env.VITE_SERVICE_NAME || 'frontend-app',
  });

  // Traces
  const traceExporter = new OTLPTraceExporter({
    url: collectorUrl,
  });

  const tracerProvider = new WebTracerProvider({
    resource: resource,
  });
  tracerProvider.addSpanProcessor(new SimpleSpanProcessor(traceExporter));
  tracerProvider.register({
    contextManager: new ZoneContextManager(),
    instrumentations: [
      new DocumentLoadInstrumentation(),
      new FetchInstrumentation(),
      new UserInteractionInstrumentation(),
    ],
  });

  // Metrics (optional)
  if (metricsEnabled) {
    const metricExporter = new OTLPMetricExporter({
      url: metricsCollectorUrl,
    });

    const meterProvider = new MeterProvider({
      resource: resource,
    });
    meterProvider.addMetricReader(
      new PeriodicExportingMetricReader({
        exporter: metricExporter,
        exportIntervalMillis: 1000, // Export every 1 second
      }),
    );

    metrics.setGlobalMeterProvider(meterProvider);
  }

  // Logs
  const logExporter = new OTLPLogExporter({
    url: logsCollectorUrl,
  });
  const loggerProvider = new LoggerProvider({ resource });
  loggerProvider.addLogRecordProcessor(new SimpleLogRecordProcessor(logExporter));
  logs.setGlobalLoggerProvider(loggerProvider);

  console.log('Observability SDK started', { metricsEnabled });
};