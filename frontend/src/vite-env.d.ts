/// <reference types="vite/client" />

declare module '*.vue' {
  import type { DefineComponent } from 'vue'
  const component: DefineComponent<Record<string, unknown>, Record<string, unknown>, unknown>
  export default component
}

interface ImportMetaEnv {
  readonly VITE_OTEL_COLLECTOR_URL: string
  readonly VITE_OTEL_COLLECTOR_METRICS_URL: string
  readonly VITE_OTEL_COLLECTOR_LOGS_URL: string
  readonly VITE_OTEL_METRICS_ENABLED: string
  readonly VITE_SERVICE_NAME: string
}

interface ImportMeta {
  readonly env: ImportMetaEnv
}
