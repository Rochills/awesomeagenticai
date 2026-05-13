> **繁體中文** | [简体中文](./README.zh-Hans.md) | [English](./README.en.md)

# 練習 3：Observability（4 個 production telemetry）

對應 [Stage 7 — Multi-Agent & Production](../../../stages/07-multi-agent-production.md) 練習 3。
> 🎓 **學習模式**：這份 `starter.py` 是**完整解答**、不是 TODO skeleton。建議用**主動模式**——`mv starter.py starter_reference.py`、看 signature 不看 body、自己重寫一份 `starter.py`、跑 `python test.py` 驗證；卡 20 分鐘再回去對照 reference。完整方法論看 [`docs/HOW_TO_USE.md`](../../../docs/HOW_TO_USE.md)。

> 📚 **想要 chapter-length 深入版？** 本 folder 的 starter 是 illustrative 版、聚焦核心 pattern + 兩條 SDK path，不是 production-grade tutorial。深度教材推薦：
> - [`datawhalechina/hello-agents`](https://github.com/datawhalechina/hello-agents) ⭐ 中文圈最完整、章節式 + 16 種 production 能力。**本練習對應 hello-agents 的 observability / tracing 章節（Extra Chapter）**
> - [Langfuse](https://github.com/langfuse/langfuse) + [Arize Phoenix](https://github.com/Arize-ai/phoenix)（OpenTelemetry-native）
> - 完整 references 見 [Stage 7 § 精選 Projects](../../../stages/07-multi-agent-production.md#-精選-projects)


## 任務

Production agent 必備 4 個 telemetry：

1. **Latency**：每個 step 多久（p50/p95/p99）
2. **Token usage**：input / output（追 cost）
3. **Trace**：multi-step agent 每一步（debug + audit）
4. **Errors**：exception + retry count

實作：`TraceContext` + `trace_span` context manager + 在 LLM call 之間 instrument。

## 怎麼跑

```bash
pip install -r requirements.txt
ollama pull qwen2.5:3b
ollama serve
python starter.py
```

預算：**$0**（Path A）。Path B 用 Claude：~$0.0001/run。

```bash
python test.py             # 5 個 test
python test_anthropic.py
```

## 4 個 primitive

### Latency（用 contextmanager）

```python
@contextmanager
def trace_span(ctx, name, **extras):
    t0 = time.perf_counter()
    try:
        yield
    finally:
        latency_ms = (time.perf_counter() - t0) * 1000
        ctx.add_span(name, latency_ms, **extras)

# usage:
with trace_span(ctx, "search_step"):
    result = expensive_search(query)
```

### Token usage

```python
resp = client.messages.create(...)
ctx.add_tokens(input_t=resp.usage.input_tokens, output_t=resp.usage.output_tokens)
```

**Anthropic**：`usage.input_tokens` / `usage.output_tokens` 精確
**OpenAI / Ollama**：`usage.prompt_tokens` / `usage.completion_tokens`、Ollama 偶爾不返回 usage

### Trace

```python
ctx = TraceContext("req_42")
with trace_span(ctx, "search"):
    ...
with trace_span(ctx, "llm_call"):
    ...
print(ctx.summary())  # 看整個 request 的 timeline
```

### Errors

```python
@contextmanager
def trace_span(ctx, name):
    try:
        yield
    except Exception as e:
        ctx.add_error(f"{name}: {e}")
        raise   # ← 重要：raise 出去、不要吞 exception
```

## Production tools（不要自己寫）

實作 primitive 是學原理。Production 用 OpenTelemetry + 託管平台：

- **[Langfuse](https://langfuse.com/)**：open-source、self-host、tracing + eval + prompt management 一條龍
- **[LangSmith](https://smith.langchain.com/)**：LangChain ecosystem
- **[Helicone](https://www.helicone.ai/)**：proxy mode、零 code change
- **[Arize Phoenix](https://github.com/Arize-ai/phoenix)**：open-source、OpenTelemetry-native
- **[Datadog LLM Observability](https://www.datadoghq.com/product/llm-observability/)**：integrate with general APM
- **[Anthropic API Console](https://console.anthropic.com/)**：Claude usage / cost 內建 dashboard

## Production checklist

對每個 production agent 至少要回答：

```
[ ] p50 / p95 / p99 latency 多少？
[ ] 每 request 平均花多少 token？($)
[ ] 哪幾個 step 最慢？
[ ] 錯誤率多少？哪一類錯最多？
[ ] retry 後 success rate 多少？
[ ] cost / request 趨勢（每月）？
[ ] 哪些 query 答錯？(連到 eval、練習 2)
```

回答不出來 = 沒 observability。

## 兩個 path 觀察重點

| 觀察項 | Anthropic Claude | Ollama qwen2.5:3b |
|---|---|---|
| `usage.tokens` 精確度 | ✅ 完整（含 cache_*） | ⚠ 偶爾沒返回 |
| Cost tracking | 直接 cost = token × pricing | $0、但 GPU 時間有成本 |
| Latency 來源 | Network + queue + inference | 純 inference |
| Production deploy 觀察 | 看 Anthropic console | 自己跑 prometheus / grafana |

## 常見坑

- **Token usage 沒記**：上線一個月才發現 cost 漏記、無法 forecast
- **Span 不夠細**：只記 "agent_call" 整體、沒拆 "search" / "rerank" / "generate"、debug 時看不到瓶頸
- **Error swallowed**：context manager 吃掉 exception、上層以為成功
- **production 直接 print()**：應該用 structured logging（JSON / OpenTelemetry）、寫去 cloud
- **沒 sample 機制**：高 QPS 全量 trace 會塞爆 backend、要 sampling（譬如 10% trace + 100% error）

## 延伸

- **OpenTelemetry 整合**：把 `trace_span` 改成 `tracer.start_as_current_span(...)` 就能丟去 Jaeger / Datadog
- **Langfuse SDK**：3 行接上 Anthropic Claude、自動 trace
- **Prometheus metrics**：counter（request_count）、histogram（latency）、gauge（active_sessions）
- **接 eval（練習 2）**：eval failure 自動 alert 到 Slack
