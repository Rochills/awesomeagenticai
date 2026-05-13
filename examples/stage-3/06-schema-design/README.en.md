> [繁體中文](./README.md) | [简体中文](./README.zh-Hans.md) | **English**

# Exercise 6: Function Schema Design (bad vs good)

Corresponds to [Stage 3 — Tool Use & Agent Intro](../../../stages/03-tool-use-and-hello-agent.en.md) Exercise 6.

## Why this matters

Schemas are **part of the prompt** — and they're the part the model **leans on hardest** when choosing a tool. This exercise gives you `starter_bad` and `starter_good` for the same question: "Convert 32 Celsius to Fahrenheit."

- **Bad schema**: short descriptions, every param as string, no `required`, no `enum` → LLM frequently misroutes temperature conversion to `process_data`
- **Good schema**: clear usage, `value: number`, `unit: enum["celsius", "fahrenheit"]`, all required fields listed → reliably routes to `convert_temperature`

When you write a schema, don't aim for "a human can read this". Aim for "the model can use this to rule out the wrong tool".

## How to run — two paths

### Path A (default, free, local, 4 starters)

```bash
pip install -r requirements.txt
ollama pull qwen2.5:3b
ollama serve

python starter_bad.py    # watch a bad schema mislead qwen
python starter_good.py   # watch a good schema lead qwen to the right tool
```

Budget: **$0**.

### Path B (Anthropic, cloud-quality comparison)

```bash
pip install -r requirements.txt
export ANTHROPIC_API_KEY=sk-ant-...

python starter_bad_anthropic.py
python starter_good_anthropic.py
```

Budget: ~**$0.0005** per run (claude-haiku-4-5, single call).

## Validate the logic without API credits (mock-based)

```bash
python test.py            # validates Path A (Ollama) starter_bad + starter_good
python test_anthropic.py  # validates Path B (Anthropic) starter_*_anthropic
```

Each test suite also asserts on the schema structure directly (`good` has `required` + `enum`; `bad` doesn't) — not just on the LLM's choice.

## Bad vs good schema A/B

| Design dimension | Bad | Good |
|---|---|---|
| Description | "Process data." | "Use only to summarize structured JSON table rows. Do not use for temperature conversion." |
| Param types | All `string` | `number` / `array` / actual types |
| Required | None | `["value", "unit"]` |
| Enum constraint | None | `["celsius", "fahrenheit"]` |
| Error return | Plain string | Structured dict + retry_hint |

## What to watch on each path (the teaching point)

**Small models are more sensitive to schema quality than large ones** — so this exercise is **more pedagogically valuable on Ollama**:

| Observation | Anthropic Claude haiku | Ollama qwen2.5:3b |
|---|---|---|
| Bad schema can still guess right | Medium-high | Low (almost always wrong) |
| Good schema picks correctly | Stable | Stable |
| Gap between bad and good | Small | Large |

In other words: **time spent writing good schemas saves you the cost of upgrading the model**. Want to run a cheap model (qwen / mistral) in production? Your schemas need to be production-grade.

## Further reading

More schema design rules in [`resources/schema-design-cheatsheet.md`](../../../resources/schema-design-cheatsheet.md): clear usage, correct types, required fields, enum constraints, structured error returns.

## Extensions

- **Deliberately break the good schema** — remove one `enum` constraint and watch qwen start to miss
- **Add a third tool** — one with usage similar to but boundary-blurry with `convert_temperature`, and observe the LLM's choice
- **Combine with the structured-error pattern** from [`../05-error-handling/`](../05-error-handling/) — schema design + error handling is the production-grade combo
