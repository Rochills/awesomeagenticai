# SDK Diff: Anthropic vs OpenAI-compat (Ollama / OpenAI / Together / most open-source)

> Same ReAct loop, 3 key differences between SDKs. Pairs with SKILL.md Step 3.

## TL;DR comparison

| Part | Anthropic SDK | OpenAI-compat SDK |
|---|---|---|
| **Tool schema wrap** | `tools=[{name, description, input_schema}]` | `tools=[{"type": "function", "function": {name, description, parameters}}]` |
| **Schema field name** | `input_schema` | `parameters` |
| **Reading tool call** | `[b for b in resp.content if b.type == "tool_use"]` | `resp.choices[0].message.tool_calls` |
| **Args format** | `call.input` is already a dict | `call.function.arguments` is a JSON string — needs `json.loads(...)` |
| **Stop detection** | `resp.stop_reason == "end_turn"` | `resp.choices[0].finish_reason == "stop"` |
| **Assistant turn append** | `messages.append({"role": "assistant", "content": resp.content})` | `messages.append({"role": "assistant", "content": msg.content, "tool_calls": msg.tool_calls})` |
| **Tool result append** | `messages.append({"role": "user", "content": [{"type": "tool_result", "tool_use_id": call.id, "content": obs}]})` | `messages.append({"role": "tool", "tool_call_id": tc.id, "content": obs})` |
| **Exception class** | `anthropic.RateLimitError` / `anthropic.APIConnectionError` | `openai.RateLimitError` / `openai.APIConnectionError` |

## Side-by-side single-turn tool call

### Anthropic

```python
import anthropic

client = anthropic.Anthropic()

TOOLS = [{
    "name": "get_weather",
    "description": "Use this when the user asks about current weather.",
    "input_schema": {
        "type": "object",
        "properties": {"city": {"type": "string"}},
        "required": ["city"]
    }
}]

resp = client.messages.create(
    model="claude-haiku-4-5",
    max_tokens=512,
    tools=TOOLS,
    messages=[{"role": "user", "content": "Is it raining in Taipei?"}]
)

# Read tool call
calls = [b for b in resp.content if b.type == "tool_use"]
city = calls[0].input["city"]   # already a dict
```

### OpenAI-compat (Ollama)

```python
from openai import OpenAI
import json

client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")

TOOLS = [{
    "type": "function",
    "function": {
        "name": "get_weather",
        "description": "Use this when the user asks about current weather.",
        "parameters": {       # ← different name
            "type": "object",
            "properties": {"city": {"type": "string"}},
            "required": ["city"]
        }
    }
}]

resp = client.chat.completions.create(
    model="qwen2.5:3b",
    tools=TOOLS,
    messages=[{"role": "user", "content": "Is it raining in Taipei?"}]
)

# Read tool call
tc = resp.choices[0].message.tool_calls[0]
args = json.loads(tc.function.arguments)   # ← needs json.loads
city = args["city"]
```

## Side-by-side ReAct loop (multi-turn)

### Anthropic full loop

```python
messages = [{"role": "user", "content": "..."}]
for step in range(5):
    resp = client.messages.create(model=MODEL, max_tokens=1024, tools=TOOLS, messages=messages)
    messages.append({"role": "assistant", "content": resp.content})   # full content list appended
    if resp.stop_reason == "end_turn":
        break
    tool_results = []
    for call in [b for b in resp.content if b.type == "tool_use"]:
        obs = TOOL_IMPL[call.name](call.input)
        tool_results.append({"type": "tool_result", "tool_use_id": call.id, "content": obs})
    messages.append({"role": "user", "content": tool_results})   # tool results wrapped in user message
```

### OpenAI-compat full loop

```python
messages = [{"role": "user", "content": "..."}]
for step in range(5):
    resp = client.chat.completions.create(model=MODEL, tools=TOOLS, messages=messages)
    msg = resp.choices[0].message
    messages.append({"role": "assistant", "content": msg.content, "tool_calls": msg.tool_calls})
    if not msg.tool_calls:
        break
    for tc in msg.tool_calls:
        args = json.loads(tc.function.arguments)
        obs = TOOL_IMPL[tc.function.name](args)
        messages.append({"role": "tool", "tool_call_id": tc.id, "content": obs})   # dedicated role
```

## 4 easy-to-trip-on spots

1. **`parameters` vs `input_schema`**: most common copy-paste trap — pasting an Anthropic schema directly into OpenAI-compat silently fails (Ollama doesn't raise; it just doesn't call the tool).
2. **`call.input` vs `json.loads(arguments)`**: forgetting `json.loads` on the OpenAI-compat side gives you a string instead of a dict — KeyError.
3. **Different role for tool result**: Anthropic uses `role="user"` + `[{"type": "tool_result", ...}]`; OpenAI-compat uses `role="tool"` + plain string content.
4. **`stop_reason` vs `finish_reason`**: both exist but with different field names and values. Anthropic `"end_turn"` / `"tool_use"`; OpenAI `"stop"` / `"tool_calls"`.

## Full comparison examples

Every Stage 3 exercise ships both starters:

- `starter.py` = OpenAI-compat / Ollama
- `starter_anthropic.py` = Anthropic

Compare any of [`../../stage-3/02-multi-tool-selection/`](../../../stage-3/02-multi-tool-selection/) ~ [`../../stage-3/06-schema-design/`](../../../stage-3/06-schema-design/).
