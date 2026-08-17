import { tracer } from '@/modules/core/observability';
import { SpanStatusCode } from '@opentelemetry/api';

export const routerInstrumentation = (router) => {
  router.beforeEach((to, from, next) => {
    const span = tracer.startSpan(`navigation: ${String(to.name)}`);
    span.setAttribute('from', String(from.name));
    span.setAttribute('to', String(to.name));

    let spanEnded = false;
    let errorHandled = false; // Add a flag for error handling

    const endSpan = (error?: Error) => {
      if (!spanEnded) {
        if (error && !errorHandled) { // Only set error status if there was an error and it hasn't been handled
          span.recordException(error);
          span.setStatus({ code: SpanStatusCode.ERROR, message: error.message });
          errorHandled = true;
        } else {
          span.setStatus({ code: SpanStatusCode.OK }); // Default to OK if no error
        }
        span.end();
        spanEnded = true;
      }
    };

    router.afterEach(() => {
      endSpan();
    });

    router.onError((err) => {
      endSpan(err); // Pass error to endSpan
    });

    next();
  });
};