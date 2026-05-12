# 给研究者 — 专业分支

> [繁體中文](./for-researcher.md) | **简体中文** | [English](./for-researcher.en.md) | [Русский](./for-researcher.ru.md)

> 🚀 **第一次装 Python / 申请 API key？** 先看 [`resources/setup-guide.zh-Hans.md` §A-C](../resources/setup-guide.zh-Hans.md)。本分支默认你会跑 Python script、有 API key、会用 git。

> [← 回主路线 README](../README.zh-Hans.md) · 走完 **Track A 的 A3** 或 **Track B 的 Stage 7** 后从这里接续。把 agentic AI 应用到研究流程上。

## 使用场景

- 文献分流与比较矩阵建立
- 论文记忆提取（claim、figure、citation）
- Multi-agent 论文审查（peer review 模式）
- NotebookLM brief 验证
- 文献管理自动化

## 精选 Projects

> 💡 **想把 Claude Code 接到 NotebookLM、Obsidian、Notion、Excel、PDF、Excalidraw 等研究常用工具？** 62 个集成在 [`resources/mcp-skills-catalog.zh-Hans.md`](../resources/mcp-skills-catalog.zh-Hans.md)（按使用场景分类）。下面这节保留「研究专属」的工具与 marketplace。

### 研究流程 Marketplace

#### [flonat/claude-research](https://github.com/flonat/claude-research) ⭐⭐⭐

给博士研究者的 Claude Code 基础建设——学术流程用的 skill、agent、hook、规则。LaTeX / 文献管理为主。

---

### 文献 RAG / Q&A

#### [Future-House/paper-qa](https://github.com/Future-House/paper-qa) ⭐⭐⭐⭐⭐

| 栏位 | 内容 |
|---|---|
| Stars | ★ 8k+ |
| License | Apache-2.0 |

**教什么**：对 PDF 文件做高准确率的 RAG，每个答案都附 grounded citation（句子层级的引用）。

**适合谁**：写文献回顾、需要「查文献时答案要可追溯」的研究者。比一般 RAG 更严谨。

---

#### [assafelovic/gpt-researcher](https://github.com/assafelovic/gpt-researcher) ⭐⭐⭐⭐

| 栏位 | 内容 |
|---|---|
| Stars | ★ 27k+ |
| License | Apache-2.0 |

**教什么**：自主 deep-research agent——planner + multi-source crawl + report 合成。给定一个研究主题，自动产出 markdown / PDF brief。

**适合谁**：要快速 scope 新题目、产 research brief 的研究者。

---

### 大纲与写作

#### [stanford-oval/storm](https://github.com/stanford-oval/storm) ⭐⭐⭐⭐

| 栏位 | 内容 |
|---|---|
| Stars | ★ 28k+ |
| License | MIT |

**教什么**：multi-perspective outline-then-write pipeline——agent 从多个角度先产大纲、再展开成 Wikipedia-style 文章。Stanford OVAL 出品。

**适合谁**：想学「**outline-driven 写作**」的人。从零产主题 brief 时的好工具，类似 NotebookLM structured report 流程的开源版。

**备注**：最后一次推送已超过 6 个月，使用前确认最新 commit 日期。

---

#### [kaixindelele/ChatPaper](https://github.com/kaixindelele/ChatPaper) ⭐⭐⭐⭐⭐（中文读者）

| 栏位 | 内容 |
|---|---|
| 语言 | 中文 + Python |
| Stars | ★ 19k+ |
| License | NOASSERTION（自定义条款，非商用） |

**教什么**：中文研究者向的 arXiv 全流程工具——论文总结 + 翻译 + 润色 + 审稿回复生成。中国研究团队维护，默认值对中文场景友好。

**适合谁**：中文研究生想找对中文友好的 paper 全流程入门工具。

**备注**：License 是自定义的非商用条款，使用前请先读原始条款；研究或个人用途常见，但条款还是要自己看过确认。

---

### 文献管理集成

#### [MuiseDestiny/zotero-gpt](https://github.com/MuiseDestiny/zotero-gpt) ⭐⭐⭐⭐

| 栏位 | 内容 |
|---|---|
| Stars | ★ 7k+ |
| License | AGPL-3.0 |

**教什么**：Zotero 的 LLM plugin——可以跟你的文献库对话、总结 selection、生成 inline notes。

**适合谁**：Zotero 重度用户，想在阅读流程里直接接 AI 而不用切到别的工具。

**备注**：AGPL-3.0 license（传染性开源）— 修改后要散布的衍生产品需遵守条款。

---

### 研究工作流 Skills（本 repo 维护者出品）

> 这几个是本 repo 维护者 [@WenyuChiou](https://github.com/WenyuChiou)（Lehigh CEE PhD candidate）日常在用的研究 skill / workspace。一并放到这里让其他研究者直接用。完整 entry 内容在 [`resources/mcp-skills-catalog.zh-Hans.md` §13-§14](../resources/mcp-skills-catalog.zh-Hans.md#13-研究工作流-skills学术--paper--文献)。

#### [WenyuChiou/ai-research-skills](https://github.com/WenyuChiou/ai-research-skills) ⭐⭐⭐⭐⭐

★ 60 · MIT — 14 个 Claude Code skills 涵盖研究全流程（文献分流、研究设计、project context、论文撰写、multi-AI delegation），打包成 5-plugin marketplace。一个指令装整套。

#### [WenyuChiou/research-hub](https://github.com/WenyuChiou/research-hub) ⭐⭐⭐⭐

★ 14 · MIT — Zotero + Obsidian + NotebookLM 三工具集成 workspace，提供 CLI / MCP / REST / dashboard 四种接口。同时用三个工具的研究者必看。

#### [WenyuChiou/zotero-skills](https://github.com/WenyuChiou/zotero-skills) ⭐⭐⭐⭐

★ 16 — Zotero CLI skill：搜 / 加 / 分类 / 标记。跟 zotero-gpt（在 Zotero 里 chat）互补，这份是让 Claude Code 从外部操作 Zotero。

#### [WenyuChiou/academic-writing-skills](https://github.com/WenyuChiou/academic-writing-skills) ⭐⭐⭐

★ 2 · MIT — 严谨学术论文撰写 / 修改 / 投稿 skill。banned-word audit、figure-text coupling、submission checklist 自动化。Per-paper 的 journal_format / style_overrides 可定制。

#### [WenyuChiou/codex-delegate](https://github.com/WenyuChiou/codex-delegate) ⭐⭐⭐⭐⭐ + [WenyuChiou/gemini-delegate-skill](https://github.com/WenyuChiou/gemini-delegate-skill) ⭐⭐⭐⭐

★ 57 + ★ 34 · MIT — Multi-LLM delegation skill 对。研究场景：Claude planner + Codex 跑实现（程序 / 图 / 表）+ Gemini 跑长文 draft（中文报告、英文 paper section）。是 Stage 7 multi-agent 的实战版。

---

### Multi-Agent for Research

#### [langchain-ai/open_deep_research](https://github.com/langchain-ai/open_deep_research) ⭐⭐⭐⭐⭐

| 栏位 | 内容 |
|---|---|
| Stars | ★ 11k+ |
| License | MIT |

**教什么**：开源版的 Deep Research——支持单 agent 跟 supervisor + multi-researcher 两种架构（multi-agent 那条目前在 `src/legacy/`）、平行搜索、再合成为有引用的 report。是学「LLM agent 怎么自动产出有引用 brief」的好参考。

**适合谁**：要打造「agent 自动产出有引用 brief」工作流程的研究者。是这个分类最 canonical 的开源选择。

**备注**：依赖 LangGraph + 搜索 tool（要 API key）。

---

#### [SakanaAI/AI-Scientist-v2](https://github.com/SakanaAI/AI-Scientist-v2) ⭐⭐⭐⭐

| 栏位 | 内容 |
|---|---|
| Stars | ★ 6k+ |
| License | The AI Scientist Source Code License（source-available，非商用 + 有 manuscript-disclosure 条款） |

**教什么**：端到端的 multi-agent 科学研究 loop：构想 → 写代码 → 跑实验 → 写 paper → 互审。Sakana AI 的「AI 写整篇 ML paper」研究实践。

**适合谁**：想看「多个 agent 跑完整研究生命周期会长什么样」的研究者。研究架构参考、不是 production 工具。

**备注**：产出是 demo 级别（不是直接投稿用），ML / CS 领域偏多。License 是自定义的 source-available 条款（含 manuscript-disclosure 规定），使用前请先读 LICENSE 文件。

---

> 还缺：peer-review 自动化、conference review pipeline 的活跃开源案例。如果你做过或知道有，欢迎开 PR。

## 必修阅读

1. [The Effortless Academic — Claude Code beginner guides](https://effortlessacademic.com/claude-code-and-cowork-for-academics-beginner-guide-part-1/)
2. [Pedro Sant'Anna — Researcher setup guide](https://paulgp.substack.com/p/getting-started-with-claude-code)

## 必练流程

- **文献分流**：用 `paper-qa` 对 PDF 库做 grounded Q&A，再用 `gpt-researcher` 自动产 brief，输出到 Obsidian / Notion
- **大纲驱动写作**：用 `storm` 从主题自动产多角度大纲，再人工展开成正式段落
- **中文 paper workflow**：用 `ChatPaper` 过总结 / 翻译 / 润色，再人工 review
- **Zotero in-app AI**：装 `zotero-gpt`，阅读时直接对 selection 提问或总结
