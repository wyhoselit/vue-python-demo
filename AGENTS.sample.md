# AGENTS.md

Project instructions for OpenCode (and compatible agents).  
Edit the placeholders marked `TODO` to match this repository.

---

## Project overview

- **Name:** TODO (e.g. demo.vuejspython)
- **Stack:** TODO (e.g. Vue 3 + Python FastAPI / TypeScript monorepo)
- **Package manager:** TODO (`pnpm` / `npm` / `bun` / `uv` / `poetry`)
- **Default branch:** TODO (`main` or `master`)

---

## Commands

Run these from the project root unless noted.

### Install

```bash
# TODO: e.g. pnpm install | npm ci | bun install | uv sync
```

### Dev

```bash
# TODO: e.g. pnpm dev | npm run dev | bun run dev
```

### Build

```bash
# TODO: e.g. pnpm build | npm run build
```

### Test

```bash
# TODO: e.g. pnpm test | npm test | pytest | bun test
```

### Lint / typecheck

```bash
# TODO: e.g. pnpm lint && pnpm typecheck
```

### Format

```bash
# TODO: e.g. pnpm format | npm run format
```

### Useful one-liners

```bash
# Full local check before PR (adjust to real scripts)
# TODO: pnpm lint && pnpm typecheck && pnpm test && pnpm build
```

---

## Conventions

- Prefer small, focused changes; one concern per commit when practical.
- Follow existing patterns in the touched area; do not invent a parallel style.
- TODO: language/style rules (e.g. TypeScript strict, no `any`, named exports).
- TODO: test expectations (e.g. unit tests next to code, or under `tests/`).
- Commit messages: conventional style when possible (`feat:`, `fix:`, `docs:`, `refactor:`, `test:`, `chore:`).
- Do not push directly to the default branch; use a feature branch + PR.

---

## Tooling priority (OpenCode)

This repo uses multiple layers. Pick the right tool; do not run every tool on every task.

| Need | Prefer | Fallback |
|------|--------|----------|
| Spec / change lifecycle | **OpenSpec** (`/opsx:*` or openspec skills) | — |
| Alignment, domain language, TDD, review, architecture deepening | **mattpocock skills** (via skill tool) | — |
| Call graph, symbol search, everyday impact | **codebase-memory** MCP | GitNexus |
| Architecture map, process flows, coordinated rename, formal blast radius | **GitNexus** MCP | codebase-memory |
| Narrative docs for humans/agents | **OpenWiki** | GitNexus generate_map |

**Default:** prefer graph tools (codebase-memory / GitNexus) over reading many files when exploring structure, callers, or impact.

### OpenSpec (change spine)

- Non-trivial feature: explore (optional) → propose/new → user accepts artifacts → apply → verify → archive.
- Do not implement before the user accepts proposal/design/tasks in a full OpenSpec flow.
- Tiny typo / docs / test-only fixes may skip OpenSpec; still prefer tests + a light impact check.

### mattpocock skills

- Load with the skill tool when the task matches:
  - `grill-with-docs` — alignment + CONTEXT.md / ADRs
  - `tdd` — red-green-refactor
  - `code-review` — standards + spec review
  - `improve-codebase-architecture` — periodic deepening survey
  - `diagnosing-bugs` — hard bugs
  - `ask-matt` — which skill/flow to use
  - `setup-matt-pocock-skills` — once per repo if not configured
- Skills may live under `.opencode/skills/`, `.claude/skills/`, or `.agents/skills/`.

### codebase-memory MCP

- After large refactors: say **Index this project** (or run `index_repository`).
- Everyday structure: `search_graph`, `trace_path`, `get_architecture`, `detect_changes` / change-impact tools.
- Prefer these for “who calls X?” and “what does this diff touch?”

### GitNexus

- Indexed as: **TODO** (e.g. `demo.vuejspython`) — update this name if the index id changes.
- Index stale? From project root:
  ```bash
  node .gitnexus/run.cjs analyze
  # or: npx gitnexus analyze
  ```
- **Before editing a non-trivial symbol** (shared API, core domain, multi-caller code): run impact (upstream) and report blast radius / risk to the user.
- **Before committing non-trivial work:** run `detect_changes()` (optionally compare to default branch).
- Warn on HIGH / CRITICAL impact before proceeding with edits.
- Unfamiliar areas: `query` / `context` instead of blind grep.
- Graph-aware renames: GitNexus `rename`, not find-and-replace.
- Skip full impact for pure one-line typo / docs / test-only changes.

Resources (adjust repo id):

- `gitnexus://repo/TODO/context`
- `gitnexus://repo/TODO/clusters`
- `gitnexus://repo/TODO/processes`

Skills (if present): `.claude/skills/gitnexus/` or `.opencode/skills/` for exploring / impact / debugging / refactoring / CLI.

### OpenWiki

This repository uses OpenWiki for recurring code documentation. Start with `openwiki/quickstart.md`, then follow its links to architecture, workflows, domain concepts, operations, integrations, testing guidance, and source maps.

The scheduled OpenWiki GitHub Actions workflow refreshes the repository wiki.  
Do not hand-edit generated OpenWiki pages unless explicitly asked; prefer updating source code/docs and letting OpenWiki regenerate (`openwiki --update` or the CI workflow).

---

## Feature workflow (short)

```text
1. Fuzzy idea  → opsx explore or grill-with-docs + graph explore
2. OpenSpec    → propose/new → review proposal / design / tasks / specs
3. Implement   → apply + tdd; use codebase-memory / GitNexus for callers & impact
4. Verify      → opsx verify + change impact + code-review (non-trivial)
5. Close out   → archive → refresh indexes → OpenWiki update if docs should change
```

Checklist:

```text
[ ] Explore / grill if the problem is fuzzy
[ ] OpenSpec artifacts accepted by user (for non-trivial work)
[ ] Impact checked for non-trivial symbol edits
[ ] Tests green (and new tests for new behavior)
[ ] detect_changes / review_change_impact before commit
[ ] Archive + index/docs refresh when done
```

---

## Safety

- Do not commit secrets, `.env` with real credentials, or private keys.
- Do not run destructive git commands (`reset --hard`, force-push to shared default branch) unless the user explicitly asks.
- Prefer feature branches and PRs for shared work.
- Ask before changing CI, release, or production deployment config.

---

## Domain & architecture notes

- Shared vocabulary lives in `CONTEXT.md` (and ADRs under `docs/adr/` if present). Prefer those terms in code and discussion.
- OpenSpec source of truth: `openspec/specs/`; active changes under `openspec/changes/`.
- For deeper workflow detail see `docs/feature-dev-workflow.md` if present in the repo.

---

*Template tuned for OpenCode + OpenSpec + codebase-memory + GitNexus + OpenWiki + mattpocock/skills.*
