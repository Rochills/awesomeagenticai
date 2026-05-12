# 給研究者 — 專業分支

> **繁體中文** | [简体中文](./for-researcher.zh-Hans.md) | [English](./for-researcher.en.md) | [Русский](./for-researcher.ru.md)

> 🚀 **第一次裝 Python / 申請 API key？** 先看 [`resources/setup-guide.md` §A-C](../resources/setup-guide.md)。本分支預設你會跑 Python script、有 API key、會用 git。

> [← 回主路線 README](../README.md) · 走完 **Track A 的 A3** 或 **Track B 的 Stage 7** 後從這裡接續。把 agentic AI 應用到研究流程上。

## 使用情境

- 文獻分流與比較矩陣建立
- 論文記憶提取（claim、figure、citation）
- Multi-agent 論文審查（peer review 模式）
- NotebookLM brief 驗證
- 文獻管理自動化

## 精選 Projects

> 💡 **想把 Claude Code 接到 NotebookLM、Obsidian、Notion、Excel、PDF、Excalidraw 等研究常用工具？** 62 個整合在 [`resources/mcp-skills-catalog.md`](../resources/mcp-skills-catalog.md)（按使用情境分類）。下面這節保留「研究專屬」的工具與 marketplace。

### 研究流程 Marketplace

#### [flonat/claude-research](https://github.com/flonat/claude-research) ⭐⭐⭐

給博士研究者的 Claude Code 基礎建設——學術流程用的 skill、agent、hook、規則。LaTeX / 文獻管理為主。

---

### 文獻 RAG / Q&A

#### [Future-House/paper-qa](https://github.com/Future-House/paper-qa) ⭐⭐⭐⭐⭐

| 欄位 | 內容 |
|---|---|
| Stars | ★ 8k+ |
| License | Apache-2.0 |

**教什麼**：對 PDF 文件做高準確率的 RAG，每個答案都附 grounded citation（句子層級的引用）。

**適合誰**：寫文獻回顧、需要「查文獻時答案要可追溯」的研究者。比一般 RAG 更嚴謹。

---

#### [assafelovic/gpt-researcher](https://github.com/assafelovic/gpt-researcher) ⭐⭐⭐⭐

| 欄位 | 內容 |
|---|---|
| Stars | ★ 27k+ |
| License | Apache-2.0 |

**教什麼**：自主 deep-research agent——planner + multi-source crawl + report 合成。給定一個研究主題，自動產出 markdown / PDF brief。

**適合誰**：要快速 scope 新題目、產 research brief 的研究者。

---

### 大綱與寫作

#### [stanford-oval/storm](https://github.com/stanford-oval/storm) ⭐⭐⭐⭐

| 欄位 | 內容 |
|---|---|
| Stars | ★ 28k+ |
| License | MIT |

**教什麼**：multi-perspective outline-then-write pipeline——agent 從多個角度先產大綱、再展開成 Wikipedia-style 文章。Stanford OVAL 出品。

**適合誰**：想學「**outline-driven 寫作**」的人。從零產主題 brief 時的好工具，類似 NotebookLM structured report 流程的開源版。

**備註**：最後一次推送已超過 6 個月，使用前確認最新 commit 日期。

---

#### [kaixindelele/ChatPaper](https://github.com/kaixindelele/ChatPaper) ⭐⭐⭐⭐⭐（中文讀者）

| 欄位 | 內容 |
|---|---|
| 語言 | 中文 + Python |
| Stars | ★ 19k+ |
| License | NOASSERTION（自訂條款，非商用） |

**教什麼**：中文研究者向的 arXiv 全流程工具——論文總結 + 翻譯 + 潤色 + 審稿回覆生成。中國研究團隊維護，預設值對中文場景友善。

**適合誰**：中文研究生想找對中文友善的 paper 全流程入門工具。

**備註**：License 是自訂的非商用條款，使用前請先讀原始條款；研究或個人用途常見，但條款還是要自己看過確認。

---

### 文獻管理整合

#### [MuiseDestiny/zotero-gpt](https://github.com/MuiseDestiny/zotero-gpt) ⭐⭐⭐⭐

| 欄位 | 內容 |
|---|---|
| Stars | ★ 7k+ |
| License | AGPL-3.0 |

**教什麼**：Zotero 的 LLM plugin——可以跟你的文獻庫對話、總結 selection、生成 inline notes。

**適合誰**：Zotero 重度使用者，想在閱讀流程裡直接接 AI 而不用切到別的工具。

**備註**：AGPL-3.0 license（傳染性開源）— 修改後要散布的衍生產品需遵守條款。

---

### 研究工作流 Skills（本 repo 維護者出品）

> 這幾個是本 repo 維護者 [@WenyuChiou](https://github.com/WenyuChiou)（Lehigh CEE PhD candidate）日常在用的研究 skill / workspace。一併放到這裡讓其他研究者直接用。完整 entry 內容在 [`resources/mcp-skills-catalog.md` §13-§14](../resources/mcp-skills-catalog.md#13-研究工作流-skills學術--paper--文獻)。

#### [WenyuChiou/ai-research-skills](https://github.com/WenyuChiou/ai-research-skills) ⭐⭐⭐⭐⭐

★ 60 · MIT — 14 個 Claude Code skills 涵蓋研究全流程（文獻分流、研究設計、project context、論文撰寫、multi-AI delegation），打包成 5-plugin marketplace。一個指令裝整套。

#### [WenyuChiou/research-hub](https://github.com/WenyuChiou/research-hub) ⭐⭐⭐⭐

★ 14 · MIT — Zotero + Obsidian + NotebookLM 三工具整合 workspace，提供 CLI / MCP / REST / dashboard 四種介面。同時用三個工具的研究者必看。

#### [WenyuChiou/zotero-skills](https://github.com/WenyuChiou/zotero-skills) ⭐⭐⭐⭐

★ 16 — Zotero CLI skill：搜 / 加 / 分類 / 標記。跟 zotero-gpt（在 Zotero 裡 chat）互補，這份是讓 Claude Code 從外部操作 Zotero。

#### [WenyuChiou/academic-writing-skills](https://github.com/WenyuChiou/academic-writing-skills) ⭐⭐⭐

★ 2 · MIT — 嚴謹學術論文撰寫 / 修改 / 投稿 skill。banned-word audit、figure-text coupling、submission checklist 自動化。Per-paper 的 journal_format / style_overrides 可客製。

#### [WenyuChiou/codex-delegate](https://github.com/WenyuChiou/codex-delegate) ⭐⭐⭐⭐⭐ + [WenyuChiou/gemini-delegate-skill](https://github.com/WenyuChiou/gemini-delegate-skill) ⭐⭐⭐⭐

★ 57 + ★ 34 · MIT — Multi-LLM delegation skill 對。研究場景：Claude planner + Codex 跑實作（程式 / 圖 / 表）+ Gemini 跑長文 draft（中文報告、英文 paper section）。是 Stage 7 multi-agent 的實戰版。

---

### Multi-Agent for Research

#### [langchain-ai/open_deep_research](https://github.com/langchain-ai/open_deep_research) ⭐⭐⭐⭐⭐

| 欄位 | 內容 |
|---|---|
| Stars | ★ 11k+ |
| License | MIT |

**教什麼**：開源版的 Deep Research——支援單 agent 跟 supervisor + multi-researcher 兩種架構（multi-agent 那條目前在 `src/legacy/`）、平行搜尋、再合成成有引用的 report。是學「LLM agent 怎麼自動產出有引用 brief」的好參考。

**適合誰**：要打造「agent 自動產出有引用 brief」工作流程的研究者。是這個分類最 canonical 的開源選擇。

**備註**：依賴 LangGraph + 搜尋 tool（要 API key）。

---

#### [SakanaAI/AI-Scientist-v2](https://github.com/SakanaAI/AI-Scientist-v2) ⭐⭐⭐⭐

| 欄位 | 內容 |
|---|---|
| Stars | ★ 6k+ |
| License | The AI Scientist Source Code License（source-available，非商用 + 有 manuscript-disclosure 條款） |

**教什麼**：端到端的 multi-agent 科學研究 loop：構想 → 寫程式 → 跑實驗 → 寫 paper → 互審。Sakana AI 的「AI 寫整篇 ML paper」研究實作。

**適合誰**：想看「多個 agent 跑完整研究 lifecycle 會長什麼樣」的研究者。研究架構參考、不是 production 工具。

**備註**：產出是 demo 等級（不是直接投稿用），ML / CS 領域偏多。License 是自訂的 source-available 條款（含 manuscript-disclosure 規定），使用前請先讀 LICENSE 檔。

---

> 還缺：peer-review 自動化、conference review pipeline 的活躍開源案例。如果你做過或知道有，歡迎開 PR。

## 必修閱讀

1. [The Effortless Academic — Claude Code beginner guides](https://effortlessacademic.com/claude-code-and-cowork-for-academics-beginner-guide-part-1/)
2. [Pedro Sant'Anna — Researcher setup guide](https://paulgp.substack.com/p/getting-started-with-claude-code)

## 必練流程

- **文獻分流**：用 `paper-qa` 對 PDF 庫做 grounded Q&A，再用 `gpt-researcher` 自動產 brief，輸出到 Obsidian / Notion
- **大綱驅動寫作**：用 `storm` 從主題自動產多角度大綱，再人工展開成正式段落
- **中文 paper workflow**：用 `ChatPaper` 過總結 / 翻譯 / 潤色，再人工 review
- **Zotero in-app AI**：裝 `zotero-gpt`，閱讀時直接對 selection 提問或總結
