# Debug Flowchart：「为什么 LLM 不调用我的 tool」

> 4-symptom 诊断流程。对应 SKILL.md Step 2。

## Section A — Symptom (a)：LLM 完全不触发 tool_calls

最常见：LLM 看 `tools=[...]`、但回了纯文字、没选任何 tool。

### Quick check（30 秒）

把这 4 个逐项勾一遍：

```
[ ] resp.choices[0].finish_reason == "tool_calls"？
[ ] 还是 "stop"？        ← 如果是 stop、LLM 主动选择不调用 tool
[ ] resp.choices[0].message.tool_calls 是 None / 空 list？
[ ] resp.choices[0].message.content 是长文字？  ← LLM 用知识回答了
```

### 5 个常见原因（按发生频率排序）

#### 1. `description` 太笼统（70% 的 case）

```python
# ❌ LLM 看不出何时用
{"name": "get_data", "description": "Get data."}

# ✅ LLM 一看就知道何时用
{"name": "get_weather", "description": "Use this when the user asks about current weather, forecast, or temperature for a specific city."}
```

**修法**：description 句首改成 "Use this when..."、列 2-3 种触发情境。

#### 2. 多 tool 边界互相重叠（15%）

两个 tool 的 description 都能套到同一个 query、LLM 选不出来、干脆都不选：

```python
# ❌ 边界重叠
tool_a = {"name": "search", "description": "Find information."}
tool_b = {"name": "lookup", "description": "Look up data."}
# user: "帮我查台北人口" → LLM 不知道哪个

# ✅ 边界互斥
tool_a = {"name": "web_search", "description": "Use for current/external info not in knowledge: news, weather, prices."}
tool_b = {"name": "fact_lookup", "description": "Use for static facts: populations, physical constants, capital cities."}
```

**修法**：每个 tool 加「Do NOT use for ...」明写负面边界。

#### 3. user query 根本不需要 tool（10%）

```python
# user: "什么是 Python？"
# tools: [calculator, weather_lookup]
# 正确行为：LLM 用知识回答、不选 tool
```

**这不是 bug**——验证一下 user query 是否真的需要 tool。

#### 4. Tool schema 结构错误（3%）

```python
# ❌ OpenAI-compat 缺外包
TOOLS = [{"name": "x", "description": "...", "parameters": {...}}]

# ✅ OpenAI-compat 要包一层
TOOLS = [{"type": "function", "function": {"name": "x", "description": "...", "parameters": {...}}}]
```

SDK 通常会 raise error；但用 Ollama 偶尔会吞掉、纯文字回答。

#### 5. Model 太小（2%）

`gemma4:e4b` / 1.5B 级 model 对 tool calling 支援不稳。**Stage 3+ 默认用 `qwen2.5:3b`** 或 `llama3.2:3b`。

```bash
ollama pull qwen2.5:3b
MODEL=qwen2.5:3b python starter.py
```

## Section B — Symptom (b)：tool 被调用、但 args 错

```python
# user: "Convert 32 Celsius to Fahrenheit"
# 预期：convert_temperature(value=32, unit="celsius")
# 实际：convert_temperature(value="32 Celsius", unit="")   ← 不对
```

### 3 个原因 + 修法

| 原因 | 观察 | 修法 |
|---|---|---|
| param 全 string | `value: "32"` 而非 `32` | `parameters.value.type = "number"` |
| 缺 `required` | `unit` 没传 | `"required": ["value", "unit"]` |
| enum 缺 | `unit: "C" / "Celsius" / "celsius"` 都出现 | `"enum": ["celsius", "fahrenheit"]` |

详细 A/B 看 [`schema-evolution.zh-Hans.md`](schema-evolution.zh-Hans.md)。

## Section C — Symptom (c)：ReAct loop 跑不停

```python
# 跑满 max_iter=10、never end_turn
```

### 3 个原因

#### 1. 忘记把 assistant response 接回 messages

```python
# ❌ 跑不停
for step in range(5):
    resp = client.chat.completions.create(...)
    # 下面忘了 messages.append({"role": "assistant", ...})
    if resp.tool_calls:
        obs = run_tool(...)
        messages.append({"role": "tool", "content": obs})
# 下轮 LLM 看不到自己上轮的 thought、无限重复

# ✅ 修
messages.append({"role": "assistant", "content": msg.content, "tool_calls": msg.tool_calls})
```

#### 2. tool message 没带 `tool_call_id`

```python
# ❌ LLM 无法配对
messages.append({"role": "tool", "content": obs})

# ✅
messages.append({"role": "tool", "tool_call_id": tc.id, "content": obs})
```

#### 3. tool 结果是 garbage、LLM 不知道什么是「完成」

```python
# user: "查台北天气"
# tool 回传 "ok"  ← LLM 不知道这是答案还是 placeholder

# ✅ tool 结果要 self-contained
return {"city": "Taipei", "forecast": "rain", "temperature_c": 24}
```

## Section D — Symptom (c, sub)：ReAct loop 漏步

多步任务中间少一个 tool call：

```
[step 0] lookup_population(city=Taipei)  → 2602000
[step 1] lookup_population(city=NewYork) → 8336000
[step 2] divide(2602000, 8336000)        → 0.3122
[step 3] end_turn: "答案是 0.3122"       ← 漏了 to_percentage
```

### 修法

1. **换大 model**：`qwen2.5:7b` 或 `claude-haiku-4-5`、多步稳定度显著提升
2. **Description 明示顺序**：`{"name": "to_percentage", "description": "Convert a ratio to percentage. **Call this LAST after dividing.**"}`
3. **加 chain-of-thought prompt**：user message 开头加「Plan the steps first, then execute one by one.」

完整对照可跑范例 → [`../../stage-3/04-multi-step-reasoning/`](../../../stage-3/04-multi-step-reasoning/)
