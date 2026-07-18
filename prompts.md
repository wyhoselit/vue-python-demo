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