import axios from 'axios';
import { tracer } from '@/modules/core/observability';
import { SpanStatusCode, context, propagation, trace } from '@opentelemetry/api';


export const axiosInstrumentation = () => {
  axios.interceptors.request.use((config) => {
    const span = tracer.startSpan(`http: ${config.method?.toUpperCase()} ${config.url}`);
    config.headers['X-Trace-Id'] = span.spanContext().traceId;
    (config as any).span = span;
    return config;
  });

  axios.interceptors.response.use(
    (response) => {
      const { span } = response.config as any;
      if (span) {
        span.setStatus({ code: SpanStatusCode.OK });
        span.end();
      }
      return response;
    },
    (error) => {
      const { span } = error.config as any;
      if (span) {
        span.recordException(error);
        span.setStatus({ code: SpanStatusCode.ERROR, message: error.message });
        span.end();
      }
      return Promise.reject(error);
    }
  );
};