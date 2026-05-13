# Schema Evolution: bad schema improved to good (worked example)

> Same tool (temperature conversion), 4 improvement steps. Pairs with SKILL.md Step 2(d). Fills the procedural gap that [`resources/schema-design-cheatsheet.en.md`](../../../../resources/schema-design-cheatsheet.en.md) (which is prescriptive) doesn't cover.

## Iteration 0: original bad schema

```python
{
    "name": "convert",
    "description": "Convert a value.",
    "parameters": {
        "type": "object",
        "properties": {
            "value": {"type": "string"},
            "unit": {"type": "string"}
        }
    }
}
```

### Observed behavior (running qwen2.5:3b)

```python
# user: "Convert 32 Celsius to Fahrenheit"
# LLM behavior (average over many runs):
# - 40% picks convert, args = {"value": "32 Celsius", "unit": ""}        ← wrong type
# - 30% picks convert, args = {"value": "32", "unit": "C"}                ← inconsistent unit
# - 20% picks a different tool (process_data, etc.)                       ← unclear boundary
# - 10% doesn't call any tool, responds in plain text                     ← description too generic
```

**Success rate ≈ 0%.** Claude haiku gets it right ~60-70% (still unstable).

## Iteration 1: fix the description

```python
# ❌ before
"description": "Convert a value."

# ✅ after (clear "when to use")
"description": "Use this when the user asks to convert temperatures between Fahrenheit and Celsius."
```

### New behavior

- LLM correctly triggers tool ~60% of the time (up from ~30%; args still off)
- Unit format still wrong

**This step fixes "will the LLM call it" — args still need work.**

## Iteration 2: fix parameter type

```python
# ❌ before
"value": {"type": "string"}

# ✅ after
"value": {"type": "number", "description": "Temperature value to convert"}
```

### New behavior

- `value` is now `32` (number) instead of `"32"` / `"32 Celsius"`
- `unit` still sometimes missing or wrong format (`"C"` vs `"celsius"`)

**Type pinned; field completeness and enum still need work.**

## Iteration 3: add `required`

```python
"parameters": {
    "type": "object",
    "properties": {
        "value": {"type": "number", "description": "Temperature value to convert"},
        "unit": {"type": "string"}
    },
    "required": ["value", "unit"]   # ✅ NEW
}
```

### New behavior

- LLM no longer skips `unit`
- Still occasionally sends `"C"` / `"Celsius"` / `"celsius"` (case/abbreviation drift)

**Mandatory fields pinned; fuzzy boundaries still need an enum.**

## Iteration 4: add `enum`

```python
"unit": {
    "type": "string",
    "enum": ["celsius", "fahrenheit"],   # ✅ NEW
    "description": "Unit of the input value"
}
```

### Final schema

```python
{
    "name": "convert_temperature",   # ✅ also more specific name
    "description": "Use this when the user asks to convert temperatures between Fahrenheit and Celsius.",
    "parameters": {
        "type": "object",
        "properties": {
            "value": {"type": "number", "description": "Temperature value to convert"},
            "unit": {
                "type": "string",
                "enum": ["celsius", "fahrenheit"],
                "description": "Unit of the input value"
            }
        },
        "required": ["value", "unit"]
    }
}
```

### Behavior

- qwen2.5:3b 95%+ correct
- Claude haiku 99%+

## Cost vs benefit of the 4 changes

| Iteration | What changed | Code delta | Accuracy lift (qwen) |
|---|---|---|---|
| 1 | description | 1 line | 0% → 60% |
| 2 | type: number | 1 line | 60% → 75% |
| 3 | required | 1 line | 75% → 85% |
| 4 | enum | 1 line | 85% → 95%+ |

**4 lines of code take accuracy from ~0% to 95%+.** That's the ROI of schema design.

## Why this matters **more** on small models

```
Accuracy (same query × 1000 runs):
              BAD schema   GOOD schema   diff
Claude haiku  60%          99%           +39%
qwen2.5:3b    0%           95%           +95%
gemma4:e4b    0%           80%           +80%
```

**Takeaway**: time spent writing good schemas **saves you the cost of upgrading the model**. Want a cheap production model? Your schemas must be production-grade.

## See the full comparison example

→ [`../../stage-3/06-schema-design/`](../../../stage-3/06-schema-design/): contains `starter_bad.py` + `starter_good.py` + trilingual READMEs (runnable both Path A Ollama and Path B Anthropic).
