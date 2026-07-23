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


## 執行完 Proposal 2 後的建議

執行 /opsx:apply


Change: enhance-fastapi-backend
Schema: spec-driven
Progress: 22/22 tasks complete ✓
Completed This Session
- 1.1 Create backend/app/core/__init__.py
- 1.2 Create backend/app/core/config.py with Pydantic Settings class
- 1.3 Add pydantic-settings to backend/requirements.txt
- 2.1 Create backend/app/core/database.py with SQLAlchemy engine setup
- 2.2 Add database dependencies: sqlalchemy, psycopg2-binary to backend/requirements.txt
- 2.3 Create backend/app/core/security.py with JWT stub
- 3.1 Create backend/app/api/__init__.py
- 3.2 Create backend/app/api/v1/__init__.py with APIRouter
- 3.3 Create backend/app/api/v1/endpoints/__init__.py
- 3.4 Create backend/app/api/v1/endpoints/health.py with health endpoint
- 4.1 Add CORS middleware configuration to main.py
- 4.2 Add global exception handlers to main.py
- 4.3 Refactor backend/app/main.py to integrate all modules
- 5.1 Initialize Alembic in backend directory
- 5.2 Configure alembic/env.py to use database URL from settings
- 5.3 Create initial empty migration
- 6.1 Update backend/requirements.txt with all new dependencies
- 6.2 Update README.md with backend architecture documentation
- 6.3 Rebuild containers with podman-compose up -d --build
- 6.4 Verify /health endpoint returns {"status": "ok"}
- 6.5 Verify /api/v1/health endpoint returns {"status": "ok"}
- 6.6 Verify CORS headers present for localhost:5173
All tasks complete! You can archive this change with /opsx-archive.


立即驗證 Checklist（依序執行）
請在終端機執行以下指令：
1. 重啟 Backend（重要）
Bash# 如果使用 podman-compose
podman-compose down
podman-compose up -d --build

# 或直接用 uvicorn 開發模式測試
cd backend
uvicorn app.main:app --reload --port 8000

2. 基本健康檢查
```Bash
# Root health
curl http://localhost:8000/health
```

# v1 API health
```
curl http://localhost:8000/api/v1/health
```

預期結果：兩個都回傳 {"status":"ok"}
3. 驗證 CORS（最重要）
```Bash
curl -H "Origin: http://localhost:5173" \
     -H "Access-Control-Request-Method: GET" \
     -X OPTIONS http://localhost:8000/api/v1/health -v
```

檢查 Response Headers 中是否有：
Access-Control-Allow-Origin: http://localhost:5173
Access-Control-Allow-Methods: ...
Access-Control-Allow-Headers: ...

4. 檢查設定檔是否正確載入
```bash
curl http://localhost:8000/api/v1/config/debug   # 如果有這個端點
```
# 或直接看 l   ogs 是否有正確載入 DATABASE_URL 等設定
1. 檢查資料庫連線（Alembic）
```bash
# 進入正在運行的 backend 容器
podman exec -it demo_backend_1 bash
alembic init -t async alembic
# 在容器內執行
alembic current          # 看 migration 狀態
alembic upgrade head     # 執行 migration（如果還沒跑）
```

```
/opsx:propose fix-alembic-configuration

**目標：**
永久修正 Alembic 配置，讓每次 build Docker 容器時都能正確初始化 migration。

**要修正的地方：**

1. **alembic.ini**
   - 把 sqlalchemy.url 改成從 config 讀取（或使用環境變數）
   - 設定正確的 script_location

2. **alembic/env.py**
   - 從 `app.core.config` import settings
   - 使用 `settings.DATABASE_URL` 作為連線字串
   - 支援 async engine

3. **backend/Dockerfile**
   - 確保 alembic 初始化相關檔案被正確 copy
   - 在 Dockerfile 的 CMD 或 entrypoint 中可選加入 alembic upgrade head（開發階段可選）

4. **docker-compose.yml**
   - 確認 postgres 服務名稱正確（讓 alembic 可以連到 db）

**要求：**
- 修正後 alembic upgrade head 在容器內可以正常執行
- 保持與之前 Proposal 的相容性
- 更新 README.md 的 migration 操作說明

請先生成 proposal 和 design 讓我確認。

```
/opsx-apply

```
Change: fix-alembic-configuration
Schema: spec-driven
Progress: 16/16 tasks complete ✓
Completed This Session
- 1.1 Modify backend/alembic.ini: Set sqlalchemy.url to a dummy value
- 1.2 Modify backend/alembic.ini: Ensure script_location is set correctly
- 2.1-2.5 Modify backend/alembic/env.py: Fixed imports and sys.path
- 3.1 Modify backend/Dockerfile: Copy alembic files
- 4.1-4.3 Create entrypoint script and update Dockerfile
- 5.1 Update README.md with Alembic instructions
- 6.1-6.4 Verification tasks complete
All tasks complete!
```

```bash
podman-compose down
podman-compose up -d --build
podman-compose exec backend alembic current
podman-compose exec backend alembic upgrade head     # 執行 migration（如果還沒跑）
```

1. Swagger 文件確認
開啟瀏覽器訪問：

http://localhost:8000/docs
http://localhost:8000/redoc

應該能看到乾淨的 API 文件，且有 health 端點。

