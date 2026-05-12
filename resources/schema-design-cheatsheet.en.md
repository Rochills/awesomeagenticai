# Function Schema Design Cheatsheet

> [繁體中文](./schema-design-cheatsheet.md) | [简体中文](./schema-design-cheatsheet.zh-Hans.md) | **English** | [Русский](./schema-design-cheatsheet.ru.md)

> Companion to [Stage 3 — Tool Use & Agent Intro](../stages/03-tool-use-and-hello-agent.en.md). 5 golden rules + 5 common anti-patterns when writing tool / function schemas.

How well an LLM uses your tool **is 80% determined by schema quality** — vague schemas defeat even strong models.

---

## 5 Golden Rules

### Rule 1: `description` is for the LLM, not for humans

The LLM only reads `description` to decide whether to call the tool and when. So:

- ✅ Write **when** + **what**: `"Call this when the user asks for current weather of a specific city."`
- ❌ Don't write implementation details: `"Uses OpenWeather API v2.5 returning JSON."`

Compare:

```python
# Bad
"description": "Get weather data."

# Good
"description": "Get current weather for a specified city. Use this when the user asks about current weather, temperature, humidity, or 'is it raining' for any specific location. Do NOT use for forecasts (use get_forecast instead) or historical data."
```

### Rule 2: Use the right `type`; collapse fuzzy params with `enum`

LLMs are loose with `type: string` and pass arbitrary text. Tighten where possible:

| Vague | Constrained |
|---|---|
| `unit: string` (celsius? fahrenheit? kelvin?) | `unit: enum["celsius", "fahrenheit"]` |
| `priority: string` (low/medium/HIGH?) | `priority: enum["low", "medium", "high"]` |
| `count: string` ("five"?) | `count: integer` |
| `enabled: string` ("true"/"True") | `enabled: boolean` |
| `tags: string` ("a,b,c"? JSON?) | `tags: array of string` |

### Rule 3: Be careful with `required` vs optional

- `required` lists **only truly mandatory** params (without it the tool can't run)
- Params with sensible defaults go in `default`, NOT `required`
- LLMs hallucinate values for `required` params even when the user didn't mention them — **fewer required is better**

```python
# Bad: timezone listed as required → LLM invents "Asia/Taipei" even if not mentioned
"required": ["city", "timezone"]

# Good
"required": ["city"]
"properties": {
    "timezone": {"type": "string", "default": "UTC", "description": "..."}
}
```

### Rule 4: Self-describing tool / param names

`do_thing(x, y, z)` and `get_weather(city, unit)` produce wildly different LLM behavior.

- ✅ `get_user_profile(user_id)`
- ❌ `fetch(id)` or `process_data(input)`

Verb-first names, signal whether it's a query / mutation / action.

### Rule 5: Errors must be recoverable

The LLM uses error messages to decide retry / pivot / give-up. Structure errors:

```json
{
    "error": "City not found",
    "code": "INVALID_CITY",
    "retry_hint": "Check spelling, or try a major city nearby"
}
```

Bare `"Error 500"` leaves the LLM stuck — no recovery signal.

---

## 5 Common Anti-Patterns

### Anti-1: God Tool

```python
# Bad: one tool for everything
def do_database_op(operation: str, table: str, data: str) -> str:
    """Do anything with the database."""
```

The LLM will pair the wrong operation with the right table and crash. **Split into `query_users` / `create_order` / `update_inventory`** etc. — selection accuracy goes way up.

### Anti-2: Description as docstring

```python
# Bad
"description": "GET /api/v2/weather endpoint. Returns JSON. See API docs."

# Good
"description": "Get current weather for a city. Returns temperature in C/F, humidity, and conditions."
```

The LLM doesn't read code — it wants **"when is this useful"**.

### Anti-3: Everything is a string

```python
# Bad
{"properties": {
    "count": {"type": "string"},     # LLM might pass "five"
    "active": {"type": "string"},    # LLM might pass "yes"
    "list": {"type": "string"}       # LLM might pass "[a, b, c]" or "a, b, c"
}}

# Good
{"properties": {
    "count": {"type": "integer", "minimum": 1, "maximum": 100},
    "active": {"type": "boolean"},
    "list": {"type": "array", "items": {"type": "string"}}
}}
```

### Anti-4: No examples in description

LLMs are noticeably more accurate when the `description` includes examples.

```python
"description": "Search products by query string. Examples: 'laptop under $1000', 'red shoes size 10'. Do NOT use for product ID lookup (use get_product_by_id)."
```

### Anti-5: Silent failures

Tool fails and returns `null` or `{}` — LLM thinks it succeeded, continues reasoning on empty data. **Always**:

- Success → `{"success": true, "data": {...}}`
- Failure → `{"success": false, "error": "...", "retry_hint": "..."}`

`success: false` is the recovery signal; without it the LLM fabricates from empty data.

---

## Schema Evolution Tips

- Adding a param → keep it backward-compatible: set `default`, don't add to `required`
- Changing a param's meaning → ship a new tool (`get_weather_v2`), deprecate the old one before removing
- Changes to `description` → re-test. LLMs are sensitive to wording, even punctuation matters.
- Before production: use [promptfoo](https://github.com/promptfoo/promptfoo) to eval "does the LLM pick the right tool on 5-10 typical queries"

---

## Further reading

- [Anthropic — Tool Use Guide](https://docs.anthropic.com/en/docs/agents-and-tools/tool-use/overview) — official schema spec
- [OpenAI — Function Calling](https://platform.openai.com/docs/guides/function-calling) — OpenAI's schema spec (slight differences from Anthropic)
- [Stage 3 — Tool Use & Agent Intro](../stages/03-tool-use-and-hello-agent.en.md) — main exercises
- [Stage 5.2 — MCP foundation](../stages/05-claude-code-ecosystem.en.md#52--mcp-model-context-protocol-foundation) — MCP server tool schemas (nearly identical structure to function-calling schema)
