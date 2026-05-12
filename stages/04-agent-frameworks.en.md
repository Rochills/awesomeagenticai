# Stage 4 — Agent Frameworks

> [繁體中文](./04-agent-frameworks.md) | [简体中文](./04-agent-frameworks.zh-Hans.md) | **English** | [Русский](./04-agent-frameworks.ru.md)


⏱ **Time estimate**: 2-3 weeks (~10-15 hours)

> 💡 Term-unfamiliar? (framework / supervisor / worker / handoff / …) → [`resources/glossary.en.md`](../resources/glossary.en.md).

You've built a ReAct agent from scratch (Stage 3). Now learn what frameworks do for you. **Pick one to deeply learn**, browse the others to know when to switch.

## 📌 Learning Goals

After this stage you will be able to:
- Compare 5 major agent frameworks (LangGraph, AutoGen, CrewAI, Smolagents, OpenAI Agents SDK)
- Pick the right framework for a given task
- Build the same agent in 2 frameworks and feel the difference
- Recognize when to drop frameworks and write from scratch

## 🚪 Entry Conditions

You should already:
- Have completed all 5 hello-X projects in Stage 3
- Have built ReAct from scratch (Exercise 3)
- Be comfortable with async Python (frameworks lean on async)

⚠️ **Memory primer (peek ahead if needed)**: Some framework features rely on memory concepts — LangGraph uses checkpointing (state persistence), CrewAI passes task results between agents (lightweight memory). [Stage 6 — Memory & RAG](06-memory-rag.md) covers these properly. You don't need to read it first, but if a framework feature feels mysterious, that's where the answer is.

## 📚 Required Reading

1. [**Anthropic — Building Effective Agents**](https://www.anthropic.com/engineering/building-effective-agents) — when to use frameworks vs raw API
2. [**LangChain — Conceptual Guide: Agents**](https://python.langchain.com/docs/concepts/agents/) — agent abstractions
3. [**Best Multi-Agent Frameworks 2026 comparison**](https://gurusup.com/blog/best-multi-agent-frameworks-2026) — current market positioning
4. **One framework's Quickstart** — pick LangGraph or CrewAI; do their official tutorial end-to-end

## 🛠 Hands-on Exercises

### Exercise 1: Same agent, two frameworks
Build the same simple agent (search + summarize task) in:
- LangGraph
- CrewAI
Compare lines of code, debugging experience, and where they hide complexity.

### Exercise 2: Multi-agent role assignment
Use CrewAI to build 2-3 agents with distinct roles working on the same task. (CrewAI is best for this.)

### Exercise 3: Graph-based workflow
Use LangGraph to build a workflow with branching logic and human-in-the-loop checkpoint. (LangGraph is best for this.)

### Exercise 4: CodeAct vs JSON tool
Build a Smolagents agent that writes Python code as actions (CodeAct pattern), then compare against the JSON tool-call route from Exercise 1. Ask the same question and observe how the two routes solve it differently.

### Exercise 5: Type-safe agent
Use Pydantic AI to build an agent that returns structured output (e.g. ask a question, get back `{ "answer": str, "confidence": float, "sources": [str] }`). Watch how Pydantic's schema validation prevents the agent from cutting corners or hallucinating structure.

## 🎯 Curated Projects

### [LangGraph](https://github.com/langchain-ai/langgraph) ⭐ Production-grade

| Field | Value |
|---|---|
| Language | Python / TypeScript |
| Stars | ★ 31k+ |
| License | MIT |
| Recommendation | ⭐⭐⭐⭐⭐ |

**What it teaches**: Graph-based agent orchestration. State management, checkpointing, human-in-the-loop, time-travel debugging.

**Best for**: Production multi-agent systems where you need audit trails and rollback. Enterprise-grade.

**Notes**: Strong enterprise adoption since 2025 (audit trails, replay-friendly graph model). Steeper learning curve than CrewAI but pays off for production. Pair with LangSmith for observability.

**Run it**:
```bash
pip install langgraph langchain-anthropic
# Tutorial: https://langchain-ai.github.io/langgraph/tutorials/introduction/
```

---

### [CrewAI](https://github.com/crewAIInc/crewAI) ⭐ Lowest learning curve

| Field | Value |
|---|---|
| Language | Python |
| Stars | ★ 50k+ |
| License | MIT |
| Recommendation | ⭐⭐⭐⭐ |

**What it teaches**: Role-based multi-agent design. "Crews" of agents with distinct roles working toward shared goals.

**Best for**: Quick prototyping multi-agent systems. ~20 lines to a working crew. Great for "research → writer → reviewer" type pipelines.

**Notes**: Lowest learning curve. But: no built-in checkpointing for long-running workflows, limited control over agent-to-agent comms, coarse error handling. Good for prototypes; LangGraph for production.

---

### [Microsoft AutoGen / AG2](https://github.com/microsoft/autogen)

| Field | Value |
|---|---|
| Language | Python |
| Stars | ★ 57k+ |
| License | CC-BY-4.0 (note: license is for documentation; code released separately) |
| Recommendation | ⭐⭐⭐⭐ |

**What it teaches**: Conversational multi-agent teams. Agents interact through multi-turn conversations. Strong group-chat coordination patterns.

**Best for**: Multi-agent debate, brainstorming, peer review patterns. Microsoft's research lineage.

**Notes**: AG2 (v0.4 rewrite) introduces async-first execution and event-driven core. The original AutoGen (v0.2) is what most tutorials still use. Be aware of the version split.

---

### [Hugging Face Smolagents](https://github.com/huggingface/smolagents)

| Field | Value |
|---|---|
| Language | Python |
| Stars | ★ 27k+ |
| License | Apache 2.0 |
| Recommendation | ⭐⭐⭐⭐ |

**What it teaches**: Code-writing agents (CodeAct pattern) — agents generate Python code instead of JSON tool calls. ≤1000 LOC philosophy.

**Best for**: Local LLM ecosystems and HuggingFace integrations. Different design philosophy worth understanding.

**Notes**: HF's bet: agents should be small. Their CodeAct approach is intellectually distinct. Compare to JSON-tool approach to see the trade-offs.

---

### [OpenAI Agents SDK](https://github.com/openai/openai-agents-python)

| Field | Value |
|---|---|
| Language | Python |
| License | MIT |
| Recommendation | ⭐⭐⭐⭐ |

**What it teaches**: OpenAI's official agent SDK. Hand-offs between agents, structured outputs, OpenAI-native ergonomics.

**Best for**: If you're committed to OpenAI ecosystem. Lightweight, tight integration with GPT-4 series.

**Notes**: Newer entrant (late 2025). Less battle-tested than LangGraph but very clean. Worth watching as it matures.

---

### [LlamaIndex Agents](https://github.com/run-llama/llama_index)

| Field | Value |
|---|---|
| Language | Python |
| Stars | ★ 49k+ |
| License | MIT |
| Recommendation | ⭐⭐⭐ |

**What it teaches**: Agents tightly integrated with RAG. If your agent needs heavy document/data retrieval, LlamaIndex is the natural choice.

**Best for**: Document-heavy agent applications. Research assistant, knowledge worker agents.

**Notes**: Stronger on retrieval than orchestration. Not the right pick for pure orchestration; ideal for retrieval-heavy work.

---

### [Pydantic AI](https://github.com/pydantic/pydantic-ai)

| Field | Value |
|---|---|
| Language | Python |
| License | MIT |
| Recommendation | ⭐⭐⭐ |

**What it teaches**: Type-safe agent framework using Pydantic for structured outputs. Strong validation guarantees.

**Best for**: Production teams that want runtime type safety + structured outputs by default.

**Notes**: Newer than alternatives. Pedigree of the Pydantic team gives confidence in API design.

---

### [agentscope-ai/agentscope](https://github.com/agentscope-ai/agentscope)

| Field | Value |
|---|---|
| Language | Python |
| Stars | ★ 24k+ |
| License | Apache 2.0 |
| Recommendation | ⭐⭐⭐ |

**What it teaches**: Multi-agent platform with strong visualization tools. "Build and run agents you can see, understand, and trust."

**Best for**: Researchers wanting visual debugging of multi-agent flows.

**Notes**: Less Western community uptake but technically solid. Strong observability tooling.

---

### [LangChain](https://github.com/langchain-ai/langchain)

| Field | Value |
|---|---|
| Language | Python / TypeScript |
| Stars | ★ 135k+ |
| License | MIT |
| Recommendation | ⭐⭐⭐ |

**What it teaches**: The original "everything bag" framework. Chains, agents, memory, retrievers, all combined.

**Best for**: Quick prototypes that need many pieces glued together.

**Notes**: Many people overuse LangChain. For agent orchestration specifically, prefer LangGraph (its successor). LangChain is best for retrieval + chaining glue, not agent orchestration.

---

### [microsoft/semantic-kernel](https://github.com/microsoft/semantic-kernel)

| Field | Value |
|---|---|
| Language | C# / Python / Java |
| Stars | ★ 27k+ |
| License | MIT |
| Recommendation | ⭐⭐⭐⭐ |

**What it teaches**: Microsoft's enterprise SDK pattern (kernels + plugins + planners) — **supports C# / Python / Java with official SDKs**, one of the few agent frameworks with all three.

**Best for**: Developers in Microsoft-stack jobs, or anyone needing agents in .NET / Java environments.

**Notes**: Heavier abstractions than smolagents — not for first-week beginners. Worth considering for enterprise environments needing .NET / Java coverage.

---

### [agno-agi/agno](https://github.com/agno-agi/agno)

| Field | Value |
|---|---|
| Language | Python |
| Stars | ★ 39k+ |
| License | Apache-2.0 |
| Recommendation | ⭐⭐⭐⭐ |

**What it teaches**: Multi-modal agent runtime + control plane — beyond just *building* agents, it covers serving, monitoring, and governance. A 2025-native agent platform.

**Best for**: Pushing agents toward "serveable + observable" without the full LangGraph + LangSmith stack. Also fine for prototype-phase quick design.

**Notes**: Stage 4 for the agent API, Stage 7 for the runtime / monitoring side.

---

### [BerriAI/litellm](https://github.com/BerriAI/litellm) (not a framework — cross-stage infra)

| Field | Value |
|---|---|
| Language | Python |
| Stars | ★ 45k+ |
| License | MIT (with separate license for `enterprise/` directory) |
| Recommendation | ⭐⭐⭐⭐ |

**What it teaches**: Provider-agnostic SDK + AI gateway — **call 100+ LLMs via OpenAI-shaped API**, with cost tracking, fallbacks, guardrails.

**Best for**: Agents that switch between Claude / GPT / Gemini / open-source models without rewriting code.

**Notes**: Strictly speaking not an agent framework — it's the provider-abstraction layer that frameworks sit on. Listed in Stage 4 because multi-provider agent work commonly needs it; Stage 7 deploy also touches it. The `enterprise/` directory is separately licensed.

---

## ✅ Self-Check Before Stage 5

Can you:
- [ ] Build the same agent in LangGraph AND CrewAI
- [ ] Pick the right framework for a given task (production vs prototype)
- [ ] Explain LangGraph's checkpoint vs CrewAI's task delegation
- [ ] Identify when CodeAct (Smolagents) is better than JSON-tool
- [ ] Decide when to drop frameworks and use raw API

If yes → proceed to [Stage 5 — Claude Code Ecosystem](05-claude-code-ecosystem.md).

## 💡 Strategic note

Don't try to learn ALL of these. Pick **one production-grade (LangGraph)** and **one quick-prototype (CrewAI)** and go deep. Browse the others' READMEs to know they exist.
