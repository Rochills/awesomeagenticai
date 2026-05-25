# 相关资源

> [繁體中文](./RESOURCES.md) | **简体中文** | [English](./RESOURCES.en.md)

> [← 返回主路线 README](README.zh-Hans.md)

这份文件集中放：用語说明、常用 MCP / Skill 集成 highlight、同主题 awesome list、中文社群资源。从主 README 抽出避免主页过长。

> 💡 **不懂某个词**（LLM、agent、RAG、token、向量数据库⋯）→ [`resources/glossary.zh-Hans.md`](resources/glossary.zh-Hans.md)（用語小词典，30 多个词每个 30-80 字解释）

---

## 三个核心用語：MCP / Skills / Plugins

主 README 跟各 stage 会频繁提到这三个 Claude Code 生态的关键***词***，先快速说明：

- **MCP（Model Context Protocol）** — Anthropic 推的开放协定，让任何 LLM host（Claude Code、其他 IDE、自写 agent）都能用同一套接口去调用外部 tool server（文件、DB、API、***自家***系统）。把它想成“LLM 的 USB 接口”。详见 [Stage 5.2](stages/05-claude-code-ecosystem.zh-Hans.md#52--mcpmodel-context-protocol-基础)。
- **Skills** — Claude Code 的“行为包”。一个 Skill 就是一份 `SKILL.zh-Hans.md`，描述“在什么***场景***要做什么、可以调用哪些 MCP tool”。写好之后 Claude Code 会自动 discover。详见 [Stage 5.3](stages/05-claude-code-ecosystem.zh-Hans.md#53--skillsclaude-code-的行为层-claude-code-生态最关键的一层)。
- **Plugins / Marketplaces** — 把 Skills、slash commands、hooks、MCP ***设置***打包成一个发布单位给 team 或社群***安装***。Marketplace 就是 plugin 的 catalog。详见 [Stage 5.4](stages/05-claude-code-ecosystem.zh-Hans.md#54--plugins-与-marketplaces)。

对应的 **动手*****练习***都在 [Stage 5](stages/05-claude-code-ecosystem.zh-Hans.md)，Track A 的 [A3](tracks/cli/A3-cli-production.zh-Hans.md) 也会用到。

---

## 接日常工具：常用 MCP server / Skill

把 Claude Code（或其他 CLI agent）接到你***已经***在用的 app，省掉***手动***切***换***的***成本***。下面几个是社群 / ***官方******比较***成熟的：

### 笔记 / 知识库

- [**MarkusPfundstein/mcp-obsidian**](https://github.com/MarkusPfundstein/mcp-obsidian) ★ 3.5k+ — 透过 Obsidian REST API plugin 让 LLM 读写你的 Obsidian vault
- [**makenotion/notion-mcp-server**](https://github.com/makenotion/notion-mcp-server) ★ 4k+ — Notion **官方** MCP server，可查询／建立 page、database
- [**PleasePrompto/notebooklm-skill**](https://github.com/PleasePrompto/notebooklm-skill) ★ 6.6k+ — NotebookLM Skill（浏览器***自动***化），用 Claude Code ***直接***查你 NotebookLM ***里***的文件，回答带 citation
- [**teng-lin/notebooklm-py**](https://github.com/teng-lin/notebooklm-py) ★ 15k+ — ***非官方*** NotebookLM Python API + CLI，***支持*** Claude Code / Codex 等 agent 集成

### 办公文件（Word / Excel / PowerPoint / PDF）

- [**anthropics/skills**](https://github.com/anthropics/skills) ★ 129k+ — Anthropic **官方** Skills 集合，docx / xlsx / pptx / pdf ***处理******直接***内建
- [**tfriedel/claude-office-skills**](https://github.com/tfriedel/claude-office-skills) ★ 646 — ***补强***版 Office skills（PPTX/DOCX/XLSX/PDF），含***自动***化 workflow

### Google Workspace（Gmail / Docs / Drive / Calendar）

- [**taylorwilsdon/google_workspace_mcp**](https://github.com/taylorwilsdon/google_workspace_mcp) ★ 2.3k+ — 一个 server 包***整套*** Google Workspace（Gmail、Calendar、Docs、Sheets、Slides、Drive）

### 开发协***作***

- [**github/github-mcp-server**](https://github.com/github/github-mcp-server) ★ 29k+ — GitHub **官方** MCP，issue / PR / repo ***操作***
- [**atlassian/atlassian-mcp-server**](https://github.com/atlassian/atlassian-mcp-server) ★ 723 — Atlassian **官方** Remote MCP（Jira、Confluence）
- [**jerhadf/linear-mcp-server**](https://github.com/jerhadf/linear-mcp-server) ★ 340+ — Linear MCP server
- [**korotovsky/slack-mcp-server**](https://github.com/korotovsky/slack-mcp-server) ★ 1.5k+ — Slack MCP，***无*** admin 权限也能用

### 研究工作流（本 repo ***维护***者出品）

- [**WenyuChiou/ai-research-skills**](https://github.com/WenyuChiou/ai-research-skills) ★ 77 — 14 个研究流程 skill，5-plugin marketplace
- [**WenyuChiou/research-hub**](https://github.com/WenyuChiou/research-hub) ★ 16 — Zotero + Obsidian + NotebookLM ***集成*** workspace
- [**WenyuChiou/zotero-skills**](https://github.com/WenyuChiou/zotero-skills) ★ 22 — Zotero CLI skill
- [**WenyuChiou/codex-delegate**](https://github.com/WenyuChiou/codex-delegate) ★ 57 + [**gemini-delegate-skill**](https://github.com/WenyuChiou/gemini-delegate-skill) ★ 34 — Multi-LLM delegation ***对***

### 中文***圈***常用

- [**leemysw/feishu-docx**](https://github.com/leemysw/feishu-docx) ★ 209 — 飞书（Lark）docs / sheet / bitable ↔ Markdown，含 Claude Skills ***支持***

> 上面只是 highlight。**完整 62 个集成***的分类***目录**（含***数据***库、浏览器***自动***化、Figma、Excalidraw、Cloudflare、Stripe、***学术******写作*** / Multi-LLM delegation 等）在 [`resources/mcp-skills-catalog.zh-Hans.md`](resources/mcp-skills-catalog.zh-Hans.md)。

> 想找更多 MCP server catalog？看 [`wong2/awesome-mcp-servers`](https://github.com/wong2/awesome-mcp-servers) / [`punkpeye/awesome-mcp-servers`](https://github.com/punkpeye/awesome-mcp-servers)（***按***分类***整理***）。**Canva** 的***官方*** MCP ***还***在 early access，社群***版本******不稳定***，等***成熟******后***再补上。

---

## 同***主题***的***清***单***型*** awesome lists

本 repo **不***取代***清***单***型*** awesome list——你***已经***知道***在***找什么工具***时***，下面这些***查***起来***更******直接***：

### MCP ***相关***

- [**modelcontextprotocol/servers**](https://github.com/modelcontextprotocol/servers) — ***官方*** MCP reference servers（filesystem、github、sqlite、git、fetch、memory 等）
- [**wong2/awesome-mcp-servers**](https://github.com/wong2/awesome-mcp-servers) — 社群 MCP server ***清***单，***按***分类***整理***（150+ ***个***）
- [**punkpeye/awesome-mcp-servers**](https://github.com/punkpeye/awesome-mcp-servers) — ***另******一***份*** MCP server ***清***单

### Claude Code / Skills / Plugins ***相关***

- [**hesreallyhim/awesome-claude-code**](https://github.com/hesreallyhim/awesome-claude-code) — Claude Code ***相关***资源***清***单（***整理***中）
- [**travisvn/awesome-claude-skills**](https://github.com/travisvn/awesome-claude-skills) — Claude Skills ***清***单
- [**anthropics/claude-plugins-official**](https://github.com/anthropics/claude-plugins-official) — Anthropic ***官方*** plugin 范本，要***打包******自己***的 plugin ***从******这***份***开始***

### 中文***圈***必看

- [**datawhalechina/hello-agents**](https://github.com/datawhalechina/hello-agents) — Datawhale ***系统***性 agent 教***学***（zh-Hans）
- [**WangRongsheng/awesome-LLM-resources**](https://github.com/WangRongsheng/awesome-LLM-resources) — ***完整***的中文 LLM 资源***整理***（8k+ stars）
- [**AiHubCN/Awesome-Chinese-LLM**](https://github.com/AiHubCN/Awesome-Chinese-LLM) — 中文***开源***大模型***整理***

---

## 还有什么？

- 主 README：[README.zh-Hans.md](README.zh-Hans.md)
- ***完整*** MCP/Skill ***目录***：[resources/mcp-skills-catalog.zh-Hans.md](resources/mcp-skills-catalog.zh-Hans.md)
- CLI agent ***比较***指南：[resources/cli-agents-guide.zh-Hans.md](resources/cli-agents-guide.zh-Hans.md)
- Style guide / ***贡献******规范***：[resources/style-guide.zh-Hans.md](resources/style-guide.zh-Hans.md)、[CONTRIBUTING.zh-Hans.md](CONTRIBUTING.zh-Hans.md)
