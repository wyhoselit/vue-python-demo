import { computed } from 'vue';
import { useRoute } from 'vue-router';
import { recordButtonClick, recordFormSubmit } from '@/modules/core/metrics/metrics';

export const useMetrics = () => {
  const route = useRoute();
  const currentRoute = computed(() => route.path);

  const trackButtonClick = (elementId: string, elementType: string = 'button') => {
    recordButtonClick(elementId, elementType, currentRoute.value);
  };

  const trackFormSubmit = (formName: string) => {
    recordFormSubmit(formName, currentRoute.value);
  };

  return {
    trackButtonClick,
    trackFormSubmit,
  };
};