# 术语小词典（Glossary）

> [繁體中文](./glossary.md) | **简体中文** | [English](./glossary.en.md) | [Русский](./glossary.ru.md)

> 本路线图会大量出现「LLM」、「RAG」、「MCP」、「agent」这类词。读到不懂的词先在这里查 30 秒，再回去读 stage 内容。
>
> 每个词**只给最小可用的解释**（30-80 字 + 在哪一个 stage 讲细的）——不是维基百科。

---

## 1. 基本概念

### LLM（Large Language Model，大语言模型）

GPT、Claude、Gemini 这类「给文字、回文字」的模型。本身是纯函数：input prompt → output text。它**不会自己上网、不会记住上次对话**——这些都要外接系统来做。

📍 详细：[Stage 1](../stages/01-llm-basics.zh-Hans.md)

### Token

LLM 看到的不是「字」，是 **token**（次字单位）。中文 1 个字 ≈ 1.5-2 token，英文 1 个 word ≈ 1.3 token。LLM 计费跟 context window 都以 token 计。「100 万 token context」≈ 75 万中文字。

📍 详细：[Stage 1](../stages/01-llm-basics.zh-Hans.md)

### Context Window（上下文视窗）

LLM 一次能「看」多少 token。Claude 200k、GPT-4o 128k、Gemini 2M。**不是越大越好**——超过某个长度后 LLM 会「在中间遗漏」（Lost in the Middle）。

### Prompt（提示词）

你给 LLM 的输入文字。**Prompt engineering** 就是设计这段输入让 LLM 给好答案。System prompt（角色设定）+ user prompt（这次的问题）是基本结构。

📍 详细：[Stage 2](../stages/02-prompt-engineering.zh-Hans.md)

### Few-shot / Zero-shot

- **Zero-shot**：直接问问题不给范例。
- **Few-shot**：给 2-5 个 input → output 的范例后再问。**Few-shot 通常显著提升准确度**，特别是格式要求严的任务。

### Chain-of-Thought（CoT，思维链）

要 LLM「先想再答」——加上「Let's think step by step」之类的指令，让它输出推理过程再给结论。**准确度通常会提升**，代价是 token 数变多。

---

## 2. Agent / 工具使用

### Agent（代理人）

让 LLM **能呼叫外部 function、看结果、再决定下一步**的系统。本路线图的核心主题。差别在于：纯 LLM 是 Q&A、agent 是「LLM + tools + 循环」。

📍 详细：[Stage 3](../stages/03-tool-use-and-hello-agent.zh-Hans.md)

### Tool Use / Function Calling

让 LLM 呼叫你定义好的 function（查 DB、算数学、开浏览器…）。LLM 回的不是文字而是 `{"function": "search", "args": {...}}`，你的程序去执行、把结果再丢回 LLM。

📍 详细：[Stage 3](../stages/03-tool-use-and-hello-agent.zh-Hans.md)

### ReAct（Reasoning + Acting）

最经典的 agent pattern：**Thought（想）→ Action（叫工具）→ Observation（看结果）→ Thought ...** 一直 loop 到答得出来。多数 agent framework 内部都实作这个。

📍 详细：[Stage 3](../stages/03-tool-use-and-hello-agent.zh-Hans.md)

### Structured Output（结构化输出）

要 LLM 输出 **JSON / 其他固定 schema**，而不是自由文字。各家 LLM API 都有 `response_format` 或类似旗标支持。Agent 框架几乎都靠这个跟 LLM 沟通。

### Agent Loop

「LLM → tool → 结果 → LLM」这个重复的循环。Loop 结束条件可能是：LLM 说「I'm done」、跑超过 N 步、超出 budget。

---

## 3. Memory / Retrieval / RAG

### RAG（Retrieval-Augmented Generation）

「先捞相关数据，再丢给 LLM 一起答」的模式。流程：用户问题 → 用 embedding 找出最相关的 K 段数据 → 把那 K 段塞进 prompt → LLM 答。**用来解决 LLM 不知道你私有数据 / 知识过期的问*题**。

📍 详细：[Stage 6](../stages/06-memory-rag.zh-Hans.md)

### Vector DB / Embedding（向量数据库 / 嵌入）

把文字（或图片）转成一串数字（向量），让「意思接近」的东西在向量空间中距离近。Vector DB（Pinecone、Chroma、Qdrant 等）就是存储 + 高效查询这些向量的数据库。RAG 的核心元件。

📍 详细：[Stage 6](../stages/06-memory-rag.zh-Hans.md)

### Semantic Search（语义搜索）

用 embedding 比较「意思相似」而不是「字符串完全相同」。「电动车怎么充电」可以捞到「EV charging tutorial」。传统关键字搜索（BM25 等）做不到这个。

### Chunking（切块）

把长文件切成适合 embedding 的小段（通常 200-1000 token）。**切法直接影响 RAG 品质**——切太碎丢脉络、切太长相关度模糊。常见策略：固定大小、按段落、按结构（heading）。

### Hybrid Search（混合搜索）

语义搜索 + 关键字搜索一起用，再 merge 排序。多半比单一方法准。production-grade RAG 标配。

### Reranking（重新排序）

第一轮 retrieval 捞 top-50，再用更贵但更准的模型（cross-encoder）重排成 top-5 给 LLM。Cohere Rerank、bge-reranker 等。

### Contextual Retrieval

Anthropic 2024 提的方法——chunk 加上「整份文件的脉络摘要」一起 embed，避免「这 chunk 拿出来看不知道是哪份文件讲的」问题。

📍 详细：[Stage 6](../stages/06-memory-rag.zh-Hans.md)

---

## 4. Multi-Agent（多 agent）

### Multi-Agent（多 agent）

多个 agent 互相协作完成一个任务。常见 pattern：

- **Supervisor + Worker**：一个 agent 规划 / 分派、其他执行
- **Swarm（群集）**：平等的 agent 群，没有固定 supervisor
- **Debate（辩论）**：多个 agent 各持立场、最后 consensus

📍 详细：[Stage 7](../stages/07-multi-agent-production.zh-Hans.md)

### Handoff

一个 agent 把任务交给另一个 agent。比直接 function call 多了「context 怎么传」、「失败谁处理」的问题。

### A2A（Agent-to-Agent）Protocol

Google 推的 agent 之间沟通协定，类似 MCP 但用于 agent ↔ agent，不是 agent ↔ tool。

---

## 5. Claude Code 生态

### MCP（Model Context Protocol）

Anthropic 推的开放协定，让任何 LLM host（Claude Code、Cursor、自写 agent）都能用同一套接口去呼叫外部 tool server。把它想成「**LLM 的 USB 接口**」。

📍 详细：[Stage 5.2](../stages/05-claude-code-ecosystem.zh-Hans.md#52--mcpmodel-context-protocol-基础)

### Skills / SKILL.md

Claude Code 的「行为包」。一个 Skill 就是一个文件夹含 `SKILL.md`（描述「在什么情境要做什么、可呼叫哪些 tool」），Claude Code 会根据当下情境自动载入合适的 skill。

📍 详细：[Stage 5.3](../stages/05-claude-code-ecosystem.zh-Hans.md#53--skillsclaude-code-的行為層)

### Plugin / Marketplace

把多个 Skills + slash commands + hooks + MCP 设置打包成一个发布单位。**Marketplace** 就是 plugin 的目录，社群可以 `claude plugin install` 安装别人写好的。

📍 详细：[Stage 5.4](../stages/05-claude-code-ecosystem.zh-Hans.md#54--plugins-与-marketplaces)

### Slash Command

Claude Code 内以 `/` 开头的指令（`/help`、`/compact`、`/plan` 等）。可以自定义——把一段 prompt 存到 `.claude/commands/<name>.md` 就变成 `/name`。

### CLAUDE.md

放在 project root 的 markdown 档，Claude Code 每次启动都会读。写 project 级的规则 / 规范 / context（用什么语言、coding style、别动哪些档等）。

### Hooks

在 Claude Code 动作前后执行的 script（pre-tool-use、post-tool-use、user-message-received 等）。可拿来做 git 自动 commit、log 记录、行为拦截等。

### Subagent（子 agent）

主 Claude Code session 之外，spawn 出来跑特定任务的 agent。有自己的 context window。例如「给我一个 code-reviewer subagent 看看 diff」。

---

## 6. Production / Eval / Cost

### Eval（评估框架）

针对 agent 跑一组 test case，量化它的准确度 / latency / cost。**production agent 没有 eval 等于没有测试**。常见工具：promptfoo、LangSmith、langfuse evals。

📍 详细：[Stage 7](../stages/07-multi-agent-production.zh-Hans.md)

### Observability

把 agent 内部跑的每一步（哪个 LLM call、哪个 tool、什么结果）都记下来。出 bug 时能 replay。常见：langfuse、Helicone、weave。

📍 详细：[Stage 7](../stages/07-multi-agent-production.zh-Hans.md)

### Prompt Caching

LLM 把 prompt 前缀 cache 起来，下次同前缀只算 cache hit 的便宜价（Anthropic 90% off、OpenAI 50% off）。Long context + 重复 query 的场景可以省很多钱。

### Token Cost / Inference Cost

每次 LLM 呼叫的成本 = input tokens × input price + output tokens × output price。Agent 跑 ReAct loop 的成本可以累积很快——大 codebase grep 一次可能花 10 万 token。

### Guardrails

防 LLM 做坏事的规则层——挡掉 prompt injection、PII 外流、有害输出等。NeMo Guardrails、Guardrails AI 等。

---

## 7. 用词 / Buzzword

### CLI Agent

跑在终端机的 agent（Claude Code、Codex、Aider、Gemini CLI 等）。对比于跑在 IDE 内（Cursor、Continue）或 web 上（ChatGPT、Claude.ai）。

📍 详细：[Track A A1](../tracks/cli/A1-cli-intro.zh-Hans.md)、[`resources/cli-agents-guide.zh-Hans.md`](cli-agents-guide.zh-Hans.md)

### BYO API Key（Bring Your Own）

工具支援你自己提供 API key 而不是绑订阅。Aider / OpenCode / goose 等 CLI 都是 BYO；Claude Code / Codex 预设是订阅制。

### Local LLM / On-Device

模型跑在你自*己*机器上（Ollama、llama.cpp、MLX、LocalAI 等），数据不外传。隐私 OK 但能力比 frontier 模型有差。

📍 详细：[Stage 1](../stages/01-llm-basics.zh-Hans.md)

### Quantization（量化）

把模型权重从 fp16 压到 int8 / int4，省内存跟速度，代价是准确度小幅降低。Local LLM 用户常碰到（Q4_K_M、Q8_0 等）。

### Hallucination（幻觉）

LLM 「自信地说错」——把不存在的 API 编出来、把错的数字当成事实写。所有 production agent 都要防这个（用 RAG / structured output / eval / guardrails）。

### Frontier Model

当下最顶的模型（GPT-5、Claude Sonnet 4.5、Gemini 2.5 Pro 等）。一般智慧任务用 frontier；简单分类 / 翻译用便宜的小模型省钱。

### Context Engineering

当 prompt 设计一个句子已经 cover 不了，要动态组**system prompt + tool definitions + memory + retrieved chunks + 多轮历史**——整个系统的设计学科。**Prompt engineering 的下一层**。

📍 详细：[Stage 2 结尾](../stages/02-prompt-engineering.md) / [Stage 6](../stages/06-memory-rag.md) / [Stage 7](../stages/07-multi-agent-production.md)
📍 延伸：[`Meirtz/Awesome-Context-Engineering`](https://github.com/Meirtz/Awesome-Context-Engineering)

### Harness Engineering

把 agent 包成 production system 的工具带设计——permissions、tool registry、memory layer、eval、observability、retry / circuit breaker 等。Claude Code、Cursor、OpenCode 等 CLI agent 都是 harness。**framework 把 LLM 包成 agent，harness 把 agent 包成 product**。

📍 详细：[Stage 7](../stages/07-multi-agent-production.md) 必修阅读
📍 延伸：[`ai-boost/awesome-harness-engineering`](https://github.com/ai-boost/awesome-harness-engineering)、[`ZhangHanDong/harness-engineering-from-cc-to-ai-coding`](https://github.com/ZhangHanDong/harness-engineering-from-cc-to-ai-coding)

---

## 找不到的词？

- 看 [Stage 5.2 — MCP](../stages/05-claude-code-ecosystem.zh-Hans.md#52--mcpmodel-context-protocol-基础) / [5.3 — Skills](../stages/05-claude-code-ecosystem.zh-Hans.md#53--skillsclaude-code-的行為層) / [5.4 — Plugins](../stages/05-claude-code-ecosystem.zh-Hans.md#54--plugins-与-marketplaces) 的内文
- 看 [Stage 1](../stages/01-llm-basics.zh-Hans.md) / [Stage 6](../stages/06-memory-rag.zh-Hans.md) / [Stage 7](../stages/07-multi-agent-production.zh-Hans.md) 的延伸阅读清单
- 找不到的词 → 开 issue 或直接 PR 加进这份小词典
