# Stage 2 — Prompt Engineering

> [繁體中文](./02-prompt-engineering.md) | [简体中文](./02-prompt-engineering.zh-Hans.md) | **English** | [Русский](./02-prompt-engineering.ru.md)


⏱ **Time estimate**: 1-2 weeks (~5-12 hours)

> 👋 **Coming from [Stage 1](01-llm-basics.en.md)?** Good — you can call an API. The next 5-12 hours: write reusable structured prompts, use few-shot and chain-of-thought for hard reasoning tasks, and quantify prompt improvement with evals. **Jumped straight here?** Make sure you can call an LLM API and estimate cost in tokens — if not, head back to [Stage 1](01-llm-basics.en.md).

> 💡 Term-unfamiliar? (prompt / few-shot / CoT / system prompt / …) → see [`resources/glossary.en.md`](../resources/glossary.en.md).

## 📌 Learning Goals

After this stage you will be able to:
- Write structured prompts (role + task + format + examples)
- Apply few-shot prompting and know when it helps
- Use chain-of-thought (CoT) for reasoning tasks
- Iteratively refine a prompt and measure improvement
- Recognize when prompting hits its limit (and you need tools / agents)

## 🚪 Entry Conditions

You should already:
- Be able to call an LLM API (Stage 1)
- Be able to parse / iterate over API responses

## 📚 Required Reading

1. [**Anthropic Prompt Engineering Guide**](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/overview) — official, well-organized
2. [**OpenAI Prompt Engineering**](https://platform.openai.com/docs/guides/prompt-engineering) — OpenAI's perspective
3. [**dair-ai Prompt Engineering Guide**](https://www.promptingguide.ai/) — academic-flavored, in-depth
4. [**Anthropic — Prompting Best Practices**](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/be-clear-and-direct) — be clear and direct

## 🛠 Hands-on Exercises

### Exercise: System Prompt
Same user message, three different system prompts. Watch the personality / output format change.

### Exercise: Few-Shot
Pick a classification task. Run it 0-shot, then 3-shot. Measure accuracy difference.

### Exercise: CoT
Pick a math word problem. Compare:
- Plain prompt
- Plain prompt + "Let's think step by step"
- Plain prompt + worked example showing CoT

### Exercise: Iterative Refinement
Take a vague prompt, refine it 5 times. Track the iterations. Notice what changes improve quality.

## 🎯 Curated Projects

### [dair-ai/Prompt-Engineering-Guide](https://github.com/dair-ai/Prompt-Engineering-Guide)

| Field | Value |
|---|---|
| Stars | ★ 60k+ |
| License | MIT |
| Recommendation | ⭐⭐⭐⭐⭐ |

**What it teaches**: End-to-end prompt engineering from basics to advanced (CoT, ToT, ReAct, RAG). Academic-flavored but practical.

**Best for**: Reference. Skim once, return when you need a specific technique.

---

### [f/awesome-chatgpt-prompts](https://github.com/f/awesome-chatgpt-prompts)

| Field | Value |
|---|---|
| Stars | ★ 130k+ |
| License | CC0 |
| Recommendation | ⭐⭐⭐ |

**What it teaches**: Hundreds of role-based prompts. "Act as a [role]..." patterns.

**Best for**: Inspiration when stuck. Don't copy verbatim — adapt the patterns.

---

### [PromptingGuide.ai](https://www.promptingguide.ai/)

**What it teaches**: Same content as dair-ai's GitHub but in website format with live examples.

**Best for**: Mobile reading.

---

### [microsoft/prompt-engine](https://github.com/microsoft/prompt-engine)

| Recommendation | ⭐⭐⭐ |
|---|---|

**What it teaches**: TypeScript library for managing prompts at scale (templating, conversation history).

**Best for**: When you start managing many prompts in production.

---

### [microsoft/promptflow](https://github.com/microsoft/promptflow)

| Field | Value |
|---|---|
| Stars | ★ 10k+ |
| Recommendation | ⭐⭐⭐ |

**What it teaches**: Visual prompt design + evaluation tooling.

**Best for**: Teams building prompt-heavy apps with eval needs.

---

### [GoogleCloudPlatform/generative-ai](https://github.com/GoogleCloudPlatform/generative-ai)

| Recommendation | ⭐⭐⭐ |
|---|---|

**What it teaches**: Google Cloud's prompting cookbook (notebooks, PaLM/Gemini focus).

**Best for**: Cross-vendor perspective if you use Google's stack.

---

### [Anthropic Cookbook — Prompt patterns](https://github.com/anthropics/anthropic-cookbook)

Already cited in Stage 1. Specifically the `misc/prompt_caching.ipynb` and `multimodal/` notebooks teach advanced prompting patterns.

---

### [stanfordnlp/dspy](https://github.com/stanfordnlp/dspy)

| Field | Value |
|---|---|
| Language | Python |
| Stars | ★ 34k+ |
| License | MIT |
| Recommendation | ⭐⭐⭐⭐⭐ |

**What it teaches**: Prompt-as-code — define signatures + modules, optimize prompts via compilers / teleprompters instead of hand-tuning f-strings. The natural Stage 2 → Stage 3 bridge. From Stanford NLP.

**Best for**: Readers who finished dair-ai's guide and ask "how do I scale prompts beyond hard-coded strings?"

**Notes**: It's a framework, not a tutorial — higher learning bar than prompt-engineering-guide. Pair with the official tutorial site dspy.ai.

---

### [NirDiamant/Prompt_Engineering](https://github.com/NirDiamant/Prompt_Engineering)

| Field | Value |
|---|---|
| Language | Python / Jupyter |
| Stars | ★ 7k+ |
| License | NOASSERTION (custom terms, research/non-commercial — read before use) |
| Recommendation | ⭐⭐⭐⭐ |

**What it teaches**: 22 prompt-engineering techniques as runnable Jupyter notebooks (zero-shot → CoT → ReAct → constitutional). 2025 vintage, more hands-on than dair-ai.

**Best for**: Learners who prefer "run-and-learn." Each technique is a standalone notebook — pick whatever interests you.

---

## 🔭 Beyond prompts: context engineering

When you find that **a single prompt can no longer cover the problem** — and you need to dynamically assemble system prompt + retrieved chunks + memory + tool definitions + multi-turn history — you've graduated from prompt engineering to **context engineering**. It's the next layer up.

**Don't try to learn it now**, just know the direction:

- You'll first hit it in [Stage 6 (Memory · RAG)](06-memory-rag.en.md) (what data goes into the prompt)
- You'll fully face it in [Stage 7 (Multi-Agent · Production)](07-multi-agent-production.en.md) (context window budget, memory layering, observability)

Further reading (optional, for when you want to dig deeper):

- [`Meirtz/Awesome-Context-Engineering`](https://github.com/Meirtz/Awesome-Context-Engineering) (★ 3k+) — comprehensive survey from prompt engineering to production agents
- [`Windy3f3f3f3f/how-claude-code-works`](https://github.com/Windy3f3f3f3f/how-claude-code-works) (★ 2k+) — Claude Code internals, includes a context-engineering chapter

## ✅ Self-Check Before Stage 3

Can you:
- [ ] Write a prompt with system message + user message + 3 example messages (few-shot)
- [ ] Demonstrate CoT improving accuracy on a reasoning task
- [ ] Iteratively refine a prompt 5 times tracking each version
- [ ] Identify when prompting is the wrong tool (and tool use is needed)

If yes → proceed to [Stage 3 — Tool Use & Agent Intro](03-tool-use-and-hello-agent.en.md). This is the most important stage — don't rush past prompts but also don't get stuck here.
