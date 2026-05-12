# A2 — CLI Workflow Patterns

> **繁體中文** | [简体中文](./A2-cli-workflow.zh-Hans.md) | [English](./A2-cli-workflow.en.md) | [Русский](./A2-cli-workflow.ru.md)

> [← A1 — CLI 入門](A1-cli-intro.md) · **Track A: CLI Power User** 第 2 站

⏱ **時間估算**：1-2 週（約 8-15 小時）

裝好 CLI、跑過第一個任務之後，下一個問題：**怎麼讓 CLI 一致地、可重複地、可分享地做事**？這節講 workflow pattern——把「我每次都要重打一遍 prompt」變成「設好一次後 CLI 自己會用對方法」。

## 📌 學習目標

- 寫一份 production-grade 的 `CLAUDE.md` / `AGENTS.md`（不是 1 行說明，是 30-50 行的工作規範）
- 設計可重複的 slash command / custom prompt
- 把多步驟任務拆成 CLI 能跑完的小步驟
- 設計 prompt 讓任務在不同 CLI 上 portable

## 📚 必修閱讀

1. [**Anthropic — CLAUDE.md best practices**](https://docs.anthropic.com/en/docs/claude-code/memory) ⭐
2. [**Stage 2 — Prompt 設計**](../../stages/02-prompt-engineering.md) — workflow design 跟 prompt design 是同一件事的兩面
3. [**Stage 5.1 — Claude Code 基礎**](../../stages/05-claude-code-ecosystem.md#51--claude-code-基礎) — slash commands 細節
4. [**`resources/cli-agents-guide.md`** §「跨 CLI 都通用的 prompt 寫法」](../../resources/cli-agents-guide.md) — portable prompt 原則

## 🛠 動手練習

### 動手練習 CLI-5：寫 production CLAUDE.md
你 CLAUDE.md 應該至少包含：
- **角色**：「你是一個 senior Python engineer / 學術寫作助手 / 等」
- **這個 repo 的 context**：是什麼專案、用什麼套件、有什麼 convention
- **不能做的事**：別亂改 main、別動 secrets、別 commit
- **怎麼做事**：先 plan、跑 test 再 commit、要寫 type hint
- **常用指令**：怎麼跑 test、怎麼 lint、怎麼 deploy

把這份提交到 git。下次新成員 clone repo，他的 Claude Code 自動載入你的 convention。

### 動手練習 CLI-6：第一個 slash command
寫 `.claude/commands/review.md`（或對應 CLI 的位置）：
```markdown
---
name: review
description: Review staged changes for security + style
---

請執行以下流程：
1. `git diff --cached` 抓 staged 的 changes
2. 找：hard-coded secrets、SQL injection、type errors
3. 對應 CLAUDE.md 內的 style 規則檢查
4. 輸出：PASS / 或 list of 具體要改的點
```
之後每次 `/review`，CLI 都跑同一套流程。

### 動手練習 CLI-7：多步驟任務拆解
給 CLI 一個複雜任務（譬如「把這 50 個 markdown 翻譯成英文 + 加 frontmatter + 移到 en/ 子目錄」）。
- 第一次：直接丟整個任務 → 觀察 CLI 怎麼做、什麼地方會錯
- 第二次：你先拆成 5 個 sub-task，逐一給 CLI → 觀察結果差別
- 學到：CLI 跟你一樣，太大的任務要拆；給太小的任務又會 over-orchestrate

### 動手練習 CLI-8：Portable prompt
寫一個 prompt 給 Claude Code 跑成功了。**換到 Codex / OpenCode / Gemini CLI 跑同一個 prompt**——什麼地方需要改？通常會發現：
- file path convention 不同（cwd vs absolute）
- 對「執行 shell」的權限預設不同
- 「先 plan 再做」的 prompt 在某些 CLI 要明確說，在某些是預設行為

把這些差異整理成你自己的 cheat sheet。

## 🎯 精選 Projects

### CLAUDE.md 範例庫

#### [Anthropic 官方範例](https://github.com/anthropics/claude-code/blob/main/CLAUDE.md)
★ official — Claude Code repo 自己的 CLAUDE.md，看官方怎麼寫。

#### [obra/superpowers](https://github.com/obra/superpowers) ⭐⭐⭐⭐
★ 178k+ — 不只是 skill collection，也是 production CLAUDE.md 範本。看 `.claude/` 整個目錄結構。

#### [mattpocock/skills](https://github.com/mattpocock/skills) ⭐⭐⭐⭐
★ 59k+ — 工程師日常用的 skill 庫。`.claude/` 結構是好參考。

> 更多 skill / SKILL.md 範例見 [Stage 5.3 — Skills](../../stages/05-claude-code-ecosystem.md#53--skillsclaude-code-的行為層)。

---

### Slash Commands / Custom Prompts

#### [anthropics/claude-plugins-official](https://github.com/anthropics/claude-plugins-official) ⭐ 官方
★ 18k+ — 官方 plugin marketplace。每個 plugin 內部的 commands / skills 是 slash command 範例。

#### [hesreallyhim/awesome-claude-code](https://github.com/hesreallyhim/awesome-claude-code)
社群整理的 Claude Code 資源清單。逛裡面的 slash command 範例。

---

### Prompt 設計參考

#### [f/awesome-chatgpt-prompts](https://github.com/f/awesome-chatgpt-prompts) ⭐⭐⭐⭐
★ 161k+ — 雖然是 ChatGPT 起家，prompt 寫法 90% 在 CLI 上也通。

#### Stage 2 — Prompt Engineering 全部 entry
[完整列表](../../stages/02-prompt-engineering.md#-精選-projects) — DSPy、Prompt-Engineering-Guide 等。

---

### 多 CLI 並用 pattern

#### [`resources/cli-agents-guide.md`](../../resources/cli-agents-guide.md) §「3 個常見搭配」
看 Setup A / B / C，挑一個合的試。

## ✅ 進 A3 前的自我檢查

你能不能：
- [ ] 寫過至少 1 份你 production / 工作 repo 的 CLAUDE.md（不是 demo repo）
- [ ] 寫過至少 2 個 slash command 並實際在用
- [ ] 把同一個 prompt 在 2 個不同 CLI 上跑過、知道差異
- [ ] 講得出「什麼任務該拆、什麼任務不該拆」的判準

如果可以 → 進 [A3 — Integration & Production](A3-cli-production.md)。

如果不行 → CLAUDE.md 一直 demo 等於白寫；先去你真實 repo 寫一份再回來。

## 💡 常見坑

- **CLAUDE.md 寫太長**：超過 100 行 CLI 會自己 truncate / 忽略後段。Sweet spot 30-60 行。
- **Slash command 寫成「請做 X、Y、Z、A、B」一句**：CLI 容易跳步驟。改寫成編號 list + 每步成功標準。
- **Portable 過頭**：每個 CLI 還是有自己的特長；不要為了能跨 CLI 把 prompt 變得太抽象、失去具體性。
- **覺得自己「都會」就不寫了**：CLAUDE.md 是給未來的你（跟新成員）看的，不是給現在的你看的。
