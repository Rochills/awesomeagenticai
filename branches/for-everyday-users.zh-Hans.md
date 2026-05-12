# 给日常用户 — 专业分支

> [繁體中文](./for-everyday-users.md) | **简体中文** | [English](./for-everyday-users.en.md) | [Русский](./for-everyday-users.ru.md)

> 🚀 **完全没写过 code / 没装过 Python？** 先看 [`resources/setup-guide.zh-Hans.md` §A-C](../resources/setup-guide.zh-Hans.md)（30 分钟从零装好）再回来。已经会 Python 和有 API key 就跳过。

> [← 回主路线 README](../README.zh-Hans.md) · 你**不一定要走完主干**才能从这里开始——这条分支是给「**只想 USE AI、不一定要 BUILD agent**」的人。

## 使用场景

- 写 email、整理笔记、改 cover letter
- 学新技能（读英文文章、学语言、复习重点）
- 查资料、做研究比较（旅游、产品、学校）
- 整理生活流程（食谱、行程、待办清单）
- 隐私敏感场景：医疗记录、个人财务（→ 本地 LLM）

## 起步：你应该从哪一层进入？

按「**动手意愿**」分 4 层，从低到高：

```
Tier 0：网页 / 手机 App（推荐从这里开始）
   ↓
Tier 1：Desktop App（要处理本地文件再升级）
   ↓
Tier 2：CLI Agent（愿意学一点命令行，能自动化日常流程）
   ↓
Tier 3：本地 LLM（隐私敏感、API 费用敏感、想 offline）
```

**多数人停在 Tier 0 / Tier 1 就够用了**——Tier 2-3 是给有特殊需求或想学的人。

---

## 🎯 精选 Projects

### Tier 0 — 网页 / 手机 App ⭐ 入门

#### [Claude.ai](https://claude.ai) ⭐⭐⭐⭐⭐
Anthropic 官方界面。长文章、深度讨论、复杂问题很适合用——回答风格较收敛、不太瞎掰。

#### [ChatGPT](https://chatgpt.com) ⭐⭐⭐⭐⭐
OpenAI 官方界面。生态最广（GPTs、Custom Instructions、Voice mode）。一般用途的标准选择。

#### [Gemini](https://gemini.google.com) ⭐⭐⭐⭐
Google 出品。长 context 窗口（百万 token）特别适合丢整本 PDF 进去问问题。集成 Google 服务（Gmail、Docs）。

#### [Perplexity](https://perplexity.ai) ⭐⭐⭐⭐
搜索引擎 × LLM——每个答案都附引用来源。比 ChatGPT 适合「需要查最新信息」的场景。

---

### Tier 1 — Desktop App

#### [Claude Desktop](https://claude.ai/download) ⭐⭐⭐⭐⭐
比网页版多了：拖文件进去、本地文件读取、保留长期对话脉络。**也是进入 MCP 生态的入口**——可以接 Slack / Gmail / 行事历 server。

#### [ChatGPT Desktop](https://openai.com/chatgpt/desktop) ⭐⭐⭐⭐
ChatGPT 桌面版。可以对屏幕截图问问题、语音对话、跟其他 App 集成。

---

### Tier 2 — CLI Agent（愿意学命令行的进阶用户）

> 这些工具虽然定位给开发者，但**日常用户也能用**——例如批量重命名文件、整理下载文件夹、自动写每周回顾、把 PDF 摘要存成 Markdown。
>
> 想看详细比较？见 [`resources/cli-agents-guide.zh-Hans.md`](../resources/cli-agents-guide.zh-Hans.md)（7 个主流 CLI agent 并列、依 use case 推荐、常见坑、实用搭配）。
>
> 想要 step-by-step 上手？见 [`tracks/cli/A1-cli-intro.zh-Hans.md`](../tracks/cli/A1-cli-intro.zh-Hans.md)（Track A 第一站，从安装到第一个任务）。
>
> 想把 CLI agent 接到你的 Notion / Obsidian / Excel / Google 文件等日常工具？见 [`resources/mcp-skills-catalog.zh-Hans.md`](../resources/mcp-skills-catalog.zh-Hans.md)（按分类整理 62 个 MCP server / Skill）。

#### [anthropics/claude-code](https://github.com/anthropics/claude-code) ⭐⭐⭐⭐⭐
★ 120k+ — Anthropic 官方的 CLI agent。能读写文件、执行指令、做多步骤任务。**日常用户最容易上手的 CLI 工具**。

#### [openai/codex](https://github.com/openai/codex) ⭐⭐⭐⭐⭐

| 栏位 | 内容 |
|---|---|
| Stars | ★ 80k+ |
| License | Apache-2.0 |

**教什么**：OpenAI 出品的轻量级 terminal coding agent。跟 Claude Code 同类，但用的是 OpenAI 的模型。

**适合谁**：已经订 ChatGPT Plus / Pro，想在终端机用同一个账号做事的人。

#### [sst/opencode](https://github.com/sst/opencode) ⭐⭐⭐⭐⭐

| 栏位 | 内容 |
|---|---|
| Stars | ★ 155k+ |
| License | MIT |

**教什么**：开源版的 coding agent，**不绑定特定 LLM provider**——可以用 Claude、GPT、Gemini、本地 Ollama 任何一个。社群维护、迭代速度快。

**适合谁**：想 self-host、不想被 API provider 绑定，或要在多个 LLM 之间切换的人。

#### [google-gemini/gemini-cli](https://github.com/google-gemini/gemini-cli) ⭐⭐⭐⭐

| 栏位 | 内容 |
|---|---|
| Stars | ★ 103k+ |
| License | Apache-2.0 |

**教什么**：Google 官方的 Gemini CLI agent。把 Gemini 的长 context 跟 Google 生态集成到终端机。

**适合谁**：Google 生态的重度用户（Gmail、Drive、Docs）。

---

### Tier 3 — 本地 LLM（隐私 / 离线 / 省钱）

#### [Ollama](https://github.com/ollama/ollama) ⭐⭐⭐⭐⭐
★ 170k+ — 一行指令跑本地 LLM。隐私敏感数据（病历、合约、家人对话）不适合送去云端时用这个。详见 [Stage 1 — Local LLM 执行](../stages/01-llm-basics.zh-Hans.md)。

#### [LM Studio](https://lmstudio.ai/)
非开源但对非开发者最友好——拖拉界面、不用 command line。Mac / Windows / Linux 都有。

---

### Prompt 素材库

#### [f/awesome-chatgpt-prompts](https://github.com/f/awesome-chatgpt-prompts) ⭐⭐⭐⭐
★ 161k+ — 社群维护的 prompt 大全。「act as 翻译家 / 履历顾问 / 厨师...」几百种角色。**不知道怎么开头时从这里找灵感**。

---

## 必修阅读

1. [**Anthropic — How to write effective prompts**](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/overview) — 不用代码也能读的 prompt 写法
2. [**OpenAI — Prompting Guide**](https://platform.openai.com/docs/guides/prompt-engineering) — 对称的官方文件
3. [**ChatGPT 怎么用得最好（中文）**](https://www.runoob.com/) — 各家中文博客的整理（runoob 等等）

如果有兴趣再深入，看 [Stage 2 — Prompt 设计](../stages/02-prompt-engineering.zh-Hans.md)，那边有正式系统性教学。

## 可以建的流程

这些是模板——配合你的场景自行调整：

- **每周周记**：跟 Claude.ai 讲你这周做什么，请它整理成周记+下周重点
- **email triage**：每天早上把待回信件贴进 Claude，请它分类成「立即回复/今天回/这周回/不用回」
- **学语言**：跟 ChatGPT Voice 模式对话练英文/日文，请它指出语法错误
- **批量整理文件**：用 Claude Code 重新命名下载文件夹的所有文件，照日期 + 主题分类
- **本地隐私 chat**：Ollama 跑 qwen2.5:7b，问医疗 / 法律 / 财务问题不送云端

## 给日常用户的层级建议

90% 的场景：**留在 Tier 0**——Claude.ai 或 ChatGPT 网页版，免安装、免付费就能跑（免费版有限额但够日常用）。

5% 升级到 Tier 1：要处理本地文件、要保留对话历史、要接 MCP server。

5% 升级到 Tier 2-3：有真的自动化需求（譬如每天要做同样的事 100 次），或隐私敏感数据不能送云端。

**不要被人催着升级**——多数人 Tier 0 就够用了。Tier 2-3 是工具，不是身份地位。

## 社群备注

这条分支也欢迎社群贡献：

- 推荐特定领域的 prompt template（料理、运动、学语言）
- 中文友善的 chat tools（国产 LLM、本地化 wrapper）
- 隐私 / 安全相关的最佳实践（什么数据能送 / 不能送）

详见 [CONTRIBUTING.md](../CONTRIBUTING.md)。
