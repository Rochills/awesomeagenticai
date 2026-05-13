# A1 — CLI Agent 入門 + 選擇

> **繁體中文** | [简体中文](./A1-cli-intro.zh-Hans.md) | [English](./A1-cli-intro.en.md) | [Русский](./A1-cli-intro.ru.md)

> [← 回主路線 README](../../README.md) · **Track A: CLI Power User** 第 1 站

⏱ **時間估算**：1 週（約 5-10 小時）

讀完 Stage 0-2 之後，你想直接用現成的 CLI agent 把工作做完，不打算自己從零寫 ReAct loop？這條軌就是給你的。第一站：**選一個 CLI agent，跑起來**。

## 📌 學習目標

完成這一節後你會：

- 知道 7 個主流 CLI agent（Claude Code / Codex / OpenCode / Gemini CLI / goose / Aider / Hermes Agent）的差別
- 依自己的場景挑出第一個 CLI 工具
- 完成安裝 + 認證 + 第一個真正的任務（不是 hello world）
- 知道什麼時候該換 / 加第二個 CLI

## 🚪 進入條件

你應該已經：
- 跑過 Stage 0 的 練習：CLI（會用命令列）
- 有 Claude / OpenAI / Google 任一個帳號（不一定是付費）
- 對 prompt 寫法基本上手（Stage 2）

## 📚 必修閱讀

1. [**`resources/agent-paradigms.md`**](../../resources/agent-paradigms.md) ⭐ — 5 種 agent 型態的全景圖；先讀這份知道 CLI agent 在整個 agent 生態中的位置（Type 2 + Type 3）
2. [**`resources/cli-agents-guide.md`**](../../resources/cli-agents-guide.md) ⭐ — 本軌的核心參考。7 個主流 CLI agent 並列比較、依 use case 推薦、實用搭配
3. [**Anthropic — Claude Code Quickstart**](https://docs.anthropic.com/en/docs/claude-code/quickstart) — 官方安裝指南
4. [**OpenAI — Codex Quickstart**](https://github.com/openai/codex/blob/main/README.md) — Codex 安裝跟認證流程

## 🛠 動手練習（基礎 illustrative 練習）

### 動手練習 CLI-1：安裝 + 第一次跑
照你選的 CLI 的 quickstart 安裝。第一個 prompt 不要寫「hello world」——直接給它一個你今天本來就要做的事，譬如：「整理我 Downloads 資料夾，把 PDF 全部 move 到 ~/Documents/PDFs」。觀察它怎麼分解任務、要哪些確認。

### 動手練習 CLI-2：CLI 內建的 system prompt 檔
- Claude Code → 寫一個 `CLAUDE.md` 在 repo 根目錄
- Codex → 寫 `AGENTS.md`
- Gemini CLI → 寫 `GEMINI.md`
- goose / OpenCode → 看各自的設定

寫進去 3 件事：「你的個性 / 偏好的 code style / 不能做的事」。再跑一個任務，觀察行為差異。

### 動手練習 CLI-3：第二個 CLI 並用
裝第二個 CLI（建議 Codex 或 OpenCode 當 backup）。用同一個 prompt 跑，比較輸出風格、速度、cost。**不是要選一個贏家——是要學「不同 CLI 解同一個問題的角度不同」**。

### 動手練習 CLI-4：認證細節
故意把 API key 弄錯一個字元，看 CLI 怎麼報錯。再做一次「正確 key 但 model 名稱錯」的實驗。Production 用一定會遇到 auth 問題，先在這裡踩過。

## 🎯 精選 Projects

### 7 個主流 CLI agent

詳細比較（star、license、強弱項、推薦場景）見 [`resources/cli-agents-guide.md`](../../resources/cli-agents-guide.md)。這裡只給快速 entry point：

#### [anthropics/claude-code](https://github.com/anthropics/claude-code) ⭐⭐⭐⭐⭐
★ 120k+ — 第一個 CLI agent 推薦。內建 SKILL / plugin 生態、CLAUDE.md prompt 系統、最完整的中文社群資源。

#### [openai/codex](https://github.com/openai/codex) ⭐⭐⭐⭐⭐
★ 80k+ — 已訂 ChatGPT Plus / Pro 的人很合適；用同一個帳號就能在終端機跑。

#### [sst/opencode](https://github.com/sst/opencode) ⭐⭐⭐⭐⭐
★ 155k+ — 開源、不綁 LLM provider、社群迭代最快。要 self-host / 不想 vendor lock-in 選這個。

#### [google-gemini/gemini-cli](https://github.com/google-gemini/gemini-cli) ⭐⭐⭐⭐
★ 103k+ — 想要 1M token 長 context 處理大 codebase / 大 PDF 時用。

#### [block/goose](https://github.com/block/goose) ⭐⭐⭐⭐
★ 43k+ — 15+ provider 支援（含 Ollama）、可用既有 Claude / ChatGPT / Gemini 訂閱。已遷至 `aaif-goose/goose`（AAIF / Linux Foundation）。

#### [Aider-AI/aider](https://github.com/Aider-AI/aider) ⭐⭐⭐⭐⭐
★ 44k+ — git-native，自動 commit / branch。「要寫 code 想要 git 流程乾淨」的人用這個。

#### [NousResearch/hermes-agent](https://github.com/NousResearch/hermes-agent) ⭐⭐⭐⭐⭐
★ 142k+ — Nous Research 出的 self-improving agent。差異化在三件事：(1) agent 跑 cloud VM，從 Telegram / Discord / Slack 任一介面跟它聊；(2) 多 LLM 中性，支援 GLM / Kimi / 小米 MiMo / MiniMax 等中文圈生態；(3) 內建 cron 排程 + skill 自動演化迴圈。⚠️ self-improving skill 是 frontier feature，目前缺獨立審計，production 任務先在低風險場景試。

---

### 進階：跟主流 CLI 互補的工具

#### [LM Studio](https://lmstudio.ai/)
非開源 desktop app——拖拉介面跑本地 LLM。如果你是 Windows / Mac 使用者不想學 command line 但想跑 local LLM，先試這個。

#### [Ollama](https://github.com/ollama/ollama)
★ 170k+ — 本地 LLM runner，跟 OpenCode / goose 搭配很好（也能單獨給 IDE 接 OpenAI 相容 API）。詳見 [Stage 1 — Local LLM 執行](../../stages/01-llm-basics.md#-本地端執行-llm不用付-api-費用)。

## ✅ 進 A2 前的自我檢查

你能不能：
- [ ] 講得出 7 個主流 CLI 的核心差別（不查表就答得出 3-4 個）
- [ ] 你已經選定一個主用 CLI，並有 working setup（裝好、認證好、跑過至少 5 個非 hello-world 任務）
- [ ] 寫過你自己的 `CLAUDE.md` / `AGENTS.md` / `GEMINI.md`
- [ ] 至少跑過第二個 CLI 一次，知道兩個的風格差異

如果可以 → 進 [A2 — CLI Workflow Patterns](A2-cli-workflow.md)。

如果不行 → 別跳。CLI 工具會用得 sloppy 不會用得 productive；A1 的 動手練習 CLI-1/2 至少各跑 3 次再走。

## 💡 給 Track A 學習者的提醒

CLI agent 跟 web 版（Claude.ai / ChatGPT）的差別不是「一樣的東西換介面」——CLI 能讀寫你電腦上的檔案、執行 shell 指令、改 git。這個能力差異**先了解再用**：
- 第一週：每個任務都加 `--dry-run` 或先 review 計畫再執行
- 不要直接讓 CLI 對 production codebase 做 commit
- 重要資料（key、合約、病歷）放在 `.cursorignore` / `.claudeignore` 排除
