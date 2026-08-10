# Docker Data Persistence Setup

本專案已更新 Docker 資料持久化架構，將所有資料集中管理至 `dockerdata/` 目錄，並分離開發與正式環境。

## 目錄結構
```text
dockerdata/
├── dev/
│   ├── backend/
│   │   ├── data/    # 存放 app.db, dev.db, test.db
│   │   └── logs/    # 存放 app.log
│   └── frontend/
│       └── nginx/   # nginx 設定檔
└── prod/
    ├── backend/
    │   ├── data/    # 正式環境資料
    │   └── logs/    # 正式環境日誌
    └── frontend/
        └── nginx/   # 正式環境 nginx 設定
```

## 使用說明

### 1. 開發環境
使用預設 `docker-compose.yml` (對應 `dockerdata/dev/`)：
```bash
podman-compose up -d --build
```

### 2. 正式環境
結合 `docker-compose.yml` 與 `docker-compose.prod.yml` (對應 `dockerdata/prod/`)：
```bash
podman-compose -f docker-compose.yml -f docker-compose.prod.yml up -d --build
```
