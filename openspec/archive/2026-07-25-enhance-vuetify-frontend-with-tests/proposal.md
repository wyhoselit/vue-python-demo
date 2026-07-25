## Why

Vue + Vuetify 前端需升級為專業 AI 平台介面，並完整覆蓋測試。目前前端僅為基本 Vuetify 專案，缺乏暗黑模式、狀態管理、元件化設計及測試覆蓋。AI 平台上線後，UI/UX 質量直接影響使用者體驗與信任度。

## What Changes

- Vuetify 3 MD3 完整配置：主題切換、暗黑模式、自訂 Icon
- 建立 DefaultLayout 元件系統：AppBar + NavigationDrawer + RouterView
- 引入 Pinia 狀態管理：Theme Store (暗黑模式切換) + Auth Store (基礎認證)
- 建立 Dashboard.vue 主介面：多元 Vuetify 元件組合 + Backend API 整合
- 完整測試基礎建設：Vitest + @vue/test-utils + vitest.config.ts
- 各核心元件測試：Layout、Theme Store、Dashboard、API Service
- 更新 README.md：包含測試執行說明

## Capabilities

### New Capabilities

- `vuetify-layout`: DefaultLayout 元件系統與響應式設計
- `theme-management`: 暗黑模式與主題切換狀態管理
- `dashboard-ui`: AI 平台儀表板介面設計
- `api-testing`: API Service 的 mock 測試與整合測試

### Modified Capabilities

- `testing-infrastructure`: 新增 Vitest 測試框架與 configurations

## Impact

- 前端目錄結構調整：新增 layouts、stores、components、tests
- package.json 依賴：新增 Vuetify 3、Pinia、Vitest、Vue Test Utils
- 需要更新 CI/CD 流程：加入測試步驟
- Backend API 需確保 CORS 設定支援前端請求