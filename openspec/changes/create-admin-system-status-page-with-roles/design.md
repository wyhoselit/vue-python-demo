## Context
系統目前缺乏使用者角色管理 (RBAC) 與後端監控機制。這導致沒有辦法將權限分配給不同等級的使用者，且維運團隊難以即時掌握系統健康狀況。

## Goals / Non-Goals
**Goals:**
- 實作使用者 Role 模型，預設為 `user`。
- 建立 Admin 權限，擁有檢視系統狀態的權限。
- 實作 Admin 專用 API，包含 Log 查看與系統資訊查詢。
- 前端 Admin 狀態頁面監控。

**Non-Goals:**
- 複雜的細粒度權限控制 (目前僅需區分 Admin/User)。
- Admin 修改 Log 或刪除使用者帳號的功能 (超出範圍)。

## Decisions
- **Role 設計**：新增 `roles` table，User 與 Role 為 Many-to-Many 關聯，以靈活彈性擴充。
- **Admin API 認證**：在 FastAPI 加入 Dependency (`check_admin_role`) 檢查 Token 是否具有 Admin role。
- **Database Migration**：使用 Alembic 進行版本控制，新增 `Role` table 與 User 關聯表，包含預設 Admin 帳號種子資料。
- **Testing Strategy**：
  - **Backend**：使用 pytest 編寫 Unit/Integration tests，涵蓋角色權限驗證與 Admin API 邊界案例。
  - **Frontend**：模擬 Admin 與 User 登入情境，驗證路由守衛與 UI 顯示正確性，並編寫端對端測試 (Playwright)。

## Risks / Trade-offs
- [安全風險]：Admin API 權限若有漏洞，可能導致敏感資訊外洩。→ 嚴格檢查 Role 與 Token。
- [效能影響]：Log 查看若檔案過大，需限制讀取區塊。→ API 設定最大行數與檔案大小限制。
