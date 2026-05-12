# Stage 3 — Tool Use 与 Agent 入门 ⭐

> [繁體中文](./03-tool-use-and-hello-agent.md) | **简体中文** | [English](./03-tool-use-and-hello-agent.en.md) | [Русский](./03-tool-use-and-hello-agent.ru.md)

⏱ **时间估算**：2-3 周（约 10-20 小时）

> 💡 用语密集（agent / tool use / function calling / ReAct / structured output⋯）→ 翻 [`resources/glossary.zh-Hans.md` §2](../resources/glossary.zh-Hans.md#2-agent--工具使用)。

这是整个学习路线最关键的一站。**你建过一个 agent 才算真懂 agent — 动手练习 不能跳。**

## 📌 学习目标

完成这个 stage 后你会：
- 讲得出为什么 LLM 需要 tools（它不是万能的，而且文字以外的事它都做不了）
- 定义一个 tool schema，并让 LLM 调用它
- 从零（不靠任何 framework）写出一个单步 ReAct agent
- 写出多步 ReAct agent，并让它自己判断何时该停
- 分得出哪种问题该用 tool use、哪种纯 prompt 就够

## 🚪 进入条件

你应该已经：
- 有可以跑的 Claude / OpenAI / Gemini API 权限（Stage 1）
- 对 prompt engineering 基础已经上手（Stage 2）
- 能写一个吃 JSON 进、吐 JSON 出的 Python 函数

## 📚 必修阅读

1. [**Anthropic — Tool Use**](https://docs.anthropic.com/en/docs/agents-and-tools/tool-use/overview) — 官方指南
2. [**ReAct: Synergizing Reasoning and Acting in Language Models**](https://arxiv.org/abs/2210.03629) — Yao et al. 2022，奠基论文。至少读 abstract 跟 Section 3。
3. [**OpenAI — Function Calling**](https://platform.openai.com/docs/guides/function-calling) — function calling 格式参考
4. [**Build an agent from scratch**](https://shafiqulai.github.io/blogs/blog_3.html) — 从零打造 agent 的故事式导览

## 🛠 动手练习（不是看过就好）

### 练习 1：Function Calling（一个工具、一次调用）
给 Claude 一个工具（假的天气 API）跟一个问题（「台北现在有下雨吗？」）。看 Claude 怎么调用工具、拿到结果、再回答你。

### 练习 2：多工具选择
给 Claude 三个工具（搜索、计算机、行事历）跟一个任务。看 Claude 怎么挑工具，顺便注意它什么时候会挑错。

### 练习 3：从零实现 ReAct（不用 framework）
用 50-80 行 Python 把 Thought → Action → Observation 循环写出来。不要 LangChain、不要 LangGraph，就是纯 `while not done: thought; action; observation; ...`。

### 练习 4：多步骤推理任务
一个需要连续调用 3-5 次 tool 的任务。例如：「找出台北人口，除以纽约人口，再把比例换成百分比。」每一步用不同的工具。

### 练习 5：错误处理
让某个工具失败（网络错误、输入无效）。看看 agent 会怎么处理错误、能不能恢复，再加上 retry 机制。

### 练习 6：Function schema 设计（坏 schema 修到好）
**先给 LLM 一份故意写烂的 schema**——`description` 模糊（「处理数据」）、参数全用 `type: string`、没分 required / optional、enum 该用没用。观察 LLM 怎么选错 tool、传错参数。然后逐项修：
- description 写到 LLM 一眼就懂这个 tool 适用情境（不是写给人读的 docstring）
- parameters 用对 type（number / boolean / enum / array），required 列清楚
- 模糊边界用 enum 强制收敛（例如 `unit: "celsius" | "fahrenheit"` 而不是 `unit: string`）
- error 回传要包 `{"error": "...", "retry_hint": "..."}` 让 LLM 能恢复

> 💡 详细 cheatsheet 看 [`resources/schema-design-cheatsheet.zh-Hans.md`](../resources/schema-design-cheatsheet.zh-Hans.md)——5 条黄金规则 + 5 个常见 anti-pattern。

## 🎯 精选 Projects

### [Anthropic — Tool Use Cookbook](https://github.com/anthropics/anthropic-cookbook/tree/main/tool_use)

| 字段 | 内容 |
|---|---|
| 语言 | Python |
| License | MIT |
| 推荐度 | ⭐⭐⭐⭐⭐ |

**教什么**：Claude 支持的所有 tool use 模式 — 单工具、多工具、并行调用、结构化输出抽取。

**适合谁**：练习 1 跟 练习 2，从这里开始。

**怎么跑**：
```bash
git clone https://github.com/anthropics/anthropic-cookbook
cd anthropic-cookbook/tool_use
jupyter notebook customer_service_agent.ipynb
```

---

### [Anthropic — Quickstarts](https://github.com/anthropics/anthropic-quickstarts)

| 字段 | 内容 |
|---|---|
| 语言 | Python / TypeScript |
| Stars | ★ 16k+ |
| License | MIT |
| 推荐度 | ⭐⭐⭐⭐⭐ |

**教什么**：Anthropic 官方的 动手练习 起手包。三个可直接 deploy 的 agent 范本：`financial-data-analyst`（数据分析 agent）、`customer-support-agent`（客服 agent）、`computer-use-demo`（让 Claude 操作屏幕）。

**适合谁**：跑完 练习 1 / 练习 2 之后，想看「真的应用会长什么样子」的官方参考。比社群实现更 canonical，部署设置也比较完整。

**备注**：每个范本都是独立 sub-folder，挑一个有兴趣的跑就好。Computer use demo 特别值得看 — 是少数示范 agent 操作 GUI 的官方范例。

---

### [pguso/ai-agents-from-scratch](https://github.com/pguso/ai-agents-from-scratch)

| 字段 | 内容 |
|---|---|
| 语言 | Python |
| License | MIT |
| 推荐度 | ⭐⭐⭐⭐⭐ |

**教什么**：用本地 LLM 从零打造 agent，零 framework。ReAct、function calling、memory，全部自己写。设计目的就是把 framework 帮你藏起来的东西摊开给你看。

**适合谁**：练习 3（从零写 ReAct）。这是最干净的「不靠 framework」参考实现。

**备注**：用本地 Ollama，不用花 API 钱。README 值得仔细读，章节结构安排得很好。

---

### [arunpshankar/react-from-scratch](https://github.com/arunpshankar/react-from-scratch)

| 字段 | 内容 |
|---|---|
| 语言 | Python |
| License | Apache-2.0 |
| 最后更新 | ⚠️ 2025 年 5 月（更新放缓） |
| 推荐度 | ⭐⭐⭐⭐ |

**教什么**：ReAct pattern 的多种变体与实现，针对 Gemini 最佳化。

**适合谁**：练习 3 的替代方案，如果你偏好 Gemini。涵盖 ReAct + Reflection + Self-consistency 等变体。

---

### [mattambrogi/agent-implementation](https://github.com/mattambrogi/agent-implementation)

| 字段 | 内容 |
|---|---|
| 语言 | Python |
| License | MIT |
| 最后更新 | ⚠️ 已停滞（2024 年 1 月）— 留作教学玩具参考 |
| 推荐度 | ⭐⭐⭐ |

**教什么**：最精简的 ReAct agent 实现。为了学习而砍到只剩约 150 行代码。

**适合谁**：逐行读代码。练习 3 卡住时可以拿来对照。

---

### [lsdefine/GenericAgent](https://github.com/lsdefine/GenericAgent)

| 字段 | 内容 |
|---|---|
| 语言 | 中文 + Python |
| Stars | ★ 9k+ |
| License | MIT |
| 推荐度 | ⭐⭐⭐⭐ |

**教什么**：最精简的自我演化 agent framework — 核心约 3K 行代码，agent 从 seed 自己长出技能树。支持 Claude / Gemini / Kimi / MiniMax。仍在持续开发。

**适合谁**：练习 3 / 练习 4 的替代方案，给想看「精简但完整」framework 的读者。介于 mattambrogi 的玩具版跟完整 LangGraph 之间。

---

### [HelloAgents (jjyaoao)](https://github.com/jjyaoao/HelloAgents) — `learn_version` 分支

| 字段 | 内容 |
|---|---|
| 语言 | 中文（zh-Hans）+ Python |
| License | CC BY-NC-SA 4.0 |
| 推荐度 | ⭐⭐⭐⭐⭐（中文读者） |

**教什么**：教学导向的多 agent 练习框架，章节式教学，搭配 [Datawhale 的 Hello-Agents 教学](https://github.com/datawhalechina/hello-agents)。涵盖 16 种能力（tool response、context engineering、session 持久化、sub-agents、circuit breaker、observability 等），用来学 production pattern 的教材，不是直接拿来上 production 的成品。

**适合谁**：中文读者。**请切到 `learn_version` 分支**，那才是对齐教材的版本。

**备注**：License 是 CC BY-NC-SA — 非商用。教材是 zh-Hans，但技术内容对 zh-TW 读者没障碍。

**怎么跑**：
```bash
pip install hello-agents
git clone -b learn_version https://github.com/jjyaoao/HelloAgents
```

---

### [datawhalechina/hello-agents](https://github.com/datawhalechina/hello-agents)

| 字段 | 内容 |
|---|---|
| 语言 | 中文（zh-Hans） |
| License | CC BY-NC-SA |
| 推荐度 | ⭐⭐⭐⭐⭐（中文读者） |

**教什么**：HelloAgents 的搭配教学。多章导读，从「什么是 agent」一路讲到 production 的实务 pattern。

**适合谁**：想要结构化教学加代码的中文读者。

**备注**：请搭配上面 HelloAgents repo 的 `learn_version` 分支一起看。

---

### [QuantaLogic/quantalogic](https://github.com/quantalogic/quantalogic)

| 字段 | 内容 |
|---|---|
| 语言 | Python |
| License | Apache-2.0 |
| 推荐度 | ⭐⭐⭐ |

**教什么**：产生 Python 代码（而不是 JSON tool call）的 ReAct agent。设计选择不同 — agent 直接写代码当作 action。

**适合谁**：跑完 练习 3 之后。比较 CodeAct（代码即 action）与 JSON tool call 的差别。

---

### [HuggingFace Smolagents](https://github.com/huggingface/smolagents)

| 字段 | 内容 |
|---|---|
| 语言 | Python |
| Stars | ★ 27k+ |
| License | Apache 2.0 |
| 推荐度 | ⭐⭐⭐⭐ |

**教什么**：Smol agents（≤1000 LOC）。会写代码的 agent — 执行 Python 而不是 JSON tool call。

**适合谁**：练习 5 的替代方案。特别适合本地 LLM 实验。

**备注**：HF 的立场：agent 应该要小。他们的 code-action 路线跟 JSON-tool 路线在思路上很不一样，值得对照来看。

---

### [LangChain — ReAct Agent Template](https://github.com/langchain-ai/react-agent)

| 字段 | 内容 |
|---|---|
| 语言 | Python |
| License | MIT |
| 推荐度 | ⭐⭐⭐ |

**教什么**：framework 怎么把 ReAct pattern 抽象化。LangGraph Studio 的范本。

**适合谁**：练习 3 之后（先自己从零写过再來）。再來比较 framework 帮你做了哪些事。

---

### [Anthropic — Building Effective Agents（部落格文章）](https://www.anthropic.com/engineering/building-effective-agents)

| 字段 | 内容 |
|---|---|
| 形式 | 文章 |
| 推荐度 | ⭐⭐⭐⭐⭐ |

**教什么**：Anthropic 自己写的指南 — 什么时候该用 agent（vs. workflow）、常见 pattern、容易踩的坑。Stage 4 之前必读。

**适合谁**：建立观念框架。练习 3 写完之后、学 framework 之前读。

---

## ✅ 进 Stage 4 前的自我检查

你能不能：
- [ ] 定义一个 tool schema（name + description + JSON schema 输入/输出）
- [ ] 用不到 100 行 Python、不靠任何 framework，把 ReAct 循环写出来
- [ ] 解释为什么 agent 需要一个「我做完了」的退出条件
- [ ] 比较 CodeAct（代码即 action）跟 JSON-tool 两种路线
- [ ] 看出哪些问题其实不需要 agent

如果可以 → 进 [Stage 4 — Agent Frameworks](04-agent-frameworks.zh-Hans.md)。

如果不行 → 把 练习 3 再跑一次，不要跳过。如果你不懂 framework 在帮你抽象什么，Stage 4 的那些东西看起来会像黑魔法。
