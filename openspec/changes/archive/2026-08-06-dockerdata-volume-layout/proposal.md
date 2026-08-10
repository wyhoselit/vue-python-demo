## Why
目前的開發環境 Docker 設定未統一掛載資料目錄，導致資料持久化分散在 host 與容器內，且未區分開發與正式環境配置，不利於資料管理與正式環境部署。

## What Changes
- 統一建立 `/dockerdata` 目錄結構以區分開發 (dev) 與正式 (prod) 環境。
- 修改 `docker-compose.yml` 將資料庫、日誌與上傳檔案掛載至統一目錄。
- 建立 `docker-compose.prod.yml` 作為正式環境部署配置。

## Capabilities

### New Capabilities
- `dockerdata-structure`: 建立符合規範的掛載目錄結構，確保環境一致性。
- `env-specific-persistence`: 區分 dev/prod 的資料持久化掛載路徑與邏輯。

### Modified Capabilities

## Impact
- 修改 `docker-compose.yml` 掛載設定。
- 新增 `docker-compose.prod.yml`。
- 修改 `backend/app/modules/core/config.py` 中的資料儲存路徑。
