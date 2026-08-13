# 新增功能完整開發流程

> 工具組合：OpenSpec · codebase-memory · OpenWiki · GitNexus · mattpocock/skills  
> 適用於 AI coding agent（Cursor / Claude Code / Codex 等）

---

## 工具角色一覽

| 工具 | 在流程中的角色 |
|------|----------------|
| **OpenSpec** | 變更的主骨架（proposal → design → tasks → 實作 → archive） |
| **mattpocock/skills** | 對齊、領域語言、TDD、架構深化、review 紀律 |
| **codebase-memory** | 即時結構情報（呼叫鏈、影響範圍、架構查詢） |
| **GitNexus** | 架構地圖、blast radius、可交付的 mermaid 文件 |
| **OpenWiki** | 給人看／給 agent 長期讀的敘事文件（模組說明、流程說明） |

---

## 一、專案啟動（每個 repo 做一次）

```text
1. Index this project                    ← codebase-memory
2. gitnexus analyze（或你平常用的 index） ← GitNexus
3. openwiki --init（或更新 wiki）        ← OpenWiki
4. openspec init                         ← OpenSpec
5. /setup-matt-pocock-skills             ← mattpocock
```

在 `CLAUDE.md` / `AGENTS.md` 加入固定規則，避免工具搶戲：

```markdown
## Tool priority for this repo
- Structure / call graph / change impact → codebase-memory first, GitNexus second
- Human-readable architecture docs → OpenWiki + GitNexus generate_map
- Feature workflow → OpenSpec (opsx) is the spine
- Alignment, domain language, TDD, architecture deepening → mattpocock skills
- Prefer graph tools over reading many files
```

---

## 二、新增功能完整流程（主線）

### Phase 0 — 想法還很模糊（可選）

| 步驟 | 你做什麼 | 工具 |
|------|----------|------|
| 0.1 | `/opsx:explore` 或 `/grill-with-docs` | OpenSpec / mattpocock |
| 0.2 | 對 AI：「用 codebase-memory 與 GitNexus 看現有架構與相關呼叫鏈」 | codebase-memory + GitNexus |
| 0.3 | 需要給人看的現況說明 → 開 OpenWiki 相關頁，或 `/gitnexus:generate_map` | OpenWiki / GitNexus |

**產出：** 共同理解；必要時更新的 `CONTEXT.md` / ADR（來自 grill-with-docs）。

---

### Phase 1 — 開變更、寫規格（先對齊再寫碼）

| 步驟 | 指令 / 動作 | 說明 |
|------|-------------|------|
| 1.1 | `/opsx:new <功能名>` 或 `/opsx:propose <功能名>` | 建立 change 資料夾 |
| 1.2 | 需要一次出齊文件 → `/opsx:ff` | 產生 proposal / design / tasks / specs |
| 1.3 | 想逐步 refinement → `/opsx:continue` | 一件件補 artifact |
| 1.4 | 設計卡關時 → `/grill-with-docs` | 邊問邊寫進 CONTEXT.md / ADR |
| 1.5 | 對 AI 要求：「設計前先用 graph 查現有模組與呼叫關係」 | codebase-memory / GitNexus |

**你要人工審核的東西：**

- `proposal.md`（為什麼做、範圍）
- `design.md`（技術取捨）
- `tasks.md`（可勾選清單）
- `specs/`（需求 delta）

> **未同意前不要進 apply。**

---

### Phase 2 — 實作（規格驅動 + TDD）

| 步驟 | 指令 / 動作 | 工具 |
|------|-------------|------|
| 2.1 | `/opsx:apply` | 依 tasks 逐項實作 |
| 2.2 | 明確要求用 TDD 時 → 讓 agent 走 `/tdd`，或在 apply 時說「每個 task 用 red-green-refactor」 | mattpocock |
| 2.3 | 碰到「誰呼叫誰、改哪會炸」→ 用 `trace_path` / `detect_changes` / GitNexus impact | codebase-memory / GitNexus |
| 2.4 | 中途規格變了 → 先改 OpenSpec artifacts，再繼續 apply | OpenSpec |

**實作時可貼給 AI 的固定提醒：**

> 實作時優先用 codebase-memory 查呼叫鏈與影響範圍；每個 task 完成後勾選 tasks.md；不確定行為先寫 failing test。

---

### Phase 3 — 驗證與影響分析

| 步驟 | 指令 / 動作 | 工具 |
|------|-------------|------|
| 3.1 | `/opsx:verify`（若有） | 對照 specs / tasks 完整性 |
| 3.2 | `/codebase-memory-mcp:review_change_impact` 或 GitNexus `detect_impact` | 變更 blast radius |
| 3.3 | `/code-review` | Standards + Spec 雙軸 review |
| 3.4 | 跑測試、必要時修 | `/tdd` 或 `/diagnosing-bugs` |

通過後再進入下一階段。

---

### Phase 4 — 收尾與文件同步

| 步驟 | 指令 / 動作 | 工具 |
|------|-------------|------|
| 4.1 | `/opsx:archive` | delta specs 併回主 specs，變更進 archive |
| 4.2 | 大改結構後：`Index this project` + 必要時重跑 GitNexus analyze | codebase-memory / GitNexus |
| 4.3 | 更新敘事文件：`openwiki --update` 或針對改動模組更新 wiki | OpenWiki |
| 4.4 | 需要對外／對團隊的架構圖 → `/gitnexus:generate_map` | GitNexus |
| 4.5 | 領域詞或決策有變 → 確認 `CONTEXT.md` / ADR 已更新 | mattpocock |

---

## 三、功能開發 Checklist（可直接勾）

```text
[ ] 0. 模糊想法？ → /opsx:explore 或 /grill-with-docs + graph 探索
[ ] 1. /opsx:new 或 /opsx:propose <功能名>
[ ] 2. /opsx:ff（或 continue）→ 審 proposal / design / tasks / specs
[ ] 3. 同意後 → /opsx:apply（搭配 /tdd）
[ ] 4. 實作中用 codebase-memory / GitNexus 查呼叫與影響
[ ] 5. /opsx:verify + review_change_impact + /code-review
[ ] 6. /opsx:archive
[ ] 7. 更新 index（codebase-memory / GitNexus）+ OpenWiki + 必要時 generate_map
```

---

## 四、工具優先順序（避免重疊）

| 需求 | 優先用 | 不要 |
|------|--------|------|
| 「這個函數誰呼叫？」 | codebase-memory `trace_path` | 大量讀檔 |
| 「這次 diff 影響範圍」 | codebase-memory 或 GitNexus impact | 只靠感覺 |
| 「給新人看的架構說明」 | OpenWiki + GitNexus map | 只留在聊天裡 |
| 「這次功能要做到什麼」 | OpenSpec artifacts | 只靠口頭 |
| 「我們領域詞是什麼」 | CONTEXT.md（grill-with-docs） | 每次重新發明 |
| 「怎麼寫才測得穩」 | `/tdd` | 先寫一堆再補測 |

**codebase-memory 與 GitNexus 都是圖：**

- **日常查詢、省 token** → codebase-memory
- **架構地圖、文件化、impact prompt** → GitNexus

兩者可並存；同一問題先問一個即可，不必兩個都跑一遍。

---

## 五、依功能規模縮放

### 小改（半小時內、不碰核心架構）

```text
簡短說明 → 直接改（必要時 /tdd）→ review_change_impact → 提交
```

可跳過完整 OpenSpec；若之後要進主規格，再補一個小 change 並 archive。

### 中大型功能（推薦完整主線）

完整走 Phase 0～4。

### 跨多 session 的大工程

OpenSpec 當變更主軸 + mattpocock `/wayfinder` 管決策票；每個 session 用 OpenSpec tasks 續接。

---

## 六、常用指令速查

### OpenSpec

| 指令 | 用途 |
|------|------|
| `/opsx:explore` | 探索想法，不寫檔 |
| `/opsx:new <name>` / `/opsx:propose <name>` | 開新變更 |
| `/opsx:ff` | 一次產生全部規劃文件 |
| `/opsx:continue` | 逐步補齊 artifact |
| `/opsx:apply` | 依 tasks 實作 |
| `/opsx:verify` | 驗證實作完整性 |
| `/opsx:archive` | 歸檔並合併 specs |

### mattpocock/skills

| 指令 | 用途 |
|------|------|
| `/setup-matt-pocock-skills` | 每個 repo 設定一次 |
| `/grill-with-docs` | 對齊設計 + 寫 CONTEXT.md / ADR |
| `/tdd` | red-green-refactor |
| `/code-review` | Standards + Spec 雙軸 review |
| `/improve-codebase-architecture` | 定期掃可深化的模組 |
| `/diagnosing-bugs` | 難解 bug 診斷迴圈 |
| `/ask-matt` | 不確定用哪個 skill 時 |

### codebase-memory

| 動作 | 用途 |
|------|------|
| `Index this project` | 建立／更新知識圖譜 |
| `search_graph` / 語意搜尋 | 找符號、模組 |
| `trace_path` | 追蹤呼叫鏈 |
| `get_architecture` | 架構總覽 |
| `detect_changes` / `review_change_impact` | 變更影響範圍 |

### GitNexus

| 動作 | 用途 |
|------|------|
| `gitnexus analyze` | 索引 repo |
| `impact` / `detect_impact` | blast radius |
| `/gitnexus:generate_map` | 產生架構文件與 mermaid |

### OpenWiki

| 動作 | 用途 |
|------|------|
| `openwiki --init` | 首次建立 wiki |
| `openwiki --update` | 依程式變更更新文件 |

---

## 七、建議養成的習慣

1. **大改前先對齊**：explore 或 grill-with-docs，再寫 OpenSpec。
2. **實作前先看圖**：用 codebase-memory / GitNexus 確認模組與呼叫關係。
3. **實作走 tasks + TDD**：勾選 tasks.md，不確定行為先寫 failing test。
4. **提交前看影響**：review_change_impact 或 detect_impact。
5. **收尾同步文件**：archive → 更新 graph → 更新 OpenWiki → 必要時 generate_map。

---

*文件產生日期：2026-08-13*
