# Glossary

> [繁體中文](./glossary.md) | [简体中文](./glossary.zh-Hans.md) | **English** | [Русский](./glossary.ru.md)

> The roadmap leans heavily on terms like LLM, RAG, MCP, agent. Look up unfamiliar ones here in 30 seconds, then go back to reading the stage.
>
> Each entry gives **the smallest usable definition** (30-80 words + which stage covers it in depth) — not Wikipedia.

---

## 1. Basic concepts

### LLM (Large Language Model)

GPT, Claude, Gemini — models that take text in and produce text out. Fundamentally a pure function: input prompt → output text. **They don't browse the web, they don't remember past conversations** — those need to be wired up externally.

📍 Detail: [Stage 1](../stages/01-llm-basics.en.md)

### Token

LLMs see **tokens** (sub-word units), not characters. Roughly 1 English word ≈ 1.3 tokens, 1 Chinese character ≈ 1.5–2 tokens. LLM pricing and context windows are measured in tokens. "1M-token context" ≈ 750k English words.

📍 Detail: [Stage 1](../stages/01-llm-basics.en.md)

### Context Window

The maximum tokens an LLM can "see" in one call. Claude 200k, GPT-4o 128k, Gemini 2M. **Bigger isn't always better** — beyond a length the LLM gets "Lost in the Middle".

### Prompt

The text you feed an LLM. **Prompt engineering** = designing that text to get good answers. Basic structure: system prompt (role/rules) + user prompt (the actual ask).

📍 Detail: [Stage 2](../stages/02-prompt-engineering.en.md)

### Few-shot / Zero-shot

- **Zero-shot**: ask directly without examples.
- **Few-shot**: give 2–5 input → output examples first. **Few-shot usually improves accuracy a lot**, especially for strict formatting.

### Chain-of-Thought (CoT)

Make the LLM "think before answering" — add "Let's think step by step" so it produces reasoning before the final answer. **Usually improves accuracy** at the cost of more tokens.

---

## 2. Agents / Tool Use

### Agent

A system that lets the LLM **call external functions, see results, and decide what to do next**. Core topic of this roadmap. The difference: a pure LLM is Q&A, an agent is "LLM + tools + loop".

📍 Detail: [Stage 3](../stages/03-tool-use-and-hello-agent.en.md)

### Tool Use / Function Calling

Lets the LLM call functions you defined (DB lookup, math, browser, …). Instead of plain text, the LLM returns `{"function": "search", "args": {…}}`. Your code executes it and feeds the result back to the LLM.

📍 Detail: [Stage 3](../stages/03-tool-use-and-hello-agent.en.md)
📍 How to write good schemas: [Function Schema Design cheatsheet](schema-design-cheatsheet.en.md)

### ReAct (Reasoning + Acting)

The classic agent pattern: **Thought → Action (call tool) → Observation (see result) → Thought ...** loop until done. Most agent frameworks implement this internally.

📍 Detail: [Stage 3](../stages/03-tool-use-and-hello-agent.en.md)

### Structured Output

Make the LLM output **JSON or another fixed schema** instead of free text. All major LLM APIs have `response_format` or similar. Agent frameworks rely on it for LLM ↔ code communication.

### Agent Loop

The "LLM → tool → result → LLM" repeated cycle. Termination: LLM says "done" / step budget exhausted / cost cap hit.

---

## 3. Memory / Retrieval / RAG

### RAG (Retrieval-Augmented Generation)

"Retrieve first, then generate." Flow: user question → embedding search for top-K relevant chunks → stuff those K chunks into the prompt → LLM answers. **Solves the LLM-doesn't-know-your-private-data and stale-knowledge problems.**

📍 Detail: [Stage 6](../stages/06-memory-rag.en.md)

### Vector DB / Embedding

Convert text (or images) into a vector of numbers so that **semantically similar things sit close** in vector space. Vector DBs (Pinecone, Chroma, Qdrant, etc.) store and efficiently query these vectors. Core RAG component.

📍 Detail: [Stage 6](../stages/06-memory-rag.en.md)

### Semantic Search

Use embeddings to compare "meaning similarity" rather than "exact string match". "How do I charge an EV" can retrieve "electric car battery tutorial". Traditional keyword search (BM25, etc.) can't do this.

### Chunking

Splitting long documents into embedding-friendly small pieces (typically 200–1000 tokens). **Chunk strategy directly affects RAG quality** — too small loses context, too long blurs relevance. Common: fixed-size, by paragraph, by structure (heading-based).

### Hybrid Search

Run semantic search and keyword search together, merge and rerank. Usually beats either alone. Production-grade RAG default.

### Reranking

After first-pass retrieval pulls top-50, use a more expensive but more accurate model (cross-encoder) to rerank to top-5 for the LLM. Cohere Rerank, bge-reranker, etc.

### Contextual Retrieval

Anthropic 2024 method — embed each chunk together with a summary of the document it came from, so "this chunk taken alone makes no sense" doesn't break retrieval.

📍 Detail: [Stage 6](../stages/06-memory-rag.en.md)

---

## 4. Multi-Agent

### Multi-Agent

Multiple agents collaborating on one task. Common patterns:

- **Supervisor + Worker**: one agent plans/dispatches, others execute.
- **Swarm**: peer agents, no fixed supervisor.
- **Debate**: agents argue different positions, then form consensus.

📍 Detail: [Stage 7](../stages/07-multi-agent-production.en.md)

### Handoff

One agent transfers a task to another. Adds "how to pass context" and "who handles failure" beyond a plain function call.

### A2A (Agent-to-Agent) Protocol

Google's protocol for agent ↔ agent communication. Sibling to MCP, but for agent-to-agent rather than agent-to-tool.

---

## 5. Claude Code Ecosystem

### MCP (Model Context Protocol)

Anthropic's open protocol that lets any LLM host (Claude Code, Cursor, your own agent) call any external tool server through one interface. Think "**USB for LLMs**".

📍 Detail: [Stage 5.2](../stages/05-claude-code-ecosystem.en.md#52--mcp-model-context-protocol-foundation)

### Skills / SKILL.md

Claude Code's "behavior bundles". A Skill is a folder with a `SKILL.md` that says "in what context, do what, can call which tools". Claude Code auto-loads matching skills based on the situation.

📍 Detail: [Stage 5.3](../stages/05-claude-code-ecosystem.en.md#53--skills-claude-code-behavior-layer)

### Plugin / Marketplace

Package multiple Skills + slash commands + hooks + MCP configs into one shippable unit. A **Marketplace** is a catalog of plugins; users `claude plugin install` to grab community-built ones.

📍 Detail: [Stage 5.4](../stages/05-claude-code-ecosystem.en.md#54--plugins--marketplaces)

### Slash Command

Commands inside Claude Code starting with `/` (`/help`, `/compact`, `/plan`, etc.). Custom-definable — drop a prompt into `.claude/commands/<name>.md` and it becomes `/name`.

### CLAUDE.md

A markdown file at project root that Claude Code reads on every launch. Project-level rules / conventions / context (language, code style, files to avoid, etc.).

### Hooks

Scripts that run before/after Claude Code actions (pre-tool-use, post-tool-use, user-message-received, etc.). Use cases: auto-commit on edits, logging, behavior gating.

### Subagent

A spawned agent from the main Claude Code session, with its own context window, dedicated to a specific task. E.g. "spin up a code-reviewer subagent for this diff."

---

## 6. Production / Eval / Cost

### Eval (Evaluation Framework)

Run a test set against your agent and quantify accuracy / latency / cost. **A production agent without eval has no tests.** Common: promptfoo, LangSmith, langfuse evals.

📍 Detail: [Stage 7](../stages/07-multi-agent-production.en.md)

### Observability

Capture every internal step (which LLM call, which tool, what result). Lets you replay when bugs hit. Common: langfuse, Helicone, weave.

📍 Detail: [Stage 7](../stages/07-multi-agent-production.en.md)

### Prompt Caching

LLM caches the prefix of a prompt; on repeat, only the new suffix is billed at full price (Anthropic 90% off cached, OpenAI 50% off). Long-context repeated queries save a lot.

### Streaming

LLM returns tokens as they're generated (one at a time) instead of waiting for the full response. Better UX (looks like typing); technically uses SSE or chunked transfer. **Default for production interactive apps**. Trade-offs: client must handle partial responses; ReAct tool-call parsing waits for stream end.

### Batch API

Bundle a large number of LLM requests for delayed (≤24h) processing. **Typically 50% off (Anthropic, OpenAI)**. Good for non-interactive: batch summarization, batch classification, eval suites, ETL pipelines. **Don't use for interactive chat** — latency unacceptable.

### Token Cost / Inference Cost

Per LLM call: input tokens × input price + output tokens × output price. Costs of an agent's ReAct loop add up fast — a single grep over a large codebase can run 100k tokens.

### Guardrails

Rule layer that prevents the LLM from doing bad things — block prompt injection, PII leakage, harmful output, etc. NeMo Guardrails, Guardrails AI, etc.

---

## 7. Buzzwords / Loose Terms

### CLI Agent

Agents that run in a terminal (Claude Code, Codex, Aider, Gemini CLI, etc.). Versus IDE-bound (Cursor, Continue) or web-based (ChatGPT, Claude.ai).

📍 Detail: [Track A A1](../tracks/cli/A1-cli-intro.en.md), [`resources/cli-agents-guide.en.md`](cli-agents-guide.en.md)

### BYO API Key (Bring Your Own)

Tool that supports user-provided API keys instead of bundled subscriptions. Aider / OpenCode / goose are BYO; Claude Code / Codex default to subscriptions.

### Local LLM / On-Device

Models running on your own hardware (Ollama, llama.cpp, MLX, LocalAI, etc.). Data stays local — privacy-friendly but capabilities lag frontier models.

📍 Detail: [Stage 1](../stages/01-llm-basics.en.md)

### Quantization

Compress model weights from fp16 down to int8 / int4 to save memory and increase speed at small accuracy cost. Local LLM users see this constantly (Q4_K_M, Q8_0, etc.).

### Hallucination

The LLM "confidently asserts something false" — invents APIs, fabricates numbers and presents them as fact. Every production agent needs defenses (RAG / structured output / eval / guardrails).

### Frontier Model

The current top tier (GPT-5, Claude Sonnet 4.5, Gemini 2.5 Pro, etc.). Use frontier for hard reasoning; use cheap small models for simple classification / translation to save cost.

### Context Engineering

When designing one prompt sentence stops being enough, and you need to dynamically assemble **system prompt + tool definitions + memory + retrieved chunks + multi-turn history** — that is the design discipline for the whole stack. **The next layer above prompt engineering.**

📍 Detail: [Stage 2 closing](../stages/02-prompt-engineering.en.md) / [Stage 6](../stages/06-memory-rag.en.md) / [Stage 7](../stages/07-multi-agent-production.en.md)
📍 Further: [`Meirtz/Awesome-Context-Engineering`](https://github.com/Meirtz/Awesome-Context-Engineering)

### Harness Engineering

The toolchain design for wrapping an agent into a production system — permissions, tool registry, memory layer, eval, observability, retry / circuit breaker. Claude Code, Cursor, OpenCode, etc. are all "harnesses". **A framework wraps an LLM into an agent; a harness wraps an agent into a product.**

📍 Detail: [Stage 7](../stages/07-multi-agent-production.en.md) required reading
📍 Further: [`ai-boost/awesome-harness-engineering`](https://github.com/ai-boost/awesome-harness-engineering), [`ZhangHanDong/harness-engineering-from-cc-to-ai-coding`](https://github.com/ZhangHanDong/harness-engineering-from-cc-to-ai-coding)

---

## Term not here?

- Read the actual stage content: [Stage 5.2 MCP](../stages/05-claude-code-ecosystem.en.md#52--mcp-model-context-protocol-foundation) / [5.3 Skills](../stages/05-claude-code-ecosystem.en.md#53--skills-claude-code-behavior-layer) / [5.4 Plugins](../stages/05-claude-code-ecosystem.en.md#54--plugins--marketplaces)
- Required reading lists in [Stage 1](../stages/01-llm-basics.en.md) / [Stage 6](../stages/06-memory-rag.en.md) / [Stage 7](../stages/07-multi-agent-production.en.md)
- Missing? Open an issue or PR a new entry.
