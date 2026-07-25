## Context

目前 Dashboard 使用靜態資料，前端有 `useApi` composable 但未正確串接後端。後端只有 `/health` 端點，缺乏 dashboard stats 和 users 端點。需建立完整的資料流：Backend API → Frontend API Service → Dashboard View → UI Components。

## Goals / Non-Goals

### Goals
- Backend 新增 `GET /api/v1/dashboard/stats` 回傳統計數據
- Backend 新增 `GET /api/v1/users` 回傳使用者列表
- Frontend Dashboard 真實呼叫 API、處理 Loading/Error 狀態
- 完整測試覆蓋（Backend pytest + Frontend Vitest）
- GitNexus 知識圖更新、OpenSpec specs 同步

### Non-Goals
- 資料庫真實模型建立（目前用假資料 mock）
- 認證/授權機制
- WebSocket 即時更新
- 分頁/搜尋/排序功能

## Decisions

### 1. Dashboard Stats Endpoint
**Choice**: 新增 `/dashboard/stats` 回傳固定結構 JSON
```json
{"total_users": 1250, "active_sessions": 42, "api_calls_24h": 15420}
```
**Rationale**: 簡單、明確、前端易於格式化。後續可換成真實 DB 查詢。

### 2. Users List Endpoint
**Choice**: 新增 `/users` 回傳使用者陣列
```json
[{"id": 1, "name": "Alice Chen", "email": "alice@example.com", "status": "active"}, ...]
```
**Rationale**: 符合前端 Data Table 需求，結構簡單。

### 3. Frontend API Calls Pattern
**Choice**: 在 `onMounted` 中並行呼叫 `stats` 和 `users`，使用 `Promise.all`
**Rationale**: 減少總等待時間，提升 UX。

### 4. Loading/Error State Management
**Choice**: 使用 Vue 3 `<script setup>` 的 `ref` 管理 `loading`、`error`、`stats`、`users`
**Rationale**: 簡潔、響應式、符合現有代碼風格。

### 5. Error Handling Strategy
**Choice**: `useApi` 的 interceptor 攔截 401/500，拋出標準錯誤；Dashboard 捕獲並顯示 `v-alert`
**Rationale**: 集中錯誤處理，UI 只需關注顯示。

## Risks / Trade-offs

| Risk | Mitigation |
|------|------------|
| API 回應格式不一致 | 定義明確的 TypeScript 介面，Backend 使用 Pydantic 模型驗證 |
| 前端測試 mock 不完整 | 使用 `vi.mock` 完整模擬 `useApi` 回傳值 |
| GitNexus 索引過期 | 變更完成後立即執行 `gitnexus analyze .` |
| 破壞既有 Layout/Router | 變更前執行完整測試套件，確認 22 tests passing |

## Migration Plan

1. **Backend**: 新增 dashboard.py、users.py 端點 → 更新 router.py → 新增測試
2. **Frontend**: 更新 Dashboard.vue → 更新測試
3. **驗證**: 執行完整測試（Backend + Frontend）
4. **文檔**: 更新 OpenSpec specs → gitnexus analyze/wiki → README