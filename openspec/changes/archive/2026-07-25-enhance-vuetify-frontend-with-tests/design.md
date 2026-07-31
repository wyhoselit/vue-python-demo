## Context

目前 Vue + Vuetify 前端僅為基本專案，無暗黑模式、狀態管理、元件化設計及測試覆蓋。Backend 已穩定（API v1 + CORS + Alembic），前端需升級為專業 AI 平台介面。

**Constraints**:
- 必須使用 Vuetify 3 + Vue 3 + TypeScript
- 必須支援暗黑模式切換
- 必須有完整測試覆蓋
- 依賴現有 Backend API

## Goals / Non-Goals

**Goals:**
- Vuetify 3 MD3 完整配置，支援暗黑模式
- DefaultLayout 元件系統（AppBar + NavigationDrawer + RouterView）
- Pinia 狀態管理：Theme Store + Auth Store
- Dashboard.vue 主介面，呼叫 Backend API
- 完整測試基礎：Vitest + @vue/test-utils
- 各核心元件測試覆蓋

**Non-Goals:**
- 不修改 Backend API
- 不實作完整 Auth 流程（僅基礎 Store 結構）
- 不實作細節 Auth 功能（登入/登出）

## Decisions

1. **Vuetify Theme 管理**：使用 `createVuetify` 設定 MD3 主題，透過 Pinia Theme Store 控制暗黑模式切換
2. **Layout 結構**：採用 Composition API + defineAsyncComponent 實作，確保測試友好性
3. **測試框架**：Vitest 作為測試執行器，@vue/test-utils 作為元件測試工具
4. **API Service**：使用 axios 作為 HTTP 客戶端，封裝為 composable 用於測試 mock

## Risks / Trade-offs

[Risk] Vuetify 3 與 Vue 3 兼容性問題 → 使用官方建議的安裝方式
[Risk] 測試覆蓋率不足 → 從 proposal 中的 4 個 capability 出發，每個 capability 至少 1 個測試檔案
[Risk] Pinia 與 Vue 3 Composition API 整合複雜 → 使用 `@pinia/vue` 的 plugin 方式

## Migration Plan

1. 安裝依賴：Vuetify 3、Pinia、Vitest、Vue Test Utils
2. 建立 config.ts：Vuetify 主題設定、Pinia 設定
3. 建立 stores：theme.ts、auth.ts
4. 建立 layouts：DefaultLayout.vue
5. 建立 components：Dashboard.vue、ApiService.ts
6. 建立測試：vitest.config.ts、各元件測試檔案
7. 更新 package.json scripts

## Open Questions

- 是否需要為 Dashboard 新增圖表元件（如 Chart.js）
- 是否需要實作完整的 Auth 流程（登入/登出/權限）