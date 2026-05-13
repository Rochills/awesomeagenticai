> [繁體中文](./README.md) | [简体中文](./README.zh-Hans.md) | **English**

# Exercise 2: Eval Pipeline ("pytest for LLMs")

Pairs with [Stage 7 — Multi-Agent & Production](../../../stages/07-multi-agent-production.en.md) Exercise 2.

## Task

Write 5 eval cases for a production agent, run a baseline, track regression. **Without eval, you ship blind.**

The 5 cases cover:
1-2. **Math** (deterministic answers)
3-4. **Geography** (factual recall)
5. **Grounding test** (fake word "flrgglemerk" — agent should say "don't know", not hallucinate)

Two evaluators:

| Method | When | Cost |
|---|---|---|
| **String match** | Deterministic substring expected | $0, instant |
| **LLM-as-judge** | Open-ended answers (recommendation / explanation) | One extra LLM call |

## How to run

### Path A (default, free, local)

```bash
pip install -r requirements.txt
ollama pull qwen2.5:3b
ollama serve
python starter.py
```

### Path B (Anthropic)

```bash
pip install -r requirements.txt
export ANTHROPIC_API_KEY=sk-ant-...
python starter_anthropic.py
```

Budget: 5 cases × 1 call ≈ **$0.003** (Claude haiku).

## Validate the logic

```bash
python test.py             # 7 tests: evaluators + run_eval aggregation
python test_anthropic.py   # Anthropic agent mock
```

## Production value of eval

```
Without eval:
   PR merge → ship → user complains → only then you discover the regression

With eval:
   PR → run eval → pass_rate drops 95% → 70% → block merge
   → find which cases regressed → fix prompt / model / retry → recover
```

**Pin a baseline**: capture the initial pass_rate (e.g., 80%) — every ship must not regress.

## Classic eval shape

```python
eval_cases = [
    {"id": ..., "input": ..., "expected_substring": ..., "instruction": ...},
    ...
]

def run_eval(cases, agent_fn, eval_fn):
    results = [...]
    return {"pass_count": ..., "pass_rate": ...}
```

**Three keys**:
1. **`id` required** — pinpoint which case regressed
2. **`expected_substring` not full match** — LLM answers have variability
3. **Eval function decoupled from agent** — swap evaluators against the same cases

## When to use LLM-as-judge

| Scenario | Substring | LLM-as-judge |
|---|---|---|
| "2+2=?" | ✅ "4" | overkill |
| "summarize this article" | ❌ no fixed substring | ✅ |
| "is the tone professional?" | ❌ | ✅ |
| "count tokens used" | ✅ regex | overkill |

**Empirical rule**: 80% of cases use substring + heuristics; 20% use LLM-as-judge (more cost / latency).

## Production tools

- **[promptfoo](https://github.com/promptfoo/promptfoo)**: YAML config + CLI runner + diff reports
- **[Anthropic Workbench eval](https://console.anthropic.com/workbench/evals)**: official UI, prompts as code
- **[LangSmith](https://smith.langchain.com/)**: LangChain ecosystem eval + observability
- **[Weights & Biases Weave](https://wandb.ai/site/weave)**: generic LLM eval framework
- **[Braintrust](https://www.braintrust.dev/)**: cross-model / version A/B, production-grade dashboards

## Path observations

| Observation | Anthropic Claude | Ollama qwen2.5:3b |
|---|---|---|
| Math pass rate | ~100% | ~80% |
| Geography pass rate | ~100% | ~70-90% |
| Grounding test (flrgglemerk) | Stays grounded, says don't know | Occasionally fabricates |
| Overall pass_rate | 95-100% | 70-85% |

**Takeaway**: production should build a 50-200-case eval set against your specific use case to decide which model.

## Common pitfalls

- **Eval set too small (< 10)**: noise dominates, regressions invisible
- **Eval set too close to training data**: model memorizes, real user queries fail
- **No grounding test**: production hallucination is the deadliest bug — always test "should say I don't know"
- **`expected_substring` too strict**: "The capital is Tokyo, Japan." as expected, "Tokyo" as answer = fail. Match only key tokens
- **LLM-as-judge bias**: same model as agent + judge → self-preference. Use a different model for judge

## Extensions

- **Track regression**: write `{"date": ..., "pass_rate": ...}` to sqlite, plot trend
- **CI integration**: GitHub Actions runs eval, `pass_rate < 90%` blocks merge
- **A/B model comparison**: same eval, run qwen / Claude / GPT, compare accuracy
- **Connect to observability (Exercise 3)**: eval failures → alert
