## Why

Dashboard 目前顯示靜態假資料（Total Users: 0, Active Sessions: 0, API Calls: 0），且 Data Table 為空。前端雖有 `useApi` composable，但未正確串接後端 API。後端僅有 `/health` 端點，缺乏 `/dashboard/stats` 與 `/users` 端點。需完整實作資料流：Backend 新增端點 → Frontend 真實呼叫 → Loading/Error 狀態 → 測試驗證。

## What Changes

### Backend
- 新增 `app/api/v1/endpoints/dashboard.py`：`GET /dashboard/stats` 回傳統計數據
- 新增 `app/api/v1/endpoints/users.py`：`GET /users` 回傳使用者列表
- 更新 `app/api/router.py` 註冊新端點
- 新增對應的 pytest 測試

### Frontend
- 更新 `Dashboard.vue`：真實呼叫 API、顯示 Loading、Error 狀態、格式化數字
- 確認 `useApi` composable 正確運作（baseURL、interceptors）
- 更新對應的 Vitest 測試（mock API）

### 品質與架構確認
- `gitnexus analyze .` 更新知識圖
- `gitnexus wiki .` 更新結構文件
- `openwiki --update` 更新 Agent Wiki
- 檢查無破壞 Layout / Router / Store 結構
- 更新 OpenSpec specs（新增 dashboard-stats、users-list capabilities）

### 文件
- 更新 `README.md` 記錄新端點與資料流

## Capabilities

### New Capabilities
- `backend-dashboard-stats`: Dashboard 統計數據 API 端點
- `backend-users-list`: 使用者列表 API 端點
- `frontend-dashboard-real-data`: Dashboard 真實資料整合與狀態處理

### Modified Capabilities
- `backend-api-versioning`: 新增 dashboard、users 端點
- `frontend-dashboard`: 改為真實 API 整合

## Impact

- 新增：`backend/app/api/v1/endpoints/dashboard.py`, `users.py`
- 新增：`backend/tests/test_dashboard.py`, `test_users.py`
- 修改：`backend/app/api/router.py`
- 修改：`frontend/src/views/Dashboard.vue`
- 修改：`frontend/src/__tests__/views/Dashboard.test.ts`
- 更新：`README.md`
- 更新：OpenSpec specs（6 檔）