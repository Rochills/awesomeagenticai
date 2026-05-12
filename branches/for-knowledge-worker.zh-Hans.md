# 给知识工作者 — 专业分支

> [繁體中文](./for-knowledge-worker.md) | **简体中文** | [English](./for-knowledge-worker.en.md) | [Русский](./for-knowledge-worker.ru.md)

> 🚀 **完全没有开发背景？** 先看 [`resources/setup-guide.zh-Hans.md` §A-D](../resources/setup-guide.zh-Hans.md)（30-45 分钟从零）。本分支后面提到的“Claude Code”“MCP”“Skills”都会用到 §D 那个 setup。

> [← 回主路线 README](../README.zh-Hans.md) · 走完 **Track A 的 A3** 或 **Track B 的 Stage 7** 后从这里接续。把 agentic AI 应用到办公室 / 知识工作上。

## 使用场景

- Email 分流与草拟回信
- 会议笔记 → 行动项目
- 多来源报告集成
- 研究 / 市场情报收集
- 决策辅助流程

## 精选 Projects

> 💡 **想把 AI agent 接到 Notion / Gmail / Outlook / Slack / Excel / 飞书？** 62 个常用 MCP server / Skill 集成在 [`resources/mcp-skills-catalog.zh-Hans.md`](../resources/mcp-skills-catalog.zh-Hans.md)（按使用场景分类）。下面这节保留 workflow / 集成平台级

### 工作流工具

#### [n8n](https://github.com/n8n-io/n8n) ⭐⭐⭐⭐
可自架的工作流自动化平台，内置 AI 集成，采用可视化节点式编辑器。

**适合谁**：要把多个 SaaS 工具串起来时（Slack + Gmail + Notion + AI）。

---

#### [Make.com](https://www.make.com/)（前身为 Integromat）
云端代管的工作流自动化平台，AI 集成节点功能完整。

---

### 知识工作者 Skills

#### [obra/superpowers](https://github.com/obra/superpowers) ⭐⭐⭐⭐

头脑风暴、规划、决策类的 skill。

---

### 知识管理 / 个人 AI

#### [khoj-ai/khoj](https://github.com/khoj-ai/khoj) ⭐⭐⭐⭐

| 栏位 | 内容 |
|---|---|
| Stars | ★ 34k+ |
| License | AGPL-3.0 |

**教什么**：自架的「第二大脑」——可以跟 web + 本地文件对话、排程自动化、自定义 agent。

**适合谁**：想自架个人知识库 + AI assistant 的人。

**备注**：AGPL-3.0 license（传染性开源）。

---

#### [lobehub/lobe-chat](https://github.com/lobehub/lobe-chat) ⭐⭐⭐⭐⭐

| 栏位 | 内容 |
|---|---|
| Stars | ★ 76k+ |
| License | LobeHub Community License（基于 Apache-2.0 + 商用附加条款） |

**教什么**：可部署的多 agent 聊天平台——含 plugin marketplace、知识库、团队协作。可自架的 AI workspace 代表选项之一。

**适合谁**：想找可自架的协作 chat workspace。

**备注**：商用使用需确认 LobeHub Community License 的附加条款。

---

#### [langflow-ai/langflow](https://github.com/langflow-ai/langflow) ⭐⭐⭐⭐

| 栏位 | 内容 |
|---|---|
| Stars | ★ 147k+ |
| License | MIT |

**教什么**：可视化 AI agent 开发平台——拖拉节点设计 agent flow，内置 API + MCP server 部署。比 n8n 更专注于 agent 设计（n8n 是泛用工作流）。

**适合谁**：宁可拉节点不写 Python 的知识工作者，或要设计 agent 跟团队沟通流程的人。

---

#### [Mintplex-Labs/anything-llm](https://github.com/Mintplex-Labs/anything-llm) ⭐⭐⭐⭐⭐

| 栏位 | 内容 |
|---|---|
| Stars | ★ 60k+ |
| License | MIT |

**教什么**：all-in-one 的私有 RAG 工作平台——上传文件、建 agent、相容 MCP、预设 on-device。**NotebookLM 的私有 self-hosted 替代方案**。

**适合谁**：知识工作者要私有部署、类 NotebookLM 的工具，避免把数据送到云端。

---

### 对知识工作者有用的 MCP Server

#### 通讯类 MCP server ⭐⭐⭐⭐
Slack / Gmail / Discord 等。Anthropic 原本维护的 reference server 已于 2025 年重整；目前由社群维护的 server 集中在 [**punkpeye/awesome-mcp-servers**](https://github.com/punkpeye/awesome-mcp-servers#communication) 跟 [**wong2/awesome-mcp-servers**](https://github.com/wong2/awesome-mcp-servers)，要找最新的 Slack / Gmail / Drive / Calendar MCP server 可以从这两个清单翻找。

---

## 可以建的流程

- **每日 email 分流**：扫 inbox → 分类 → 草拟回信让你 review → 标已读
- **会议 → 行动项目**：逐字稿 → 主要决策 + 行动项目 → 指派 + 公告
- **每周报告集成**：从 N 个工具拉指标 → 整理 → email summary
- **研究 / 市场情报**：问题 → 多来源搜索 → 交叉验证 → 备忘录

## 层级建议

大多数知识工作者应该从 **Tier 0**（Claude.ai 网页版）开始，当你需要对本机 / 云端文件重复跑的流程时，再升级到 **Tier 1**（Claude Desktop 加 MCP）。

**Tier 3+（CLI / SDK）对大多数知识工作者任务来说太重。** 不要被别人怂恿过去。

## 阅读

- [How I Turned Claude Code Into My Personal AI Agent OS](https://aimaker.substack.com/p/how-i-turned-claude-code-into-personal-ai-agent-operating-system-for-writing-research-complete-guide) — 知识工作者个案研究
