## Why

App.vue 已正確使用 `<DefaultLayout />` 包裹 `<router-view />`，但原 proposal 描述的「硬編碼 Hello World」問題已在實作中解決。此變更聚焦於：
1. 驗證現有實作符合規範
2. 確保 build 配置正確排除測試檔
3. 建立自動化檢查機制防止未來回歸

## What Changes

- 驗證 `src/App.vue` 已正確使用 DefaultLayout 結構
- 確認 `tsconfig.json` 與 `vitest.config.ts` 配置不干擾 build
- 建立 App.vue Layout 整合的自動驗證規則

## Capabilities

### Modified Capabilities

- `frontend-proposal-validation`: 強制檢查 App.vue 是否正確使用 Layout 結構

## Impact

- `src/App.vue` - 驗證現有實作
- `tsconfig.json` - 確保測試檔排除
- `vitest.config.ts` - 確認測試配置
- Docker 部署 - podman-compose build