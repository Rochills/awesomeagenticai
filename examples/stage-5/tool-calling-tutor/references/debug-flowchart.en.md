# Debug Flowchart: "Why won't the LLM call my tool?"

> 4-symptom diagnostic. Pairs with SKILL.md Step 2.

## Section A — Symptom (a): LLM doesn't trigger tool_calls at all

Most common: you pass `tools=[...]`, the LLM responds in plain text, no tool selected.

### Quick check (30 seconds)

Tick each of these:

```
[ ] resp.choices[0].finish_reason == "tool_calls"?
[ ] Or "stop"?        ← if "stop", the LLM actively chose not to call a tool
[ ] Is resp.choices[0].message.tool_calls None / empty?
[ ] Is resp.choices[0].message.content a long block of text?  ← LLM answered from knowledge
```

### 5 common causes (by frequency)

#### 1. `description` is too generic (70% of cases)

```python
# ❌ LLM can't tell when to use it
{"name": "get_data", "description": "Get data."}

# ✅ LLM knows immediately when this applies
{"name": "get_weather", "description": "Use this when the user asks about current weather, forecast, or temperature for a specific city."}
```

**Fix**: rewrite descriptions to start with "Use this when..." and list 2-3 trigger situations.

#### 2. Multiple tools have overlapping boundaries (15%)

Both tool descriptions match the same query — LLM can't pick — so it picks neither:

```python
# ❌ Overlapping
tool_a = {"name": "search", "description": "Find information."}
tool_b = {"name": "lookup", "description": "Look up data."}
# user: "look up Taipei's population" → LLM can't pick

# ✅ Mutually exclusive
tool_a = {"name": "web_search", "description": "Use for current/external info not in knowledge: news, weather, prices."}
tool_b = {"name": "fact_lookup", "description": "Use for static facts: populations, physical constants, capital cities."}
```

**Fix**: add "Do NOT use for ..." to each tool to spell out the negative boundary.

#### 3. The query genuinely doesn't need a tool (10%)

```python
# user: "What is Python?"
# tools: [calculator, weather_lookup]
# Correct behavior: LLM answers from knowledge, doesn't select a tool
```

**Not a bug** — sanity-check whether the query actually needs a tool.

#### 4. Tool schema structure is wrong (3%)

```python
# ❌ OpenAI-compat missing the wrapper
TOOLS = [{"name": "x", "description": "...", "parameters": {...}}]

# ✅ OpenAI-compat needs the wrapper
TOOLS = [{"type": "function", "function": {"name": "x", "description": "...", "parameters": {...}}}]
```

SDKs usually raise; Ollama sometimes swallows it and replies in plain text.

#### 5. Model is too small (2%)

`gemma4:e4b` / 1.5B-class models have unstable tool-calling support. **Stage 3+ defaults to `qwen2.5:3b`** or `llama3.2:3b`.

```bash
ollama pull qwen2.5:3b
MODEL=qwen2.5:3b python starter.py
```

## Section B — Symptom (b): tool called, but args are wrong

```python
# user: "Convert 32 Celsius to Fahrenheit"
# expected: convert_temperature(value=32, unit="celsius")
# actual:   convert_temperature(value="32 Celsius", unit="")   ← wrong
```

### 3 causes + fixes

| Cause | Symptom | Fix |
|---|---|---|
| All params `string` | `value: "32"` instead of `32` | `parameters.value.type = "number"` |
| No `required` | `unit` missing | `"required": ["value", "unit"]` |
| No `enum` | `unit: "C" / "Celsius" / "celsius"` appearing randomly | `"enum": ["celsius", "fahrenheit"]` |

Full A/B in [`schema-evolution.en.md`](schema-evolution.en.md).

## Section C — Symptom (c): ReAct loop won't terminate

```python
# Hits max_iter=10, never end_turn
```

### 3 causes

#### 1. Forgot to append assistant response to messages

```python
# ❌ infinite loop
for step in range(5):
    resp = client.chat.completions.create(...)
    # missing: messages.append({"role": "assistant", ...})
    if resp.tool_calls:
        obs = run_tool(...)
        messages.append({"role": "tool", "content": obs})
# Next round LLM can't see its previous thought — infinite repeat

# ✅ fix
messages.append({"role": "assistant", "content": msg.content, "tool_calls": msg.tool_calls})
```

#### 2. Tool message missing `tool_call_id`

```python
# ❌ LLM can't pair result with call
messages.append({"role": "tool", "content": obs})

# ✅
messages.append({"role": "tool", "tool_call_id": tc.id, "content": obs})
```

#### 3. Tool returns garbage — LLM doesn't know what "done" looks like

```python
# user: "Check Taipei weather"
# tool returns "ok"  ← LLM can't tell if this is the answer or a placeholder

# ✅ tool results must be self-contained
return {"city": "Taipei", "forecast": "rain", "temperature_c": 24}
```

## Section D — Symptom (c, sub): ReAct loop skips a step

Multi-step task misses an intermediate tool call:

```
[step 0] lookup_population(city=Taipei)  → 2602000
[step 1] lookup_population(city=NewYork) → 8336000
[step 2] divide(2602000, 8336000)        → 0.3122
[step 3] end_turn: "The answer is 0.3122"   ← skipped to_percentage
```

### Fixes

1. **Upgrade model**: `qwen2.5:7b` or `claude-haiku-4-5` substantially improves multi-step stability
2. **Description encodes ordering**: `{"name": "to_percentage", "description": "Convert a ratio to percentage. **Call this LAST after dividing.**"}`
3. **Add chain-of-thought prompt**: prepend user message with "Plan the steps first, then execute one by one."

Full runnable comparison → [`../../stage-3/04-multi-step-reasoning/`](../../../stage-3/04-multi-step-reasoning/)
