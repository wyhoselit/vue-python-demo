import { tracer } from '@/modules/core/observability';
import { Span } from '@opentelemetry/api';

export function instrumentRouter(router) {
  let span: Span | undefined;

  router.beforeEach((to, from, next) => {
    span = tracer.startSpan(`Navigation to ${to.name}`);
    span.setAttribute('from', from.fullPath);
    span.setAttribute('to', to.fullPath);
    next();
  });

  router.afterEach(() => {
    if (span) {
      span.end();
    }
  });
}
