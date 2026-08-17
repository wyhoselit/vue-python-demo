import type { Router } from 'vue-router';
import { tracer } from '@/modules/core/observability';
import { Span, SpanStatusCode } from '@opentelemetry/api';

export const routerInstrumentation = (router: Router) => {
  let currentSpan: Span | undefined;

  router.beforeEach((to, from, next) => {
    currentSpan = tracer.startSpan(`Navigation to ${to.name?.toString() || to.path}`);
    currentSpan.setAttribute('from', from.fullPath);
    currentSpan.setAttribute('to', to.fullPath);
    next();
  });

  router.afterEach((to, from, failure) => {
    if (currentSpan) {
      if (failure) {
        currentSpan.setStatus({ code: SpanStatusCode.ERROR, message: failure.message });
      } else {
        currentSpan.setStatus({ code: SpanStatusCode.OK });
      }
      currentSpan.end();
    }
  });

  router.onError((error: Error) => {
    if (currentSpan) {
      currentSpan.setStatus({ code: SpanStatusCode.ERROR, message: error.message });
      currentSpan.end();
    }
  });
};
