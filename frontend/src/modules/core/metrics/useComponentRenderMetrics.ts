import { onBeforeMount, onMounted, getCurrentInstance } from 'vue';
import { useRoute } from 'vue-router';
import { recordComponentRender } from '@/modules/core/metrics/metrics';

export const useComponentRenderMetrics = () => {
  const instance = getCurrentInstance();
  const route = useRoute();
  let startTime: number;

  onBeforeMount(() => {
    startTime = performance.now();
  });

  onMounted(() => {
    const duration = performance.now() - startTime;
    const componentName = instance?.type.__name || 'UnknownComponent';
    recordComponentRender(componentName, route.path, duration);
  });
};