<div align="right">
  <strong>繁體中文</strong> | <a href="./README.zh-CN.md">简体中文</a> | <a href="./README.en.md">English</a>
</div>

<div align="center">

![AI Agent 學習路徑](resources/diagrams/banner.png)

# awesome-agentic-ai-zh

### 🤖 AI Agent 學習地圖 — 從基本 LLM 概念到自己打造多 agent 系統

<p><em>結構化 7 階段學習路徑，從「LLM 是什麼、token 怎麼算」一路到 multi-agent 編排、本地部署，<br/>每階段都有必做的 動手練習、必修閱讀、精選 project</em></p>

[![License](https://img.shields.io/badge/license-MIT-blue?style=flat)](LICENSE)
[![繁中](https://img.shields.io/badge/語言-繁體中文-red?style=flat)](README.md)
[![简中](https://img.shields.io/badge/語言-简体中文-orange?style=flat)](README.zh-CN.md)
[![EN](https://img.shields.io/badge/lang-English-blue?style=flat)](README.en.md)
![GitHub stars](https://img.shields.io/github/stars/WenyuChiou/awesome-agentic-ai-zh?style=flat&logo=github)
![GitHub forks](https://img.shields.io/github/forks/WenyuChiou/awesome-agentic-ai-zh?style=flat&logo=github)

</div>

---

## 🎯 專案介紹

- [OpenClaw Monitor](https://github.com/flik2002/openclaw-monitor) - Real-time AI agent monitoring dashboard for OpenClaw — tracks Gateway status, sessions, token usage & trends


這個專案是為**想學習 AI 或 AI agent 的人**設計的。

本 repo 把網路上散落各處的高品質專案、教材、動手練習、必修閱讀蒐集起來，按**從零開始、循序漸進**的順序整理成 **7 個階段**——每階段都會清楚指出**該學什麼、必做哪些 動手練習、推薦哪幾個 project、進入下一階段前該檢查什麼**。

走完整條路線，你會從「**LLM 使用者**」進階到「**agent 系統建構者**」——能看懂 framework 在做什麼、能設計多 agent 協作、能寫自己的 MCP server。

---

## 📋 目錄

- [🎯 專案介紹](#-專案介紹)
- [📚 快速開始](#-快速開始)
  - [線上閱讀](#線上閱讀)
  - [本地下載](#本地下載)
  - [✨ 你會收穫什麼？](#-你會收穫什麼)
- [🗺️ 學習地圖（兩條學習路徑）](#️-學習地圖兩條學習路徑)
- [💡 如何學習](#-如何學習)
- [📚 相關資源](#-相關資源)
- [🤝 如何貢獻](#-如何貢獻)
- [🙏 致謝](#-致謝)
- [🎓 引用](#-引用)
- [License](#license)

---

## 📚 快速開始

### 線上閱讀
- **[學習地圖（兩條學習路徑）](#️-學習地圖兩條學習路徑)** — 看完這節決定走 Track A 還 Track B
- **[Stage 0 基礎準備](stages/00-foundations.md)** — 已經會 Python / git / API 的人可以直接跳 Stage 1

### 本地下載
```bash
git clone https://github.com/WenyuChiou/awesome-agentic-ai-zh.git
cd awesome-agentic-ai-zh
# 從 stages/00-foundations.md 開始
```

### ✨ 你會收穫什麼？

- 📖 **完全免費** — MIT 授權，所有內容開放共學
- 🗺️ **兩條學習路徑** — Track A（CLI Power User）給「想 USE 現成 CLI agent」的人；Track B（Agent Builder）給「想 BUILD 自己 agent」的人。共用 Stage 0-2 基礎
- 🛠️ **必做動手練習** — 每階段都有 1-5 個 mini project（題目 + 成功標準，**自己動手寫**，不是現成 demo），光看不練不算學會
- 🎯 **精選 145+ 個 projects** — 每個都附星等推薦、適合誰、教什麼、怎麼跑（含本地 LLM 執行：Ollama、llama.cpp、LocalAI、MLX）
- 🌏 **中文 / 英文雙語** — 繁中為主、英文版完整對照
- 🎓 **不只「框架」、還有「Claude Code 生態」** — MCP / Skills / Plugins / SDK 完整堆疊
- 🔬 **5 條依使用者分流的延伸路線** — 研究員 / 開發者 / 老師 / 知識工作者 / **日常使用者**
- ⏱️ **預估時程寫清楚** — 主幹最少 14-19 週、現實 5-6 個月（每週 5-8 hr）

---

## 🗺️ 學習地圖（兩條學習路徑）

![AI Agent 學習地圖](resources/diagrams/learning-map.png)

走完 **Stage 0-2（共用基礎）** 之後，依你的目的選一條學習路徑：

- **Track A — CLI Power User**：你想**用**現成的 CLI agent（Claude Code、Codex、OpenCode、Gemini CLI 等）把工作做順、效率拉高，不打算自己從零寫 agent。3 個 sub-stage（A1-A3）。
- **Track B — Agent Builder**：你想**從零打造**自己的 agent——學 framework、寫 ReAct、設計 multi-agent。Stage 3-7 是主路線。

兩條學習路徑**不互斥**——多數人是先走 A 把 CLI 用起來，再回到 B 學內部運作；或反過來也行。Stage 5（Claude Code 生態）兩條路徑都會用到。

### 共用基礎（Stage 0-2）

| Stage | 主題 | 關鍵內容 | 預估時程 |
|---|---|---|---|
| **0** | [基礎準備](stages/00-foundations.md) | Python · CLI · git · API · JSON | 1-2 週 |
| **1** | [LLM 入門](stages/01-llm-basics.md) | token · API · 各家 LLM 比較 · 本地 LLM | 1 週 |
| **2** | [Prompt 設計](stages/02-prompt-engineering.md) | 系統 prompt · few-shot · CoT | 1-2 週 |

### Track A — CLI Power User（想用 CLI 把事情做完）

| Stage | 主題 | 關鍵內容 | 預估時程 |
|---|---|---|---|
| **A1** | [CLI Agent 入門 + 選擇](tracks/cli/A1-cli-intro.md) | 6 主流 CLI 比較 · 安裝 · 第一次跑 | 1 週 |
| **A2** | [CLI Workflow Patterns](tracks/cli/A2-cli-workflow.md) | CLAUDE.md · slash command · 多步驟拆解 | 1-2 週 |
| **A3** | [Integration & Production](tracks/cli/A3-cli-production.md) | MCP 接 CLI · CI 自動化 · cost / observability | 1-2 週 |

> **Track A 預估總時程**：3-5 週（含 Stage 0-2 約 6-8 週）。核心參考：[`resources/cli-agents-guide.md`](resources/cli-agents-guide.md)。

### Track B — Agent Builder（從零打造 agent）

| Stage | 主題 | 關鍵內容 | 預估時程 |
|---|---|---|---|
| **3** ⭐ | [Tool Use & Agent 入門](stages/03-tool-use-and-hello-agent.md) | function calling · ReAct · 5 個動手練習 | 2-3 週 |
| **4** | [Agent 框架](stages/04-agent-frameworks.md) | LangGraph · AutoGen · CrewAI · Smolagents | 2-3 週 |
| **5** ⭐⭐ | [Claude Code 生態](stages/05-claude-code-ecosystem.md) | MCP · Skills · Plugins · Marketplace（兩條路徑都會用到） | 3-4 週 |
| **6** | [Memory · RAG · 進階](stages/06-memory-rag.md) | vector DB · long-term memory · contextual retrieval | 2 週 |
| **7** | [進階 Multi-Agent](stages/07-multi-agent-production.md) | multi-agent orchestration · eval · observability · SDK 進階 | 2-4 週 |

> **Track B 預估總時程**：主幹最少 **14-19 週**、現實 **5-6 個月**（每週 5-8 hr 兼職）

> 💡 **想看跨 stage 的完整範例？** [7 步打造你的第一個 AI Agent](walkthroughs/build-first-agent-in-7-steps.md) — 同一個 Paper Summary Bot 從 Stage 1 一路寫到 Stage 7，~350 行真實程式碼（**Track B 適用**）

走完主幹後，依你的身分挑一條延伸路線繼續走。**不確定挑哪條？**

![Branch 決策樹](resources/diagrams/branch-decision-tree.png)

> 💡 **「日常使用者」這條路線不必走完主幹就能直接讀**——是給「想用 AI、但不一定要寫 code」的人。

| 路線 | 適合誰 | 主題 |
|---|---|---|
| 🔬 [研究人員](branches/for-researcher.md) | 研究生、博後、PI | 文獻整理 · paper 寫作 · multi-agent review |
| 💻 [開發者](branches/for-developer.md) | 軟體工程師 | Cursor · Aider · CLI delegation · code review |
| 🎓 [教師](branches/for-teacher.md) 🚧 | 老師、講師 | 備課 · 投影片 · 學生 feedback *（目前最薄、歡迎貢獻）* |
| 📊 [知識工作者](branches/for-knowledge-worker.md) | 顧問、PM、分析師 | Email · 會議紀錄 · report 自動化 |
| 👥 [日常使用者](branches/for-everyday-users.md) | ChatGPT / Claude.ai 使用者 | 寫信 · 學習 · 隱私場景 · CLI agent 入門 |

---

## 💡 如何學習

這份路線圖兼顧概念與實作，目標是帶你**從 LLM 使用者一路走到 agent 系統建構者**。適合**有基本 Python 能力**的開發者、研究生、自學者。動手之前，先確認你有：

- **基本 Python** — 寫過 function、用過 API、看得懂 JSON
- **基本 git** — clone、commit、push
- **想學的動機** — agent 是 2025 年之後變化最快的領域，需要持續投入

上面有缺的就從 Stage 0 補齊；都會了就**直接跳 Stage 1**。

主幹分 4 部分：

- **Part 1（Stage 0-2）：基礎與 LLM 入門** — Python / git / API、什麼是 LLM、怎麼設計 prompt
- **Part 2（Stage 3-4）：建構你的 Agent** — 從 tool use 進化到 agent，學主流 framework
- **Part 3（Stage 5）：Claude Code 生態系** — MCP / Skills / Plugins，這是整條路線的核心
- **Part 4（Stage 6-7）：進階整合** — memory / RAG / multi-agent 協作

走完主幹（14-19 週）後，依你的身分（研究員 / 開發者 / 老師 / 知識工作者 / 日常使用者）挑一條延伸路線繼續走。

最重要的一句話：**不要跳過 動手練習**。每個 stage 的 動手練習都是「不動手就學不會」的東西，光讀過去後面會卡住。

準備好了嗎？[從 Stage 0 開始](stages/00-foundations.md)。

---

## 📚 相關資源

完整的相關資源（用語說明 + 常用 MCP / Skill highlight + awesome lists + 中文社群）抽到 **[RESOURCES.md](RESOURCES.md)** 避免主頁過長。

直接看常用入口：

- 📖 **不懂某個詞？**（LLM、agent、RAG、token、MCP、Skill、向量資料庫⋯）→ [`resources/glossary.md`](resources/glossary.md) — 30 多個常出現的詞，每個 30-80 字解釋 + 哪 stage 講細的
- 🍳 **想動手做出來**（寫 Skill / 寫 MCP server / 接 Word / 接 NotebookLM / 接 Zotero）→ [`resources/cookbook.md`](resources/cookbook.md) — 5 個 step-by-step recipe（每個 30-50 分鐘）
- 🔑 **MCP / Skills / Plugins 用語怎麼解釋** → [RESOURCES.md §三個核心用語](RESOURCES.md#三個核心用語mcp--skills--plugins)
- 🔌 **接 Notion / Obsidian / Excel / GitHub 等日常工具** → [RESOURCES.md §接日常工具](RESOURCES.md#接日常工具常用-mcp-server--skill) 或完整 57 條目錄 [`resources/mcp-skills-catalog.md`](resources/mcp-skills-catalog.md)
- 🔬 **研究 workflow + multi-LLM delegation skill 對** → [RESOURCES.md §研究工作流](RESOURCES.md#研究工作流本-repo-維護者出品)
- 📚 **同主題的 awesome list / 中文社群** → [RESOURCES.md §同主題清單](RESOURCES.md#同主題的清單型-awesome-lists)

---

## 🤝 如何貢獻

這是一個開放共學的社群，歡迎各種貢獻：

- 🐛 **回報 Bug** — 內容錯誤、連結失效、過時資訊 → 開 Issue
- 💡 **提建議** — 缺什麼 stage、該加哪個 project → 開 Issue 討論
- 📝 **完善內容** — 改進現有 stage 內容、修 typo → 直接 PR
- ✍️ **新增 project** — 在某個 stage 加 1-3 個 project，並附上「為什麼這個 project 適合放這個 stage」的說明
- 🌏 **翻譯** — 補英文 companion 沒翻到的段落，或翻成其他語言
- 🌱 **擔任 Stage / Branch maintainer** — 長期 review 特定領域，詳見 [CONTRIBUTORS.md](CONTRIBUTORS.md)

PR 流程跟 style 規範請看 [CONTRIBUTING.md](CONTRIBUTING.md) 跟 [resources/style-guide.md](resources/style-guide.md)。

> Maintainer 內部進度與 launch checklist 放在 [`.github/launch-checklist.md`](.github/launch-checklist.md)（內部文件）。

---

## 🙏 致謝

### Inspiration

- [**Datawhale Hello-Agents**](https://github.com/datawhalechina/hello-agents) — 系統性 agent 教學的範本，本 repo 的「章節 + 進度」結構就是受這份啟發
- [**Datawhale 社群**](https://github.com/datawhalechina) — 中文 ML 共學社群的標竿，本 repo 多個 anchor project 來自這裡
- [**liyupi/ai-guide**](https://github.com/liyupi/ai-guide) — 中文圈最大「AI 資源大全」，跟 Vibe Coding 教學齊全（涵蓋 Agent Skills / RAG / MCP / A2A / Harness Engineering）。本 repo 是「結構化路線」、ai-guide 是「廣度資源庫」，互為補充

### 其他相關專案

同主題、不同切入角度的清單，搜資源時可以一起用：

- [`wong2/awesome-mcp-servers`](https://github.com/wong2/awesome-mcp-servers) — MCP server 清單，按分類整理
- [`punkpeye/awesome-mcp-servers`](https://github.com/punkpeye/awesome-mcp-servers) — 另一份 MCP server 清單
- [`hesreallyhim/awesome-claude-code`](https://github.com/hesreallyhim/awesome-claude-code) — Claude Code 相關工具與 plugin 清單

這些是純清單形式（看到再挑），本 repo 的不同點是有「**從 Stage 0 一路走到 production 的學習順序**」。

### 個人

- [@WenyuChiou](https://github.com/WenyuChiou) — Maintainer

---

## 🎓 引用

如果這個學習地圖對你的學習或工作有幫助，歡迎引用：

```bibtex
@misc{awesome_agentic_ai_zh_2026,
  title  = {awesome-agentic-ai-zh: A Structured Learning Roadmap for Agentic AI},
  author = {Chiou, Wenyu},
  year   = {2026},
  url    = {https://github.com/WenyuChiou/awesome-agentic-ai-zh},
  note   = {7-stage learning path from prerequisites to advanced multi-agent systems, with curated projects + hello-X demos. Bilingual (zh-TW / English).}
}
```

---

## License

MIT。Maintained by [@WenyuChiou](https://github.com/WenyuChiou)。

<div align="center">
  <p>⭐ 如果這個 repo 對你有幫助，歡迎給個 Star — 這對作者繼續更新是很大的鼓勵</p>
</div>
