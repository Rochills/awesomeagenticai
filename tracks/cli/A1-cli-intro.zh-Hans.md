# A1 — 选一个 CLI Agent，开始用它做事（CLI Agent Intro & Selection）

> [繁體中文](./A1-cli-intro.md) | **简体中文** | [English](./A1-cli-intro.en.md)

> [← 回主线路 README](../../README.zh-Hans.md) · **Track A: CLI Power User** 第 1 站

⏱ **时间估算**：1 周（约 5-10 小时）

> 📋 **本章组成**：学习目标 → 进入条件 → 必修阅读 → 动手练习 → 精选 Projects → 自我检查
> 🔑 **关键名词**：本页只用到 **CLI agent**（在终端机跑的 AI 工具）。MCP / Skill / plugin 等其他生态名词会在 A2 / A3 第一次使用时再解释。完整词表见 [`resources/glossary.zh-Hans.md`](../../resources/glossary.zh-Hans.md)。

读完 Stage 0-2 之后，你想直接用现成的 CLI agent 把工作做完，**不打算自己写 agent 程序，只想先用现成工具完成任务**？这条轨就是给你的。第一站：**选一个 CLI agent，跑起来**。

## 📌 学习目标

完成后你会：

- 知道 8 个主流 CLI agent（Claude Code / Codex / OpenCode / Gemini CLI / goose / Aider / Hermes Agent / Grok Build）的差别
- 依自己的场景挑出第一个 CLI 工具
- 完成安装 + 认证 + 第一个真正的任务（不是 hello world）
- 知道什么 时候该换 / 加第二个 CLI

## 🚪 进入条件

你应该已经：
- 跑过 Stage 0 的 练习：CLI（会用命令行）
- 有 Claude / OpenAI / Google 任一个 账号（不一定是付费）
- 对 prompt 写法基本上手（Stage 2）

## 📚 必修阅读

1. [**`resources/agent-paradigms.zh-Hans.md`**](../../resources/agent-paradigms.zh-Hans.md) ⭐ — 5 种 agent 型态的全景图；先读这份知道 CLI agent 在整个 agent 生态中的位置（Type 2 + Type 3）
2. [**`resources/cli-agents-guide.zh-Hans.md`**](../../resources/cli-agents-guide.zh-Hans.md) ⭐ — 本轨的核心参考。8 个主流 CLI agent 并列比较、依 use case 推荐、实用搭配
3. [**Anthropic — Claude Code Quickstart**](https://docs.anthropic.com/en/docs/claude-code/quickstart) — 官方安装指南
4. [**OpenAI — Codex Quickstart**](https://github.com/openai/codex/blob/main/README.md) — Codex 安装跟认证流程

## 🛠 动手练习（基础 illustrative 练习）

### 动手练习 CLI-1：安装 + 第一次跑

**3 步走完**：

1. **装**：照你选的 CLI 的 quickstart 安装（每个 CLI 官网都有 ≤ 5 分钟的安装指南）
2. **挑一个低风险真实任务**：不要写 "hello world"——挑一件你今天本来就要做的事（例：整理我 Downloads 文件夹，把 PDF 全部 move 到 ~/Documents/PDFs）
3. **观察 3 件事**：它怎么分解任务、何时要求确认、输出格式如何

→ 用真任务跑，才能感受 agent 跟 chatbot 的差别。

### 动手练习 CLI-2：CLI 内建的 system prompt 文件
- Claude Code → 写一个 `CLAUDE.md` 在 repo 根目录
- Codex → 写 `AGENTS.md`
- Gemini CLI → 写 `GEMINI.md`
- goose / OpenCode → 看各自的设置

写进去 3 件事：你的个性 / 偏好的 code style / 不能做的事。再跑一个任务，观察行为差异。

### 动手练习 CLI-3：第二个 CLI 并用
装第二个 CLI（建议 Codex 或 OpenCode 当 backup）。用同一个 prompt 跑，比较输出风格、速度、cost。**不是要选一个赢家——是要学“不同 CLI 解同一个问题的角度不同”**。

### 动手练习 CLI-4：认证细节
故意把 API key 弄错一个字符，看 CLI 怎么报错。再做一次“正确 key 但 model 名称错”的实验。Production 用一定 会遇到 auth 问题，先在这里踩过。

## 🎯 精选 Projects

### 8 个主流 CLI agent

详细比较（star、license、强弱项、推荐场景）见 [`resources/cli-agents-guide.zh-Hans.md`](../../resources/cli-agents-guide.zh-Hans.md)。这里只给快速 entry point：

#### [anthropics/claude-code](https://github.com/anthropics/claude-code) ⭐⭐⭐⭐⭐
★ 138k+ — 第一个 CLI agent 推荐。内建 SKILL / plugin 生态、CLAUDE.md prompt 系统、中文社群资源丰富。

#### [openai/codex](https://github.com/openai/codex) ⭐⭐⭐⭐⭐
★ 99k+ — 已订 ChatGPT Plus / Pro 的人很合适；用同一个 账号就能在终端机跑。

#### [sst/opencode](https://github.com/sst/opencode) ⭐⭐⭐⭐⭐
★ 187k+ — 开源、不绑 LLM provider、社群迭代最快。要 self-host / 不想 vendor lock-in 选这个。

#### [google-gemini/gemini-cli](https://github.com/google-gemini/gemini-cli) ⭐⭐⭐⭐
★ 103k+ — 想要 1M token 长 context 处理大 codebase / 大 PDF 时用。

#### [block/goose](https://github.com/block/goose) ⭐⭐⭐⭐
★ 51k+ — 15+ provider 支援（含 Ollama）、可用既有 Claude / ChatGPT / Gemini 订阅。已迁至 `aaif-goose/goose`（AAIF / Linux Foundation）。

#### [Aider-AI/aider](https://github.com/Aider-AI/aider) ⭐⭐⭐⭐⭐
★ 44k+ — git-native，自动 commit / branch。要写 code 想要 git 流程干净的人用这个。

#### [NousResearch/hermes-agent](https://github.com/NousResearch/hermes-agent) ⭐⭐⭐⭐⭐
★ 217k+ — Nous Research 出的自动演化型 agent。差异化在三件事：(1) agent 跑 cloud VM，从 Telegram / Discord / Slack 任一界面跟它聊；(2) 多 LLM 中性，支持 GLM / Kimi / 小米 MiMo / MiniMax 等中文圈生态；(3) 内建 cron 排程 + skill 自动演化回圈（★ 数据截至 2026-05；以官方 GitHub 为准）。⚠️ 自动演化 skill 是实验性功能，缺第三方独立审计，production 用前请自行验证安全性与维护状态，先在低风险场景试。

#### [xai-org/grok-build](https://github.com/xai-org/grok-build) ⭐⭐⭐
★ 20k+ — SpaceXAI（xAI）官方 TUI coding agent（Rust、支持 headless 模式 / ACP 编辑器嵌入）。⚠️ 2026-07-14 才开源、非常新——先观察、不建议当第一个 CLI agent。

---

### 进阶：跟主流 CLI 互补的工具

#### [LM Studio](https://lmstudio.ai/)
非开源 desktop app——拖拉界面跑本地 LLM。如果你是 Windows / Mac 用户不想学 command line 但想跑 local LLM，先试这个。

#### [Ollama](https://github.com/ollama/ollama)
★ 170k+ — 本地 LLM runner，跟 OpenCode / goose 搭配很好（也能单独给 IDE 接 OpenAI 相容 API）。详见 [Stage 1 — Local LLM 执行](../../stages/01-llm-basics.zh-Hans.md#练习-6local-llm)。

## ✅ 进 A2 前的自我检查

你能不能：

- [ ] 讲得出 8 个主流 CLI 的核心差别（不查表就答得出 3-4 个）
- [ ] 你已经選定一个主用 CLI，并有 working setup（装好、认证好、跑过至少 5 个非 hello-world 任务）
- [ ] 写过你自己的 `CLAUDE.md` / `AGENTS.md` / `GEMINI.md`
- [ ] 至少跑过第二个 CLI 一次，知道两个的风格差异

如果可以 → 进 [A2 — CLI Workflow Patterns](A2-cli-workflow.zh-Hans.md)。

如果不行 → 别跳。CLI 工具会用得 sloppy 不会用得 productive；A1 的 动手练习 CLI-1/2 至少各跑 3 次再走。

## 💡 给 Track A 学习者的提醒

CLI agent 跟 web 版（Claude.ai / ChatGPT）的差别不是“一样的东西换界面”——CLI 能读写你电脑上的文件、执行 shell 指令、改 git。这个能力差异**先了解再用**：
- 第一周：每个任务都加 `--dry-run` 或先 review 计划再执行
- 不要直接让 CLI 对 production codebase 做 commit
- 重要数据（key、合约、病历）放在 `.cursorignore` / `.claudeignore` 排除
