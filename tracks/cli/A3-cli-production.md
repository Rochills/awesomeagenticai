# A3 — Integration & Production

> **繁體中文** | [简体中文](./A3-cli-production.zh-Hans.md) | [English](./A3-cli-production.en.md) | [Русский](./A3-cli-production.ru.md)

> [← A2 — CLI Workflow Patterns](A2-cli-workflow.md) · **Track A: CLI Power User** 第 3 站（最後）

⏱ **時間估算**：1-2 週（約 8-15 小時）

CLI 跑得順了之後，下一步：**把它接到你的真實工作流程裡**。MCP server 整合、CI 自動化、cost / observability。這節之後，CLI 不只是你個人在用的工具，而是 team 工作流的一部分。

## 📌 學習目標

- 把 1-3 個 MCP server 接到你的 CLI（Slack / Gmail / 你的 internal API / DB）
- 設定 GitHub Actions 自動跑 Claude Code（PR review、release notes 等）
- 加 observability（trace、cost、latency）到 CLI workflow
- 規劃 cost budget，知道大 task 會花多少 token

## 📚 必修閱讀

1. [**Stage 5.2 — MCP（Model Context Protocol）**](../../stages/05-claude-code-ecosystem.md#52--mcpmodel-context-protocol-基礎) — MCP 概念跟基礎
2. [**Anthropic — Prompt Caching**](https://www.anthropic.com/news/prompt-caching) — 90% cost reduction 的關鍵技巧
3. [**Stage 7 — Observability section**](../../stages/07-multi-agent-production.md#observability) — langfuse / Helicone / weave
4. [**`resources/cli-agents-guide.md`** §「常見坑」](../../resources/cli-agents-guide.md) — production 用 CLI 最常踩的問題

## 🛠 動手練習

### 動手練習 CLI-9：MCP server 接 CLI
照 [Stage 5.2 練習：MCP client](../../stages/05-claude-code-ecosystem.md#hello-x) 的步驟，把至少一個有用的 MCP server 接到你的 CLI：
- `filesystem` server → 讓 CLI 在指定目錄外也能讀檔
- `github` server → 讓 CLI 直接讀 PR / issue
- 自架 server → 接你的 internal API / DB

成功標準：在 CLI 對話裡直接問「我這個 PR 有 conflict 嗎」，CLI 透過 MCP 回答你（不用你開瀏覽器）。

### 動手練習 CLI-10：GitHub Actions + CLI
寫一個 `.github/workflows/cli-review.yml`：
- 觸發：PR opened / synchronize
- 跑：在 GH Actions runner 內執行 Claude Code（或 Codex），給它 `git diff` + 你的 `.claude/commands/review.md`
- 輸出：PR comment

成功標準：開新 PR，1-2 分鐘內 PR 出現 review comment。

> 起點：Anthropic 官方有 [`claude-code-action`](https://github.com/anthropics/claude-code-action)（GitHub Actions 整合）；Codex 有 GitHub App 跟 CLI 兩種模式。

### 動手練習 CLI-11：Cost tracking
跑你日常的一個 task，**先預估** token 用量，再實際跑、查 token usage。差距通常很大（多半你低估）。
- 算式：input tokens + output tokens 各乘以 model 單價
- 接 langfuse 或 Helicone（[Stage 7 Observability section](../../stages/07-multi-agent-production.md#observability)）做 trace
- 觀察：哪個 sub-task 花最多 token？是不是有不必要的 long context？

### 動手練習 CLI-12：Skill / plugin 跨 team 分享
把你的 `.claude/commands/` 跟 `CLAUDE.md` 打包成 plugin，發布到內部 marketplace 或 GitHub。Team 其他人 `claude plugin install` 之後就有同樣的工作流。
- Skill / plugin 細節見 [Stage 5.3 + 5.4](../../stages/05-claude-code-ecosystem.md)
- 範本：[anthropics/claude-plugins-official](https://github.com/anthropics/claude-plugins-official)

## 🎯 精選 Projects

### MCP server collection（接 CLI 用）

> 💡 **要找接日常工具的 MCP**（Notion / Obsidian / Excel / Postgres / Playwright / Slack / Linear / Figma 等）：[`resources/mcp-skills-catalog.md`](../../resources/mcp-skills-catalog.md)——62 個分類整理，每個都有 stars / license / 適合誰。下面只列「寫自己 MCP server / 找 reference」用的核心 catalog。

#### [modelcontextprotocol/servers](https://github.com/modelcontextprotocol/servers) ⭐⭐⭐⭐⭐
★ 85k+ — 官方 reference servers。filesystem、github、sqlite、git、time、fetch、memory、sequential-thinking。
> 詳見 [Stage 5.2](../../stages/05-claude-code-ecosystem.md#52--mcpmodel-context-protocol-基礎)。

#### [wong2/awesome-mcp-servers](https://github.com/wong2/awesome-mcp-servers)
社群 MCP server catalog。150+ 個依分類整理。

---

### CI 整合 patterns

#### [anthropics/claude-code-action](https://github.com/anthropics/claude-code-action)
官方 GitHub Action 範本。PR review、issue triage、自動 fix。

#### [continuedev/continue](https://github.com/continuedev/continue) ⭐⭐⭐⭐
★ 33k+ — 把 AI checks 接到 CI，可在 PR pipeline 強制執行。
> 完整介紹見 [`branches/for-developer.md`](../../branches/for-developer.md)。

---

### Observability + Cost

#### [langfuse/langfuse](https://github.com/langfuse/langfuse) ⭐⭐⭐⭐⭐
★ 26k+ — open source LLM observability。把 trace、cost、session 都接起來。
> 詳見 [Stage 7 Observability](../../stages/07-multi-agent-production.md#observability)。

#### [Helicone](https://github.com/Helicone/helicone) ⭐⭐⭐⭐
★ 5k+ — proxy-based 監控。改 base_url 就有 logging + caching。

#### [promptfoo/promptfoo](https://github.com/promptfoo/promptfoo) ⭐⭐⭐⭐⭐
★ 20k+ — eval framework。CLI workflow 升級到 production 前用這個跑回歸測試。
> 詳見 [Stage 7 Eval](../../stages/07-multi-agent-production.md#evaluation-frameworks)。

---

### Production CLI workflow 範本

#### [obra/superpowers](https://github.com/obra/superpowers) ⭐⭐⭐⭐
★ 178k+ — 整套 production-ready skill collection。看別人怎麼把 CLI workflow 做完整。

#### [obra/superpowers-marketplace](https://github.com/obra/superpowers-marketplace)
★ 900+ — 最簡 marketplace template。要把你 team 的 CLI workflow 打包共用時參考。

## ✅ Track A 完整通關自我檢查

你能不能：
- [ ] 已有至少 1 個 MCP server 接到你日常 CLI
- [ ] 已有至少 1 個 CI workflow 在自動跑 CLI agent
- [ ] 你能講出某個 task 跑下去的 token 用量、cost、latency 大致範圍
- [ ] 把你的 CLAUDE.md / commands 打包過至少一次（即使只有自己用）
- [ ] 知道什麼任務值得加 observability、什麼不值得

如果都可以 → **Track A 完整通關**。挑一個 [specialized branch](../../README.md#️-學習地圖兩條軌道) 繼續走（researcher / developer / teacher / knowledge-worker / everyday-users）。

如果想再深入「**怎麼寫自己的 CLI agent**」（不是用現有的）→ 跳到 [Track B Stage 3](../../stages/03-tool-use-and-hello-agent.md) 開始。Track A 跟 Track B 互補。

## 💡 接下來

走完 Track A 你已經是 CLI power user。下一階段選擇：

1. **加深 CLI workflow**（持續優化你的 setup）
   - 訂閱 Anthropic / OpenAI changelog
   - 每季 review 一次 [`resources/cli-agents-guide.md`](../../resources/cli-agents-guide.md) 看新工具
   - 跟你 team 分享 CLAUDE.md / skills

2. **跨到 Track B**（學怎麼寫自己的 agent）
   - Stage 3-4 學 tool use + framework
   - Stage 5 深挖 Claude Code 內部運作
   - Stage 7 寫自己的 multi-agent system

3. **走 specialized branch**（把 CLI 應用在特定領域）
   - 研究人員 / 開發者 / 知識工作者 / 教師 / 日常使用者
   - 各 branch 都會用到 Track A 學的東西
