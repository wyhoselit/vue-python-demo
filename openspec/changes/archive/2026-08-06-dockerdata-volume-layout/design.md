## Context
目前開發環境與正式環境的資料持久化配置混亂，且未預留未來擴充路徑。開發團隊需要一個統一、一致的 docker 磁碟掛載架構，以便在 host 端輕鬆管理與備份資料。

## Goals / Non-Goals

**Goals:**
- 建立標準化的 `dockerdata/` 目錄樹。
- 透過 docker-compose 掛載機制實現環境隔離 (dev/prod)。
- 確保所有持久化資料 (資料庫、日誌、上傳) 皆從 container 抽離。

**Non-Goals:**
- 目前不處理 Docker 網路架構變更。
- 目前不導入外部雲端儲存服務 (如 S3)。

## Decisions

- **統一掛載目錄**: 所有持久化資料置於專案根目錄的 `dockerdata/` 下。
- **目錄分隔策略**: 依 `dockerdata/{env}/{service}/{type}/` 結構分類，例如 `dockerdata/dev/backend/data`。
- **環境差異化配置**:
    - `docker-compose.yml` (dev) 直接掛載 `./dockerdata/dev`。
    - `docker-compose.prod.yml` (prod) 掛載 `./dockerdata/prod`。

## Risks / Trade-offs

- [Host 資料夾權限] → 容器內可能會遇到寫入權限問題，需確保 host 目錄擁有適當的 uid/gid。
- [掛載點衝突] → 當容器已掛載路徑被修改時，可能導致已存在的資料無法讀取。
