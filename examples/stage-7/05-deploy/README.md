> **繁體中文** | [简体中文](./README.zh-Hans.md) | [English](./README.en.md)

# 練習 5：Deploy（FastAPI + Docker）

對應 [Stage 7 — Multi-Agent & Production](../../../stages/07-multi-agent-production.md) 練習 5。
> 🎓 **學習模式**：這份 `starter.py` 是**完整解答**、不是 TODO skeleton。建議用**主動模式**——`mv starter.py starter_reference.py`、看 signature 不看 body、自己重寫一份 `starter.py`、跑 `python test.py` 驗證；卡 20 分鐘再回去對照 reference。完整方法論看 [`docs/HOW_TO_USE.md`](../../../docs/HOW_TO_USE.md)。

> 📚 **想要 chapter-length 深入版？** 本 folder 的 starter 是 illustrative 版、聚焦核心 pattern + 兩條 SDK path，不是 production-grade tutorial。深度教材推薦：
> - [`datawhalechina/hello-agents`](https://github.com/datawhalechina/hello-agents) ⭐ 中文圈最完整、章節式 + 16 種 production 能力。**本練習對應 hello-agents 的 production deploy / harness 章節**
> - [FastAPI official tutorial](https://fastapi.tiangolo.com/tutorial/) + [awesome-harness-engineering](https://github.com/ai-boost/awesome-harness-engineering)（harness pattern 全集）
> - 完整 references 見 [Stage 7 § 精選 Projects](../../../stages/07-multi-agent-production.md#-精選-projects)


## 任務

把 agent 包進 production-style HTTP API：

- FastAPI app with `/health` + `/chat` endpoints
- Structured logging with request_id
- Proper HTTP status codes (200 / 422 / 429 / 503 / 500)
- Pydantic schema validation (FastAPI 自動驗）
- Dockerfile（含 Ollama 跟 Anthropic 兩個 deploy 模式）

## 怎麼跑

### Local Ollama

```bash
pip install -r requirements.txt
ollama pull qwen2.5:3b
ollama serve

uvicorn starter:app --reload --port 8000

# 另一個 shell:
curl -X POST http://localhost:8000/chat \
  -H 'Content-Type: application/json' \
  -d '{"message": "hi"}'
```

### Local Anthropic

```bash
pip install -r requirements.txt
export ANTHROPIC_API_KEY=sk-ant-...
uvicorn starter_anthropic:app --reload --port 8000
```

### Docker

```bash
docker build -t agent-api .

# Ollama path（需 host 跑著 ollama）
docker run -p 8000:8000 \
  -e OLLAMA_API_BASE=http://host.docker.internal:11434/v1 \
  agent-api

# Anthropic path
docker run -p 8000:8000 \
  -e APP_MODULE=starter_anthropic:app \
  -e ANTHROPIC_API_KEY=$ANTHROPIC_API_KEY \
  agent-api
```

## 不啟 server 驗證

```bash
python test.py             # 5 個 test、用 fastapi.TestClient
python test_anthropic.py   # 3 個 test（含 429 rate limit）
```

`fastapi.TestClient` 用 in-process ASGI、不開真 port、不用 docker。

## Production-grade 必備

| 元素 | 為什麼 | 在這份 starter |
|---|---|---|
| `/health` endpoint | K8s liveness / readiness probe | ✅ |
| `request_id` per call | trace / debug 必備 | ✅ uuid4 |
| Structured logging | ELK / Datadog / Loki 看得懂 | ✅ JSON-like format |
| Pydantic schema validation | malformed JSON 自動 422 | ✅ FastAPI 內建 |
| Specific exception → HTTP status | 503 ≠ 500，client 知道該不該 retry | ✅ APIConnectionError → 503 |
| Token tracking response | cost / token usage 透明 | ✅ Path B 含 input_tokens / output_tokens |

## Status code 對照

| 情況 | HTTP code | client 該怎樣 |
|---|---|---|
| LLM 答了 | 200 | 用答案 |
| user 沒傳 message field | 422 | 修 request、別 retry |
| Anthropic rate limit (429) | 429 | exponential backoff retry |
| LLM 服務斷線 (APIConnectionError) | 503 | retry（transient） |
| 其他 unexpected | 500 | log + alert、別自動 retry |

## Deploy targets

| Target | 適合 | 注意 |
|---|---|---|
| **Local uvicorn** | dev | 1 worker、不適 production |
| **Docker + uvicorn** | small prod | 加 `--workers N`、reverse proxy（nginx）前面 |
| **K8s** | scalable prod | liveness/readiness probe 用 `/health` |
| **AWS Lambda + API Gateway** | sporadic traffic | cold start 慢、適合輕量 agent |
| **Cloud Run / Fargate** | 中規模 prod | scale-to-zero、簡單 |
| **Anthropic Computer Use / Skills** | very specific use cases | 看 Stage 5 |

## 常見坑

- **沒 health check**：load balancer 不知道 instance 死了、流量繼續送
- **`/health` 太重**：去打 LLM 確認 = 耗 cost、且 cold start 慢就被踢
- **`request_id` 沒記**：trace 散在各 log 裡找不到對應
- **All errors → 500**：client 無法分辨 transient（retry）vs permanent（don't retry）。要分 status code
- **synchronous LLM call**：FastAPI 用 `def` 而非 `async def`、會 block event loop。Production 應該用 `async def` + `await client.messages.create(...)` 或 thread pool
- **No rate limiting**：被攻擊或 client bug 會打爆 LLM bill。前面加 `slowapi` / nginx rate limit
- **Hard-coded secret**：API key 直接寫 code = git 流出。用 env var + secret manager

## 接前面 stages

- **練習 3 observability**：把 `TraceContext` 加進 endpoint、每 request 記 latency / tokens / errors
- **練習 2 eval**：deploy 後跑 CI eval、`pass_rate < 90%` 就 rollback
- **練習 4 caching**：把 system prompt 加 `cache_control`、production cost 立刻減 90%
- **Stage 6 RAG**：endpoint 接 vector DB + memory store

## 延伸

- **加 streaming endpoint**：`@app.post("/chat/stream")` 配 `StreamingResponse` + SSE format
- **加 auth**：FastAPI `Depends(verify_token)` + JWT / API key
- **加 cost limit**：每 user / day 上限 X token、超過 reject
- **接 OpenTelemetry**：`tracer.start_as_current_span("chat_endpoint")` 自動丟去 Datadog
- **K8s manifests**：Deployment + Service + HPA + ConfigMap
