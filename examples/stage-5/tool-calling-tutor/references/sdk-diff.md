# SDK Diff：Anthropic vs OpenAI-compat（Ollama / OpenAI / Together / 多數開源）

> 同一個 ReAct loop、不同 SDK 的 3 個關鍵差異。對應 SKILL.md Step 3。

## TL;DR 對照表

| 部分 | Anthropic SDK | OpenAI-compat SDK |
|---|---|---|
| **Tool schema 包法** | `tools=[{name, description, input_schema}]` | `tools=[{"type": "function", "function": {name, description, parameters}}]` |
| **Schema 欄位名** | `input_schema` | `parameters` |
| **抓 tool call** | `[b for b in resp.content if b.type == "tool_use"]` | `resp.choices[0].message.tool_calls` |
| **Args 格式** | `call.input` 已是 dict | `call.function.arguments` 是 JSON string、要 `json.loads(...)` |
| **判完成** | `resp.stop_reason == "end_turn"` | `resp.choices[0].finish_reason == "stop"` |
| **Assistant 接回** | `messages.append({"role": "assistant", "content": resp.content})` | `messages.append({"role": "assistant", "content": msg.content, "tool_calls": msg.tool_calls})` |
| **Tool result 接回** | `messages.append({"role": "user", "content": [{"type": "tool_result", "tool_use_id": call.id, "content": obs}]})` | `messages.append({"role": "tool", "tool_call_id": tc.id, "content": obs})` |
| **Exception class** | `anthropic.RateLimitError` / `anthropic.APIConnectionError` | `openai.RateLimitError` / `openai.APIConnectionError` |

## 並排程式碼對照（單輪 tool call）

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
    messages=[{"role": "user", "content": "台北現在有下雨嗎？"}]
)

# 抓 tool call
calls = [b for b in resp.content if b.type == "tool_use"]
city = calls[0].input["city"]   # 已是 dict
```

### OpenAI-compat（Ollama）

```python
from openai import OpenAI
import json

client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")

TOOLS = [{
    "type": "function",
    "function": {
        "name": "get_weather",
        "description": "Use this when the user asks about current weather.",
        "parameters": {       # ← 名字不同
            "type": "object",
            "properties": {"city": {"type": "string"}},
            "required": ["city"]
        }
    }
}]

resp = client.chat.completions.create(
    model="qwen2.5:3b",
    tools=TOOLS,
    messages=[{"role": "user", "content": "台北現在有下雨嗎？"}]
)

# 抓 tool call
tc = resp.choices[0].message.tool_calls[0]
args = json.loads(tc.function.arguments)   # ← 要 json.loads
city = args["city"]
```

## 並排 ReAct loop（多輪）

### Anthropic 完整 loop

```python
messages = [{"role": "user", "content": "..."}]
for step in range(5):
    resp = client.messages.create(model=MODEL, max_tokens=1024, tools=TOOLS, messages=messages)
    messages.append({"role": "assistant", "content": resp.content})   # 整個 content list 直接接
    if resp.stop_reason == "end_turn":
        break
    tool_results = []
    for call in [b for b in resp.content if b.type == "tool_use"]:
        obs = TOOL_IMPL[call.name](call.input)
        tool_results.append({"type": "tool_result", "tool_use_id": call.id, "content": obs})
    messages.append({"role": "user", "content": tool_results})   # tool results 包在 user message
```

### OpenAI-compat 完整 loop

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
        messages.append({"role": "tool", "tool_call_id": tc.id, "content": obs})   # 自己的 role
```

## 4 個容易踩錯的地方

1. **`parameters` vs `input_schema`**：複製貼上時最常踩——抄 Anthropic schema 直接給 OpenAI-compat 用會 silent fail（Ollama 不會 raise、就是不呼叫 tool）。
2. **`call.input` vs `json.loads(arguments)`**：OpenAI-compat 忘記 `json.loads` 會拿到 string 不是 dict、KeyError。
3. **Tool result 接回 role 不同**：Anthropic 用 `role="user"` + `[{"type": "tool_result", ...}]`；OpenAI-compat 用 `role="tool"` + 純 string content。
4. **`stop_reason` vs `finish_reason`**：兩個都存在、但欄位名跟值不同。Anthropic `"end_turn"` / `"tool_use"`；OpenAI `"stop"` / `"tool_calls"`。

## 完整對照範例

每個 Stage 3 練習都同時 ship 兩個 starter：

- `starter.py` = OpenAI-compat / Ollama
- `starter_anthropic.py` = Anthropic

對照 [`../../stage-3/02-multi-tool-selection/`](../../../stage-3/02-multi-tool-selection/) ~ [`../../stage-3/06-schema-design/`](../../../stage-3/06-schema-design/) 任一個 folder。
