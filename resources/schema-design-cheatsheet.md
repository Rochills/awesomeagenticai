# Function Schema 設計 Cheatsheet

> **繁體中文** | [简体中文](./schema-design-cheatsheet.zh-Hans.md) | [English](./schema-design-cheatsheet.en.md) | [Русский](./schema-design-cheatsheet.ru.md)

> [Stage 3 — Tool Use & Agent 入門](../stages/03-tool-use-and-hello-agent.md) 的補充參考。寫 tool / function schema 時的 5 條黃金規則 + 5 個 anti-pattern。

LLM 怎麼用你的 tool **80% 取決於 schema 寫得好不好**——schema 模糊，再強的模型也會選錯、傳錯。

---

## 5 條黃金規則

### 規則 1：description 是寫給 LLM 看的，不是 docstring

LLM 只看 `description` 決定要不要叫這個 tool、什麼時候叫。所以要：

- ✅ 寫**情境**（when）跟**做什麼**（what）：`"當使用者問特定城市的當前天氣時呼叫"`
- ❌ 不要寫實作細節：`"使用 OpenWeather API v2.5 取得 JSON"`

對照：

```python
# 壞
"description": "Get weather data."

# 好
"description": "Get current weather for a specified city. Use this when the user asks about the current weather, temperature, humidity, or 'is it raining' for any specific location. Do NOT use for forecasts (use get_forecast instead) or historical data."
```

### 規則 2：參數用對 type，模糊處用 enum 收斂

LLM 對 `type: string` 自由度高、容易亂傳。能用窄型別就用：

| 模糊 | 收斂 |
|---|---|
| `unit: string`（攝氏？華氏？kelvin？） | `unit: enum["celsius", "fahrenheit"]` |
| `priority: string`（low/中/HIGH？） | `priority: enum["low", "medium", "high"]` |
| `count: string`（"五個"？） | `count: integer` |
| `enabled: string`（"true" / "True"） | `enabled: boolean` |
| `tags: string`（"a,b,c"？JSON？） | `tags: array of string` |

### 規則 3：required vs optional 分清楚

- `required` 列**真的必要**的參數（少了這個 tool 就跑不起來）
- 有預設值的放 `default`，不要列 required
- LLM 看到 required 多會「**自己編參數**」，所以 required 越少越好

```python
# 壞：把 timezone 列 required，LLM 會亂編「Asia/Taipei」即便使用者沒提到
"required": ["city", "timezone"]

# 好
"required": ["city"]
"properties": {
    "timezone": {"type": "string", "default": "UTC", "description": "..."}
}
```

### 規則 4：tool name + parameter name 要自說明

LLM 看到 `do_thing(x, y, z)` 跟看到 `get_weather(city, unit)` 用法完全不同。

- ✅ `get_user_profile(user_id)`
- ❌ `fetch(id)` 或 `process_data(input)`

動詞開頭，說清楚是 query / mutation / action。

### 規則 5：error 回傳要讓 LLM 可以恢復

LLM 看到錯誤訊息後決定要 retry / 換工具 / 放棄。錯誤訊息要結構化：

```json
{
    "error": "City not found",
    "code": "INVALID_CITY",
    "retry_hint": "Check spelling, or try a major city nearby"
}
```

而不是只回 `"Error 500"`——LLM 拿這個沒招。

---

## 5 個常見 Anti-Pattern

### Anti-1：「萬用工具」（God Tool）

```python
# 壞：一個 tool 做所有事
def do_database_op(operation: str, table: str, data: str) -> str:
    """Do anything with the database."""
```

LLM 會把錯的 operation 配上對的 table 然後爛掉。**拆成 `query_users` / `create_order` / `update_inventory`** 等具體 tool，LLM 選擇正確率大幅提升。

### Anti-2：description 是 docstring

```python
# 壞
"description": "GET /api/v2/weather endpoint. Returns JSON. See API docs."

# 好
"description": "Get current weather for a city. Returns temperature in C/F, humidity, and conditions."
```

LLM 不是程式，它要的是 **「這個 tool 什麼時候有用」**。

### Anti-3：所有東西都是 string

```python
# 壞
{"properties": {
    "count": {"type": "string"},     # LLM 可能傳 "five"
    "active": {"type": "string"},    # LLM 可能傳 "yes"
    "list": {"type": "string"}       # LLM 可能傳 "[a, b, c]" 或 "a, b, c"
}}

# 好
{"properties": {
    "count": {"type": "integer", "minimum": 1, "maximum": 100},
    "active": {"type": "boolean"},
    "list": {"type": "array", "items": {"type": "string"}}
}}
```

### Anti-4：沒寫範例

LLM 對 description **加上 example 比沒加準確很多**。

```python
"description": "Search products by query string. Examples: 'laptop under $1000', 'red shoes size 10'. Do NOT use for product ID lookup (use get_product_by_id)."
```

### Anti-5：沉默的失敗

Tool 失敗只回 `null` 或 `{}`，LLM 以為成功，繼續用空資料推論。**永遠回**：

- 成功 → `{"success": true, "data": {...}}`
- 失敗 → `{"success": false, "error": "...", "retry_hint": "..."}`

LLM 看到 `success: false` 就知道要處理錯誤，不會把空資料當答案編造。

---

## Schema 演進的小建議

- 加參數要 backward-compatible：新參數設 `default` 而不是 required
- 改參數含義 → 開新 tool（`get_weather_v2`），舊的標 deprecated 一段時間再下
- description 改了要重新測——LLM 行為對 description 敏感，連標點都會影響
- 上 production 前用 [promptfoo](https://github.com/promptfoo/promptfoo) eval 一下「LLM 在 5-10 個典型 query 是否選對 tool」

---

## 延伸閱讀

- [Anthropic — Tool Use Guide](https://docs.anthropic.com/en/docs/agents-and-tools/tool-use/overview) — 官方 schema 規格
- [OpenAI — Function Calling](https://platform.openai.com/docs/guides/function-calling) — OpenAI 的 schema 規格（跟 Anthropic 略有差異）
- [Stage 3 — Tool Use & Agent 入門](../stages/03-tool-use-and-hello-agent.md) — 主要動手練習
- [Stage 5.2 — MCP 基礎](../stages/05-claude-code-ecosystem.md#52--mcpmodel-context-protocol-基礎) — MCP server 的 tool schema（跟 function calling schema 結構幾乎相同）
