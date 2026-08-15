import { PiniaPluginContext } from 'pinia';
import { tracer } from '@/modules/core/observability';

export function piniaPlugin(context: PiniaPluginContext) {
  context.store.$onAction(({ name, args, after, onError }) => {
    const span = tracer.startSpan(`Pinia Action: ${name}`);
    span.setAttribute('store', context.store.$id);
    span.setAttribute('action', name);
    span.setAttribute('args', JSON.stringify(args));

    after((result) => {
      span.setAttribute('result', JSON.stringify(result));
      span.end();
    });

    onError((error) => {
      span.setAttribute('error', error.message);
      span.end();
    });
  });
}