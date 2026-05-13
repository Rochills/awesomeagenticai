# Stage 7 — Multi-Agent · Production

> [繁體中文](./07-multi-agent-production.md) | [简体中文](./07-multi-agent-production.zh-Hans.md) | **English** | [Русский](./07-multi-agent-production.ru.md)


⏱ **Time estimate**: 2-4 weeks (~15-30 hours)

> 💡 Term-dense (multi-agent / handoff / eval / observability / guardrails / …) → see [`resources/glossary.en.md` §4 + §6](../resources/glossary.en.md#4-multi-agent).

The final stage. You're moving from "I can build agents" to "I can run them in production with multiple agents coordinating, evaluation, observability, and deployment."

## 📌 Learning Goals

- Design multi-agent orchestration patterns (debate, planner-executor, peer review)
- Set up evaluation harness for agents
- Add observability (tracing, logging, cost tracking)
- Use Anthropic SDK / OpenAI SDK for production deployment (advanced features: streaming, prompt caching, batching)
- Deploy agents to production (Docker, serverless, monitoring)

## 📚 Required Reading

1. [**Anthropic — Building Effective Agents**](https://www.anthropic.com/engineering/building-effective-agents) — re-read with production lens
2. [**Anthropic — Prompt Caching**](https://www.anthropic.com/news/prompt-caching) — 90% cost reduction technique
3. [**Anthropic — Message Batches API**](https://docs.anthropic.com/en/docs/build-with-claude/batch-processing) — async batch jobs
4. **One eval framework's docs** — promptfoo OR LangSmith OR weave
5. [**ai-boost/awesome-harness-engineering**](https://github.com/ai-boost/awesome-harness-engineering) (* 780+) — agent harness toolkit / patterns / eval / memory / MCP / observability all in one. **Frameworks wrap LLMs into agents; harnesses wrap agents into production systems** — that is exactly what this stage is about.
6. [**ZhangHanDong/harness-engineering-from-cc-to-ai-coding**](https://github.com/ZhangHanDong/harness-engineering-from-cc-to-ai-coding) (* 1.3k+) — harness design lessons from reading Claude Code source (Chinese)

## 🛠 Hands-on Exercises (foundational, illustrative)

### Exercise 1: Multi-Agent debate
Two agents debate a topic (e.g. "Python vs Rust for backend"), a third agent judges. Watch for convergence vs divergence patterns.

### Exercise 2: Eval
Write an eval for one of your earlier agents, run it N times, measure success rate. Replace "I'll just eyeball it."

### Exercise 3: Observability
Connect LangSmith / Helicone / weave to an agent, view the full trace. Understand: "agent debugging without observability = black box."

### Exercise 4: SDK advanced
Use streaming + prompt caching + tool use in one call. Watch how cost drops.

### Exercise 5: Deploy
Package an agent in Docker, deploy to cloud (any provider). Learn to ship a prototype as something others can run.

## 🎯 Curated Projects

### Multi-Agent Orchestration

#### [microsoft/autogen](https://github.com/microsoft/autogen)

Already cited in Stage 4. In production context, AutoGen's GroupChat coordination pattern is a strong reference for multi-agent debate / brainstorming.

---

#### [crewAIInc/crewAI](https://github.com/crewAIInc/crewAI)

Already cited in Stage 4. For role-based multi-agent (e.g., research → writer → reviewer pipelines), CrewAI is the simplest production pattern.

---

#### [langchain-ai/langgraph](https://github.com/langchain-ai/langgraph)

Already cited in Stage 4. For production with audit trails, checkpointing, and human-in-the-loop, LangGraph leads.

---

### Evaluation Frameworks

#### [promptfoo/promptfoo](https://github.com/promptfoo/promptfoo)

| Field | Value |
|---|---|
| Stars | ★ 20k+ |
| License | MIT |
| Recommendation | ⭐⭐⭐⭐⭐ |

**What it teaches**: YAML-based eval harness for prompts and agents. Compare across models, run regression tests in CI.

**Best for**: Standardized eval pipeline. Replaces "I'll just eyeball it."

**Run it**:
```bash
npx promptfoo init
# Edit promptfooconfig.yaml
npx promptfoo eval
```

---

#### [EleutherAI/lm-evaluation-harness](https://github.com/EleutherAI/lm-evaluation-harness)

| Field | Value |
|---|---|
| Stars | ★ 12k+ |
| License | MIT |
| Recommendation | ⭐⭐⭐⭐ |

**What it teaches**: Academic-grade eval framework with hundreds of standardized benchmarks (MMLU, HellaSwag, GSM8K).

**Best for**: When you need to claim "we got X% on benchmark Y." Research-flavored.

---

#### [openai/evals](https://github.com/openai/evals)

| Field | Value |
|---|---|
| Stars | ★ 18k+ |
| Recommendation | ⭐⭐⭐⭐ |

**What it teaches**: OpenAI's eval framework. Custom evals for specific use cases.

**Best for**: When you need OpenAI-specific evals or want to contribute back.

---

### Observability

#### [langfuse/langfuse](https://github.com/langfuse/langfuse)

| Field | Value |
|---|---|
| Stars | ★ 26k+ |
| License | MIT (open source) + paid cloud |
| Recommendation | ⭐⭐⭐⭐⭐ |

**What it teaches**: Open-source LLM observability — traces, sessions, evals, prompt management.

**Best for**: Self-hosted production observability. Strong open-source alternative to LangSmith.

---

#### [LangSmith](https://www.langchain.com/langsmith) (proprietary)

**What it teaches**: LangChain's observability platform. Traces, evals, prompt iteration.

**Best for**: If you're deep in LangChain/LangGraph stack. Hosted-only.

---

#### [Helicone](https://github.com/Helicone/helicone)

| Field | Value |
|---|---|
| Stars | ★ 5k+ |
| License | Apache 2.0 (open source) + paid cloud |
| Recommendation | ⭐⭐⭐⭐ |

**What it teaches**: LLM observability via proxy — drop-in replacement for OpenAI/Anthropic clients, gets you logging + caching.

**Best for**: Quick instrumentation without rewriting code.

---

#### [weave (by Weights & Biases)](https://github.com/wandb/weave)

| Recommendation | ⭐⭐⭐⭐ |
|---|---|

**What it teaches**: Tracing + eval framework from W&B. Integrates with their ML platform.

**Best for**: Teams already on W&B for ML experiment tracking.

---

### Anthropic SDK Advanced

#### [anthropics/anthropic-sdk-python](https://github.com/anthropics/anthropic-sdk-python)

| Recommendation | ⭐⭐⭐⭐⭐ |
|---|---|

**What it teaches**: Official Python SDK (base API layer). Streaming, async, tool use, prompt caching, batches, files API.

**Best for**: Building apps directly on the Claude API when you want raw API control rather than a higher-level agent runtime.

---

#### [anthropics/anthropic-sdk-typescript](https://github.com/anthropics/anthropic-sdk-typescript)

**What it teaches**: TS equivalent of the lower-level Python SDK.

**Best for**: TypeScript / Node / web apps that want the base API layer.

---

#### [anthropics/claude-agent-sdk-python](https://github.com/anthropics/claude-agent-sdk-python) ⭐ agent-specific

| Field | Value |
|---|---|
| Stars | ★ 6k+ |
| License | MIT |
| Recommendation | ⭐⭐⭐⭐⭐ |

**What it teaches**: Anthropic's **agent-specific SDK** (released mid-2025) — distinct from the lower-level `anthropic-sdk-python`. Built-in tool use loop, file access, sandboxed execution, subagent orchestration. Exposes Claude Code's agent capabilities for Python apps to use directly.

**Best for**: Developers building Claude-based agents rather than just calling the API. Saves you from hand-rolling a ReAct loop, managing tool execution, etc.

**Notes**: Shares the same agent runtime as Claude Code; reading this SDK's source is the fastest path to understanding how Claude Code works internally.

---

#### [anthropics/claude-agent-sdk-typescript](https://github.com/anthropics/claude-agent-sdk-typescript)

| Field | Value |
|---|---|
| Stars | ★ 1.4k+ |
| License | NOASSERTION |
| Recommendation | ⭐⭐⭐⭐ |

**What it teaches**: TypeScript version of the Claude Agent SDK.

**Best for**: Developers building Claude agents in Node / web app environments.

---

#### [Anthropic Cookbook — Advanced patterns](https://github.com/anthropics/anthropic-cookbook)

Already cited. Specifically the `prompt_caching.ipynb`, `tool_use/`, and `multimodal/` notebooks teach advanced SDK usage.

---

### Deployment

#### [BentoML/BentoML](https://github.com/bentoml/BentoML)

| Field | Value |
|---|---|
| Stars | ★ 8k+ |
| License | Apache 2.0 |
| Recommendation | ⭐⭐⭐⭐ |

**What it teaches**: Serve any ML/LLM model as a production API. Docker + serving framework.

**Best for**: Wrapping your agent into a deployable service.

---

#### [LangServe](https://github.com/langchain-ai/langserve)

**What it teaches**: Deploy LangChain apps as REST APIs. FastAPI under the hood.

**Best for**: Quick deployment of LangChain-based agents.

---

#### [datawhalechina/self-llm](https://github.com/datawhalechina/self-llm)

| Field | Value |
|---|---|
| Language | 中文 (zh-Hans) |
| Stars | ★ 30k+ |
| License | Apache-2.0 |
| Recommendation | ⭐⭐⭐⭐ |

**What it teaches**: A comprehensive Chinese-language guide for fine-tuning and deploying open-source LLMs in Linux environments. Covers Qwen / Llama / GLM / multimodal models, full-parameter + LoRA + deployment.

**Best for**: Chinese-speaking teams self-hosting open-source LLMs. Comprehensive Chinese-language tutorial covering training, fine-tuning, and deployment.

---

#### [hiyouga/LLaMA-Factory](https://github.com/hiyouga/LLaMA-Factory)

| Field | Value |
|---|---|
| Language | Python |
| Stars | ★ 70k+ |
| License | Apache-2.0 |
| Recommendation | ⭐⭐⭐⭐⭐ |

**What it teaches**: The most widely used LLM fine-tuning framework in the Chinese community — unifies SFT / DPO / PPO / GRPO training across 100+ open-source models (Llama / Qwen / DeepSeek / Yi / Mistral, etc.). Web UI lets you fine-tune without writing code.

**Best for**: Anyone fine-tuning open-source LLMs (not just prompt engineering). More focused on training itself than self-llm's broader scope.

**Notes**: Combined with Stage 1's Ollama / llama.cpp, you get a complete "fine-tune → quantize → local deploy" loop.

---

### [vLLM](https://github.com/vllm-project/vllm)

| Field | Value |
|---|---|
| Stars | ★ 79k+ |
| License | Apache 2.0 |
| Recommendation | ⭐⭐⭐⭐ |

**What it teaches**: High-throughput LLM serving. Run open-source models in production.

**Best for**: Self-hosting open-source LLMs (Llama, Qwen, etc.) instead of paying API.

---

### Multi-Agent Case Studies

#### [geekan/MetaGPT](https://github.com/geekan/MetaGPT)

| Field | Value |
|---|---|
| Stars | ★ 67k+ |
| License | MIT |
| Recommendation | ⭐⭐⭐⭐⭐ |

**What it teaches**: SOP-driven multi-agent software development team — PM / Architect / Engineer roles each producing artifacts (PRD → design → code) and handing off to the next role.

**Best for**: Seeing how the **role-specialization + artifact handoff** pattern is implemented. A different design path from LangGraph's state-machine approach.

**Notes**: Maintained by a Chinese team; the docs site has zh content. Worth comparing against AutoGen's free-form group chat.

---

#### [OpenBMB/ChatDev](https://github.com/OpenBMB/ChatDev)

| Field | Value |
|---|---|
| Language | Python |
| Stars | ★ 33k+ |
| License | Apache-2.0 |
| Recommendation | ⭐⭐⭐⭐ |

**What it teaches**: "Communicative" software development pattern — agents debate at each phase (design / code / test) before advancing. The standard open-source case study for the **agent debate / peer-review pattern**, with an academic paper backing it.

**Best for**: Building workflows where "two agents must challenge each other before producing a conclusion." More focused on the debate mechanism than AutoGen.

**Notes**: Has `README-zh.md`, friendly to Chinese readers.

---

#### [princeton-nlp/SWE-agent](https://github.com/princeton-nlp/SWE-agent)

| Field | Value |
|---|---|
| Language | Python |
| Stars | ★ 19k+ |
| License | MIT |
| Recommendation | ⭐⭐⭐⭐ |

**What it teaches**: **Agent-Computer Interface (ACI)** design — the *shape* of the tool surface (not the prompt) determines agent performance on SWE-Bench. Princeton NLP's research output.

**Best for**: After learning tool use in Stages 3-4, understand "**why tool design matters more than prompt tuning**."

**Notes**: Paper + open-source code — a great reference for academic multi-agent research.

---

## ✅ Self-Check After Stage 7

Can you:
- [ ] Design a multi-agent system with explicit coordination protocol
- [ ] Set up automated eval pipeline running in CI
- [ ] Connect observability (tracing) to a production agent
- [ ] Measure and compare cost before/after prompt caching on a real workload
- [ ] Deploy an agent to a cloud service (any provider)

If yes → you've completed the main path. Choose a [specialized branch](../README.en.md#the-7-stage-learning-map) or contribute to this repo.

## 💡 What's Next

You now have foundational competence. The next 6-12 months should be about:
1. **Pick one production system** to take from prototype → production
2. **Contribute to upstream** (LangGraph, AutoGen, MCP servers, Anthropic cookbook)
3. **Read papers** — agent research is moving fast
4. **Build something visible** — open source a real tool, not another tutorial
