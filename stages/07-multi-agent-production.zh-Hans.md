# Stage 7 — Multi-Agent · Production

> [繁體中文](./07-multi-agent-production.md) | **简体中文** | [English](./07-multi-agent-production.en.md) | [Русский](./07-multi-agent-production.ru.md)

⏱ **时间估算**：2-4 周（约 15-30 小时）

> 💡 用语密度高（multi-agent / handoff / eval / observability / guardrails⋯）→ 翻 [`resources/glossary.zh-Hans.md`](../resources/glossary.zh-Hans.md#4-multi-agent)。

最后一个阶段。你正从“我会做 agent”走向“我能在 production 跑起来，多个 agent 协作、有 eval、有 observability、会 deploy”。

## 📌 学习目标

- 设计 multi-agent orchestration 模式（debate、planner-executor、peer review）
- 为 agent 架一套 evaluation harness
- 加上 observability（tracing、logging、cost tracking）
- 用 Anthropic SDK / OpenAI SDK 做 production deploy（进阶功能：streaming、prompt caching、batching）
- 把 agent deploy 到 production（Docker、serverless、monitoring）

## 📚 必修阅读

1. [**Anthropic — Building Effective Agents**](https://www.anthropic.com/engineering/building-effective-agents) — 用 production 的角度再读一次
2. [**Anthropic — Prompt Caching**](https://www.anthropic.com/news/prompt-caching) — 90% 成本下降的技巧
3. [**Anthropic — Message Batches API**](https://docs.anthropic.com/en/docs/build-with-claude/batch-processing) — 异步 batch job
4. **任一 eval framework 的文件** — promptfoo 或 LangSmith 或 weave
5. [**ai-boost/awesome-harness-engineering**](https://github.com/ai-boost/awesome-harness-engineering)（★ 780+）— agent harness 的工具 / pattern / eval / memory / MCP / observability 全集合。**framework 把 LLM 包成 agent；harness 把 agent 包成 production system**——这个 stage 学的就是 harness。
6. [**ZhangHanDong/harness-engineering-from-cc-to-ai-coding**](https://github.com/ZhangHanDong/harness-engineering-from-cc-to-ai-coding)（★ 1.3k+）— 从 Claude Code 源码学 harness 设计（中文）

## 🛠 动手练习（必跑、不是看就好）

### 练习 1：Multi-Agent 辩论
两个 agent 辩论一个题目（例如“该用 Python 还是 Rust 写 backend”），第三个 agent 当裁判。观察辩论收敛或分歧的 pattern。

### 练习 2：Eval
替你前面的 agent 写一份 eval，跑 N 次量成功率。把“我用眼睛看一下”的习惯换掉。

### 练习 3：Observability
把 LangSmith、Helicone、或 weave 接上一个 agent，看完整 trace。理解“没 observability 的 agent debug = 黑盒”。

### 练习 4：SDK 进阶
在同一次呼叫里用 streaming + prompt caching + tool use。看成本怎么降下来。

### 练习 5：Deploy
把一个 agent 包进 Docker，deploy 到云端（任何 provider 都行）。学会把 prototype 变成可以给别人跑的东西。

## 🎯 精选 Projects

### Multi-Agent Orchestration

#### [microsoft/autogen](https://github.com/microsoft/autogen)

Stage 4 已提过。在 production 场景下，AutoGen 的 GroupChat 协作模式是 multi-agent 辩论 / brainstorming 的好参考。

---

#### [crewAIInc/crewAI](https://github.com/crewAIInc/crewAI)

Stage 4 已提过。要做角色式的 multi-agent（例如 research → writer → reviewer 流水线），CrewAI 是最简单的 production pattern。

---

#### [langchain-ai/langgraph](https://github.com/langchain-ai/langgraph)

Stage 4 已提过。要 production 加上 audit trail、checkpoint、human-in-the-loop，LangGraph 领先。

---

### Evaluation Frameworks

#### [promptfoo/promptfoo](https://github.com/promptfoo/promptfoo)

| 栏位 | 内容 |
|---|---|
| Stars | ★ 20k+ |
| License | MIT |
| 推荐度 | ⭐⭐⭐⭐⭐ |

**教什么**：以 YAML 为基础的 prompt 跟 agent eval harness。可以跨模型比较、在 CI 跑回归测试。

**适合谁**：把 eval 流程标准化。取代“我用眼睛看一下就好”。

**怎么跑**：
```bash
npx promptfoo init
# 编辑 promptfooconfig.yaml
npx promptfoo eval
```

---

#### [EleutherAI/lm-evaluation-harness](https://github.com/EleutherAI/lm-evaluation-harness)

| 栏位 | 内容 |
|---|---|
| Stars | ★ 12k+ |
| License | MIT |
| 推荐度 | ⭐⭐⭐⭐ |

**教什么**：学术等级的 eval framework，内置几百个标准 benchmark（MMLU、HellaSwag、GSM8K）。

**适合谁**：你需要主张“我们在 benchmark Y 上拿到 X%”的时候。比较研究风格。

---

#### [openai/evals](https://github.com/openai/evals)

| 栏位 | 内容 |
|---|---|
| Stars | ★ 18k+ |
| 推荐度 | ⭐⭐⭐⭐ |

**教什么**：OpenAI 的 eval framework。可以针对特定 use case 写客制 eval。

**适合谁**：你需要 OpenAI 专属 eval、或想回馈上游时。

---

### Observability

#### [langfuse/langfuse](https://github.com/langfuse/langfuse)

| 栏位 | 内容 |
|---|---|
| Stars | ★ 26k+ |
| License | MIT（开源）+ 付费云端 |
| 推荐度 | ⭐⭐⭐⭐⭐ |

**教什么**：开源的 LLM observability——traces、sessions、evals、prompt management。

**适合谁**：自架的 production observability。LangSmith 的开源替代方案，实力很强。

---

#### [LangSmith](https://www.langchain.com/langsmith)（商业）

**教什么**：LangChain 的 observability 平台。Trace、eval、prompt 迭代。

**适合谁**：整套 stack 都在 LangChain / LangGraph 上面。只有 hosted 版。

---

#### [Helicone](https://github.com/Helicone/helicone)

| 栏位 | 内容 |
|---|---|
| Stars | ★ 5k+ |
| License | Apache 2.0（开源）+ 付费云端 |
| 推荐度 | ⭐⭐⭐⭐ |

**教什么**：用 proxy 做 LLM observability——当作 OpenAI/Anthropic client 的替身，顺便拿到 logging + caching。

**适合谁**：不想改程式、想快速上 instrumentation 时。

---

#### [weave（Weights & Biases 出品）](https://github.com/wandb/weave)

| 栏位 | 内容 |
|---|---|
| 推荐度 | ⭐⭐⭐⭐ |

**教什么**：W&B 出的 tracing + eval framework。跟他们的 ML 平台集成。

**适合谁**：团队已经在用 W&B 做 ML 实验追踪。

---

### Anthropic SDK 进阶

#### [anthropics/anthropic-sdk-python](https://github.com/anthropics/anthropic-sdk-python)

| 栏位 | 内容 |
|---|---|
| 推荐度 | ⭐⭐⭐⭐⭐ |

**教什么**：官方 Python SDK（基础 API 层）。streaming、async、tool use、prompt caching、batches、files API。

**适合谁**：直接基于 Claude API 做应用。

---

#### [anthropics/anthropic-sdk-typescript](https://github.com/anthropics/anthropic-sdk-typescript)

**教什么**：Python SDK 的 TS 版本。

**适合谁**：TypeScript / Node / web app。

---

#### [anthropics/claude-agent-sdk-python](https://github.com/anthropics/claude-agent-sdk-python) ⭐ agent 专用

| 栏位 | 内容 |
|---|---|
| Stars | ★ 6k+ |
| License | MIT |
| 推荐度 | ⭐⭐⭐⭐⭐ |

**教什么**：Anthropic 在 2025 年中释出的 **agent 专用 SDK**，跟基础 `anthropic-sdk-python` 不同——这个内置 tool use loop、file access、sandbox 执行、subagent 编排，把 Claude Code 用的 agent capabilities 开放给 Python 应用直接用。

**适合谁**：要打造 Claude-based agent 而不是只呼叫 API 的开发者。比起手刻 ReAct loop、自己管 tool execution，这个 SDK 把这些抽象都做好了。

**备注**：跟 Claude Code 共用同一套 agent runtime；想理解 Claude Code 内部怎么运作的，读这个 SDK 的源码是最快的路径。

---

#### [anthropics/claude-agent-sdk-typescript](https://github.com/anthropics/claude-agent-sdk-typescript)

| 栏位 | 内容 |
|---|---|
| Stars | ★ 1.4k+ |
| License | NOASSERTION |
| 推荐度 | ⭐⭐⭐⭐ |

**教什么**：Claude Agent SDK 的 TypeScript 版。

**适合谁**：要在 Node / web app 环境打造 Claude agent 的开发者。

---

#### [Anthropic Cookbook — Advanced patterns](https://github.com/anthropics/anthropic-cookbook)

之前已提过。特别是 `prompt_caching.ipynb`、`tool_use/`、`multimodal/` 三个 notebook，教进阶 SDK 用法。

---

### Deployment

#### [BentoML/BentoML](https://github.com/bentoml/BentoML)

| 栏位 | 内容 |
|---|---|
| Stars | ★ 8k+ |
| License | Apache 2.0 |
| 推荐度 | ⭐⭐⭐⭐ |

**教什么**：把任何 ML/LLM model 包成 production API。Docker + serving framework。

**适合谁**：把 agent 包成可 deploy 的 service。

---

#### [LangServe](https://github.com/langchain-ai/langserve)

**教什么**：把 LangChain app deploy 成 REST API。底层用 FastAPI。

**适合谁**：以 LangChain 为基础的 agent 想快速 deploy。

---

#### [datawhalechina/self-llm](https://github.com/datawhalechina/self-llm)

| 栏位 | 内容 |
|---|---|
| 语言 | 中文（zh-Hans） |
| Stars | ★ 30k+ |
| License | Apache-2.0 |
| 推荐度 | ⭐⭐⭐⭐ |

**教什么**：开源大模型食用指南——一份完整的中文指南，讲怎么在 Linux 上 fine-tune 跟 deploy 开源 LLM。涵盖 Qwen / Llama / GLM / 多模态模型，全参数 + LoRA + deployment 都有。

**适合谁**：要自架开源 LLM 的中文团队。training-to-deployment 整个流程的 production 等级中文教学。

---

#### [hiyouga/LLaMA-Factory](https://github.com/hiyouga/LLaMA-Factory)

| 栏位 | 内容 |
|---|---|
| 语言 | Python |
| Stars | ★ 70k+ |
| License | Apache-2.0 |
| 推荐度 | ⭐⭐⭐⭐⭐ |

**教什么**：中文社群最广泛使用的 LLM fine-tuning framework——统一 100+ 个开源模型（Llama / Qwen / DeepSeek / Yi / Mistral 等）的 SFT、DPO、PPO、GRPO 训练流程。Web UI 可以零代码跑 fine-tuning。

**适合谁**：要 fine-tune 开源 LLM（不只是 prompt-engineering）的人。比 self-llm 范围更聚焦在“训练”本身。

**备注**：搭配前面 Stage 1 的 Ollama / llama.cpp，能完整跑“fine-tune → quantize → 本地 deploy”的闭环。

---

### [vLLM](https://github.com/vllm-project/vllm)

| 栏位 | 内容 |
|---|---|
| Stars | ★ 79k+ |
| License | Apache 2.0 |
| 推荐度 | ⭐⭐⭐⭐ |

**教什么**：高吞吐量的 LLM serving。可以在 production 跑开源模型。

**适合谁**：自架开源 LLM（Llama、Qwen 等等）取代付费 API 的场景。

---

### Multi-Agent 案例研究

#### [geekan/MetaGPT](https://github.com/geekan/MetaGPT)

| 栏位 | 内容 |
|---|---|
| Stars | ★ 67k+ |
| License | MIT |
| 推荐度 | ⭐⭐⭐⭐⭐ |

**教什么**：以 SOP（Standard Operating Procedure）为核心的多 agent 软件开发 team——PM / Architect / Engineer 各自有角色，从 PRD → 设计 → 代码一路产出 artifact 交接给下一棒。

**适合谁**：想看“**角色分工 + artifact 交接**”这种 pattern 怎么实作的人。跟 LangGraph 的 state machine 路线不同，是另一条 multi-agent 设计思路。

**备注**：中文团队维护，docs site 有 zh 内容。值得拿来跟 AutoGen 的 free-form group chat 对比。

---

#### [OpenBMB/ChatDev](https://github.com/OpenBMB/ChatDev)

| 栏位 | 内容 |
|---|---|
| 语言 | Python |
| Stars | ★ 33k+ |
| License | Apache-2.0 |
| 推荐度 | ⭐⭐⭐⭐ |

**教什么**：“对话式”软件开发 pattern——agents 在 design / code / test 各阶段互相辩论才推进。这是 **agent debate / peer-review pattern** 最标准的开源案例，背后有论文。

**适合谁**：要打造“两个 agent 互相挑战才产出结论”这种 workflow 的人。比 AutoGen 更聚焦在 debate 机制。

**备注**：有 `README-zh.md`，中文读者友善。

---

#### [princeton-nlp/SWE-agent](https://github.com/princeton-nlp/SWE-agent)

| 栏位 | 内容 |
|---|---|
| 语言 | Python |
| Stars | ★ 19k+ |
| License | MIT |
| 推荐度 | ⭐⭐⭐⭐ |

**教什么**：**Agent-Computer Interface (ACI)** 的设计思路——tool 介面的形状（不是 prompt）决定 agent 在 SWE-Bench 上的成绩。Princeton NLP 的论文成果。

**适合谁**：在 Stage 3-4 学完 tool use 之后，想理解“**为什么 tool 设计比 prompt tuning 重要**”的人。

**备注**：论文 + 实作开源，是学术 multi-agent 研究的好参考。

---

## ✅ Stage 7 之后的自我检查

你能不能：
- [ ] 设计一个 multi-agent 系统，协作协定讲得清楚
- [ ] 在 CI 跑自动 eval pipeline
- [ ] 把 observability（tracing）接到 production agent
- [ ] 在真实 workload 上量测 prompt caching 前后的成本差异
- [ ] 把 agent deploy 到云端（任何 provider）

如果都可以 → 你已经跑完主路线。挑一个[特化分支](../README.zh-Hans.md#️-7-阶段学习地图)，或回头来贡献这份 repo。

## 💡 接下来

你已经有基础能力了。接下来 6-12 个月应该专注在：
1. **挑一个 production 系统** 从 prototype 推到 production
2. **回馈上游**（LangGraph、AutoGen、MCP servers、Anthropic cookbook）
3. **读论文**——agent 研究进展很快
4. **做出看得到的东西**——开源一个真的工具，不要再写教学了
