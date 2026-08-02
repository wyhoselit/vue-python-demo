# API 版本管理與 Fallback 設計提案

## 目標
建立一個支援 API 版本化 (v1, v2) 的架構，具備以下特性：
1. **模組隔離**：v2 的新功能置於 `app/modules/v2/`。
2. **自動 Fallback**：若 v2 對應模組不存在，自動路由至 v1。

## 方案選擇：Router Delegation (推薦)

建議採用「顯式路由聚合」策略。此策略利用 FastAPI 的路由層級管理，透過一個 Dispatcher Router 來控制流量，既維持 FastAPI 的靜態型別優勢，又具備自動 Fallback 能力。

### 路由結構建議

```text
app/api/
├── v1/
│   └── router.py (聚合所有 v1 模組)
├── v2/
│   └── router.py (聚合 v2 模組，fallback 至 v1)
└── router.py (總入口)
```

### 關鍵機制：Dispatcher 聚合

在 `v2/router.py` 中進行選擇性註冊：

```python
# 範例 pseudo-code
from fastapi import APIRouter
from app.modules.v2.admin import router as admin_v2
from app.api.v1.endpoints import users as users_v1

v2_router = APIRouter()

# 1. 註冊 v2 已實作模組
v2_router.include_router(admin_v2, prefix="/admin")

# 2. 為未實作模組註冊 v1 fallback
# 針對 /api/v2/users 自動 fallback 至 v1
v2_router.include_router(users_v1, prefix="/users")
```

## 風險分析
| 方案 | 優點 | 缺點 |
| :--- | :--- | :--- |
| **Router Delegation** | 型別安全、易於測試、路由邊界清晰 | 需維護一份顯式的 fallback 清單 |
| **Middleware Rewrite** | 路由自動化、對 Controller 透明 | 請求上下文可能在 Rewrite 後變複雜 |

---

### 下一步決策
1. 是否接受「顯式聚合」帶來的維護負擔？
2. 是否有特定的模組需要優先實作 Fallback？
