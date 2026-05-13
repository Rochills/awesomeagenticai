"""Stage 7 練習 3：Observability — Path A（Ollama 默認、$0）。

Production agent 必備 4 個 telemetry：
1. **Latency**：每個 LLM call 多久（追 p50/p95/p99）
2. **Token usage**：input / output / total tokens（追 cost）
3. **Trace**：multi-step agent 的每一步（debug + audit）
4. **Errors**：捕 exception + retry count

跑法：
    pip install -r requirements.txt
    ollama pull qwen2.5:3b
    ollama serve
    python starter.py
"""

from __future__ import annotations

import json
import logging
import os
import sys
import time
from contextlib import contextmanager
from typing import Any

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from openai import OpenAI

MODEL = os.environ.get("MODEL", "qwen2.5:3b")
OLLAMA_BASE = os.environ.get("OLLAMA_API_BASE", "http://localhost:11434/v1")

# Structured logger — production 應該寫去 cloud (Datadog / CloudWatch / Loki)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
)
logger = logging.getLogger("agent.observability")


# === 4 個 telemetry primitives ===

class TraceContext:
    """Per-request trace context. Production 通常用 OpenTelemetry。"""

    def __init__(self, request_id: str):
        self.request_id = request_id
        self.spans: list[dict] = []
        self.total_tokens = {"input": 0, "output": 0}
        self.errors: list[str] = []

    def add_span(self, name: str, latency_ms: float, **extras):
        span = {"name": name, "latency_ms": latency_ms, **extras}
        self.spans.append(span)
        logger.info(f"[{self.request_id}] span={name} ms={latency_ms:.1f} {json.dumps(extras)}")

    def add_tokens(self, input_t: int, output_t: int):
        self.total_tokens["input"] += input_t
        self.total_tokens["output"] += output_t

    def add_error(self, msg: str):
        self.errors.append(msg)
        logger.error(f"[{self.request_id}] error={msg}")

    def summary(self) -> dict:
        total_ms = sum(s["latency_ms"] for s in self.spans)
        return {
            "request_id": self.request_id,
            "total_latency_ms": total_ms,
            "span_count": len(self.spans),
            "input_tokens": self.total_tokens["input"],
            "output_tokens": self.total_tokens["output"],
            "error_count": len(self.errors),
        }


@contextmanager
def trace_span(ctx: TraceContext, name: str, **extras):
    """Context manager 計時 + 記 span。"""
    t0 = time.perf_counter()
    err = None
    try:
        yield
    except Exception as e:
        err = str(e)
        ctx.add_error(f"{name}: {err}")
        raise
    finally:
        latency_ms = (time.perf_counter() - t0) * 1000
        ctx.add_span(name, latency_ms, error=err, **extras)


# === Instrumented agent ===

def observable_agent(question: str, ctx: TraceContext, llm: Any = None) -> str:
    """LLM call wrapped in trace span + token logging。"""
    llm = llm or OpenAI(base_url=OLLAMA_BASE, api_key="ollama")

    with trace_span(ctx, "llm_call", model=MODEL):
        resp = llm.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": question}],
        )

    # Token usage（OpenAI / Ollama 都有 usage 欄位、不一定每個 Ollama 版本支援）
    usage = getattr(resp, "usage", None)
    if usage:
        ctx.add_tokens(
            input_t=getattr(usage, "prompt_tokens", 0),
            output_t=getattr(usage, "completion_tokens", 0),
        )

    return resp.choices[0].message.content or ""


def multi_step_agent(question: str, llm: Any = None) -> dict:
    """模擬 multi-step agent：search → reason → answer、每步 traced。"""
    ctx = TraceContext(request_id=f"req_{int(time.time()*1000)}")

    with trace_span(ctx, "search"):
        time.sleep(0.05)  # simulate tool call latency
        search_result = "Fake search result for: " + question

    answer = observable_agent(f"Based on '{search_result}', answer: {question}", ctx, llm=llm)

    return {
        "answer": answer,
        "trace_summary": ctx.summary(),
        "spans": ctx.spans,
    }


if __name__ == "__main__":
    print("Running instrumented agent...\n")
    result = multi_step_agent("What's 2+2?")
    print(f"\n📊 Trace summary:")
    for k, v in result["trace_summary"].items():
        print(f"   {k}: {v}")
    print(f"\n📝 Spans:")
    for s in result["spans"]:
        print(f"   {s['name']}: {s['latency_ms']:.1f}ms")

    assert result["trace_summary"]["span_count"] >= 2  # search + llm_call
    print(f"\n✅ 練習 3 通過 — 觀察 4 個 telemetry primitive、$0/run")
