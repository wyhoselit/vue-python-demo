## Why
目前的系統缺乏權限管理與 Admin 狀態監控，導致管理員無法有效維護系統健康與控制用戶訪問。

## What Changes
- 新增 `Role` 模型與使用者權限管理系統。
- 新增 `/api/v1/admin/` 系統監控與除錯 API。
- 新增前端 `AdminStatus.vue` 頁面與權限路由守衛。
- 預設 Admin 使用者自動建立機制。

## Capabilities

### New Capabilities
- `role-management`: 使用者角色模型與存取控制 (RBAC)。
- `admin-system-status`: 系統資訊與 Log 監控 API。

### Modified Capabilities
- `user-auth`: 註冊時預設賦予使用者權限。

## Impact
- 修改 `User` 模型與資料庫 Schema。
- 新增後端 Admin API 端點。
- 前端路由與 UI 元件新增。
