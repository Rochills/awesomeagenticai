# Function Schema Design Cheatsheet

> [繁體中文](./schema-design-cheatsheet.md) | [简体中文](./schema-design-cheatsheet.zh-Hans.md) | [English](./schema-design-cheatsheet.en.md) | **Русский**

> Companion к [Этапу 3 — Tool Use & Agent Intro](../stages/03-tool-use-and-hello-agent.ru.md). 5 золотых правил + 5 распространённых анти-паттернов при написании tool / function schemas.

То, насколько хорошо LLM использует твой tool, **на 80% определяется качеством schema** — расплывчатые schema побеждают даже сильные модели.

---

## 5 золотых правил

### Правило 1: `description` — для LLM, не для людей

LLM читает только `description`, чтобы решить, звать ли tool и когда. Поэтому:

- ✅ Пиши **когда** + **что**: `"Call this when the user asks for current weather of a specific city."`
- ❌ Не пиши детали реализации: `"Uses OpenWeather API v2.5 returning JSON."`

Сравни:

```python
# Bad
"description": "Get weather data."

# Good
"description": "Get current weather for a specified city. Use this when the user asks about current weather, temperature, humidity, or 'is it raining' for any specific location. Do NOT use for forecasts (use get_forecast instead) or historical data."
```

### Правило 2: используй правильный `type`; сжимай нечёткие params через `enum`

LLM либеральны с `type: string` и передают произвольный текст. Затягивай где можно:

| Расплывчатое | Ограниченное |
|---|---|
| `unit: string` (celsius? fahrenheit? kelvin?) | `unit: enum["celsius", "fahrenheit"]` |
| `priority: string` (low/medium/HIGH?) | `priority: enum["low", "medium", "high"]` |
| `count: string` ("five"?) | `count: integer` |
| `enabled: string` ("true"/"True") | `enabled: boolean` |
| `tags: string` ("a,b,c"? JSON?) | `tags: array of string` |

### Правило 3: будь осторожен с `required` vs optional

- `required` перечисляет **только истинно обязательные** params (без них tool не запустится)
- Params с разумными дефолтами идут в `default`, НЕ в `required`
- LLM hallucinate'ят значения для `required` params, даже если пользователь не упомянул — **меньше required — лучше**

```python
# Bad: timezone в required → LLM придумывает "Asia/Taipei", даже если не упомянуто
"required": ["city", "timezone"]

# Good
"required": ["city"]
"properties": {
    "timezone": {"type": "string", "default": "UTC", "description": "..."}
}
```

### Правило 4: само-описывающие имена tool / param

`do_thing(x, y, z)` и `get_weather(city, unit)` дают дико разное поведение LLM.

- ✅ `get_user_profile(user_id)`
- ❌ `fetch(id)` или `process_data(input)`

Verb-first имена, сигнализируй query / mutation / action.

### Правило 5: ошибки должны быть восстановимыми

LLM использует сообщения об ошибке, чтобы решить retry / pivot / give-up. Структурируй ошибки:

```json
{
    "error": "City not found",
    "code": "INVALID_CITY",
    "retry_hint": "Check spelling, or try a major city nearby"
}
```

Голое `"Error 500"` оставляет LLM в тупике — нет recovery-сигнала.

---

## 5 распространённых анти-паттернов

### Anti-1: God Tool

```python
# Bad: один tool для всего
def do_database_op(operation: str, table: str, data: str) -> str:
    """Do anything with the database."""
```

LLM сочетает неправильную операцию с правильной таблицей и падает. **Разбей на `query_users` / `create_order` / `update_inventory`** и т. д. — точность выбора резко вырастает.

### Anti-2: Description как docstring

```python
# Bad
"description": "GET /api/v2/weather endpoint. Returns JSON. See API docs."

# Good
"description": "Get current weather for a city. Returns temperature in C/F, humidity, and conditions."
```

LLM не читает код — он хочет **«когда это полезно»**.

### Anti-3: всё — строка

```python
# Bad
{"properties": {
    "count": {"type": "string"},     # LLM может передать "five"
    "active": {"type": "string"},    # LLM может передать "yes"
    "list": {"type": "string"}       # LLM может передать "[a, b, c]" или "a, b, c"
}}

# Good
{"properties": {
    "count": {"type": "integer", "minimum": 1, "maximum": 100},
    "active": {"type": "boolean"},
    "list": {"type": "array", "items": {"type": "string"}}
}}
```

### Anti-4: нет примеров в description

LLM заметно точнее, когда `description` включает примеры.

```python
"description": "Search products by query string. Examples: 'laptop under $1000', 'red shoes size 10'. Do NOT use for product ID lookup (use get_product_by_id)."
```

### Anti-5: silent failures

Tool падает и возвращает `null` или `{}` — LLM думает, что успешно, продолжает reasoning на пустых данных. **Всегда**:

- Успех → `{"success": true, "data": {...}}`
- Провал → `{"success": false, "error": "...", "retry_hint": "..."}`

`success: false` — recovery-сигнал; без него LLM фабрикует из пустых данных.

---

## Tips по эволюции schema

- Добавляешь param → держи backward-compatible: ставь `default`, не добавляй в `required`
- Меняешь смысл param → выкатывай новый tool (`get_weather_v2`), depriкейт старый перед удалением
- Изменения `description` → перетестируй. LLM чувствительны к формулировкам, даже пунктуация важна.
- Перед production: используй [promptfoo](https://github.com/promptfoo/promptfoo) для eval'а «LLM выбирает правильный tool на 5–10 типичных запросах»

---

## Дальнейшее чтение

- [Anthropic — Tool Use Guide](https://docs.anthropic.com/en/docs/agents-and-tools/tool-use/overview) — официальная spec schema
- [OpenAI — Function Calling](https://platform.openai.com/docs/guides/function-calling) — schema-spec OpenAI (слегка отличается от Anthropic)
- [Этап 3 — Tool Use & Agent Intro](../stages/03-tool-use-and-hello-agent.ru.md) — основные упражнения
- [Этап 5.2 — MCP foundation](../stages/05-claude-code-ecosystem.ru.md#52--mcp-model-context-protocol-foundation) — tool schemas для MCP-серверов (почти идентичная структура с function-calling schema)
