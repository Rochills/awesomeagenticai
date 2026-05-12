# 給日常使用者 — 專業分支

> **繁體中文** | [简体中文](./for-everyday-users.zh-Hans.md) | [English](./for-everyday-users.en.md) | [Русский](./for-everyday-users.ru.md)

> 🚀 **完全沒寫過 code / 沒裝過 Python？** 先看 [`resources/setup-guide.md` §A-C](../resources/setup-guide.md)（30 分鐘從零裝好）再回來。已經會 Python 跟有 API key 就跳過。

> [← 回主路線 README](../README.md) · 你**不一定要走完整條主幹**才能從這裡開始——這條分支是給「**只想 USE AI、不一定要 BUILD agent**」的人。

## 使用情境

- 寫 email、整理筆記、改 cover letter
- 學新技能（讀英文文章、學語言、複習重點）
- 查資料、做研究比較（旅遊、產品、學校）
- 整理生活流程（食譜、行程、待辦清單）
- 隱私敏感場景：醫療紀錄、個人財務（→ 本地 LLM）

## 起步：你應該從哪一層進來？

按「**動手願意度**」分 4 層，從低到高：

```
Tier 0：網頁 / 手機 App（推薦從這裡開始）
   ↓
Tier 1：Desktop App（要處理本機檔案再升級）
   ↓
Tier 2：CLI Agent（願意學一點命令列，能自動化日常流程）
   ↓
Tier 3：本地 LLM（隱私敏感、API 費用敏感、想 offline）
```

**多數人停在 Tier 0 / Tier 1 就夠用了**——Tier 2-3 是給有特殊需求或想學的人。

---

## 🎯 精選 Projects

### Tier 0 — 網頁 / 手機 App ⭐ 入門

#### [Claude.ai](https://claude.ai) ⭐⭐⭐⭐⭐
Anthropic 官方介面。長文章、深度討論、複雜問題很適合用——回答風格較收斂、不太瞎掰。

#### [ChatGPT](https://chatgpt.com) ⭐⭐⭐⭐⭐
OpenAI 官方介面。生態最廣（GPTs、Custom Instructions、Voice mode）。一般用途的標準選擇。

#### [Gemini](https://gemini.google.com) ⭐⭐⭐⭐
Google 出品。長 context 窗口（百萬 token）特別適合丟整本 PDF 進去問問題。整合 Google 服務（Gmail、Docs）。

#### [Perplexity](https://perplexity.ai) ⭐⭐⭐⭐
搜尋引擎 × LLM——每個答案都附引用來源。比 ChatGPT 適合「需要查最新資訊」的場景。

---

### Tier 1 — Desktop App

#### [Claude Desktop](https://claude.ai/download) ⭐⭐⭐⭐⭐
比網頁版多了：拖檔案進去、本機檔案讀取、保留長期對話脈絡。**也是進入 MCP 生態的入口**——可以接 Slack / Gmail / 行事曆 server。

#### [ChatGPT Desktop](https://openai.com/chatgpt/desktop) ⭐⭐⭐⭐
ChatGPT 桌面版。可以對螢幕截圖問問題、語音對話、跟其他 App 整合。

---

### Tier 2 — CLI Agent（願意學命令列的進階使用者）

> 這些工具雖然定位給開發者，但**日常使用者也能用**——例如批次重新命名檔案、整理下載資料夾、自動寫每週回顧、把 PDF 摘要存成 Markdown。
>
> 想看詳細比較？見 [`resources/cli-agents-guide.md`](../resources/cli-agents-guide.md)（7 個主流 CLI agent 並列、依 use case 推薦、常見坑、實用搭配）。
>
> 想要 step-by-step 上手？見 [`tracks/cli/A1-cli-intro.md`](../tracks/cli/A1-cli-intro.md)（Track A 第一站，從安裝到第一個任務）。
>
> 想把 CLI agent 接到你的 Notion / Obsidian / Excel / Google 文件等日常工具？見 [`resources/mcp-skills-catalog.md`](../resources/mcp-skills-catalog.md)（按分類整理 62 個 MCP server / Skill）。

#### [anthropics/claude-code](https://github.com/anthropics/claude-code) ⭐⭐⭐⭐⭐
★ 120k+ — Anthropic 官方的 CLI agent。能讀寫檔案、執行指令、做多步驟任務。**日常使用者最容易上手的 CLI 工具**。

#### [openai/codex](https://github.com/openai/codex) ⭐⭐⭐⭐⭐

| 欄位 | 內容 |
|---|---|
| Stars | ★ 80k+ |
| License | Apache-2.0 |

**教什麼**：OpenAI 出品的輕量級 terminal coding agent。跟 Claude Code 同類，但用的是 OpenAI 的模型。

**適合誰**：已經訂 ChatGPT Plus / Pro，想在終端機用同一個帳號做事的人。

#### [sst/opencode](https://github.com/sst/opencode) ⭐⭐⭐⭐⭐

| 欄位 | 內容 |
|---|---|
| Stars | ★ 155k+ |
| License | MIT |

**教什麼**：開源版的 coding agent，**不綁特定 LLM provider**——可以用 Claude、GPT、Gemini、本地 Ollama 任何一個。社群維護、迭代速度快。

**適合誰**：想 self-host、不想被 API provider 綁住，或要在多個 LLM 之間切換的人。

#### [google-gemini/gemini-cli](https://github.com/google-gemini/gemini-cli) ⭐⭐⭐⭐

| 欄位 | 內容 |
|---|---|
| Stars | ★ 103k+ |
| License | Apache-2.0 |

**教什麼**：Google 官方的 Gemini CLI agent。把 Gemini 的長 context 跟 Google 生態整合到終端機。

**適合誰**：Google 生態的重度使用者（Gmail、Drive、Docs）。

---

### Tier 3 — 本地 LLM（隱私 / 離線 / 省錢）

#### [Ollama](https://github.com/ollama/ollama) ⭐⭐⭐⭐⭐
★ 170k+ — 一行指令跑本地 LLM。隱私敏感資料（病歷、合約、家人對話）不適合送去雲端時用這個。詳見 [Stage 1 — Local LLM 執行](../stages/01-llm-basics.md)。

#### [LM Studio](https://lmstudio.ai/)
非開源但對非開發者最友善——拖拉介面、不用 command line。Mac / Windows / Linux 都有。

---

### Prompt 素材庫

#### [f/awesome-chatgpt-prompts](https://github.com/f/awesome-chatgpt-prompts) ⭐⭐⭐⭐
★ 161k+ — 社群維護的 prompt 大全。「act as 翻譯家 / 履歷顧問 / 廚師...」幾百種角色。**不知道怎麼開頭時從這裡找靈感**。

---

## 必修閱讀

1. [**Anthropic — How to write effective prompts**](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/overview) — 不用程式碼也能讀的 prompt 寫法
2. [**OpenAI — Prompting Guide**](https://platform.openai.com/docs/guides/prompt-engineering) — 對位的官方文件
3. [**ChatGPT 怎麼用得最好（中文）**](https://www.runoob.com/) — 各家中文部落格的整理（runoob 等等）

如果有興趣再深入，看 [Stage 2 — Prompt 設計](../stages/02-prompt-engineering.md)，那邊有正式系統性教學。

## 可以建的流程

這些是模板——配合你的場景自行調整：

- **每週週記**：跟 Claude.ai 講你這週做什麼，請它整理成週記+下週重點
- **email triage**：每天早上把待回信件貼進 Claude，請它分類成「立即回覆/今天回/這週回/不用回」
- **學語言**：跟 ChatGPT Voice 模式對話練英文/日文，請它指出文法錯誤
- **批次整理檔案**：用 Claude Code 重新命名下載資料夾的所有檔案，照日期 + 主題分類
- **本地隱私 chat**：Ollama 跑 qwen2.5:7b，問醫療 / 法律 / 財務問題不送雲端

## 給日常使用者的層級建議

90% 的場景：**留在 Tier 0**——Claude.ai 或 ChatGPT 網頁版，免安裝、免付費就能跑（免費版有限額但夠日常用）。

5% 升級到 Tier 1：要處理本機檔案、要保留對話歷史、要接 MCP server。

5% 升級到 Tier 2-3：有真的自動化需求（譬如每天要做同樣的事 100 次），或隱私敏感資料不能送雲端。

**不要被人催著升級**——多數人 Tier 0 就夠用了。Tier 2-3 是工具，不是身份地位。

## 社群備註

這條分支也歡迎社群貢獻：

- 推薦特定領域的 prompt template（料理、運動、學語言）
- 中文友善的 chat tools（國產 LLM、本地化 wrapper）
- 隱私 / 安全相關的最佳實踐（什麼資料能送 / 不能送）

詳見 [CONTRIBUTING.md](../CONTRIBUTING.md)。
