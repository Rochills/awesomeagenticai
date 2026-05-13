# Debug Flowchart：「為什麼 LLM 不呼叫我的 tool」

> 4-symptom 診斷流程。對應 SKILL.md Step 2。

## Section A — Symptom (a)：LLM 完全不觸發 tool_calls

最常見：LLM 看 `tools=[...]`、但回了純文字、沒選任何 tool。

### Quick check（30 秒）

把這 4 個逐項勾一遍：

```
[ ] resp.choices[0].finish_reason == "tool_calls"？
[ ] 還是 "stop"？        ← 如果是 stop、LLM 主動選擇不呼叫 tool
[ ] resp.choices[0].message.tool_calls 是 None / 空 list？
[ ] resp.choices[0].message.content 是長文字？  ← LLM 用知識回答了
```

### 5 個常見原因（按發生頻率排序）

#### 1. `description` 太籠統（70% 的 case）

```python
# ❌ LLM 看不出何時用
{"name": "get_data", "description": "Get data."}

# ✅ LLM 一看就知道何時用
{"name": "get_weather", "description": "Use this when the user asks about current weather, forecast, or temperature for a specific city."}
```

**修法**：description 句首改成 "Use this when..."、列 2-3 種觸發情境。

#### 2. 多 tool 邊界互相重疊（15%）

兩個 tool 的 description 都能套到同一個 query、LLM 選不出來、乾脆都不選：

```python
# ❌ 邊界重疊
tool_a = {"name": "search", "description": "Find information."}
tool_b = {"name": "lookup", "description": "Look up data."}
# user: "幫我查台北人口" → LLM 不知道哪個

# ✅ 邊界互斥
tool_a = {"name": "web_search", "description": "Use for current/external info not in knowledge: news, weather, prices."}
tool_b = {"name": "fact_lookup", "description": "Use for static facts: populations, physical constants, capital cities."}
```

**修法**：每個 tool 加「Do NOT use for ...」明寫負面邊界。

#### 3. user query 根本不需要 tool（10%）

```python
# user: "什麼是 Python？"
# tools: [calculator, weather_lookup]
# 正確行為：LLM 用知識回答、不選 tool
```

**這不是 bug**——驗證一下 user query 是否真的需要 tool。

#### 4. Tool schema 結構錯誤（3%）

```python
# ❌ OpenAI-compat 缺外包
TOOLS = [{"name": "x", "description": "...", "parameters": {...}}]

# ✅ OpenAI-compat 要包一層
TOOLS = [{"type": "function", "function": {"name": "x", "description": "...", "parameters": {...}}}]
```

SDK 通常會 raise error；但用 Ollama 偶爾會吞掉、純文字回答。

#### 5. Model 太小（2%）

`gemma4:e4b` / 1.5B 級 model 對 tool calling 支援不穩。**Stage 3+ 默認用 `qwen2.5:3b`** 或 `llama3.2:3b`。

```bash
ollama pull qwen2.5:3b
MODEL=qwen2.5:3b python starter.py
```

## Section B — Symptom (b)：tool 被呼叫、但 args 錯

```python
# user: "Convert 32 Celsius to Fahrenheit"
# 預期：convert_temperature(value=32, unit="celsius")
# 實際：convert_temperature(value="32 Celsius", unit="")   ← 不對
```

### 3 個原因 + 修法

| 原因 | 觀察 | 修法 |
|---|---|---|
| param 全 string | `value: "32"` 而非 `32` | `parameters.value.type = "number"` |
| 缺 `required` | `unit` 沒傳 | `"required": ["value", "unit"]` |
| enum 缺 | `unit: "C" / "Celsius" / "celsius"` 都出現 | `"enum": ["celsius", "fahrenheit"]` |

詳細 A/B 看 [`schema-evolution.md`](schema-evolution.md)。

## Section C — Symptom (c)：ReAct loop 跑不停

```python
# 跑滿 max_iter=10、never end_turn
```

### 3 個原因

#### 1. 忘記把 assistant response 接回 messages

```python
# ❌ 跑不停
for step in range(5):
    resp = client.chat.completions.create(...)
    # 下面忘了 messages.append({"role": "assistant", ...})
    if resp.tool_calls:
        obs = run_tool(...)
        messages.append({"role": "tool", "content": obs})
# 下輪 LLM 看不到自己上輪的 thought、無限重複

# ✅ 修
messages.append({"role": "assistant", "content": msg.content, "tool_calls": msg.tool_calls})
```

#### 2. tool message 沒帶 `tool_call_id`

```python
# ❌ LLM 無法配對
messages.append({"role": "tool", "content": obs})

# ✅
messages.append({"role": "tool", "tool_call_id": tc.id, "content": obs})
```

#### 3. tool 結果是 garbage、LLM 不知道什麼是「完成」

```python
# user: "查台北天氣"
# tool 回傳 "ok"  ← LLM 不知道這是答案還是 placeholder

# ✅ tool 結果要 self-contained
return {"city": "Taipei", "forecast": "rain", "temperature_c": 24}
```

## Section D — Symptom (c, sub)：ReAct loop 漏步

多步任務中間少一個 tool call：

```
[step 0] lookup_population(city=Taipei)  → 2602000
[step 1] lookup_population(city=NewYork) → 8336000
[step 2] divide(2602000, 8336000)        → 0.3122
[step 3] end_turn: "答案是 0.3122"      ← 漏了 to_percentage
```

### 修法

1. **換大 model**：`qwen2.5:7b` 或 `claude-haiku-4-5`、多步穩定度顯著提升
2. **Description 明示順序**：`{"name": "to_percentage", "description": "Convert a ratio to percentage. **Call this LAST after dividing.**"}`
3. **加 chain-of-thought prompt**：user message 開頭加「Plan the steps first, then execute one by one.」

完整對照可跑範例 → [`../../stage-3/04-multi-step-reasoning/`](../../../stage-3/04-multi-step-reasoning/)
