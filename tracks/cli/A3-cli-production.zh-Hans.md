# A3 — Integration & Production

> [繁體中文](./A3-cli-production.md) | **简体中文** | [English](./A3-cli-production.en.md) | [Русский](./A3-cli-production.ru.md)

> [← A2 — CLI Workflow Patterns](A2-cli-workflow.zh-Hans.md) · **Track A: CLI Power User** 第 3 站（最后）

⏱ **时间估算**：1-2 周（约 8-15 小时）

CLI 跑得顺了之后，下一步：**把它接到你的真实工作流程里**。MCP server 集成、CI 自动化、cost / observability。这节之后，CLI 不只是你个人的工具，而是 team 工作流的一部分。

## 📌 学习目标

- 把 1-3 个 MCP server 接到你的 CLI（Slack / Gmail / 你的 internal API / DB）
- 设置 GitHub Actions 自动跑 Claude Code（PR review、release notes 等）
- 加 observability（trace、cost、latency）到 CLI workflow
- 规划 cost budget，知道大 task 会花多少 token

## 📚 必修阅读

1. [**Stage 5.2 — MCP（Model Context Protocol）**](../../stages/05-claude-code-ecosystem.zh-Hans.md#52--mcpmodel-context-protocol-基础) — MCP 概念跟基础
2. [**Anthropic — Prompt Caching**](https://www.anthropic.com/news/prompt-caching) — 90% cost reduction 的关键技巧
3. [**Stage 7 — Observability section**](../../stages/07-multi-agent-production.zh-Hans.md#observability) — langfuse / Helicone / weave
4. [**`resources/cli-agents-guide.zh-Hans.md`** §“常见坑”]../../resources/cli-agents-guide.zh-Hans.md) — production 用 CLI 最常踩的问题

## 🛠 动手练习

### 动手练习 CLI-9：MCP server 接 CLI
照 [Stage 5.2 练习：MCP client](../../stages/05-claude-code-ecosystem.zh-Hans.md#hello-x) 的步骤，把至少一个有用的 MCP server 接到你的 CLI：
- `filesystem` server → 让 CLI 在指定目录外也能读文件
- `github` server → 让 CLI 直接读 PR / issue
- 自架 server → 接你的 internal API / DB

成功标准：在 CLI 对话里直接问“我这个 PR 有 conflict 吗”，CLI 通过 MCP 回答你（不用你开浏览器）。

### 动手练习 CLI-10：GitHub Actions + CLI
写一个 `.github/workflows/cli-review.yml`：
- 触发：PR opened / synchronize
- 跑：在 GH Actions runner 内执行 Claude Code（或 Codex），给它 `git diff` + 你的 `.claude/commands/review.zh-Hans.md`
- 输出：PR comment

成功标准：开新 PR，1-2 分钟内 PR 出现 review comment。

> 起点：Anthropic 官方有 [`claude-code-action`](https://github.com/anthropics/claude-code-action)（GitHub Actions 集成）；Codex 有 GitHub App 跟 CLI 两种模式。

### 动手练习 CLI-11：Cost tracking
跑你日常的一个 task，**先预估** token 用量，再实际跑、查 token usage。差距通常很大（多半你低估）。
- 算式：input tokens + output tokens 各乘以 model 单价
- 接 langfuse 或 Helicone（[Stage 7 Observability section](../../stages/07-multi-agent-production.zh-Hans.md#observability)）做 trace
- 观察：哪个 sub-task 花最多 token？是不是有不必要的 long context？

### 动手练习 CLI-12：Skill / plugin 跨 team 分享
把你的 `.claude/commands/` 跟 `CLAUDE.zh-Hans.md` 打包成 plugin，发布到内部 marketplace 或 GitHub。Team 其他人 `claude plugin install` 之后就有同样的工作流。
- Skill / plugin 细节见 [Stage 5.3 + 5.4](../../stages/05-claude-code-ecosystem.zh-Hans.md)
- 范本：[anthropics/claude-plugins-official](https://github.com/anthropics/claude-plugins-official)

## 🎯 精选 Projects

### MCP server collection（接 CLI 用）

> 💡 **要找接日常工具的 MCP**（Notion / Obsidian / Excel / Postgres / Playwright / Slack / Linear / Figma 等）：[`resources/mcp-skills-catalog.zh-Hans.md`](../../resources/mcp-skills-catalog.zh-Hans.md)——62 个分类整理，每个都有 stars / license / 适合谁。下面只列“写自己 MCP server / 找 reference”用的核心 catalog。

#### [modelcontextprotocol/servers](https://github.com/modelcontextprotocol/servers) ⭐⭐⭐⭐⭐
★ 85k+ — 官方 reference servers。filesystem、github、sqlite、git、time、fetch、memory、sequential-thinking。
> 详见 [Stage 5.2](../../stages/05-claude-code-ecosystem.zh-Hans.md#52--mcpmodel-context-protocol-基础)。

#### [wong2/awesome-mcp-servers](https://github.com/wong2/awesome-mcp-servers)
社群 MCP server catalog。150+ 个依分类整理。

---

### CI 集成 patterns

#### [anthropics/claude-code-action](https://github.com/anthropics/claude-code-action)
官方 GitHub Action 范本。PR review、issue triage、自动 fix。

#### [continuedev/continue](https://github.com/continuedev/continue) ⭐⭐⭐⭐
★ 33k+ — 把 AI checks 接到 CI，可在 PR pipeline 强制执行。
> 完整介绍见 [`branches/for-developer.zh-Hans.md`](../../branches/for-developer.zh-Hans.md)。

---

### Observability + Cost

#### [langfuse/langfuse](https://github.com/langfuse/langfuse) ⭐⭐⭐⭐⭐
★ 26k+ — open source LLM observability。把 trace、cost、session 都接起来。
> 详见 [Stage 7 Observability](../../stages/07-multi-agent-production.zh-Hans.md#observability)。

#### [Helicone](https://github.com/Helicone/helicone) ⭐⭐⭐⭐
★ 5k+ — proxy-based 监控。改 base_url 就有 logging + caching。

#### [promptfoo/promptfoo](https://github.com/promptfoo/promptfoo) ⭐⭐⭐⭐⭐
★ 20k+ — eval framework。CLI workflow 升级到 production 前用这个跑回归测试。
> 详见 [Stage 7 Eval](../../stages/07-multi-agent-production.zh-Hans.md#evaluation-frameworks)。

---

### Production CLI workflow 范本

#### [obra/superpowers](https://github.com/obra/superpowers) ⭐⭐⭐⭐
★ 178k+ — 整套 production-ready skill collection。看别人怎么把 CLI workflow 做完整。

#### [obra/superpowers-marketplace](https://github.com/obra/superpowers-marketplace)
★ 900+ — 最简 marketplace template。要把你 team 的 CLI workflow 打包共用时参考。

## ✅ Track A 完整通关自我检查

你能不能：
- [ ] 已有至少 1 个 MCP server 接到你日常 CLI
- [ ] 已有至少 1 个 CI workflow 在自动跑 CLI agent
- [ ] 你能讲出某个 task 跑下去的 token 用量、cost、latency 大致范围
- [ ] 把你的 CLAUDE.zh-Hans.md / commands 打包过至少一次（即使只有自己用）
- [ ] 知道什么任务值得加 observability、什么不值得

如果都可以 → **Track A 完整通关**。挑一个 [specialized branch](../../README.zh-Hans.md#️-学习地图两条轨道) 继续走（researcher / developer / teacher / knowledge-worker / everyday-users）。

如果想再深入“**怎么写自己的 CLI agent**”（不是用现有的）→ 跳到 [Track B Stage 3](../../stages/03-tool-use-and-hello-agent.zh-Hans.md) 开始。Track A 跟 Track B 互补。

## 💡 接下来

走完 Track A 你已经是 CLI power user。下一阶段选择：

1. **加深 CLI workflow**（持续优化你的 setup）
   - 订阅 Anthropic / OpenAI changelog
   - 每季 review 一次 [`resources/cli-agents-guide.zh-Hans.md`](../../resources/cli-agents-guide.zh-Hans.md) 看新工具
   - 跟你 team 分享 CLAUDE.zh-Hans.md / skills

2. **跨到 Track B**（学怎么写自己的 agent）
   - Stage 3-4 学 tool use + framework
   - Stage 5 深挖 Claude Code 内部运作
   - Stage 7 写自己的 multi-agent system

3. **走 specialized branch**（把 CLI 应用在特定领域）
   - 研究人员 / 开发人员 / 知识工作者 / 教师 / 日常用户
   - 各 branch 都会用到 Track A 学的东西
