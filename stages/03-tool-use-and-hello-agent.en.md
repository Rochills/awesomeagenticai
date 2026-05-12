# Stage 3 — Tool Use & Agent Intro ⭐

> [繁體中文](./03-tool-use-and-hello-agent.md) | [简体中文](./03-tool-use-and-hello-agent.zh-Hans.md) | **English** | [Русский](./03-tool-use-and-hello-agent.ru.md)


⏱ **Time estimate**: 2-3 weeks (~10-20 hours)

> 💡 Term-dense stage (agent / tool use / function calling / ReAct / structured output / …) → see [`resources/glossary.en.md` §2](../resources/glossary.en.md#2-agents--tool-use).

This is the most important stage. **You don't understand agents until you've built one.** No skipping the hello-X demos.

## 📌 Learning Goals

After this stage you will be able to:
- Explain why LLMs need tools (they're not omniscient and can't do anything outside text)
- Define a tool schema and let an LLM call it
- Build a single-step ReAct agent from scratch (no framework)
- Build a multi-step ReAct agent that decides when to stop
- Recognize when a problem needs tool use vs. plain prompting

## 🚪 Entry Conditions

You should already:
- Have working Claude / OpenAI / Gemini API access (Stage 1)
- Be comfortable with prompt engineering basics (Stage 2)
- Be able to write a Python function that takes JSON input and returns JSON

## 📚 Required Reading

1. [**Anthropic — Tool Use**](https://docs.anthropic.com/en/docs/agents-and-tools/tool-use/overview) — official guide
2. [**ReAct: Synergizing Reasoning and Acting in Language Models**](https://arxiv.org/abs/2210.03629) — Yao et al. 2022, the foundational paper. Read at least the abstract and Section 3.
3. [**OpenAI — Function Calling**](https://platform.openai.com/docs/guides/function-calling) — function-calling format reference
4. [**Build an agent from scratch**](https://shafiqulai.github.io/blogs/blog_3.html) — narrative walkthrough

## 🛠 Hands-on Exercises (5 to do)

### Exercise 1: Function Calling (single tool, single call)
Give Claude one tool (a fake weather API) and one question ("Is it raining in Taipei?"). Watch Claude call the tool, get the result, and answer.

### Exercise 2: Multi-Tool Selection
Give Claude three tools (search, calculator, calendar) and a task. Watch Claude select the right tool. Notice when Claude makes the wrong choice.

### Exercise 3: ReAct from Scratch (no framework)
Implement the Thought → Action → Observation loop in 50-80 lines of Python. No LangChain, no LangGraph. Just `while not done: thought; action; observation; ...`.

### Exercise 4: Multi-Step Reasoning Task
A task that requires 3-5 tool calls in sequence. E.g., "Find the population of Taipei, then divide by the population of New York, and convert the ratio to percent." Each step uses a different tool.

### Exercise 5: Error Handling
Make a tool fail (network error, invalid input). Watch how the agent recovers (or doesn't). Add retry logic.

### Exercise 6: Function schema design (fix a bad schema)
**Start with a deliberately bad schema** — vague `description` ("processes data"), all params typed as `string`, no required/optional split, missing `enum` where it should exist. Watch the LLM pick the wrong tool / pass wrong args. Then fix it piece by piece:
- Rewrite `description` so the LLM understands *when* to call this tool (not docstring style)
- Use proper types (number / boolean / enum / array); be explicit about required
- Collapse fuzzy fields with `enum` (e.g. `unit: "celsius" | "fahrenheit"` instead of `unit: string`)
- Make errors recoverable: return `{"error": "...", "retry_hint": "..."}` so the LLM can retry intelligently

> 💡 Detailed cheatsheet: [`resources/schema-design-cheatsheet.en.md`](../resources/schema-design-cheatsheet.en.md) — 5 golden rules + 5 common anti-patterns.

## 🎯 Curated Projects

### [Anthropic — Tool Use Cookbook](https://github.com/anthropics/anthropic-cookbook/tree/main/tool_use)

| Field | Value |
|---|---|
| Language | Python |
| License | MIT |
| Recommendation | ⭐⭐⭐⭐⭐ |

**What it teaches**: Every tool-use pattern Claude supports — single tool, multi-tool, parallel calls, structured output extraction.

**Best for**: Exercise 1 and Exercise 2. Start here.

**Run it**:
```bash
git clone https://github.com/anthropics/anthropic-cookbook
cd anthropic-cookbook/tool_use
jupyter notebook customer_service_agent.ipynb
```

---

### [Anthropic — Quickstarts](https://github.com/anthropics/anthropic-quickstarts)

| Field | Value |
|---|---|
| Language | Python / TypeScript |
| Stars | ★ 16k+ |
| License | MIT |
| Recommendation | ⭐⭐⭐⭐⭐ |

**What it teaches**: Anthropic's official hands-on starter kit. Three deployable agent templates: `financial-data-analyst` (data analysis agent), `customer-support-agent`, and `computer-use-demo` (Claude operating a screen).

**Best for**: After Exercise 1/Exercise 2, when you want to see "what does a real application look like" from the canonical source. More polished than community implementations, with proper deployment setup.

**Notes**: Each template is a self-contained sub-folder — pick one and run it. The computer-use demo is especially worth studying as one of the few official examples of a GUI-operating agent.

---

### [pguso/ai-agents-from-scratch](https://github.com/pguso/ai-agents-from-scratch)

| Field | Value |
|---|---|
| Language | Python |
| License | MIT |
| Recommendation | ⭐⭐⭐⭐⭐ |

**What it teaches**: Build agents with local LLMs and ZERO frameworks. ReAct, function calling, memory — all from scratch. Designed to demystify what frameworks hide.

**Best for**: Exercise 3 (ReAct from scratch). This is the cleanest "no-framework" reference.

**Notes**: Uses local Ollama, so works without API costs. Read the README carefully — the pedagogical structure is excellent.

---

### [arunpshankar/react-from-scratch](https://github.com/arunpshankar/react-from-scratch)

| Field | Value |
|---|---|
| Language | Python |
| License | Apache-2.0 |
| Last update | ⚠️ May 2025 (slowing) |
| Recommendation | ⭐⭐⭐⭐ |

**What it teaches**: ReAct pattern variations and implementations, optimized for Gemini.

**Best for**: Exercise 3 alternative if you prefer Gemini. Covers ReAct + Reflection + Self-consistency variants.

---

### [mattambrogi/agent-implementation](https://github.com/mattambrogi/agent-implementation)

| Field | Value |
|---|---|
| Language | Python |
| License | MIT |
| Last update | ⚠️ Stale (Jan 2024) — kept as educational toy reference |
| Recommendation | ⭐⭐⭐ |

**What it teaches**: Minimal ReAct agent implementation. Ultra-stripped-down (~150 lines) for learning.

**Best for**: Reading the source line-by-line. Use as a reference when stuck on Exercise 3.

---

### [lsdefine/GenericAgent](https://github.com/lsdefine/GenericAgent)

| Field | Value |
|---|---|
| Language | 中文 + Python |
| Stars | ★ 9k+ |
| License | MIT |
| Recommendation | ⭐⭐⭐⭐ |

**What it teaches**: Minimal self-evolving agent framework — core ~3K lines of code, agent grows skill tree from a seed. Supports Claude / Gemini / Kimi / MiniMax. Active development.

**Best for**: Exercise 3 / Exercise 4 alternative for readers who want a more "minimal but full" framework reference. Good middle ground between mattambrogi's toy and full LangGraph.

---

### [HelloAgents (jjyaoao)](https://github.com/jjyaoao/HelloAgents) — `learn_version` branch

| Field | Value |
|---|---|
| Language | 中文 (zh-Hans) + Python |
| License | CC BY-NC-SA 4.0 |
| Recommendation | ⭐⭐⭐⭐⭐ for zh readers |

**What it teaches**: Teaching-oriented multi-agent practice framework taught chapter-by-chapter, paired with [Datawhale's Hello-Agents tutorial](https://github.com/datawhalechina/hello-agents). 16 capabilities (tool response, context engineering, session persistence, sub-agents, circuit breaker, observability, etc.) — material to *learn* production patterns from, not a finished production-ready product itself.

**Best for**: Chinese-speaking learners. **Switch to the `learn_version` branch** for the tutorial-aligned version.

**Notes**: License is CC BY-NC-SA — non-commercial. Tutorial content is in zh-Hans; technical content transfers to zh-TW readers fine.

**Run it**:
```bash
pip install hello-agents
git clone -b learn_version https://github.com/jjyaoao/HelloAgents
```

---

### [datawhalechina/hello-agents](https://github.com/datawhalechina/hello-agents)

| Field | Value |
|---|---|
| Language | 中文 (zh-Hans) |
| License | CC BY-NC-SA |
| Recommendation | ⭐⭐⭐⭐⭐ for zh readers |

**What it teaches**: The companion tutorial for HelloAgents. Multi-chapter walkthrough from "what is an agent" to production patterns.

**Best for**: Chinese-speaking learners who want a structured tutorial alongside code.

**Notes**: Pair this with the `learn_version` branch of the HelloAgents repo above.

---

### [QuantaLogic/quantalogic](https://github.com/quantalogic/quantalogic)

| Field | Value |
|---|---|
| Language | Python |
| License | Apache-2.0 |
| Recommendation | ⭐⭐⭐ |

**What it teaches**: ReAct agent that generates Python code instead of JSON tool calls. Different design choice — agent writes code as actions.

**Best for**: After Exercise 3. Compare CodeAct (code as action) vs JSON tool calls.

---

### [HuggingFace Smolagents](https://github.com/huggingface/smolagents)

| Field | Value |
|---|---|
| Language | Python |
| Stars | ★ 27k+ |
| License | Apache 2.0 |
| Recommendation | ⭐⭐⭐⭐ |

**What it teaches**: Smol agents (≤1000 LOC). Code-writing agents that execute Python instead of JSON tool calls.

**Best for**: Exercise 5 alternative. Especially good for local LLM experimentation.

**Notes**: HF's stance: agents should be small. Their code-action approach is intellectually distinct from JSON-tool approach. Worth comparing.

---

### [LangChain — ReAct Agent Template](https://github.com/langchain-ai/react-agent)

| Field | Value |
|---|---|
| Language | Python |
| License | MIT |
| Recommendation | ⭐⭐⭐ |

**What it teaches**: How a framework abstracts the ReAct pattern. Template for LangGraph Studio.

**Best for**: After Exercise 3 (build from scratch first). Then compare what frameworks do for you.

---

### [Anthropic — Building Effective Agents (blog post)](https://www.anthropic.com/engineering/building-effective-agents)

| Field | Value |
|---|---|
| Format | Article |
| Recommendation | ⭐⭐⭐⭐⭐ |

**What it teaches**: Anthropic's own guide to when to use agents (vs. workflows), common patterns, and pitfalls. Required reading before Stage 4.

**Best for**: Conceptual framing. Read after Exercise 3 but before learning frameworks.

---

## ✅ Self-Check Before Stage 4

Can you:
- [ ] Define a tool schema (name + description + JSON schema input/output)
- [ ] Implement ReAct loop in <100 lines of Python without any framework
- [ ] Explain why an agent needs an "I'm done" exit condition
- [ ] Compare CodeAct (code as action) vs JSON-tool approach
- [ ] Identify when a problem doesn't need an agent

If yes → proceed to [Stage 4 — Agent Frameworks](04-agent-frameworks.md).

If no → run Exercise 3 again. Don't skip it. The frameworks in Stage 4 will mystify you if you don't understand what they're abstracting.
