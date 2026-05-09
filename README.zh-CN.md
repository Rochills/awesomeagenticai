<div align="right">
  <a href="./README.md">繁體中文</a> | <strong>简体中文</strong> | <a href="./README.en.md">English</a>
</div>

<div align="center">

![AI Agent 学习路径](resources/diagrams/banner.zh-CN.png)

# awesome-agentic-ai-zh

### 🤖 AI Agent 学习地图 — 从基础 LLM 概念到自己构建多 agent 系统

<p><em>结构化 7 阶段学习路径，从「LLM 是什么、token 怎么算」一路到 multi-agent 编排、本地部署，<br/>每阶段都有必做的 動手練習 练习、必修阅读、精选 project</em></p>

[![License](https://img.shields.io/badge/license-MIT-blue?style=flat)](LICENSE)
[![繁中](https://img.shields.io/badge/語言-繁體中文-red?style=flat)](README.md)
[![简中](https://img.shields.io/badge/語言-简体中文-orange?style=flat)](README.zh-CN.md)
[![EN](https://img.shields.io/badge/lang-English-blue?style=flat)](README.en.md)
![GitHub stars](https://img.shields.io/github/stars/WenyuChiou/awesome-agentic-ai-zh?style=flat&logo=github)
![GitHub forks](https://img.shields.io/github/forks/WenyuChiou/awesome-agentic-ai-zh?style=flat&logo=github)

</div>

---

## 🎯 项目介绍

这个项目是为“想学习 AI 或 AI agent 的人”设计的。

本 repo 把网上散落各处的高质量项目、教材、動手練習、必修阅读收集起来，按“从零开始、循序渐进”的顺序整理成 7 个阶段——每阶段都会清楚指出“该学什么、必做哪些 動手練習 练习、推荐哪几个 project、进入下一阶段前该检查什么”。

走完这条路线，你会从“LLM 用户”进阶到“agent 系统构建者”——能看懂 framework 在做什么、能设计多 agent 协作、能写自己的 MCP server。

---

## 📚 快速开始

### 在线阅读
- **[学习地图（两条学习路径）](#️-学习地图两条学习路径)** — 看完这节决定走 Track A 还 Track B
- **[Stage 0 基础准备](stages/00-foundations.zh-CN.md)** — 已经会 Python / git / API 的人可以直接跳 Stage 1

### 本地下载
```bash
git clone https://github.com/WenyuChiou/awesome-agentic-ai-zh.git
cd awesome-agentic-ai-zh
# 从 stages/00-foundations.zh-CN.md 开始
```

### ✨ 你会收获什么？

- 📖 **完全免费** — MIT 授权，所有内容开放共学
- 🗺️ **两条学习路径** — Track A（CLI Power User）给“想 USE 现成 CLI agent”的人；Track B（Agent Builder）给“想 BUILD 自己 agent”的人。共用 Stage 0-2 基础
- 🛠️ **必做 動手練習 练习** — 每阶段都有 1-5 个 mini project（题目 + 成功标准，**自己动手写**），光看不练不算学会
- 🎯 **精选 145+ 个 projects** — 每个都附星等推荐、适合谁、教什么、怎么跑（含本地 LLM 执行：Ollama、llama.cpp、LocalAI、MLX）
- 🌏 **中文 / 英文双语** — 简体中文为主、英文版完整对照
- 🎓 **不只「框架」、还有「Claude Code 生态」** — MCP / Skills / Plugins 完整堆叠
- 🔬 **5 条依用户分流的延伸路线** — 研究员 / 开发者 / 老师 / 知识工作者 / 日常用户
- ⏱️ **预估时程写清楚** — 主干最少 14-19 周、现实 5-6 个月（每周 5-8 hr）

---

## 🗺️ 学习地图（两条学习路径）

![AI Agent 学习地图](resources/diagrams/learning-map.zh-CN.png)

走完 **Stage 0-2（共用基础）** 之后，依你的目的选一条学习路径：

- **Track A — CLI Power User**：你想**用**现成的 CLI agent（Claude Code、Codex、OpenCode、Gemini CLI 等）把工作做顺、效率拉高，不打算自己从零写 agent。3 个 sub-stage（A1-A3）。
- **Track B — Agent Builder**:  你想**从零构建**自己的 agent——学 framework、写 ReAct、设计 multi-agent。Stage 3-7 是主路线。

两条学习路径**不互斥**——多数人是先走 A 把 CLI 用起来，再回到 B 学内部运作；或反过来也行。Stage 5（Claude Code 生态）两条路径都会用到。

### 共用基础（Stage 0-2）

| Stage | 主题 | 关键内容 | 预估时程 |
|---|---|---|---|
| **0** | [基础准备](stages/00-foundations.zh-CN.md) | Python · CLI · git · API · JSON | 1-2 周 |
| **1** | [LLM 入门](stages/01-llm-basics.zh-CN.md) | token · API · 各家 LLM 比较 · 本地 LLM | 1 周 |
| **2** | [Prompt 设计](stages/02-prompt-engineering.zh-CN.md) | 系统 prompt · few-shot · CoT | 1-2 周 |

### Track A — CLI Power User（想用 CLI 把事情做完）

| Stage | 主题 | 关键内容 | 预估时程 |
|---|---|---|---|
| **A1** | [CLI Agent 入门 + 选择](tracks/cli/A1-cli-intro.zh-CN.md) | 6 个主流 CLI 比较 · 安装 · 第一次跑 | 1 周 |
| **A2** | [CLI Workflow Patterns](tracks/cli/A2-cli-workflow.zh-CN.md) | CLAUDE.md · slash command · 多步骤拆解 | 1-2 周 |
| **A3** | [Integration & Production](tracks/cli/A3-cli-production.zh-CN.md) | MCP 接 CLI · CI 自动化 · cost / observability | 1-2 周 |

> **Track A 预估总时程**：3-5 周（含 Stage 0-2 约 6-8 周）。核心参考：[`resources/cli-agents-guide.zh-CN.md`](resources/cli-agents-guide.zh-CN.md)。

### Track B — Agent Builder（想从零构建 agent）

| Stage | 主题 | 关键内容 | 预估时程 |
|---|---|---|---|
| **3** ⭐ | Tool Use & Agent 入門 | function calling · ReAct · 5 个动手练习 | 2-3 周 |
| **4** | Agent 框架 | LangGraph · AutoGen · CrewAI · Smolagents | 2-3 周 |
| **5** ⭐⭐ | Claude Code 生态 | MCP · Skills · Plugins · Marketplace（两条路径都会用到） | 3-4 周 |
| **6** | Memory · RAG · 进阶 | vector DB · long-term memory · contextual retrieval | 2 周 |
| **7** | 进阶 Multi-Agent | multi-agent orchestration · eval · observability · SDK 进阶 | 2-4 周 |

> **Track B 预估总时程**：主干最少 **14-19 周**、现实 **5-6 个月**（每周 5-8 hr 兼职）

> 💡 **想看跨 stage 的完整示例？** [7 步构建你的第一个 AI Agent](walkthroughs/build-first-agent-in-7-steps.zh-CN.md) — 同一个 Paper Summary Bot 从 Stage 1 一路写到 Stage 7，~350 行真实代码（**Track B 适用**）

走完主干（14-19 周）后，依你的身份挑一条延伸路线继续走。**不确定挑哪条？**

![Branch 决策树](resources/diagrams/branch-decision-tree.zh-CN.png)

> 💡 **“日常用户”这条路线不必走完主干就能直接读**——是给“想用 AI、但不一定要写 code”的人。

| 路线 | 适合谁 | 主题 |
|---|---|---|
| 🔬 [研究员](branches/for-researcher.zh-CN.md) | 研究生、博后、PI | 文献整理 · paper 写作 · multi-agent review |
| 💻 [开发者](branches/for-developer.zh-CN.md) | 软件工程师 | Cursor · Aider · CLI delegation · code review |
| 🎓 [老师](branches/for-teacher.zh-CN.md) | 老师、讲师 | 备课 · 幻灯片 · 学生 feedback · 隐私 / 伦理 · prompt 范本 |
| 📊 [知识工作者](branches/for-knowledge-worker.zh-CN.md) | 顾问、PM、分析师 | Email · 会议记录 · report 自动化 |
| 👥 [日常用户](branches/for-everyday-users.zh-CN.md) | ChatGPT / Claude.ai 用户 | 写信 · 学习 · 隐私场景 · CLI agent 入门 |

---

## 💡 如何学习

这份路线图兼顾概念与实作，目标是带你“从 LLM 用户一路走到 agent 系统构建者”。适合“有基本 Python 能力”的开发者、研究生、自学者。动手之前，先确认你有：

- 基本 Python — 写过 function、用过 API、看得懂 JSON
- 基本 git — clone、commit、push
- 想学的动机 — agent 是 2025 年之后变化最快的领域，需要持续投入

上面有缺的就从 Stage 0 补齐；都会了就直接跳 Stage 1。

主干分 4 部分：

- **Part 1（Stage 0-2）：基础与 LLM 入门** — Python / git / API、什么 LLLM、怎么设计 prompt
- **Part 2（Stage 3-4）：构建你的 Agent** — 从 tool use 进化到 agent，学主流 framework
- **Part 3（Stage 5）：Claude Code 生态** — MCP / Skills / Plugins，这是整条路线的核心
- **Part 4（Stage 6-7）：进阶集成** — memory / RAG / multi-agent 协作

走完主干（14-19 周）后，依你的身份挑一条延伸路线继续走。

最重要的说一句话：**不要跳过 動手練習**。每个 stage 的 動手練習都是“不动手就学不会”的东西，光读过去后面会卡住。

准备好了吗？[从 Stage 0 开始](stages/00-foundations.zh-CN.md)。

---

## 📚 相关资源

### 三个核心用语：MCP / Skills / Plugins

README 跟各 stage 会频繁提到这三个 Claude Code 生态的关键词，先快速说明：

- **MCP（Model Context Protocol）** — Anthropic 推的开放协议，让任何 LLM host（Claude Code、其他 IDE、自写 agent）都能用同一套接口去呼叫外部 tool server（文件、DB、API、自家服务）。把它想成“LLM 的 USB 接口”。详见 [Stage 5.2](stages/05-claude-code-ecosystem.zh-CN.md#52--mcpmodel-context-protocol-基础)。
- **Skills** — Claude Code 的“行为包”。一个 Skill 就是一份 `SKILL.md`，描述“在什么情境要做什么、可以呼叫哪些 MCP tool”。写好之后 Claude Code 会自动 discover。详见 [Stage 5.3](stages/05-claude-code-ecosystem.zh-CN.md#53--skillsclaude-code-的行为层)。
- **Plugins / Marketplaces** — 把 Skills、slash commands、hooks、MCP 设置打包成一个发布单位给 team 或社群安装。Marketplace 就是 plugin 的 catalog。详见 [Stage 5.4](stages/05-claude-code-ecosystem.zh-CN.md#54--plugins-与-marketplaces)。

对, 应的 動手練習 练习都在 [Stage 5](stages/05-claude-code-ecosystem.zh-CN.md)，Track A 的 [A3](tracks/cli/A3-cli-production.zh-CN.md) 也会用到。

### 接日常工具：常用 MCP server / Skill

把 Claude Code（或其他 CLI agent）接到你已经在用的 app，省掉手动切换的成本。下面几个是社群 / 官方比较成熟的：

**笔记 / 知识库**

- [**MarkusPfundstein/mcp-obsidian**](https://github.com/MarkusPfundstein/mcp-obsidian) ★ 3.5k+ — 通过 Obsidian REST API plugin 让 LLM 读写你的 Obsidian vault
- [**makenotion/notion-mcp-server**](https://github.com/makenotion/notion-mcp-server) ★ 4k+ — Notion **官方** MCP server，可查询／创建 page、database
- [**PleasePrompto/notebooklm-skill**](https://github.com/PleasePrompto/notebooklm-skill) ★ 6k+ — NotebookLM Skill（浏览器自动化），用 Claude Code 直接查你 NotebookLM 里的文件，回答带 citation
- [**teng-lin/notebooklm-py**](https://github.com/teng-lin/notebooklm-py) ★ 12k+ — 非官方 NotebookLM Python API + CLI，支持 Claude Code / Codex 等 agent 集成

**办公文件（Word / Excel / PowerPoint / PDF）**

- [**anthropics/skills**](https://github.com/anthropics/skills) ★ 129k+ — Anthropic **官方** Skills 集合，docx / xlsx / pptx / pdf 处理直接内置
- [**tfriedel/claude-office-skills**](https://github.com/tfriedel/claude-office-skills) ★ 580+ — 增强版 Office skills（PPTX/DOCX/XLSX/PDF），含自动化 workflow

**Google Workspace（Gmail / Docs / Drive / Calendar）**

- [**taylorwilsdon/google_workspace_mcp**](https://github.com/taylorwilsdon/google_workspace_mcp) ★ 2.3k+ — 一个 server 包整套 Google Workspace（Gmail、Calendar、Docs、Sheets、Slides、Drive）

**开发协作**

- [**github/github-mcp-server**](https://github.com/github/github-mcp-server) ★ 29k+ — GitHub **官方** MCP，issue / PR / repo 操作
- [**atlassian/atlassian-mcp-server**](https://github.com/atlassian/atlassian-mcp-server) ★ 650+ — Atlassian **官方** Remote MCP（Jira、Confluence）
- [**jerhadf/linear-mcp-server**](https://github.com/jerhadf/linear-mcp-server) ★ 340+ — Linear MCP server
- [**korotovsky/slack-mcp-server**](https://github.com/korotovsky/slack-mcp-server) ★ 1.5k+ — Slack MCP，无 admin 权限也能用

**中文圈常用**

- [**leemysw/feishu-docx**](https://github.com/leemysw/feishu-docx) ★ 190+ — 飞书（Lark）docs / sheet / bitable ↔ Markdown，含 Claude Skills 支持

> 上面只是 highlight。**完整 57 个集成**（含数据库、浏览器自动化、Figma、Excalidraw、Cloudflare、Stripe…）：[`resources/mcp-skills-catalog.zh-CN.md`](resources/mcp-skills-catalog.zh-CN.md)。

> 想找更多 MCP server catalog？看 [`wong2/awesome-mcp-servers`](https://github.com/wong2/awesome-mcp-servers) / [`punkpeye/awesome-mcp-servers`](https://github.com/punkpeye/awesome-mcp-servers)（按分类整理）。**Canva** 的官方 MCP 还在 early access，社群版本不稳定，等成熟后再补上。

### 同主题的清单型 awesome lists

这个 repo **不取代**清单型 awesome list — 你已经知道在找什么工具时，下面这些查起来更直接：

**MCP 相关**

- [**modelcontextprotocol/servers**](https://github.com/modelcontextprotocol/servers) — 官方 MCP reference servers（filesystem、github、sqlite、git、fetch、memory 等）
- [**wong2/awesome-mcp-servers**](https://github.com/wong2/awesome-mcp-servers) — 社群 MCP server 清单，按分类整理（150+ 个）
- [**punkpeye/awesome-mcp-servers**](https://github.com/punkpeye/awesome-mcp-servers) — 另一份 MCP server 清单

**Claude Code / Skills / Plugins 相关**

- [**hesreallyhim/awesome-claude-code**](https://github.com/hesreallyhim/awesome-claude-code) — Claude Code 相关工具与 plugin 清单（整理中）
- [**travisvn/awesome-claude-skills**](https://github.com/travisvn/awesome-claude-skills) — Claude Skills 清单
- [**anthropics/claude-plugins-official**](https://github.com/anthropics/claude-plugins-official) — Anthropic 官方 plugin 模板，要打包自己的 plugin 从这份开始

**中文圈常用**

- [**datawhalechina/hello-agents**](https://github.com/datawhalechina/hello-agents) — Datawhale 系统性 agent 教学（zh-CN）
- [**WangRongsheng/awesome-LLM-resources**](https://github.com/WangRongsheng/awesome-LLM-resources) — 完整的中文 LLM 资源整理（8k+ stars）
- [**AiHubCN/Awesome-Chinese-LLM**](https://github.com/AiHubCN/Awesome-Chinese-LLM) — 中文开源大模型整理

---

## 🤝 如何贡献

这个 repo 是一个 AI 学习文档，如果你也有收集很好的资源，也欢迎贡献：

- 🐛 **汇报 Bug** — 内容错误、链接失效、过时信息 → 开 Issue
- 💡 **提建议** — 缺什么 stage、该加哪个 project → 开 Issue 讨论
- 📝 **完善内容** — 改进现有 stage 内容、修 typo → 直接 PR
- ✍️ **新增 project** — 在某个 stage 加 1-3 个 project，并附上“为什么这个 project 适合放这个 stage”的说明
- 🌏 **翻译** — 补英文 companion 没翻到的段落，或翻成其他语言
- 🌱 **担任 Stage / Branch maintainer** — 长期 review 特定领域，详见 [CONTRIBUTING.md](CONTRIBUTING.md) 和 [resources/style-guide.zh-CN.md](resources/style-guide.zh-CN.md)。

PR 流程跟 style 规范请看 [CONTRIBUTING.md](CONTRIBUTING.md) 和 [resources/style-guide.zh-CN.md](resources/style-guide.zh-CN.md)。

> Maintainer 内部进度与 launch checklist 放在 [.github/launch-checklist.md](.github/launch-checklist.md)（内部文件）。

---

## 🙏 致谢

### Inspiration

- [**Datawhale Hello-Agents**](https://github.com/datawhalechina/hello-agents) — 系统性 agent 教学的模板，本 repo 的“章节 + 进度”结构就是受这份启发
- [**Datawhale 社群**](https://github.com/datawhalechina) — 中文 ML 共学社群的标杆，本 repo 多个 anchor project 来自这里
- [**liyupi/ai-guide**](https://github.com/liyupi/ai-guide) — 中文圈最大"AI 资源大全" + Vibe Coding 教学（涵盖 Agent Skills / RAG / MCP / A2A / Harness Engineering）。本 repo 是"结构化路线"、ai-guide 是"广度资源库"，互为补充

### 其他相关项目

同主题、不同切入角度的清单，搜资源时可以一起用：

- [`wong2/awesome-mcp-servers`](https://github.com/wong2/awesome-mcp-servers) — MCP server 清单，按分类整理
- [`punkpeye/awesome-mcp-servers`](https://github.com/punkpeye/awesome-mcp-servers) — 另一份 MCP server 清单
- [`hesreallyhim/awesome-claude-code`](https://github.com/hesreallyhim/awesome-claude-code) — Claude Code 相关工具与 plugin 清单（整理中）
- [`travisvn/awesome-claude-skills`](https://github.com/travisvn/awesome-claude-skills) — Claude Skills 清单
- [`anthropics/claude-plugins-official`](https://github.com/anthropics/claude-plugins-official) — Anthropic 官方 plugin 模板，要打包自己的 plugin 从这份开始
- [`nowork-studio/awesome-ai-startups`](https://github.com/nowork-studio/awesome-ai-startups) — 独立开发者打造的 bootstrapped、pre-seed 与天使轮 AI 产品精选清单

这些是纯清单形式（看到再挑），本 repo 的不同点是有“从 Stage 0 一路走到 production 的学习顺序”。

### 贡献者

[![Contributors](https://contrib.rocks/image?repo=WenyuChiou/awesome-agentic-ai-zh)](https://github.com/WenyuChiou/awesome-agentic-ai-zh/graphs/contributors)

新贡献者会自动出现在上方。完整列表 → [GitHub Contributors](https://github.com/WenyuChiou/awesome-agentic-ai-zh/graphs/contributors)。

### 个人

- [@WenyuChiou](https://github.com/WenyuChiou) — Maintainer

---

## 🎓 引用

如果这个学习地图对你的学习或工作有帮助，欢迎引用：

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

## 📈 Star History

[![Star History Chart](https://api.star-history.com/svg?repos=WenyuChiou/awesome-agentic-ai-zh&type=Date)](https://star-history.com/#WenyuChiou/awesome-agentic-ai-zh&Date)

---

## License

MIT。Maintained by [@WenyuChiou](https://github.com/WenyuChiou)。

<div align="center">
  <p>⭐ 如果这个 repo 对你有帮助，欢迎给个 Star — 这对作者继续更新是很大的鼓励</p>
</div>
