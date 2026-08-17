## MODIFIED Requirements

### Requirement: Router Navigation Tracing
The system SHALL create OpenTelemetry spans for each router navigation event.

#### Scenario: Span created on navigation start
- **WHEN** a router navigation begins (beforeEach guard)
- **THEN** an OpenTelemetry span SHALL be started with name "Navigation to <route>" and attributes for "from" and "to" paths.

#### Scenario: Span ended on navigation completion
- **WHEN** a router navigation completes successfully (afterEach hook)
- **THEN** the active span SHALL be ended with status OK.

#### Scenario: Span marked error on navigation failure
- **WHEN** a router navigation fails or encounters an error (onError hook)
- **THEN** the active span SHALL be ended with status ERROR and the error message recorded.

### Requirement: Axios Request Tracing
The system SHALL create OpenTelemetry spans for each outgoing HTTP request via Axios.

#### Scenario: Span created for each request
- **WHEN** an Axios request is sent
- **THEN** an OpenTelemetry span SHALL be started with name "http: <METHOD> <URL>" and attributes for HTTP method and URL.

#### Scenario: Span records response status on success
- **WHEN** an Axios request receives a successful response
- **THEN** the span SHALL set attribute "http.status_code" and end with status OK.

#### Scenario: Span records error on failure
- **WHEN** an Axios request fails or receives an error response
- **THEN** the span SHALL record the exception, set status ERROR with error message, and end.

### Requirement: Pinia Action Tracing
The system SHALL create OpenTelemetry spans for Pinia store actions.

#### Scenario: Span created for each Pinia action
- **WHEN** a Pinia action is invoked
- **THEN** an OpenTelemetry span SHALL be started with name "Pinia Action: <actionName>" and attributes for store name.

#### Scenario: Span attributes set for store and action
- **WHEN** a Pinia action span is created
- **THEN** attributes SHALL include "store" (store name) and "action" (action name).

### Requirement: Application Observability Initialization
The system SHALL initialize OpenTelemetry tracing, metrics, and logging on application startup.

#### Scenario: Tracing, metrics, and logging configured
- **WHEN** `setupObservability()` is called
- **THEN** the system SHALL configure:
  - WebTracerProvider with OTLP trace exporter
  - MeterProvider with OTLP metric exporter (if enabled)
  - LoggerProvider with OTLP log exporter
  - Resource attributes including service name
  - ZoneContextManager for context propagation