# Stage 5 — Claude Code 生态系 ⭐⭐

> [繁體中文](./05-claude-code-ecosystem.md) | **简体中文** | [English](./05-claude-code-ecosystem.en.md) | [Русский](./05-claude-code-ecosystem.ru.md)

⏱ **时间估算**：3-4 周（约 15-25 小时）

> 💡 整个 stage 围绕 4 个关键词（**MCP / Skills / Plugins / Marketplace**）展开 → 不熟先翻 [`resources/glossary.zh-Hans.md` §5](../resources/glossary.zh-Hans.md#5-claude-code-生态)。

> 📌 **这个 stage 两条轨都用**：
> - **Track A（CLI Power User）**：A2 用 [5.1（Claude Code 基础）](#51--claude-code-基础)；A3 用 [5.2（MCP）](#52--mcpmodel-context-protocol-基础) + 选择性用到 [5.3（Skills）](#53--skillsclaude-code-的行为层) 跟 [5.4（Plugins）](#54--plugins-与-marketplaces)（A3 的 动手练习 CLI-12 会教把 CLAUDE.md 跟 commands 打包成 plugin）。读的角度是「**怎么用 Claude Code 把工作做好**」
> - **Track B（Agent Builder）**：把整个 stage 当「**Claude Code 内部怎么运作**」的深度学习，从 5.1 完整走到 5.4

> 🗺️ **Claude Code 属于哪种 agent 型态**？→ [`resources/agent-paradigms.zh-Hans.md`](../resources/agent-paradigms.zh-Hans.md) §Type 1（IDE-coupled）+ §Type 2（Terminal pair-programmer）；想看完整 5 种 paradigm 对照也从这份开始。

> ⚠️ **想用本地 LLM？这个 stage 不是那条路线。** Claude Code 需要 Anthropic API / OAuth，不能直接改接 Ollama 或本地 endpoint。离线、隐私资料或不想用 API 额度时，请看 [`resources/cookbook.md` Recipe 6](../resources/cookbook.zh-Hans.md#6-本地-llm--cli-agent-快速-walkthrough)，用 OpenCode / goose / Aider / Hermes 这类支持 BYO LLM 的 CLI agent。

## Stack 一览

由上往下，每一层都建立在底下那一层上：

![Claude Code Ecosystem Stack](../resources/diagrams/stage5-stack.zh-Hans.png)

每一层各自加上一种能力：
- **API + SDK**：用程序存取 LLM
- **Tool Use**：让 LLM 调用你定义的 function
- **MCP**：标准化协议，让任何 LLM host 都能使用任何 tool server
- **Skills**：Claude Code 的行为包，可以封装 MCP tool
- **Plugins**：把 Skills、hooks、commands、MCP 设置打包成一个单位发布

这个阶段有 4 个子章节，**请按顺序做**——每一节都建立在前一节之上。

```
5.1  Claude Code 基础          3-5 天   （安装、slash commands、CLAUDE.md）
5.2  MCP — 协议层              5-7 天   （写你的第一个 MCP server）
5.3  Skills — 行为层            5-7 天   （写你的第一个 SKILL.md）
5.4  Plugins 与 Marketplaces   5-7 天   （打包并发布）
```

跑完这个阶段，你会能扩充 Claude Code、写自己的 MCP server、发布一个 plugin marketplace。

---

## 5.1 — Claude Code 基础

### 学习目标
- 在你的操作系统上安装 Claude Code
- 使用 slash commands（`/help`、`/compact`、`/clear`、`/plan`）
- 了解 `~/.claude/` 目录结构
- 写一份项目层级的 `CLAUDE.md` 来定制化行为

### 必修阅读
1. [**Anthropic — Claude Code Quickstart**](https://docs.anthropic.com/en/docs/claude-code/quickstart) — 官方安装指南
2. [**Anthropic — CLAUDE.md best practices**](https://docs.anthropic.com/en/docs/claude-code/memory) — 怎么写项目 memory
3. [**KimYx0207/Claude-Code-x-OpenClaw-Guide-Zh**](https://github.com/KimYx0207/Claude-Code-x-OpenClaw-Guide-Zh) — 简中入门指南

### 动手练习
- **练习：Claude Code** — 安装、跑第一个 session、请 Claude 读文件并摘要
- **练习：CLAUDE.md** — 写一份项目 CLAUDE.md，观察行为的差异

### 精选 Projects
- [**anthropics/claude-code**](https://github.com/anthropics/claude-code) — 官方 repo（issues、releases）
- [**KimYx0207/Claude-Code-x-OpenClaw-Guide-Zh**](https://github.com/KimYx0207/Claude-Code-x-OpenClaw-Guide-Zh) — 简中导读
- [**hesreallyhim/awesome-claude-code**](https://github.com/hesreallyhim/awesome-claude-code) — 较广泛的资源清单（目前正在重整）

---

## 5.2 — MCP（Model Context Protocol）⭐ 基础

### 学习目标
- 解释 MCP 的三个抽象（Tools、Resources、Prompts）
- 把现成的 MCP server 接上 Claude Desktop 或 Claude Code
- 用 Python 写一个最小的 MCP server，提供 1-2 个 tool
- 区分 MCP server vs Tool Use vs Skills vs Plugins

### 必修阅读
1. [**Anthropic — Introducing MCP**](https://www.anthropic.com/news/model-context-protocol) — 最初发表，概念总览
2. [**MCP Specification**](https://modelcontextprotocol.io/specification) — 实际的协议规格
3. [**Complete Guide to MCP in 2026**](https://dev.to/x4nent/complete-guide-to-mcp-model-context-protocol-in-2026-architecture-implementation-and-4a11) — 实践导读

### 动手练习
- **练习：MCP client** — 安装 `modelcontextprotocol/servers/filesystem`，从 Claude Desktop 连上去。看着 Claude 读你的文件。
- **练习：MCP server** — 写一个 Python MCP server，提供一个 tool（例如「换算温度」）。从 Claude Code 连过去。**step-by-step 怎么做** → [`resources/cookbook.zh-Hans.md` §2](../resources/cookbook.zh-Hans.md#2-写你的第一个-mcp-server)
- **练习：MCP in production** — 在同一个 Claude session 里同时连 2-3 个 MCP server，看它们互相搭配。

### 精选 Projects

> 💡 **找日常工具的 MCP（Notion / Obsidian / Excel / Postgres / Playwright / Figma 等）？**
> 看 [`resources/mcp-skills-catalog.zh-Hans.md`](../resources/mcp-skills-catalog.zh-Hans.md)——按 14 个分类整理 62 个常用 MCP server / Skill，每个都附 stars / license / 适合谁。下面这节保留的是「**写自己 MCP server 时的 reference**」性质的官方 server / SDK。


#### [modelcontextprotocol/servers](https://github.com/modelcontextprotocol/servers) ⭐ 官方

| 字段 | 内容 |
|---|---|
| 语言 | TypeScript / Python |
| Stars | ★ 85k+ |
| License | MIT |
| 推荐度 | ⭐⭐⭐⭐⭐ |

**教什么**：20+ 个参考用 MCP server（filesystem、git、github、sqlite、time、fetch、memory、sequential thinking）。写自己的 server 时最标准的示例。

**适合谁**：练习 1 以及之后当参考用。读 `everything` server 跟 `filesystem` server 的源代码，理解协议怎么运作。

**怎么跑**：
```bash
npx -y @modelcontextprotocol/server-filesystem /path/to/dir
# 或用 Python servers：
pip install mcp-server-fetch
```

---

#### [modelcontextprotocol/python-sdk](https://github.com/modelcontextprotocol/python-sdk)

| 字段 | 内容 |
|---|---|
| 语言 | Python |
| License | MIT |
| 推荐度 | ⭐⭐⭐⭐⭐ |

**教什么**：写 MCP server 的官方 Python SDK。练习 2 用这个。

**怎么跑**：
```bash
pip install mcp
# 然后跟着 https://github.com/modelcontextprotocol/python-sdk#quickstart 做
```

---

#### [modelcontextprotocol/typescript-sdk](https://github.com/modelcontextprotocol/typescript-sdk)

| 字段 | 内容 |
|---|---|
| 语言 | TypeScript |
| License | MIT |
| 推荐度 | ⭐⭐⭐⭐ |

**教什么**：Python SDK 的 TypeScript 版本。喜欢 TS 的人选这个。

---

#### [wong2/awesome-mcp-servers](https://github.com/wong2/awesome-mcp-servers) ⭐ 目录

| 字段 | 内容 |
|---|---|
| 形式 | 精选清单 |
| 推荐度 | ⭐⭐⭐⭐⭐ |

**教什么**：150+ 个社区 MCP server 的目录，按类别分类——search、code、cloud、communication、finance。

**适合谁**：在自己写之前，先看看是不是已经有现成的。有特定 tool 需求时来逛这个。

**备注**：投稿要走他们网站（mcpservers.org）。

---

#### [punkpeye/awesome-mcp-servers](https://github.com/punkpeye/awesome-mcp-servers)

| 字段 | 内容 |
|---|---|
| 推荐度 | ⭐⭐⭐⭐ |

**教什么**：另一份 MCP server 目录，组织方式不同（通常更新比较实时）。

**适合谁**：跟 wong2 的清单交叉比对。不同策展人会挖出不同的项目。

---

#### [github/github-mcp-server](https://github.com/github/github-mcp-server)

| 字段 | 内容 |
|---|---|
| 推荐度 | ⭐⭐⭐⭐ |

**教什么**：真正在 production 跑的 MCP server 长什么样子。GitHub 官方维护。

**适合谁**：把源代码当作 production 等级 MCP server 的参考实现来读。

---

#### [21st-dev/magic-mcp](https://github.com/21st-dev/magic-mcp)

| 字段 | 内容 |
|---|---|
| Stars | ★ 4.8k+ |
| License | NOASSERTION |
| 推荐度 | ⭐⭐⭐ |

**教什么**：一个非平凡的 MCP server，会生成 UI 组件。让你看到 MCP 不只能做数据抓取。

**适合谁**：做完 练习 2 之后找灵感——MCP server 还能做出什么有创意的东西。

---

## 5.3 — Skills（Claude Code 的行为层）

### 学习目标
- `SKILL.md` 的结构（YAML frontmatter + 本文）
- skill 何时会自动加载（description 比对）
- 怎么写一份能解决你日常工作的 SKILL.md
- `references/`、`scripts/`、`evals/` 子目录的用途

### 必修阅读
1. [**Anthropic — Claude Skills 文档**](https://docs.anthropic.com/en/docs/claude-code/skills)
2. **几份示例 SKILL.md**——从 `anthropics/claude-code` 或社区 marketplace 拿
3. [**Hello-Agents — Extra08 如何写出好的 Skill**](https://github.com/datawhalechina/hello-agents/blob/main/Extra-Chapter/Extra08-如何写出好的Skill.md) — 中文最完整的 Skill 最佳实践
4. [**Hello-Agents — Extra05 Agent Skills 与 MCP 对比解读**](https://github.com/datawhalechina/hello-agents/blob/main/Extra-Chapter/Extra05-AgentSkills解读.md) — Skills vs MCP 概念对比

### 动手练习
- **练习：SKILL.md** — 写一份 200 字的 skill，解决你日常工作中的某一件事。**step-by-step 怎么做** → [`resources/cookbook.zh-Hans.md` §1](../resources/cookbook.zh-Hans.md#1-写你的第一个-skill)
- **练习：SKILL with references** — 加一份 `references/` markdown 让 skill 可以引用
- **练习：SKILL eval** — 加 `evals/evals.json`，放 3-5 个自我测试

> 📦 **本 repo 自带 meta-example**：[`examples/stage-5/tool-calling-tutor/`](../examples/stage-5/tool-calling-tutor/) 是这个 stage 的对应 skill 范本——完整 frontmatter（含 trigger phrases + Do NOT use for）、3 份 `references/`、`evals/evals.json` 5 个 test case，**直接 fork 改成你自己的 skill**。双重用途：(a) 学习者自用、卡在 tool calling 时让它 auto-load 帮你 debug；(b) Stage 5 §5.3 SKILL.md 写法的对照样板。

### 精选 Projects

> 💡 **找日常用 Skill（NotebookLM、Excalidraw、Office docs 等）？**
> 看 [`resources/mcp-skills-catalog.zh-Hans.md`](../resources/mcp-skills-catalog.zh-Hans.md)——按使用场景分类，含 Anthropic 官方 + 社区 Skill。下面这节保留的是「**写自己 Skill 时的 reference**」性质的 spec / showcase。

#### [anthropics/skills](https://github.com/anthropics/skills) ⭐ 官方 spec

| 字段 | 内容 |
|---|---|
| Stars | ★ 128k+ |
| License | NOASSERTION |
| 推荐度 | ⭐⭐⭐⭐⭐ |

**教什么**：Anthropic 官方的 Skills repo——`spec/`（SKILL.md frontmatter 标准）+ `template/`（起手模板）+ `skills/`（pdf、docx、xlsx、pptx、skill-creator 等 reference 实现）。

**适合谁**：写自己的 SKILL.md 之前先读这个——SKILL.md 结构与 frontmatter 的重要参考实现。

**备注**：跟 `anthropics/claude-code` 不一样——这个是专门的 Skills repo，后者是 Claude Code 的主 repo。Agent Skills 的更广义标准另见 [agentskills.io](https://agentskills.io)。

---

#### [anthropics/claude-code](https://github.com/anthropics/claude-code)

| 字段 | 内容 |
|---|---|
| 推荐度 | ⭐⭐⭐⭐ |

**教什么**：Claude Code 主 repo，内含 issues、releases 与一些 inline skill 示例。

**适合谁**：追踪新版功能、回报 bug、看 release notes。

**备注**：在这个 stage（学 Skills），这个 repo 排在 `anthropics/skills`（⭐⭐⭐⭐⭐ 官方 spec）后面，所以给 ⭐⭐⭐⭐。在 branches（给 end-user 当入口）里会看到 ⭐⭐⭐⭐⭐ 评等，是因为角色不同。

---

#### [travisvn/awesome-claude-skills](https://github.com/travisvn/awesome-claude-skills)

| 字段 | 内容 |
|---|---|
| 推荐度 | ⭐⭐⭐⭐ |

**教什么**：社区 Claude Skills 的精选目录。

**适合谁**：自己写之前先看看有没有现成的。

---

#### [obra/superpowers](https://github.com/obra/superpowers)

| 字段 | 内容 |
|---|---|
| 推荐度 | ⭐⭐⭐⭐ |

**教什么**：20+ 个经过实战检验的 skill（TDD、debugging、合作模式），附 `/brainstorm`、`/write-plan`、`/execute-plan` 命令以及 skills-search tool。

**适合谁**：power user 的设置。读 SKILL.md 源代码学进阶写法。

---

#### [VoltAgent/awesome-agent-skills](https://github.com/VoltAgent/awesome-agent-skills)

| 字段 | 内容 |
|---|---|
| Stars | ★ 20k+ |
| License | MIT |
| 推荐度 | ⭐⭐⭐ |

**教什么**：1000+ 个 agent skill，兼容于 Claude Code、Codex、Gemini CLI、Cursor。跨工具的视角。

**适合谁**：搞懂 SKILL.md 之后，逛逛找想法。

---

#### [alirezarezvani/claude-skills](https://github.com/alirezarezvani/claude-skills)

| 字段 | 内容 |
|---|---|
| 推荐度 | ⭐⭐⭐ |

**教什么**：232+ 个 Claude Code skill，跨 engineering、marketing、product、compliance。

**适合谁**：找特定领域的 skill 示例。

---

#### [mattpocock/skills](https://github.com/mattpocock/skills)

| 字段 | 内容 |
|---|---|
| Stars | ★ 61k+ |
| License | MIT |
| 推荐度 | ⭐⭐⭐⭐ |

**教什么**：Matt Pocock（TypeScript 社区知名教学者）公开自己工作中真实在用的 `.claude/` 目录。每个 SKILL.md 都很短（10-50 行），不过度工程化。

**适合谁**：想看「真实工程师日常用的 SKILL.md 长什么样子」的人。对照那些动辄 200 行的 over-engineered skill，这份特别有参考价值。

---

#### [wshobson/agents](https://github.com/wshobson/agents)

| 字段 | 内容 |
|---|---|
| Stars | ★ 35k+ |
| License | MIT |
| 推荐度 | ⭐⭐⭐⭐ |

**教什么**：把 skills + subagents 组合起来做 multi-agent 编排。**从单一 SKILL.md 进化到 agent-as-skill 组合 pattern** 的示例。

**适合谁**：跑过几个 SKILL.md 之后，想知道「skill 之间怎么互相调用、怎么变成更大的 agent workflow」的中阶学习者。

---

## 5.4 — Plugins 与 Marketplaces

### 学习目标
- `plugin.json` schema（name、version、skills array、configuration）
- `marketplace.json` schema（plugins array、source、metadata）
- `claude plugin marketplace add` 的流程
- 区分 single-plugin bundle vs multi-plugin marketplace
- 发布自己的 marketplace

### 必修阅读
1. [**Anthropic — Plugins 文档**](https://docs.anthropic.com/en/docs/claude-code/plugins)
2. **读下面 2-3 个 marketplace 的 `plugin.json` 与 `marketplace.json`**

### 动手练习
- **练习：plugin install** — 安装下面的某一个 marketplace，看它加载
- **练习：plugin.json** — 把 5.3 写的 SKILL.md 打包成一个 plugin
- **练习：marketplace publish** — push 到 GitHub，用 `claude plugin marketplace add` 安装

### 精选 Projects

> 💡 **想看别人的 plugin 怎么包**：[`resources/mcp-skills-catalog.zh-Hans.md`](../resources/mcp-skills-catalog.zh-Hans.md) 的开发协作 / 设计 / 监控分类底下不少都附 plugin 包装（例如 `timescale/pg-aiguide` 同时是 MCP 跟 plugin）。下面这节保留的是「**marketplace 结构模板**」性质的 reference。

#### [anthropics/claude-plugins-official](https://github.com/anthropics/claude-plugins-official) ⭐ 官方

| 字段 | 内容 |
|---|---|
| Stars | ★ 18k+ |
| License | NOASSERTION（每个 plugin 独立 license，请看各自目录） |
| 推荐度 | ⭐⭐⭐⭐⭐ |

**教什么**：Anthropic 官方的 marketplace 模板——`.claude-plugin/marketplace.json` 标准 schema、`plugins/` 内含 plugin 本体、`external_plugins/` 引用外部 repo 的 plugin。

**适合谁**：写自己的 marketplace 之前，这是最该对着抄的官方模板——「**marketplace.json 该长什么样**」直接看这个。

**备注**：除了 schema 之外，也是观察 Anthropic 怎么分类官方 plugin（chrome-devtools、deepwiki、code-research、jam 等）的好参考。

---

#### [obra/superpowers-marketplace](https://github.com/obra/superpowers-marketplace)

| 字段 | 内容 |
|---|---|
| Stars | ★ 900+ |
| License | MIT |
| 推荐度 | ⭐⭐⭐⭐ |

**教什么**：**最简 marketplace template**——repo 里只有 `.claude-plugin/marketplace.json` + README，plugin 本体放在外部 repo。展示「**curator-only marketplace**」（策展者只负责挑选、不打包源代码）的最小形式。

**适合谁**：要做「我策展、别人写」型 marketplace 的人。比 anthropics/claude-plugins-official 更精简，是最小可行模板。

---

#### [trailofbits/skills-curated](https://github.com/trailofbits/skills-curated)

| 字段 | 内容 |
|---|---|
| Stars | ★ 388 |
| License | CC-BY-SA-4.0 |
| 推荐度 | ⭐⭐⭐ |

**教什么**：知名资安公司 Trail of Bits 维护的 curated marketplace，重点在 **supply-chain security**——每个 skill 都经过审查，README 写清楚审核标准。

**适合谁**：在意供应链信任、想学「**curator-vouches-for-safety**」这种模式的 reviewer 跟团队。

**备注**：规模小但意义大——示范 marketplace 不只是 skill 的清单，也可以是信任机制。

---

#### [rohitg00/awesome-claude-code-toolkit](https://github.com/rohitg00/awesome-claude-code-toolkit)

| 字段 | 内容 |
|---|---|
| 推荐度 | ⭐⭐⭐ |

**教什么**：社区中规模最大的 Claude Code agents、skills、hooks、templates 目录之一。涵盖的 use case 很广。

**适合谁**：跑完 练习 3 之后逛逛看外面有什么。

---

#### [anthropics/life-sciences](https://github.com/anthropics/life-sciences)（领域特化示例）

| 字段 | 内容 |
|---|---|
| Stars | ★ 331 |
| License | NOASSERTION（marketplace 本身未提供 SPDX；里面每个 MCP server 由各自 provider 授权） |
| 推荐度 | ⭐⭐⭐ |

**教什么**：Anthropic 自己发的**领域特化 marketplace** 示例（针对生物 / 健康科学）——展示如何把 `marketplace.json` 为单一 vertical 量身设计，而不是塞通用清单。

**适合谁**：要做特定领域 marketplace（医疗、金融、法律、教育等）的人，可以参考 Anthropic 自己怎么处理。

**备注**：payload 偏生科 MCP server，但 marketplace.json 结构本身才是学习重点。

---

> **「如何发布自己的 marketplace」教学还缺**——目前最可靠的是 [Anthropic 官方 plugin 文档](https://docs.claude.com/en/docs/claude-code/plugins)。社区有写过好的 walkthrough 博客 / repo？欢迎开 PR 补上。

---

## ✅ 进入 Stage 6 前的自我检查

你能不能：
- [ ] 安装 Claude Code 并使用 5 个不同的 slash command
- [ ] 在同一个 Claude session 里接 2 个 MCP server
- [ ] 用 Python 写自己的 MCP server，提供 1 个能用的 tool
- [ ] 写一份能在特定触发词自动加载的 `SKILL.md`
- [ ] 把 skill 打包成 plugin，再用 `marketplace.json` 发布
- [ ] 从角色分工说出 MCP / Skills / Plugins / SDK 各自的位置

如果都可以 → 前往 [Stage 6 — Memory & RAG](./06-memory-rag.zh-Hans.md)。

## 💡 Bonus：完成这个阶段之后

- 对 [`anthropics/claude-cookbooks`](https://github.com/anthropics/claude-cookbooks) 发一个 PR（小修正、文档更新）
- 把自己的 plugin 投稿到社区 marketplace
- 写一篇文章，比较自己的 hello-MCP server 跟官方 `modelcontextprotocol/servers` 收的某一个
