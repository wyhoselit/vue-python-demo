Proposal 1：建立專案基礎結構（最優先）


/opsx:propose setup-project-skeleton



**目標：**
建立乾淨的 Monorepo 專案骨架，為 Vuetify + FastAPI 全端 Demo 打好基礎。

**要做的事情：**
1. 在 root 建立以下資料夾結構：
   - backend/
   - frontend/
   - docker/
   - docker-compose.yml
   - .env.example
   - README.md

2. backend 基本設定：
   - FastAPI 專案初始化（app/main.py）
   - requirements.txt（包含 fastapi, uvicorn, pydantic-settings 等）
   - 簡單的 /health 端點

3. frontend 基本設定：
   - Vue 3 + TypeScript + Vite 專案
   - 安裝 Vuetify 3
   - 基本 Vuetify 設定（plugins/vuetify.ts）
   - 簡單 Layout（AppBar + 一個 Hello World 頁面）

4. Docker 基礎：
   - docker-compose.yml（能同時啟動 backend + frontend）
   - 基本的 Dockerfile（backend 和 frontend）

5. README.md 寫清楚啟動指令

**要求：**
- 使用 TypeScript（frontend）
- 保持結構清晰、加上註解
- 暫時不要加入複雜功能（Auth、資料庫等留到後面）

請產生 proposal、design、tasks 文件，確認後再 apply。


## Proposal 2：Backend 核心設定（下一個做這個）

/opsx:propose enhance-fastapi-backend

**目標：**
在現有骨架基礎上，強化 Backend 成為企業級可維護結構。

**目前狀態：**
- 已存在基本的 FastAPI 專案（app/main.py 有 /health 端點）
- 使用 Podman 運行

**這次要新增/優化的項目：**

1. **Core 模組**
   - `app/core/config.py`：使用 Pydantic Settings 管理環境變數（DATABASE_URL, SECRET_KEY, DEBUG 等）
   - `app/core/database.py`：SQLAlchemy 引擎與 Session 管理（支援 PostgreSQL）
   - `app/core/security.py`：基本 JWT 設定（可先留空實作）

2. **API 結構**
   - 使用 APIRouter 建立版本控制：`app/api/v1/`
   - 建立 `app/api/v1/endpoints/__init__.py`
   - 把 health 端點移到 v1 底下，或保留 root

3. **其他基礎**
   - 中間件：CORS（允許 http://localhost:5173）
   - 全局例外處理
   - `main.py` 乾淨整合所有模組
   - 更新 requirements.txt（加入 sqlalchemy, alembic, psycopg2-binary, python-jose[cryptography], passlib[bcrypt] 等）

4. **Alembic 初始設定**
   - 產生 alembic 目錄與基本 migration 配置

**要求：**
- 保持與現有結構完全相容
- 所有新檔案加上清楚註解
- 更新 README.md 的 Backend 部分
- 確保 Podman / docker-compose 仍可正常運行

請先生成 proposal、design、tasks 文件，供我審核後再 apply。