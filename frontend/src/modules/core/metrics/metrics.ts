import { metrics, Meter, Counter, Histogram } from '@opentelemetry/api';
import { SemanticAttributes } from '@opentelemetry/semantic-conventions';

const METER_NAME = 'frontend-app';
let meter: Meter;

// Declare instruments as `let` and initialize them in `initializeMetrics`
let pageViewCounter: Counter;
let buttonClickCounter: Counter;
let formSubmitCounter: Counter;
let componentRenderDurationHistogram: Histogram;
let apiCallDurationHistogram: Histogram;

export const initializeMetrics = () => {
  meter = metrics.getMeter(METER_NAME);

  // Counters
  pageViewCounter = meter.createCounter('frontend.app.page_view', {
    description: 'Counts page views',
    unit: '1',
  });

  buttonClickCounter = meter.createCounter('frontend.app.button_click', {
    description: 'Counts button clicks',
    unit: '1',
  });

  formSubmitCounter = meter.createCounter('frontend.app.form_submit', {
    description: 'Counts form submissions',
    unit: '1',
  });

  // Histograms
  componentRenderDurationHistogram = meter.createHistogram('frontend.app.component_render_duration', {
    description: 'Measures component render duration',
    unit: 'ms',
  });

  apiCallDurationHistogram = meter.createHistogram('http.client.duration', {
    description: 'Measures HTTP client request duration',
    unit: 'ms',
  });
};

export const recordPageView = (routeName: string, routePath: string) => {
  if (!pageViewCounter) {
    console.warn('Metrics not initialized: pageViewCounter');
    return;
  }
  pageViewCounter.add(1, { 'route.name': routeName, 'route.path': routePath });
};

export const recordButtonClick = (elementId: string, elementType: string, pageRoute: string) => {
  if (!buttonClickCounter) {
    console.warn('Metrics not initialized: buttonClickCounter');
    return;
  }
  buttonClickCounter.add(1, { 'element_id': elementId, 'element_type': elementType, 'page_route': pageRoute });
};

export const recordFormSubmit = (formName: string, pageRoute: string) => {
  if (!formSubmitCounter) {
    console.warn('Metrics not initialized: formSubmitCounter');
    return;
  }
  formSubmitCounter.add(1, { 'form_name': formName, 'page_route': pageRoute });
};

export const recordComponentRender = (componentName: string, routePath: string, duration: number) => {
  if (!componentRenderDurationHistogram) {
    console.warn('Metrics not initialized: componentRenderDurationHistogram');
    return;
  }
  componentRenderDurationHistogram.record(duration, { 'component_name': componentName, 'route.path': routePath });
};

export const recordApiCall = (method: string, url: string, statusCode: number, duration: number) => {
  if (!apiCallDurationHistogram) {
    console.warn('Metrics not initialized: apiCallDurationHistogram');
    return;
  }
  apiCallDurationHistogram.record(duration, {
    [SemanticAttributes.HTTP_METHOD]: method,
    [SemanticAttributes.HTTP_URL]: url, // Consider generalizing URL if it contains high-cardinality values
    [SemanticAttributes.HTTP_STATUS_CODE]: statusCode,
  });
};
