> [繁體中文](./README.md) | [简体中文](./README.zh-Hans.md) | **English**

# Exercise 3: ReAct from Scratch (no framework)

Corresponds to [Stage 3 — Tool Use & Agent Intro](../../../stages/03-tool-use-and-hello-agent.en.md) Exercise 3.

## Why write it from scratch

ReAct (Reasoning + Acting) is the foundational pattern of modern agents:

```
while not done:
    thought     = LLM reads current context and verbalizes the next step
    action      = LLM calls a tool
    observation = tool result, fed back to the LLM
```

LangGraph / CrewAI hide this loop from you. **Writing it once yourself** is what teaches you:
- Why the `messages` array keeps growing
- How `tool_use_id` pairs with `tool_result`
- Why `stop_reason` is `tool_use` vs `end_turn`
- Why `max_iter` is a mandatory safety net

All of that is covered in 70 lines of Python.

## How to run

```bash
pip install -r requirements.txt
export ANTHROPIC_API_KEY=sk-ant-...
python starter.py
```

Expected:

```
❓ Question: Divide Taipei's population by NYC's population, 4 decimal places.
------------------------------------------------------------
[step 0] thought: Let me look up Taipei's population...
           tool: lookup_fact({'query': '台北人口'}) → 2602000
[step 1] thought: Now NYC's...
           tool: lookup_fact({'query': '紐約人口'}) → 8336000
[step 2] thought: Compute the ratio...
           tool: calculator({'expression': '2602000 / 8336000'}) → 0.3121...
[step 3] thought: The answer is 0.3122.
------------------------------------------------------------
✅ Final answer: Taipei / NYC ≈ 0.3122
   Took 4 rounds.
✅ Exercise 3 passed — the ReAct loop chained lookup_fact and calculator on its own.
```

## Validate the logic without spending API credits

```bash
python test.py
```

`test.py` uses `unittest.mock.MagicMock` to replace the Anthropic client and feed canned responses, validating your loop logic. Expected:

```
✅ test_calculator_basic
✅ test_calculator_rejects_eval_injection
✅ test_lookup_fact
✅ test_react_loop_single_tool_call
✅ test_react_loop_multi_step
✅ test_react_loop_respects_max_iter

🎉 All tests passed — your ReAct loop logic is correct.
```

## Program structure walkthrough

| Section | Lines | What it does |
|---|---|---|
| `tool_calculator` | ~30-40 | Safe calculator (whitelist filter, avoids `eval` injection) |
| `tool_lookup_fact` | ~42-50 | Fake fact lookup (teaching-only, avoids external API dep) |
| `TOOLS_SPEC` | ~52-75 | Tool schema that the LLM sees |
| `TOOL_IMPL` | ~77-80 | name → callable dispatch table |
| `react_loop` | ~85-130 | Main loop, with max_iter safety, `messages` accumulation, tool_result wiring |

## Common pitfalls

1. **Forgetting to append the assistant response to messages** — next round the LLM can't see what it just said, leading to infinite loops
2. **Not passing `tool_use_id` with tool_result** — the LLM can't pair results to calls
3. **`while True` without `max_iter`** — if a tool returns garbage the LLM may call it forever; safety net is mandatory
4. **Unfiltered eval** — `eval(user_input)` in calculator = RCE; use a whitelist or `ast.literal_eval`

## Want smarter answers?

Default model is `claude-haiku-4-5` (cheapest). Switch to Sonnet:

```bash
MODEL=claude-sonnet-4-5 python starter.py
```

Or change `MODEL = ...` in `starter.py`.

## Extensions

- **Add more tools** — append one entry each to `TOOLS_SPEC` + `TOOL_IMPL`
- **Add streaming** — swap `client.messages.create(...)` for `with client.messages.stream(...) as s:`, print as it goes
- **Add prompt cache** — pass `cache_control={"type":"ephemeral"}` on `system=` or `tools=` to save 90% on repeat calls
- **Plug into [LangGraph](https://langchain-ai.github.io/langgraph/) or [Pydantic AI](https://ai.pydantic.dev/)** to see how frameworks hide these 70 lines
