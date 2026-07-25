## Context

`src/App.vue` 已正確整合 `DefaultLayout` 與 `<router-view />`。此設計文件將聚焦於驗證此整合的正確性，並確保相關配置（尤其是在 build 流程中排除測試檔案的設定）是健全的。

## Goals / Non-Goals

**Goals:**
- **驗證** `App.vue` 正確使用 `DefaultLayout` + `RouterView` 結構。
- **確認** `vite build` 與 `podman-compose build` 成功，且沒有來自測試檔案的類型錯誤。
- **驗證**所有測試通過 (`22 tests passing`)。

**Non-Goals:**
- 修改 `DefaultLayout.vue` 內容 (已確認其功能正常)。
- 修改路由配置。
- 修改 `Dashboard.vue`。

## Decisions

1. **App.vue 結構驗證**：確認 `<DefaultLayout><router-view /></DefaultLayout>` 結構的存在，且移除了多餘的 Vuetify 組件硬編碼。
2. **測試檔案排除**：確認 `tsconfig.json` 配置 `exclude` 屬性，明確排除 `__tests__` 目錄。
3. **`vitest.config.ts` 配置**：確認 `vitest.config.ts` 中的路徑解析（例如 `alias`）設置正確，且不與 `vue-tsc` 產生衝突。

## Risks / Trade-offs

[Risk] DefaultLayout 可能有依賴 Theme Store → 已在 `main.ts` 初始化 `themeStore.initTheme()`。
[Risk] RouterView 需要 vue-router → 已在 `main.ts` 註冊 `router`。
[Risk] `vue-tsc` 在 `npm run build` 時可能仍然包含測試檔案進行類型檢查 → 需仔細檢查 `tsconfig.json` 的 `exclude` 設置。

## Verification Plan

1. 執行 `npm run dev` 並確認新 Layout + Dashboard 正常顯示。
2. 執行 `npm run build` 並確認成功，且無來自測試檔案的類型錯誤。
3. 執行 `npm test` 並確認所有測試通過 (22 tests passing)。
4. 執行 `podman-compose build` 並確認成功。