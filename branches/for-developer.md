# 給開發者 — 專業分支

> **繁體中文** | [简体中文](./for-developer.zh-Hans.md) | [English](./for-developer.en.md) | [Русский](./for-developer.ru.md)

> 🚀 **第一次裝 Claude Code / 寫 `CLAUDE.md` / `SKILL.md`？** 快速 setup 指南在 [`resources/setup-guide.md` §D-E](../resources/setup-guide.md)。已經熟可以跳過。

> [← 回主路線 README](../README.md) · 走完 **Track A 的 A3** 或 **Track B 的 Stage 7** 後從這裡接續。把 agentic AI 應用到開發流程上。

## 使用情境

- AI 結對程式設計（Cursor、Aider、Claude Code、Cline、Continue）
- Code review 自動化
- 測試生成
- Multi-agent coding 任務（規劃 + 執行）
- IDE 整合與 CI 規範

## 精選 Projects

> 7 個主流 CLI agent（Claude Code / Codex / OpenCode / Gemini CLI / goose / Aider / Hermes Agent）的並列比較見 [`resources/cli-agents-guide.md`](../resources/cli-agents-guide.md)。第一次接觸 CLI agent 想要 step-by-step 入門 → [`tracks/cli/A1-cli-intro.md`](../tracks/cli/A1-cli-intro.md)（Track A 第一站）。要把 CLI 接到日常工具（GitHub、Linear、Atlassian、Postgres、Playwright、Figma 等）→ [`resources/mcp-skills-catalog.md`](../resources/mcp-skills-catalog.md)（62 個分類整理）。下面只列開發者該知道的關鍵 entry。

### Coding Agents

#### [Cursor](https://www.cursor.com/) ⭐⭐⭐⭐⭐
編輯器整合的 AI 結對程式設計工具。AI 輔助 coding 的業界標準。

#### [Aider-AI/aider](https://github.com/Aider-AI/aider) ⭐⭐⭐⭐⭐
★ 44k+ · Apache-2.0 — git-aware 的 CLI pair-programmer。直接編輯你 repo 中的檔案，commit 都自動寫好。**「git-native AI 編輯流程」的開源範本**。模型不限。

#### [anthropics/claude-code](https://github.com/anthropics/claude-code) ⭐⭐⭐⭐⭐
★ 120k+ — Anthropic 官方的 agentic coding 助理。有 Skills + plugin 生態系。

#### [cline/cline](https://github.com/cline/cline) ⭐⭐⭐⭐⭐
★ 61k+ · Apache-2.0 — VS Code extension，autonomous in-IDE agent：tool use、browser、step-by-step approval。**VS Code 使用者要 IDE-native agentic dev 的好選項**。

#### [continuedev/continue](https://github.com/continuedev/continue) ⭐⭐⭐⭐
★ 33k+ · Apache-2.0 — source-controlled AI checks，可以在 CI 強制執行。代表「**團隊 / governance**」這條角度的 coding agent。

#### [OpenHands (前身為 OpenDevin)](https://github.com/All-Hands-AI/OpenHands) ⭐⭐⭐⭐
★ 72k+ · MIT — open source 的自主軟體開發 agent。設計上比 Aider / Claude Code 更激進——agent 自己跑 sandbox、自己 commit，適合「整個 issue 丟給它解」場景。

#### [block/goose](https://github.com/block/goose) ⭐⭐⭐⭐
★ 43k+ · Apache-2.0 — 開源、可擴充的 AI agent，超出純 code suggestion——能 install / execute / edit / test，搭配任何 LLM。同時支援多家 LLM provider 跟 MCP，提供 desktop app、CLI、API 三種介面。（repo 現指向 `aaif-goose/goose`。）

#### [RooCodeInc/Roo-Code](https://github.com/RooCodeInc/Roo-Code) ⭐⭐⭐⭐
★ 23k+ · Apache-2.0 — VS Code 的 coding agent，採用「**多種專業 mode**」的設計，跟 Cline 的單一 agent flow 不同。VS Code 使用者要 multi-mode 替代方案的選擇。

### Code Review

#### [obra/superpowers](https://github.com/obra/superpowers) ⭐⭐⭐⭐
20+ 個經過實戰驗證的 skill，包括 TDD 模式、debug、協作模式。設計 code-review skill 時的好參考。

## 必練流程

- **AI 結對程式設計**：日常工作用 Claude Code、Cursor、或 Cline 任一個
- **Git-native AI 編輯**：用 Aider 跑一週，習慣「AI 編輯 → commit → review」這個節奏
- **CI 上的 AI check**：用 Continue 把 AI 檢查接到 PR pipeline
- **測試生成**：寫一個 skill / prompt，從 function signature 生出 pytest 測試
- **Code review 自動化**：在每一個 PR 上呼叫 Claude API 的 GitHub Action

### 3 個具體 workflow recipe

**1. AI 結對程式設計（每日節奏）**
1. 開新 feature → `git checkout -b feature/xxx`
2. 把任務丟給 Claude Code / Cursor，**先讓它寫 plan**（不直接寫 code）
3. Review plan、修正方向 → 才 approve 寫 code
4. 寫完跑 tests + lint → 自己 review diff（**不要 blind accept**）
5. Commit message 自己寫或 prompt 生草稿後改

**2. Aider git-native 流程（最像「跟 AI pair」）**
```bash
# 進入 repo 後
aider --model anthropic/claude-sonnet-4-20250514

# 自然語言請求
> 幫我把 utils.py 的 parse_date 加上時區參數，預設 UTC

# Aider 會自動編輯 + commit。若不滿意：
> /undo  # 退掉最後一次 AI commit
```

**3. PR 上的 Claude code review（GitHub Action）**

`.github/workflows/claude-review.yml`：
```yaml
on:
  pull_request:
jobs:
  review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
      - name: Run Claude review
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
        run: |
          # 用 anthropics/claude-code-action 或自寫 script
          # 抓 git diff、跑 prompt、結果 post 回 PR
```
參考 [`anthropics/claude-code-action`](https://github.com/anthropics/claude-code-action) 官方 GitHub Action。

## 常見踩坑（Anti-patterns）

| ❌ 不要 | ✅ 改成 |
|---|---|
| 讓 AI 直接 push 到 main | 永遠 PR → review → merge |
| Blind accept 大規模 refactor diff | 拆成 < 50 LOC 改動，逐個 review |
| 把 .env / API key 丟給 AI 看 | 用工具對應的排除機制：Cursor `.cursorignore` / Aider `.aiderignore` / Claude Code 用 `.claude/settings.json` 的 `permissions.deny` |
| 讓 AI 在 production code 自由跑 shell | sandbox 限制、permission whitelist |
| 用 AI 生 test 後不檢查 assertion | 跑覆蓋率 + 故意改一個 bug 看 test 抓不抓得到 |
| 跨多個 commit 才發現方向錯 | **plan-first** 模式：先 review plan 再寫 code |

## Tier 升級路徑

- **Tier 0**：Cursor / Claude Desktop——IDE 內 chat、不寫 agent
- **Tier 1**：Claude Code / Cline / OpenCode——CLI 接 file system、有 CLAUDE.md，但仍 human-in-the-loop
- **Tier 2**：自寫 Skills + MCP server——把你的 dev workflow 包成 skill team 共用
- **Tier 3**：CI 自動跑 agent + production observability——進到 [Stage 7](../stages/07-multi-agent-production.md) 領域

> Tier 0-1 應該滿足 90% 開發者。**升級到 Tier 2+ 要先確認 ROI**——團隊夠大、流程夠重複、事故不可逆，才值得 invest。

## 也適用其他分支

開發者重疊度高的分支：

- **要做 ML 研究 / 寫 paper** → [研究員分支](./for-researcher.md)
- **接 Notion / Linear / Atlassian / Postgres / Figma** 等 dev tool → [`resources/mcp-skills-catalog.md`](../resources/mcp-skills-catalog.md)
- **要寫自己的 Skill / MCP server** → [Stage 5](../stages/05-claude-code-ecosystem.md) + [`resources/cookbook.md`](../resources/cookbook.md)
- **想看 schema 設計細節** → [`resources/schema-design-cheatsheet.md`](../resources/schema-design-cheatsheet.md)
- **CLI 從零開始** → [Track A](../tracks/cli/A1-cli-intro.md)（A1 → A2 → A3）

## 社群備註

特別歡迎以下貢獻：

- IDE-specific 設定範本（Cursor `.cursorrules`、Claude Code `CLAUDE.md` for Python / Go / Rust 等）
- 程式語言特化 skill（Python / TypeScript / Rust / Go 各自的 best practice）
- CI / pre-commit hook 整合 case study
- **跨多人團隊用 AI dev 的 governance pattern**——多 dev 共用 Skills、permission 設計、cost tracking

請見 [CONTRIBUTING.md](../CONTRIBUTING.md)。
