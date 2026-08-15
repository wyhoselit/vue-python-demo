import { tracer } from '@/modules/core/observability';
import { SpanStatusCode } from '@opentelemetry/api';

export const routerInstrumentation = (router) => {
  router.beforeEach((to, from, next) => {
    const span = tracer.startSpan(`navigation: ${String(to.name)}`);
    span.setAttribute('from', String(from.name));
    span.setAttribute('to', String(to.name));

    router.afterEach(() => {
      span.end();
    });

    router.onError((err) => {
        span.recordException(err);
        span.setStatus({ code: SpanStatusCode.ERROR, message: err.message });
        span.end();
    });

    next();
  });
};