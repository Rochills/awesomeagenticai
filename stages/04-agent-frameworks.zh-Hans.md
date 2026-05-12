> [繁體中文](./04-agent-frameworks.md) | **简体中文** | [English](./04-agent-frameworks.en.md) | [Русский](./04-agent-frameworks.ru.md)

# 第 4 阶段 — Agent 框架

⏱ **时间估算**：2-3 周（约 10-15 小时）

> 💡 用语不熟（framework / supervisor / worker / handoff⋯）→ 翻 [`resources/glossary.zh-Hans.md`](../resources/glossary.zh-Hans.md)。

你已经从零打造过一个 ReAct agent（第 3 阶段）。现在来看 framework 到底帮你做了什么。**挑一个深入学**，其他的浏览过去就好，知道什么时候该换。

## 📌 学习目标

完成这个阶段后你会：
- 比较 5 个主流 agent 框架（LangGraph、AutoGen、CrewAI、Smolagents、OpenAI Agents SDK）
- 为任务挑出对的框架
- 用两个框架各做一次同样的 agent，亲身感受差异
- 看出什么时候该丢掉框架、自己写

## 🚪 进入条件

你应该已经：
- 跑完第 3 阶段的全部 5 个 hello-X projects
- 从零写过 ReAct（练习 3）
- 对 async Python 上手（框架大量依赖 async）

⚠️ **内存预备（需要时偷看一下）**：有些框架功能会用到内存的概念 — LangGraph 用 checkpointing（状态持久化），CrewAI 在 agent 之间传递任务结果（轻量内存）。这些东西在 [第 6 阶段 — 内存 & RAG](06-memory-rag.zh-Hans.md) 会讲清楚。你不必先读完那篇，只是当某个框架功能让你看不懂的时候，去那边找答案就对了。

## 📚 必修阅读

1. [**Anthropic — Building Effective Agents**](https://www.anthropic.com/engineering/building-effective-agents) — 什么时候用框架、什么时候直接用 raw API
2. [**LangChain — Conceptual Guide: Agents**](https://python.langchain.com/docs/concepts/agents/) — agent 的抽象概念
3. [**Best Multi-Agent Frameworks 2026 comparison**](https://gurusup.com/blog/best-multi-agent-frameworks-2026) — 当前市场定位
4. **挑一个框架的 Quickstart** — 选 LangGraph 或 CrewAI，把官方教学从头跑到尾

## 🛠 动手练习

### 练习 1：同一个 agent、两个框架
用以下两个框架各做一次同样的简单 agent（搜索 + 摘要）：
- LangGraph
- CrewAI
比较代码行数、debug 体验、以及它们各自把哪些复杂度藏在哪里。

### 练习 2：多 agent 角色分配
用 CrewAI 做一个 2-3 个 agent、各自有不同角色一起完成同一个任务的 demo。（这种情境 CrewAI 最拿手。）

### 练习 3：图式工作流
用 LangGraph 做一个有分支逻辑跟 human-in-the-loop checkpoint 的 workflow。（这种情境 LangGraph 最拿手。）

### 练习 4：CodeAct vs JSON tool
用 Smolagents 做一个会写 Python 代码当作 action 的 agent（CodeAct pattern），跟练习 1 用的 JSON tool call 路线比较。问同一个问题，看两种路线怎么解。

### 练习 5：类型安全 agent
用 Pydantic AI 做一个会回传结构化输出的 agent（例如：问问题回 `{ "answer": str, "confidence": float, "sources": [str] }`）。看 Pydantic 的 schema validation 怎么防止 agent 偷懒或 hallucinate 结构。

## 🎯 精选 Projects

### [LangGraph](https://github.com/langchain-ai/langgraph) ⭐ production 等级

| 字段 | 内容 |
|---|---|
| 语言 | Python / TypeScript |
| Stars | ★ 31k+ |
| License | MIT |
| 推荐度 | ⭐⭐⭐⭐⭐ |

**教什么**：基于图的 agent orchestration。状态管理、checkpointing、human-in-the-loop、time-travel debugging。

**适合谁**：production 级的多 agent 系统，需要稽核轨迹与 rollback 的场景。企业级。

**备注**：2025 年起企业采用率明显上升（稽核轨迹、replay-friendly 图模型）。学习曲线比 CrewAI 陡，但 production 场景值得。建议搭配 LangSmith 做 observability。

**怎么跑**：
```bash
pip install langgraph langchain-anthropic
# Tutorial: https://langchain-ai.github.io/langgraph/tutorials/introduction/
```

---

### [CrewAI](https://github.com/crewAIInc/crewAI) ⭐ 最容易上手

| 字段 | 内容 |
|---|---|
| 语言 | Python |
| Stars | ★ 50k+ |
| License | MIT |
| 推荐度 | ⭐⭐⭐⭐ |

**教什么**：以角色为核心的多 agent 设计。一群（Crew）有不同角色的 agent 朝同一个目标合作。

**适合谁**：快速雏形多 agent 系统。约 20 行就能跑出一个 crew。「研究员 → 写手 → 审稿」这类管线特别合用。

**备注**：学习曲线最低。但是：长时间 workflow 没有内置 checkpointing、agent 之间的沟通可控性有限、错误处理偏粗糙。雏形用 CrewAI、production 用 LangGraph。

---

### [Microsoft AutoGen / AG2](https://github.com/microsoft/autogen)

| 字段 | 内容 |
|---|---|
| 语言 | Python |
| Stars | ★ 57k+ |
| License | CC-BY-4.0（注意：这是文件 license，代码另外释出） |
| 推荐度 | ⭐⭐⭐⭐ |

**教什么**：对话式多 agent 团队。agent 透过​​多轮对话互动。group-chat 协调模式是它的强项。

**适合谁**：多 agent 辩论、脑力激荡、peer review 类的 pattern。Microsoft 研究院血统。

**备注**：AG2（v0.4 重写版）改成 async-first 执行、event-driven 核心。多数既有教学仍在用原本的 AutoGen（v0.2），请留意版本分支。

---

### [Hugging Face Smolagents](https://github.com/huggingface/smolagents)

| 字段 | 内容 |
|---|---|
| 语言 | Python |
| Stars | ★ 27k+ |
| License | Apache 2.0 |
| 推荐度 | ⭐⭐⭐⭐ |

**教什么**：写代码的 agent（CodeAct pattern）— agent 产生 Python 代码，而不是 JSON tool call。≤1000 LOC 的设计哲学。

**适合谁**：本地 LLM 生态、HuggingFace 集成场景。设计理念跟主流不同，值得理解。

**备注**：HF 的赌注：agent 应该要小。他们的 CodeAct 路线在思路上很不一样，跟 JSON-tool 路线对照看，可以看出彼此的取舍。

---

### [OpenAI Agents SDK](https://github.com/openai/openai-agents-python)

| 字段 | 内容 |
|---|---|
| 语言 | Python |
| License | MIT |
| 推荐度 | ⭐⭐⭐⭐ |

**教什么**：OpenAI 官方的 agent SDK。agent 之间 hand-off、结构化输出、OpenAI 原生的开发体验。

**适合谁**：你已经押注 OpenAI 生态。轻量、跟 GPT-4 系列集成很紧。

**备注**：较新的选手（2025 年下半年才推出）。实战历练不如 LangGraph，但 API 很干净，值得持续关注它的后续发展。

---

### [LlamaIndex Agents](https://github.com/run-llama/llama_index)

| 字段 | 内容 |
|---|---|
| 语言 | Python |
| Stars | ★ 49k+ |
| License | MIT |
| 推荐度 | ⭐⭐⭐ |

**教什么**：跟 RAG 紧密集成的 agent。如果你的 agent 需要大量文档/数据 retrieval，LlamaIndex 是自然选择。

**适合谁**：文档密集型的 agent 应用。研究助理、知识工作者类 agent。

**备注**：retrieval 强、orchestration 弱。纯 orchestration 场景不该选它；retrieval 为主的工作很适合。

---

### [Pydantic AI](https://github.com/pydantic/pydantic-ai)

| 字段 | 内容 |
|---|---|
| 语言 | Python |
| License | MIT |
| 推荐度 | ⭐⭐⭐ |

**教什么**：类型安全的 agent 框架，用 Pydantic 处理结构化输出。验证保证很强。

**适合谁**：production 团队，预设就要 runtime 类型安全 + 结构化输出。

**备注**：比竞品新。Pydantic 团队的血统让人对 API 设计有信心。

---

### [agentscope-ai/agentscope](https://github.com/agentscope-ai/agentscope)

| 字段 | 内容 |
|---|---|
| 语言 | Python |
| Stars | ★ 24k+ |
| License | Apache 2.0 |
| 推荐度 | ⭐⭐⭐ |

**教什么**：多 agent 平台，可视化工具是强项。「打造你看得到、看得懂、信得过的 agent」。

**适合谁**：想要可视化 debug 多 agent 流程的研究者。

**备注**：在西方社群采用度较低，但技术扎实。observability 工具很不错。

---

### [LangChain](https://github.com/langchain-ai/langchain)

| 字段 | 内容 |
|---|---|
| 语言 | Python / TypeScript |
| Stars | ★ 135k+ |
| License | MIT |
| 推荐度 | ⭐⭐⭐ |

**教什么**：最早的「万用工具袋」框架。chains、agents、memory、retrievers 全部一锅。

**适合谁**：需要把很多零件黏在一起的快速雏形。

**备注**：很多人 LangChain 用过头了。专做 agent orchestration 的话，请改用它的继任者 LangGraph。LangChain 比较适合 retrieval + chaining 的黏合，不适合 agent orchestration。

---

### [microsoft/semantic-kernel](https://github.com/microsoft/semantic-kernel)

| 字段 | 内容 |
|---|---|
| 语言 | C# / Python / Java |
| Stars | ★ 27k+ |
| License | MIT |
| 推荐度 | ⭐⭐⭐⭐ |

**教什么**：Microsoft 出品的企业级 SDK——kernel + plugin + planner pattern，**同时支持 C# / Python / Java**，是少数三语言都有官方 SDK 的 agent 框架。

**适合谁**：在 Microsoft 技术栈上工作的开发者，或要在 .NET / Java 环境做 agent 的人。

**备注**：抽象层比 smolagents 厚，不适合第一周的初学者。要在企业环境跑、需要 .NET / Java 的场景值得考虑。

---

### [agno-agi/agno](https://github.com/agno-agi/agno)

| 字段 | 内容 |
|---|---|
| 语言 | Python |
| Stars | ★ 39k+ |
| License | Apache-2.0 |
| 推荐度 | ⭐⭐⭐⭐ |

**教什么**：multi-modal agent runtime + control plane——除了 build agent，还涵盖 serving、monitoring、governance。2025 年新一代的 agent platform。

**适合谁**：要把 agent 推到「能 serve、能监控」的阶段，但又不想全套 LangGraph + LangSmith 的人。也适合 prototype 阶段的快速设计。

**备注**：第 4 阶段学它的 agent API，第 7 阶段再用它的 runtime / 监控功能。

---

### [BerriAI/litellm](https://github.com/BerriAI/litellm)（不是框架，是跨阶段基础设施）

| 字段 | 内容 |
|---|---|
| 语言 | Python |
| Stars | ★ 45k+ |
| License | MIT（含 `enterprise/` 子目录的另外授权） |
| 推荐度 | ⭐⭐⭐⭐ |

**教什么**：provider-agnostic SDK + AI gateway——**用 OpenAI 形状的 API 调用 100+ 个 LLM**，附 cost tracking、fallback、guardrail。

**适合谁**：要做能切换 Claude / GPT / Gemini / 开源模型的 agent，不想为了切换 provider 改一堆代码的人。

**备注**：严格来说 LiteLLM 不是 agent 框架，而是框架底下的「provider 抽象层」——放在第 4 阶段是因为写 multi-provider agent 时很常会用到。第 7 阶段 deploy 时也会再用到。Repo 内 `enterprise/` 目录是另外的授权条款。

---

## ✅ 进第 5 阶段前的自我检查

你能不能：
- [ ] 用 LangGraph 跟 CrewAI 各做一次同一个 agent
- [ ] 为任务挑出对的框架（production vs 雏形）
- [ ] 解释 LangGraph 的 checkpoint 跟 CrewAI 的 task delegation 差在哪
- [ ] 看出什么时候 CodeAct（Smolagents）比 JSON-tool 更好
- [ ] 判断什么时候该丢掉框架、直接用 raw API

如果可以 → 进 [第 5 阶段 — Claude Code Ecosystem](05-claude-code-ecosystem.zh-Hans.md)。

## 💡 策略提示

不要想把这些全部学完。挑**一个 production 等级的（LangGraph）**跟**一个快速雏形用的（CrewAI）**深入学。其他的 README 浏览过去就好，知道有这些选项存在即可。
