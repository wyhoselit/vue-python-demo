## 1. 資料庫層與遷移
- [x] 1.1 新增 User Role 定義與關聯模型
- [x] 1.2 建立 Alembic Migration 檔案以建立 Roles 與 UserRoles
- [x] 1.3 更新 User 模型以支援 Roles 關聯
- [x] 1.4 實作 Admin 預設帳號初始化與 Migration Seed

## 2. 後端 Admin API 實作
- [x] 2.1 實作 Admin 權限檢查 Dependency
- [x] 2.2 實作 GET /api/v1/admin/system-info
- [x] 2.3 實作 GET /api/v1/admin/logs

## 3. 前端 Admin 頁面與整合
- [x] 3.1 新增 AdminStatus 頁面與 API 對接
- [x] 3.2 加入 Vue Router 權限守衛
- [x] 3.3 側邊欄權限顯示邏輯

## 4. 測試計畫
- [x] 4.1 編寫 Backend 權限檢查測試 (pytest)
- [x] 4.2 編寫 Admin API 功能測試 (pytest)
- [x] 4.3 編寫前端 路由權限測試 (Vitest/Playwright)
