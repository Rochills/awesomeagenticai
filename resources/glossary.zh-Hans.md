# 术语小词典（Glossary）

> [繁體中文](./glossary.md) | **简体中文** | [English](./glossary.en.md)

> 本路线图会大量出现“LLM”、“RAG”、“MCP”、“agent”这类词。读到不懂的词先在这里查 30 秒，再回去读 stage 内容。
>
> 每个词**只给最小可用的解释**（30-80 字 + 在哪一个 stage 讲细的）——不是维基百科。

## 🌐 统一词汇对照表（中英对照、跨 stage 一致）

本表是项目内**强制统一的命名约定**——所有 stage 用同一个中文理解名。如果你在 stage 内看到不一致，请报 issue。

| 英文术语 | 中文理解名 | 主要 stage |
|---|---|---|
| Prompt Engineering | Prompt 设计 | Stage 2 |
| Context Engineering | 上下文管理 | Stage 6 |
| Harness Engineering | Agent 执行系统设计 | Stage 7 |
| Tool Use | 工具使用 | Stage 3 |
| Function Calling | 函数 / 工具调用 | Stage 3 |
| Structured Output | 结构化输出 | Stage 3 |
| Agent Loop | Agent 执行循环 | Stage 3 |
| Framework | 框架 | Stage 4 |
| Orchestration | 协调与编排 | Stage 4 / 7 |
| Handoff | 任务交接 | Stage 7 |
| Supervisor / Worker | 协调者 / 执行者 | Stage 7 |
| Runtime | 执行层 | Stage 7 |
| Scaffolding | 支撑架构 | Stage 7 |
| Observability | 观测与记录 | Stage 7 |
| Telemetry | 运行记录 | Stage 7 |
| Eval | 效果评估 | Stage 7 |
| Evaluation Harness | 评估框架 | Stage 7 |
| Production | 可稳定使用 / 上线化 | Stage 7 |
| Production-grade | 可长期稳定使用的 | Stage 7 |
| Deployment | 部署 | Stage 7 |
| Cost Tracking | 成本追踪 | Stage 7 |
| Latency | 延迟 / 等待时间 | Stage 7 |
| Vector DB | 向量数据库 | Stage 6 |
| Retrieval | 检索 | Stage 6 |
| Reranking | 重排序 | Stage 6 |
| Long Context | 长上下文 | Stage 6 |
| Fine-tuning | 模型微调 | Stage 6 |
| Agent Interfaces | Agent 操作界面 | Stage 8 |
| Code Sandbox | 隔离程序执行环境 | Stage 8 |
| Cold Start | 启动延迟 | Stage 8 |
| Reward Hacking | 钻评分漏洞 | Stage 7 / 8 |

→ 详细定义请看下面各区块。

---

## 1. 基本概念

### LLM（Large Language Model，大语言模型）

GPT、Claude、Gemini 这类“给文字、回文字”的模型。本身是纯函数：input prompt → output text。它**不会自己上网、不会记住上次对话**——这些都要外接系统来做。

📍 详细：[Stage 1](../stages/01-llm-basics.zh-Hans.md)

### Token

LLM 看到的不是“字”，是 **token**（次字单位）。中文 1 个字 ≈ 1.5-2 token，英文 1 个 word ≈ 1.3 token。LLM 计费跟 context window 都以 token 计。“100 万 token context”≈ 75 万中文字。

📍 详细：[Stage 1](../stages/01-llm-basics.zh-Hans.md)

### Context Window（上下文视窗）

LLM 一次能“看”多少 token。**2026 frontier**：Claude Sonnet 4.6 / Opus 4.7 1M、GPT-5.5 ~400k、Gemini 3.1 Pro 2M。**不是越大越好**——超过某个长度后 LLM 会“在中间遗漏”（Lost in the Middle）。

### Prompt（提示词）

你给 LLM 的输入文字。**Prompt engineering** 就是设计这段输入让 LLM 给好答案。System prompt（角色设定）+ user prompt（这次的问题）是基本结构。

📍 详细：[Stage 2](../stages/02-prompt-engineering.zh-Hans.md)

### Few-shot / Zero-shot

- **Zero-shot**：直接问问题不给范例。
- **Few-shot**：给 2-5 个 input → output 的范例后再问。**Few-shot 通常显著提升准确度**，特别是格式要求严的任务。

### Chain-of-Thought（CoT，思维链）

要 LLM“先想再答”——让它先输出推理过程，再给结论。**常见有两种形式**：

- **Few-shot CoT**（原始 paper、[Wei et al. 2022](https://arxiv.org/abs/2201.11903)）：在 prompt 里放几个带推理步骤的例子，让 LLM 模仿着想
- **Zero-shot CoT**（[Kojima et al. 2022](https://arxiv.org/abs/2205.11916)）：在 prompt 结尾加上“Let's think step by step”来触发 reasoning trace

**准确度通常会提升**，代价是 token 数变多。Few-shot 通常比 zero-shot 更准。

---

## 2. Agent / 工具使用

### Agent（代理人）

以 LLM 为核心、能在**循环**中**感知状态 → 做决策 → 采取行动 → 观察结果**、重复直到完成目标的系统。**核心三要素**：

- **LLM**（推理 / 规划 / decide）
- **Actions**（做事的手段——不限于 function call。可以是写代码执行（CodeAct）、操作浏览器（computer use）、查 KB（RAG retrieval）、call MCP server、纯规划拆任务等）
- **Loop**（心跳——agent 跟纯 LLM Q&A 的根本差别）

差别在于：纯 LLM = Q&A；agent = 三要素 + 持续循环，直到目标达成或预算耗尽。**ReAct 是其中一种 agent pattern，不是 agent 的定义**——CodeAct、computer-use、planning agent 都是 agent。

📍 详细：[Stage 3](../stages/03-tool-use-and-hello-agent.zh-Hans.md)

### Tool Use / Function Calling

让 LLM 调用你定义好的 function（查 DB、算数学、开浏览器…）。LLM 回的不是文字而是 `{"function": "search", "args": {...}}`，你的程序去执行、把结果再丢回 LLM。

**两个词概念相同，但 API schema 不一样**：
- **Anthropic 的 "Tool Use"**：schema 用 `input_schema`（直接放 JSON Schema）
- **OpenAI / Ollama 的 "Function Calling"**：外面再包一层 `{"type": "function", "function": {...}}`
- LLM 内部接收到的 token 表达也不同，写跨厂商 SDK 时要记得对应好

📍 详细：[Stage 3](../stages/03-tool-use-and-hello-agent.zh-Hans.md)
📍 schema 怎么写好：[Function Schema 设计 cheatsheet](schema-design-cheatsheet.zh-Hans.md)

### ReAct（Reasoning + Acting）

最经典的 agent pattern：**Thought（想）→ Action（叫工具）→ Observation（看结果）→ Thought ...** 一直 loop 到答得出来。多数 agent framework 内部都实作这个。

📍 详细：[Stage 3](../stages/03-tool-use-and-hello-agent.zh-Hans.md)

### Structured Output（结构化输出）

要 LLM 输出 **JSON / 其他固定 schema**，而不是自由文字。各家 LLM API 都有 `response_format` 或类似旗标支持。Agent 框架几乎都靠这个跟 LLM 沟通。

### Agent Loop

“LLM → tool → 结果 → LLM”这个重复的循环。Loop 结束条件可能是：LLM 说“I'm done”、跑超过 N 步、超出 budget。

### Self-Refine（基础版反思 / 无记忆）

agent 自我评估上一轮输出、修改下一轮的做法——“Actor 出答案 → Critic 找问题 → Actor 看 feedback 再答”的 single-session loop。**不需要持久记忆层**，本质上就是 reasoning loop 机制，是 ReAct 的 sibling pattern。production agent（Cursor / Cline / Claude Code）每天都在跑这种变体。

代表 paper：[Self-Refine (Madaan 2023)](https://arxiv.org/abs/2303.17651)。**完整版 Reflexion**（含 episodic memory）见 3 Memory / Retrieval / RAG（这是不同层的东西）。

📍 详细 + 路由：[Stage 3 反思](../stages/03-tool-use-and-hello-agent.zh-Hans.md#-反思reflexion--self-refine-概念--路由)

---

## 3. Memory / Retrieval / RAG

### Memory（记忆）— 两种正交分类轴

“memory”常被混在一起讲，其实有 **2 种正交分类轴**：

- **时效轴**：short-term（当前对话）vs long-term（跨 session 持久）
- **内容轴**（CoALA framework）：**Working**（暂存）/ **Episodic**（过去经历）/ **Semantic**（事实知识）/ **Procedural**（怎么做）

→ 两条轴并不冲突：long-term memory 里可以**同时**有 episodic（user 上次说了什么）+ semantic（公司知识库事实）+ procedural（用过的 tool sequence）。

📍 详细：[Stage 6 Memory 是什么 + 如何设计](../stages/06-memory-rag.zh-Hans.md#-memory-是什么--怎么设计) + [Stage 6 CoALA Framework](../stages/06-memory-rag.zh-Hans.md#进阶coala-framework--agent-memory-的-4-层分类法)

### RAG（Retrieval-Augmented Generation）

两阶段架构模式：

1. **Ingest**（一次性 / 定期）：document → chunk → embed → 存进 vector store（建一个可检索的 KB）
2. **Query**（每次 user 提问）：question embed → semantic search（或 hybrid + BM25）→ top-K chunks → 塞进 prompt → LLM 回答

**解决的是 LLM 不知道你的私有 / 变动 / 过期资料**。Retrieval **不只限于 dense embedding**——production 默认配置通常是 hybrid（dense + BM25）+ reranker。

📍 详细：[Stage 6](../stages/06-memory-rag.zh-Hans.md)
📍 paper：[Lewis et al. 2020](https://arxiv.org/abs/2005.11401)

### Reflexion（完整版反思 / 带 episodic memory）

跟 Self-Refine（2 Agent）不同：Reflexion **需要持久 episodic memory store**——agent 跑完一次 trial 后，会**写一段 reflection summary 进 memory**，下一次 trial 开始时再检索进 prompt。**跨 trial 累积教训**才是 Reflexion 的本质（不是 single-session loop）。

放在 3 而不是 2 Agent，是因为它**本质上是 memory pattern**——episodic memory store 是核心，不是 optional。

代表 paper：[Reflexion (Shinn 2023)](https://arxiv.org/abs/2303.11366)。

📍 详细：[Stage 6 进阶：带持久记忆的 Reflexion 完整版](../stages/06-memory-rag.zh-Hans.md#-进阶带持久记忆的-reflexion-完整版--track-b-选读)

### Embedding（嵌入）

把文字 / 图片转成 N 维**向量**，让“意思接近”的东西距离更近。本路线图默认指 **dense embedding**（稠密向量，由 sentence-transformers / OpenAI ada-002 等产生）；另外也有 **sparse embedding**（BM25 / SPLADE 等，按字面 token 匹配）——production RAG 往往两者一起用来做 hybrid search。

📍 详细：[Stage 6](../stages/06-memory-rag.zh-Hans.md)

### Vector DB（向量数据库）

存储 + 高效查询 embedding 的存储层。**主要查询类型 = approximate nearest-neighbor (ANN)**——Vector DB 存在的意义就是 ANN 比直接做 cosine 全扫快几百倍。代表：Pinecone / Chroma / Qdrant / Weaviate / pgvector。

📍 详细：[Stage 6](../stages/06-memory-rag.zh-Hans.md)

### Semantic Search（语义搜索）

用 embedding 比较“意思相似”而不是“字符串完全相同”。“电动车怎么充电”可以捞到“EV charging tutorial”。传统关键字搜索（BM25 等）做不到这个。

### Chunking（切块）

把长文件切成适合 embedding 的小段（通常 200-1000 token）。**切法直接影响 RAG 质量**——切太碎丢脉络、切太长相关度模糊。常见策略：固定大小、按段落、按结构（heading）。

### Hybrid Search（混合搜索）

语义搜索 + 关键字搜索一起用，再 merge 排序。多半比单一方法准。production-grade RAG 标配。

### Reranking（重新排序）

第一轮 retrieval 捞 top-50，再用更贵但更准的模型（cross-encoder）重排成 top-5 给 LLM。Cohere Rerank、bge-reranker 等。

### Contextual Retrieval

Anthropic 2024 提的方法——chunk 加上“整份文件的脉络摘要”一起 embed，避免“这 chunk 拿出来看不知道是哪份文件讲的”问题。

📍 详细：[Stage 6](../stages/06-memory-rag.zh-Hans.md)

### Fine-tuning（模型微调）

拿你自己的资料**再训练**模型、把知识或行为“烧进”权重里（跟 RAG 不同——RAG 是 inference 时才把资料塞进 context、不改权重）。适合让模型稳定学会某种**格式 / 风格 / 领域用语**；**不适合**拿来塞“最新事实”（那是 RAG 的活，fine-tune 进去的事实会过期又难更新）。多数 agent 场景**先试 prompt + RAG**，真的不够才考虑 fine-tune。

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

一个 agent 把任务交给另一个 agent。比直接 function call 多了“context 怎么传”、“失败谁处理”的问题。

### A2A（Agent-to-Agent）Protocol

Google 推的 agent 之间沟通协定，类似 MCP 但用于 agent ↔ agent，不是 agent ↔ tool。

---

## 5. Claude Code 生态

### MCP（Model Context Protocol）

Anthropic 在 2024 推出的开放协定，让任何 LLM host（Claude Code、Cursor、自写 agent）都能用同一套接口连接外部 tool server。把它想成“**LLM 的 USB 接口**”。

**技术上标准化了 3 种 primitives**：
- **Tools**：LLM 可调用的 function（read DB / search web / send email…）
- **Resources**：LLM 可读取的数据（文件内容、API response、DB rows…）
- **Prompts**：可复用的 prompt 模板（给用户在 host 内用 `/` 触发）

**架构**：server / client 模式——tool server 跑在本地或远端，LLM host 当 client 连接。Server 通过 stdio / SSE / HTTP 三种 transport 之一暴露这些 primitives。

📍 详细：[Stage 5.2](../stages/05-claude-code-ecosystem.zh-Hans.md#52--mcpmodel-context-protocol-基础)

### Skills / SKILL.md

Claude Code 的“行为包”。一个 Skill = 一个文件夹，里面有 `SKILL.md`（描述“在什么情境要做什么、可调用哪些 tool”）+ 可选的 reference files / scripts。

**触发机制**（很多人不知道，但很关键）：Claude Code 每次处理你消息**前**，都会扫描所有可用 skill 的 **frontmatter `description` 字段**——如果匹配当前情境，就会自动载入对应的 SKILL.md。**所以 description 写得好不好，直接决定 skill 会不会被触发。** 实务上以 “Use when ...” 开头最有效。

📍 详细：[Stage 5.3](../stages/05-claude-code-ecosystem.zh-Hans.md#53--skillsclaude-code-的行为层-claude-code-生态最关键的一层)

### Plugin / Marketplace

把多个 Skills + slash commands + hooks + MCP 设置打包成一个发布单位。**Marketplace** 就是 plugin 的目录，社群可以 `claude plugin install` 安装别人写好的。

📍 详细：[Stage 5.4](../stages/05-claude-code-ecosystem.zh-Hans.md#54--plugins-与-marketplaces)

### Slash Command

Claude Code 内以 `/` 开头的指令（`/help`、`/compact`、`/plan` 等）。可以自定义——把一段 prompt 存到 `.claude/commands/<name>.md` 就变成 `/name`。

### CLAUDE.md

放在 project root 的 markdown 档，Claude Code 每次启动都会读。写 project 级的规则 / 规范 / context（用什么语言、coding style、别动哪些档等）。

### Hooks

在 Claude Code 特定事件前后执行的 script。**官方支持 7 种事件类型**：

| Hook | 触发时机 | 典型用途 |
|---|---|---|
| `PreToolUse` | 工具调用**前** | 拦截危险操作（`rm -rf`、destructive op）、改参数 |
| `PostToolUse` | 工具调用**后** | 记 log、自动格式化刚写好的文件 |
| `UserPromptSubmit` | user 提交消息时 | 加 context（git status / 当前时间） |
| `Notification` | Claude Code 发通知时 | 桌面 toast / Slack ping |
| `Stop` | session 结束时 | 自动 commit / 清理 |
| `PreCompact` | 自动 compact 前 | 把重要决定提升到 memory |
| `PostCompact` | compact 后 | 确认哪些 context 被压缩 |

写法：在 `.claude/settings.json` 里加 `"hooks"` 区块，指向 script 路径。

### Subagent（子 agent）

主 Claude Code session 之外，spawn 出来跑特定任务的 agent。有自己的 context window。例如“给我一个 code-reviewer subagent 看看 diff”。

写法：在 `.claude/agents/<name>.md` 放 frontmatter + system prompt + tool whitelist。主 session 用 Task tool invoke（自动 parallel / sequential）。**跟 framework-based multi-agent 对照**：subagent 不需要装 LangGraph / CrewAI 等 framework，直接写 markdown 即可；但绑定 Claude Code runtime。完整教学见 [Stage 5.5](../stages/05-claude-code-ecosystem.zh-Hans.md#55--subagentsclaude-code-原生-multi-agent-机制-2025-新功能)；**15 个复制粘贴即用的 dispatch recipe** → [`subagent-cookbook.zh-Hans.md`](./subagent-cookbook.zh-Hans.md)。

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

每次 LLM 调用的成本 = input tokens × input price + output tokens × output price。Agent 跑 ReAct loop 的成本可以累积很快——大 codebase grep 一次可能花 10 万 token。

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

LLM “自信地说错”——把不存在的 API 编出来、把错的数字当成事实写。所有 production agent 都要防这个（用 RAG / structured output / eval / guardrails）。

### Frontier Model

当下最顶的模型（GPT-5、Claude Sonnet 4.5、Gemini 2.5 Pro 等）。一般智慧任务用 frontier；简单分类 / 翻译用便宜的小模型省钱。

### Context Engineering

工程 **每次 LLM call 时，context window 里装什么信息** 的学科——动态把 RAG retrieve 结果、memory、tool definitions、对话 history 组装成模型看得到的 context。Karpathy 2025：把 **刚好对下一步有用的信息** 填进窗口的精细艺术。重点是 *what goes in the window*，不是“跨了几次 call”。**Prompt engineering 的下一层**——前者工程 **字符串**，后者工程 **信息**。

📍 详细：[Stage 2 结尾](../stages/02-prompt-engineering.zh-Hans.md) / [Stage 6](../stages/06-memory-rag.zh-Hans.md) / [Stage 7](../stages/07-multi-agent-production.zh-Hans.md)
📍 延伸：[`Meirtz/Awesome-Context-Engineering`](https://github.com/Meirtz/Awesome-Context-Engineering)

### Harness Engineering

工程 **模型外面的执行与控制层**——所有不是 model weights、也不是 prompt string 本身的工程元件：agent loop / tool registry / context manager / permissions / safety layer / memory layer / eval / observability / retry / circuit breaker 等。Simon Willison 2025：**coding agent = LLM + harness**。Addy Osmani：harness = 所有不是 model 本身的代码。[OpenAI 也在 2026-02 使用了 "Harness Engineering" 这个说法](https://openai.com/index/harness-engineering)。Claude Code、Cursor、OpenCode 等 CLI agent 都是 harness。**framework 把 LLM 包成 agent，harness 把 agent 包成可上线使用的产品**。

对比：
- **Framework**（Stage 4）规范 **API**：你调用的接口长什么样
- **Harness**（本词）规范 **runtime**：怎么跑、怎么 recovery、怎么观测

📍 学科级概念（**8 个核心元件** / prompt→context→harness 三层工程分工 / framework vs harness）：[Stage 7 Harness Engineering](../stages/07-multi-agent-production.zh-Hans.md)
📍 Reference implementation case study（读 Claude Code source）：[Stage 5 5.6](../stages/05-claude-code-ecosystem.zh-Hans.md)
📍 延伸：[`anthropics/claude-agent-sdk-python`](https://github.com/anthropics/claude-agent-sdk-python)、[`ai-boost/awesome-harness-engineering`](https://github.com/ai-boost/awesome-harness-engineering)、[`ZhangHanDong/harness-engineering-from-cc-to-ai-coding`](https://github.com/ZhangHanDong/harness-engineering-from-cc-to-ai-coding)

---

## 8. Agent Interfaces

### Computer Use（屏幕级 agent）

Agent 通过 **screenshot → vision → 算坐标 → 模拟键鼠** 操作真实桌面 app——不靠 API、直接像人类用屏幕。代表：Anthropic Claude Computer Use（Opus 4.7 / Sonnet 4.6）/ OpenAI Codex desktop / Google Gemini in Chrome。**2024-10 Anthropic 公开 beta 开启、2026 OSWorld 达 76.26% superhuman**。

📍 完整解说 + 4 强对比：[Stage 8 Computer Use](../stages/08-agent-interfaces.zh-Hans.md)

### Browser Use（web 级 agent）

Agent 操作网页、主要用 **DOM-aware navigation**（直接 query CSS selector）+ 必要时 vision fallback。代表闭源：Atlas / Comet / Dia / Gemini in Chrome。代表 OSS：[browser-use](https://github.com/browser-use/browser-use)（★ 95k+）。

📍 完整解说 + 5 强对比 + OSS 框架：[Stage 8 Browser Use](../stages/08-agent-interfaces.zh-Hans.md)

### Sandbox（程序代码隔离环境）

让 agent 写的 code 在隔离环境跑、不在 host 机器——避免 agent `rm -rf /` / 连 internet 泄资料 / 偷 credentials 等灾难。代表：E2B（Firecracker microVM）/ Daytona（Container）/ Modal（GPU sandbox）/ Vercel / Cloudflare。**OpenAI Agents SDK 2026-04 内建支持这些 provider**。

📍 完整 9-row 术语小词典（含 microVM / Container 差异）+ 7 强对比：[Stage 8 Code Sandbox](../stages/08-agent-interfaces.zh-Hans.md)

### microVM（micro Virtual Machine）

VM 的精简版、极小 footprint、启动 < 100ms 但仍**独立 kernel**——介于 Docker container（快 + 弱隔离）跟 full VM（慢 + 强隔离）之间。**Agent sandbox 多半选 microVM**。代表实现：[Firecracker](#firecracker)（AWS、E2B 用）。

📍 完整对比：[Stage 8 术语小词典](../stages/08-agent-interfaces.zh-Hans.md)

### Firecracker

AWS 开源的 microVM、Rust 写、**AWS Lambda 底层** + E2B sandbox 用它做 isolation。强隔离 + 快启动兼顾。

📍 [Stage 8 术语小词典](../stages/08-agent-interfaces.zh-Hans.md)

### gVisor

Google 写的“用户空间 kernel”、拦截 syscall 自己模拟、**不用 hypervisor**——介于 container 跟 VM。

📍 [Stage 8 术语小词典](../stages/08-agent-interfaces.zh-Hans.md)

---

## 找不到的词？

- 看 [Stage 5.2 — MCP](../stages/05-claude-code-ecosystem.zh-Hans.md#52--mcpmodel-context-protocol-基础) / [5.3 — Skills](../stages/05-claude-code-ecosystem.zh-Hans.md#53--skillsclaude-code-的行为层-claude-code-生态最关键的一层) / [5.4 — Plugins](../stages/05-claude-code-ecosystem.zh-Hans.md#54--plugins-与-marketplaces) 的内文
- 看 [Stage 1](../stages/01-llm-basics.zh-Hans.md) / [Stage 6](../stages/06-memory-rag.zh-Hans.md) / [Stage 7](../stages/07-multi-agent-production.zh-Hans.md) / [Stage 8](../stages/08-agent-interfaces.zh-Hans.md) 的延伸阅读清单
- 找不到的词 → 开 issue 或直接 PR 加进这份小词典
