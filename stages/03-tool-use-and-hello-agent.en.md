# Stage 3 — Tool Use & Agent Intro ⭐

> [繁體中文](./03-tool-use-and-hello-agent.md) | [简体中文](./03-tool-use-and-hello-agent.zh-Hans.md) | **English** | [Русский](./03-tool-use-and-hello-agent.ru.md)


⏱ **Time estimate**: 2-3 weeks (~10-20 hours)

> 💡 Term-dense stage (agent / tool use / function calling / ReAct / structured output / …) → see [`resources/glossary.en.md` §2](../resources/glossary.en.md#2-agents--tool-use).
> 🗺️ **Before committing to Track A (CLI Power User) or Track B (Agent Builder)**, read [`resources/agent-paradigms.en.md`](../resources/agent-paradigms.en.md) — the 5-paradigm map of the agent landscape that helps you pick a track.

This is the most important stage. **You don't understand agents until you've built one** — we recommend writing the foundational exercises by hand at least once, then visiting [hello-agents](https://github.com/datawhalechina/hello-agents) or this stage's curated projects for chapter-length depth.

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

## 🛠 Hands-on Exercises (foundational, illustrative)

> 🦙 **This stage defaults to Ollama qwen2.5:3b** (cost-driven; reliable tool-use support). Once you enter Stage 3 — tool calling and the ReAct loop — `gemma4:e4b` no longer suffices; switch to `qwen2.5:3b` (1.9 GB; install with `ollama pull qwen2.5:3b`). Every exercise has Path A (Ollama, default) + Path B (Anthropic, optional — when you want to see cloud-quality tool use).
>
> 💰 **Stage 3 budget estimate** (6 exercises, tool-use heavy): **all local = $0**, **all haiku ≈ $0.50**, **all sonnet ≈ $1.50**. A typical ReAct loop is 4-6 tool calls × 5 exercises × 5 reps ≈ $0.80 haiku. Full budget: [`examples/README.en.md#recommended-llm-list`](../examples/README.en.md#recommended-llm-list-local--cloud-user-perspective).
>
> Full three-path trade-off in [`examples/README.en.md`](../examples/README.en.md#three-paths--default-is-ollama-cost-driven).
>
> 🆘 **Stuck?** Tool calling is the steepest curve in the curriculum. Install [`examples/stage-5/tool-calling-tutor/`](../examples/stage-5/tool-calling-tutor/) — when you prompt Claude Code with "why won't the LLM call my tool" or "what's wrong with my schema", it auto-loads and runs a 4-symptom diagnostic.

### Exercise 1: Function Calling (single tool, single call)
Give Claude one tool (a fake weather API) and one question ("Is it raining in Taipei?"). Watch Claude call the tool, get the result, and answer.

<details open>
<summary>📋 <b>Starter code — Path A (local Ollama qwen2.5:3b, default)</b> (copy to <code>practice_1.py</code>)</summary>

```python
# Requires: pip install openai
# Pre-req: ollama pull qwen2.5:3b && ollama serve
# Note: Stage 3+ uses qwen2.5:3b (stable tool-use support), not gemma4:e4b
import sys, json
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from openai import OpenAI

client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")

# Step 1: Define tool schema — OpenAI-compatible wraps it in {"type": "function", "function": {...}}
weather_tool = {
    "type": "function",
    "function": {
        "name": "get_weather",
        "description": "Look up the current weather (sunny/rainy/cloudy) for a city. Returns a short string.",
        "parameters": {
            "type": "object",
            "properties": {
                "city": {"type": "string", "description": "City name (e.g. 'Taipei')"},
            },
            "required": ["city"],
        },
    },
}

# Step 2: Ask the question; let the LLM decide whether to call the tool
resp = client.chat.completions.create(
    model="qwen2.5:3b",
    max_tokens=512,
    tools=[weather_tool],
    messages=[{"role": "user", "content": "Is it raining in Taipei right now?"}],
)

# === Self-check ===
msg = resp.choices[0].message
print("finish_reason:", resp.choices[0].finish_reason)
print("tool_calls:", msg.tool_calls)

assert msg.tool_calls, "Expected the LLM to call a tool (not answer directly)."
tc = msg.tool_calls[0]
assert tc.function.name == "get_weather", f"Expected get_weather, got {tc.function.name}."
args = json.loads(tc.function.arguments)
assert args.get("city"), "Expected the city argument to be filled in."
print(f"✅ Exercise 1 passed — qwen2.5:3b picked get_weather with city='{args['city']}'.")
```

**Expected output** (sample):
```
finish_reason: tool_calls
tool_calls: [ChatCompletionMessageToolCall(id='call_xxx', function=Function(name='get_weather', arguments='{"city": "Taipei"}'), type='function')]
✅ Exercise 1 passed — qwen2.5:3b picked get_weather with city='Taipei'.
```

**No Ollama installed?** Replace the client with a `unittest.mock.MagicMock` that returns a canned tool-call response; the asserts still work. Full mock pattern: [`examples/stage-3/03-react-from-scratch/test.py`](../examples/stage-3/03-react-from-scratch/test.py) (cross-backend pattern).

</details>

<details>
<summary>📋 <b>Starter code — Path B (Anthropic API, optional)</b> (copy to <code>practice_1_anthropic.py</code>)</summary>

```python
# Requires: pip install anthropic
# Env: export ANTHROPIC_API_KEY=sk-ant-...
import anthropic

client = anthropic.Anthropic()

# Anthropic native tool schema — no wrapper needed
weather_tool = {
    "name": "get_weather",
    "description": "Look up the current weather (sunny/rainy/cloudy) for a city. Returns a short string.",
    "input_schema": {
        "type": "object",
        "properties": {
            "city": {"type": "string", "description": "City name (e.g. 'Taipei')"},
        },
        "required": ["city"],
    },
}

resp = client.messages.create(
    model="claude-haiku-4-5",
    max_tokens=512,
    tools=[weather_tool],
    messages=[{"role": "user", "content": "Is it raining in Taipei right now?"}],
)

# === Self-check ===
assert resp.stop_reason == "tool_use", f"unexpected stop_reason: {resp.stop_reason}"
tool_calls = [b for b in resp.content if b.type == "tool_use"]
assert tool_calls[0].name == "get_weather"
assert tool_calls[0].input.get("city")
print(f"✅ Exercise 1 passed (Anthropic) — Claude picked get_weather with city='{tool_calls[0].input['city']}'.")
```

**3 key SDK differences**:
- **Schema wrapping**: Anthropic uses `tools=[{name, description, input_schema}]` directly; OpenAI/Ollama needs `[{"type":"function", "function":{...}}]`
- **Response path**: Anthropic reads from `resp.content[i].type=="tool_use"`; OpenAI/Ollama reads from `resp.choices[0].message.tool_calls[i]`
- **Args format**: Anthropic `.input` is already a dict; OpenAI/Ollama `.function.arguments` is a JSON string — `json.loads(...)` it

**Cost**: ~$0.001/call. **Claude's tool use is more reliable than qwen2.5:3b** — the gap widens with complex scenarios (5+ tools, ambiguous questions).

</details>

### Exercise 2: Multi-Tool Selection
Give Claude three tools (search, calculator, calendar) and a task. Watch Claude select the right tool. Notice when Claude makes the wrong choice.

<details>
<summary>📋 <b>Simplified core idea — Path A (Ollama)</b></summary>

**NEW vs Exercise 1**: tools go from 1 to 3. The LLM relies on `description` boundaries to choose — the more your `description` reads like a "docstring for humans", the more often the LLM picks wrong.

```python
from openai import OpenAI
import json

client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")

TOOLS = [
    {"type": "function", "function": {"name": "web_search",
        "description": "Search current or external info not in the prompt.",
        "parameters": {"type": "object", "properties": {"query": {"type": "string"}}, "required": ["query"]}}},
    {"type": "function", "function": {"name": "calculator",
        "description": "Evaluate basic arithmetic with +, -, *, /, parentheses.",
        "parameters": {"type": "object", "properties": {"expression": {"type": "string"}}, "required": ["expression"]}}},
    {"type": "function", "function": {"name": "calendar_lookup",
        "description": "Look up events for a specific date.",
        "parameters": {"type": "object", "properties": {"date": {"type": "string"}}, "required": ["date"]}}},
]

resp = client.chat.completions.create(model="qwen2.5:3b", tools=TOOLS,
    messages=[{"role": "user", "content": "What is (19 * 42) - 8?"}])

tc = resp.choices[0].message.tool_calls[0]
print(f"LLM picked: {tc.function.name}, args: {json.loads(tc.function.arguments)}")
# Expected: calculator, {"expression": "(19 * 42) - 8"}
```

**Punchline**: the three tools' `description` boundaries must be mutually exclusive. A `calendar` description that just says "calendar" is too vague — it'll collide with `web_search`. "Look up events for a specific date" is clear. Small models are more sensitive to description quality than Claude.

**Path B (Anthropic) differs in 3 lines**: drop the `{"type": "function", "function": {...}}` wrapper; `tool_calls` becomes `[b for b in resp.content if b.type == "tool_use"]`; `tc.input` is already a dict — no `json.loads` needed. Full version in folder.

</details>

→ **Full runnable version** → [`examples/stage-3/02-multi-tool-selection/`](../examples/stage-3/02-multi-tool-selection/)

### Exercise 3: ReAct from Scratch (no framework)
Implement the Thought → Action → Observation loop in 50-80 lines of Python. No LangChain, no LangGraph. Just `while not done: thought; action; observation; ...`.

<details>
<summary>📋 <b>Simplified core idea — Path A (Ollama), the whole ReAct loop fits in 13 lines</b></summary>

**NEW vs Exercise 2**: wrap the single call in a loop, watch `messages` grow each iteration, and stop when there are no more `tool_calls`.

```python
# Assume TOOLS + TOOL_IMPL (dict: name → callable) are defined as in Exercise 2
messages = [{"role": "user", "content": "Taipei population divided by NYC population?"}]

for step in range(5):  # max_iter safety net
    r = client.chat.completions.create(model="qwen2.5:3b", tools=TOOLS, messages=messages)
    msg = r.choices[0].message
    # Append assistant response back to messages (critical! otherwise next round can't see what it just said)
    messages.append({"role": "assistant", "content": msg.content, "tool_calls": msg.tool_calls})
    if not msg.tool_calls:
        print(f"✅ done: {msg.content}"); break
    for tc in msg.tool_calls:
        args = json.loads(tc.function.arguments)
        obs = TOOL_IMPL[tc.function.name](args)  # local execution
        # Append observation back (use role="tool" with matching tool_call_id)
        messages.append({"role": "tool", "tool_call_id": tc.id, "content": obs})
```

**Three common pitfalls**:
1. **Forgetting to append assistant response to messages** — the next round can't see what the LLM just said, leading to infinite loops
2. **`tool` message missing `tool_call_id`** — the LLM can't pair which result goes with which call
3. **No `max_iter`** — if a tool returns garbage, the LLM may call it forever. A safety net is mandatory.

**Path B (Anthropic) differs in a few lines**: same loop structure; `msg.tool_calls` becomes `[b for b in resp.content if b.type == "tool_use"]`; use `stop_reason == "end_turn"` to break; tool results go in as `{"type": "tool_result", "tool_use_id": ..., "content": obs}` inside a user message. Full version in folder.

</details>

→ **Full runnable version** → [`examples/stage-3/03-react-from-scratch/`](../examples/stage-3/03-react-from-scratch/) (includes mock-based test.py so you can validate the logic without spending API credits)

### Exercise 4: Multi-Step Reasoning Task
A task that requires 3-5 tool calls in sequence. E.g., "Find the population of Taipei, then divide by the population of New York, and convert the ratio to percent." Each step uses a different tool.

<details>
<summary>📋 <b>Simplified core idea — same loop as Exercise 3, just runs longer</b></summary>

**NEW vs Exercise 3**: **literally the same loop** — `TOOLS` swaps to 4 tools (`lookup_population` / `divide` / `to_percentage` / `round_int`), and the task naturally requires 4 tool-call rounds before the LLM closes.

```python
# No new code — just different TOOLS / TOOL_IMPL content
TOOL_IMPL = {
    "lookup_population": lambda i: lookup_population(i["city"]),
    "divide":            lambda i: divide(i["a"], i["b"]),
    "to_percentage":     lambda i: to_percentage(i["ratio"]),
    "round_int":         lambda i: round_int(i["x"]),
}
# Loop is identical to Exercise 3, just with max_iter bumped to 8
```

**Punchline**: multi-step reasoning isn't a new pattern — it's **letting the same ReAct loop run a bit longer**. **The real challenge is "does the LLM skip a step?"** qwen2.5:3b may skip "convert to percentage"; Claude haiku is more stable. **This is exactly the experiment for "model scale vs multi-step stability"**. Try `MODEL=qwen2.5:7b python starter.py` to compare.

</details>

→ **Full runnable version** → [`examples/stage-3/04-multi-step-reasoning/`](../examples/stage-3/04-multi-step-reasoning/)

### Exercise 5: Error Handling
Make a tool fail (network error, invalid input). Watch how the agent recovers (or doesn't). Add retry logic.

<details>
<summary>📋 <b>Simplified core idea — tool errors are data, not exceptions</b></summary>

**NEW vs Exercise 4**: tool errors return a **structured dict**, not `raise`. The loop hands the dict back to the LLM, and the model itself decides whether to retry, rephrase, or give up.

```python
def fetch_weather(city: str) -> dict:
    if network_failed():
        return {"error": "network timeout", "retry_hint": "try again in 1s"}
    return {"city": city, "forecast": "rain", "temperature_c": 24}

# Inside the loop:
obs = fetch_weather(args["city"])
messages.append({"role": "tool", "tool_call_id": tc.id,
                 "content": json.dumps(obs, ensure_ascii=False)})  # error dict also stringified
# Next round the LLM sees retry_hint — it may retry, give up, or rephrase
```

**Why not `raise`**: `raise` immediately breaks the loop, leaving the LLM no chance to recover. **In production, retry doesn't live in Python — it lives in the LLM.** This mental flip is the heart of Exercise 5.

**Bad vs good error returns**:

| Bad | Good |
|---|---|
| `raise Exception("failed")` | `return {"error": "network timeout", "retry_hint": "try again in 1s"}` |
| `return "failed"` | `return {"error": "...", "category": "transient", "retry_hint": "..."}` |
| Unbounded retry | `max_iter` safety + business-layer retry quota |

**Small-model observation**: qwen2.5:3b follows `retry_hint` less reliably than Claude haiku — it may give up immediately. Full version (including a "repeated failure, graceful end" case) in folder.

</details>

→ **Full runnable version** → [`examples/stage-3/05-error-handling/`](../examples/stage-3/05-error-handling/)

### Exercise 6: Function schema design (fix a bad schema)
**Start with a deliberately bad schema** — vague `description` ("processes data"), all params typed as `string`, no required/optional split, missing `enum` where it should exist. Watch the LLM pick the wrong tool / pass wrong args. Then fix it piece by piece:
- Rewrite `description` so the LLM understands *when* to call this tool (not docstring style)
- Use proper types (number / boolean / enum / array); be explicit about required
- Collapse fuzzy fields with `enum` (e.g. `unit: "celsius" | "fahrenheit"` instead of `unit: string`)
- Make errors recoverable: return `{"error": "...", "retry_hint": "..."}` so the LLM can retry intelligently

> 💡 Detailed cheatsheet: [`resources/schema-design-cheatsheet.en.md`](../resources/schema-design-cheatsheet.en.md) — 5 golden rules + 5 common anti-patterns.

<details>
<summary>📋 <b>Simplified core idea — bad vs good schema A/B</b></summary>

**NEW vs Exercise 5**: same tool (temperature conversion), two schema styles. Four key differences.

```python
# ❌ BAD — qwen2.5:3b almost always picks wrong (Claude haiku can still guess but accuracy drops sharply)
{"name": "convert", "description": "Convert a value.",
 "parameters": {"type": "object", "properties": {
     "value": {"type": "string"}, "unit": {"type": "string"}}}}

# ✅ GOOD — even qwen reliably picks the right tool
{"name": "convert_temperature",
 "description": "Use when user asks to convert temperatures between Fahrenheit and Celsius.",
 "parameters": {"type": "object", "properties": {
     "value": {"type": "number", "description": "Temperature value"},
     "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]}},
     "required": ["value", "unit"]}}
```

**Four improvements**: (1) specific `name`; (2) `description` says **when to use** instead of **what it does**; (3) `value` typed as `number`; (4) added `required` + `enum`.

**Punchline**: **Time spent writing good schemas saves you the cost of upgrading models.** Small models are more sensitive to schema quality than large ones — the same bad schema where Claude can still guess will reliably mislead qwen. Want to run a cheap production model? Your schemas must be production-grade.

**Stuck designing a schema?** Install [`examples/stage-5/tool-calling-tutor/`](../examples/stage-5/tool-calling-tutor/) — when you hit "the LLM won't call my tool" or "what's wrong with this schema?" the skill auto-loads to help you debug.

</details>

→ **Full runnable version** → [`examples/stage-3/06-schema-design/`](../examples/stage-3/06-schema-design/) (includes bad-schema vs good-schema side-by-side)

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
