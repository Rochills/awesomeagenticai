# 给开发者 — 专业分支

> [繁體中文](./for-developer.md) | **简体中文** | [English](./for-developer.en.md) | [Русский](./for-developer.ru.md)

> 🚀 **第一次装 Claude Code / 写 `CLAUDE.md` / `SKILL.md`？** 快速 setup 指南在 [`resources/setup-guide.zh-Hans.md` §D-E](../resources/setup-guide.zh-Hans.md)。已经熟可以跳过。

> [← 回主路线 README](../README.zh-Hans.md) · 走完 **Track A 的 A3** 或 **Track B 的 Stage 7** 后从这里接续。把 agentic AI 应用到开发流程上。

## 使用场景

- AI 结对编程（Cursor、Aider、Claude Code、Cline、Continue）
- Code review 自动化
- 测试生成
- Multi-agent coding 任务（规划 + 执行）
- IDE 集成与 CI 规范

## 精选 Projects

> 7 个主流 CLI agent（Claude Code / Codex / OpenCode / Gemini CLI / goose / Aider / Hermes Agent）的并列比较见 [`resources/cli-agents-guide.zh-Hans.md`](../resources/cli-agents-guide.zh-Hans.md)。第一次接触 CLI agent 想要 step-by-step 入门 → [`tracks/cli/A1-cli-intro.zh-Hans.md`](../tracks/cli/A1-cli-intro.zh-Hans.md)（Track A 第一站）。要把 CLI 接到日常工具（GitHub、Linear、Atlassian、Postgres、Playwright、Figma 等）→ [`resources/mcp-skills-catalog.zh-Hans.md`](../resources/mcp-skills-catalog.zh-Hans.md)（62 个分类整理）。下面只列开发者该知道的关键 entry。

### Coding Agents

#### [Cursor](https://www.cursor.com/) ⭐⭐⭐⭐⭐
编辑器集成的 AI 结对编程工具。AI 辅助 coding 的业界标准。

#### [Aider-AI/aider](https://github.com/Aider-AI/aider) ⭐⭐⭐⭐⭐
★ 44k+ · Apache-2.0 — git-aware 的 CLI pair-programmer。直接编辑你 repo 中的文件，commit 都自动写好。**「git-native AI 编辑流程」的开源模板**。模型不限。

#### [anthropics/claude-code](https://github.com/anthropics/claude-code) ⭐⭐⭐⭐⭐
★ 120k+ — Anthropic 官方的 agentic coding 助理。有 Skills + plugin 生态系。

#### [cline/cline](https://github.com/cline/cline) ⭐⭐⭐⭐⭐
★ 61k+ · Apache-2.0 — VS Code extension，autonomous in-IDE agent：tool use、browser、step-by-step approval。**VS Code 用户想 IDE-native agentic dev 的好选项**。

#### [continuedev/continue](https://github.com/continuedev/continue) ⭐⭐⭐⭐
★ 33k+ · Apache-2.0 — source-controlled AI checks，可以在 CI 强制执行。代表「**团队 / governance**」这条角度的 coding agent。

#### [OpenHands (前身为 OpenDevin)](https://github.com/All-Hands-AI/OpenHands) ⭐⭐⭐⭐
★ 72k+ · MIT — open source 的自主软件开发 agent。设计上比 Aider / Claude Code 更激进——agent 自己跑 sandbox、自己 commit，适合「整个 issue 丢给它解」场景。

#### [block/goose](https://github.com/block/goose) ⭐⭐⭐⭐
★ 43k+ · Apache-2.0 — 开源、可扩展的 AI agent，超出纯 code suggestion——能 install / execute / edit / test，搭配任何 LLM。同时支持多家 LLM provider 跟 MCP，提供 desktop app、CLI、API 三种接口。（repo 现指向 `aaif-goose/goose`。）

#### [RooCodeInc/Roo-Code](https://github.com/RooCodeInc/Roo-Code) ⭐⭐⭐⭐
★ 23k+ · Apache-2.0 — VS Code 的 coding agent，采用「**多种专业模式**」的设计，跟 Cline 的单一 agent flow 不同。VS Code 用户想 multi-mode 替代方案的选择。

### Code Review

#### [obra/superpowers](https://github.com/obra/superpowers) ⭐⭐⭐⭐
20+ 个经过实战验证的 skill，包括 TDD 模式、debug、协作模式。设计 code-review skill 时的好参考。

## 必练流程

- **AI 结对编程**：日常工作用 Claude Code、Cursor、或 Cline 任意一个
- **Git-native AI 编辑**：用 Aider 跑一周，习惯「AI 编辑 → commit → review」这个节奏
- **CI 上的 AI check**：用 Continue 把 AI 检查接到 PR pipeline
- **测试生成**：写一个 skill / prompt，从 function signature 生成 pytest 测试
- **Code review 自动化**：在每一个 PR 上调用 Claude API 的 GitHub Action

### 3 个具体 workflow recipe

**1. AI 结对编程（每日节奏）**
1. 开新 feature → `git checkout -b feature/xxx`
2. 把任务丢给 Claude Code / Cursor，**先让它写 plan**（不直接写 code）
3. Review plan、修正方向 → 才 approve 写 code
4. 写完跑 tests + lint → 自己 review diff（**不要 blind accept**）
5. Commit message 自己写或 prompt 生草稿后改

**2. Aider git-native 流程（最像「跟 AI pair」）**
```bash
# 进入 repo 后
aider --model anthropic/claude-sonnet-4-20250514

# 自然语言请求
> 帮我把 utils.py 的 parse_date 加上时区参数，默认 UTC

# Aider 会自动编辑 + commit。若不满意：
> /undo  # 退掉最后一次 AI commit
```

**3. PR 上的 Claude code review（GitHub Action）**

`.github/workflows/claude-review.yml`：
```yaml
on:
  pull_request:
jobs:
  review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
      - name: Run Claude review
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
        run: |
          # 用 anthropics/claude-code-action 或自写 script
          # 抓 git diff、跑 prompt、结果 post 回 PR
```
参考 [`anthropics/claude-code-action`](https://github.com/anthropics/claude-code-action) 官方 GitHub Action。

## 常见踩坑（Anti-patterns）

| ❌ 不要 | ✅ 改成 |
|---|---|
| 让 AI 直接 push 到 main | 永远 PR → review → merge |
| Blind accept 大规模 refactor diff | 拆成 < 50 LOC 改动，逐个 review |
| 把 .env / API key 丢给 AI 看 | 用工具对应的排除机制：Cursor `.cursorignore` / Aider `.aiderignore` / Claude Code 用 `.claude/settings.json` 的 `permissions.deny` |
| 让 AI 在 production code 自由跑 shell | sandbox 限制、permission whitelist |
| 用 AI 生 test 后不检查 assertion | 跑覆盖率 + 故意改一个 bug 看 test 抓不抓得到 |
| 跨多个 commit 才发现方向错 | **plan-first** 模式：先 review plan 再写 code |

## Tier 升级路径

- **Tier 0**：Cursor / Claude Desktop——IDE 内 chat、不写 agent
- **Tier 1**：Claude Code / Cline / OpenCode——CLI 接 file system、有 CLAUDE.md，但仍 human-in-the-loop
- **Tier 2**：自写 Skills + MCP server——把你的 dev workflow 包成 skill team 共用
- **Tier 3**：CI 自动跑 agent + production observability——进到 [Stage 7](../stages/07-multi-agent-production.zh-Hans.md) 领域

> Tier 0-1 应该满足 90% 开发者。**升级到 Tier 2+ 要先确认 ROI**——团队够大、流程够重复、事故不可逆，才值得 invest。

## 也适用其他分支

开发者重叠度高的分支：

- **要做 ML 研究 / 写 paper** → [研究员分支](./for-researcher.zh-Hans.md)
- **接 Notion / Linear / Atlassian / Postgres / Figma** 等 dev tool → [`resources/mcp-skills-catalog.zh-Hans.md`](../resources/mcp-skills-catalog.zh-Hans.md)
- **要写自己的 Skill / MCP server** → [Stage 5](../stages/05-claude-code-ecosystem.zh-Hans.md) + [`resources/cookbook.zh-Hans.md`](../resources/cookbook.zh-Hans.md)
- **想看 schema 设计细节** → [`resources/schema-design-cheatsheet.zh-Hans.md`](../resources/schema-design-cheatsheet.zh-Hans.md)
- **CLI 从零开始** → [Track A](../tracks/cli/A1-cli-intro.zh-Hans.md)（A1 → A2 → A3）

## 社群备注

特别欢迎以下贡献：

- IDE-specific 设置范本（Cursor `.cursorrules`、Claude Code `CLAUDE.md` for Python / Go / Rust 等）
- 编程语言特化 skill（Python / TypeScript / Rust / Go 各自的 best practice）
- CI / pre-commit hook 集成 case study
- **跨多人团队用 AI dev 的 governance pattern**——多 dev 共用 Skills、permission 设计、cost tracking

请见 [CONTRIBUTING.md](../CONTRIBUTING.md)。
