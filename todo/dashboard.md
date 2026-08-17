# Grafana Dashboard 故障排除進度

## 已完成修正與驗證 (Completed Fixes and Verification)

### 1. Loki 查詢語法修正 (Syntax Fix for Loki Queries)
- **問題**: Grafana 顯示 `bad_data: invalid parameter "query": unexpected character inside braces: '.'` 錯誤，原因是 Loki label key 不支援 `.`。
- **解決方案**: 將 `service.name` 替換為 `job`。
  - **受影響檔案**:
    - `dockerdata/observability/grafana/provisioning/dashboards/combined-application-logs.json`
    - `dockerdata/observability/grafana/provisioning/dashboards/otel-dashboard.json`
- **驗證**: `combined-application-logs` 儀表板目前已顯示資料。

### 2. Prometheus 指標過濾及名稱修正 (Prometheus Metric Filtering and Naming)
- **問題**: Prometheus 儀表板查詢中使用了不存在的 `service.name` label，或使用了與實際 OpenTelemetry 導出名稱不符的 metric 名稱 (`http_request_duration_seconds_count`)。
- **解決方案**:
  - 將 Prometheus 查詢中的 `job="otel-collector", service.name="backend-service"` 替換為 `job="backend-service"`。
  - 將 `by (service.name)` 替換為 `by (job)` 或移除。
  - 將 metric 名稱 `http_request_duration_seconds_count` 替換為實際可用的 `http_server_duration_milliseconds_count`。
  - 更新 `legendFormat` 從 `{{service}}` 到 `{{job}}`。
- **受影響檔案**:
  - `dockerdata/observability/grafana/provisioning/dashboards/otel-dashboard.json`
  - `dockerdata/observability/grafana/provisioning/dashboards/backend-observability.json`
- **驗證**: `backend` 儀表板目前已顯示資料。Prometheus 已成功從 `otel-collector` 抓取到 `http_server_active_requests` 及 `http_server_duration_milliseconds_bucket` 等指標。

### 3. 後端 OpenTelemetry 指標導出機制修正 (Backend OpenTelemetry Metric Export)
- **問題**: 後端應用程式 (`backend-service`) 的 OpenTelemetry 指標未成功傳送至 OTel Collector，導致 Prometheus 儀表板無資料。後端僅透過 `prometheus_fastapi_instrumentator` 直接暴露 Prometheus 指標，但 Prometheus 僅抓取 OTel Collector。
- **解決方案**:
  - 移除 `backend/app/modules/core/observability.py` 中的 `Instrumentator().instrument(app).expose(app)`。
  - 移除 `backend/app/main.py` 中的 `/test-metrics` 測試端點。
  - 確保後端透過 `FastAPIInstrumentor` 將 OpenTelemetry 指標發送至 OTel Collector。
- **驗證**: `backend` 儀表板目前已顯示資料。

---

## 仍需處理的問題 (Remaining Issues)

### 1. Frontend 儀表板無資料 (Frontend Dashboard - No Data)
- **問題分析**: `frontend-observability.json` 仍無資料。這可能與前端 OpenTelemetry 設定、指標名稱或服務名稱傳遞有關。
- **建議處理方式**:
  1. **檢查前端應用程式碼**: 找出前端 Vue.js 應用程式的入口點 (例如 `src/main.js` 或 `src/App.vue` 或相關設定檔)。
  2. **驗證前端 OpenTelemetry 設定**: 確認 OpenTelemetry 在前端是否正確初始化，以及 HTTP 請求是否已啟用追蹤和指標導出。
  3. **確認前端 `SERVICE_NAME`**: 確保前端應用程式的 `SERVICE_NAME` 環境變數已正確設定為 `frontend-app` (或預期的名稱)，並正確傳遞到 OTel Collector。
  4. **檢查 OTel Collector 中的前端指標**: 嘗試 `curl otel-collector:8889/metrics` 並 `grep` 搜尋與前端相關的指標 (例如 `http_client_request_duration_seconds_bucket`)，確認前端指標是否已抵達 Collector。

### 2. OTel 儀表板部分無資料 (OTel Dashboard - Partial No Data)
- **問題分析**: 儘管 Prometheus 和 Loki 的部分已修正，但 `otel-dashboard.json` 中可能仍有其他部分 (例如 Tempo 追蹤) 或與前端相關的指標無資料。
- **建議處理方式**:
  1. **Prometheus 指標名稱一致性**: 再次確認 `otel-dashboard.json` 中所有 Prometheus 查詢使用的指標名稱與 OTel Collector 實際導出的指標名稱 (例如 `http_server_requests_seconds_count` vs `http_server_duration_milliseconds_count`) 完全一致。如有不一致，請進行調整。
  2. **Tempo 追蹤查詢驗證**:
     - 查閱 Tempo 相關文件，確認其追蹤過濾語法，特別是 `resource.service.name` 是否為正確的過濾方式。
     - 確認後端 (`fastapi-backend`) 發送的 Traces 中，實際使用的 `service.name` 值為何。這可以透過 OTel Collector 的日誌或 Tempo 的 UI 來觀察。如果值不符，請修正查詢。

---

## 下一步行動 (Next Steps)

1.  **執行上述「建議處理方式」**，針對前端和 OTel 儀表板中仍無資料的部分進行偵錯和修正。
2.  **每次變更後**: 重啟相關服務 (Frontend, Backend, OTel Collector, Grafana)，並再次驗證儀表板數據。