"""Stage 7 練習 3：Observability — Path B（Anthropic、含 token usage 詳細）。

Anthropic SDK 的 resp.usage 欄位精確（input_tokens / output_tokens / cache_*）、
比 Ollama 完整。Production 用 Claude 通常 token tracking 更精準。

跑法：
    pip install -r requirements.txt
    export ANTHROPIC_API_KEY=sk-ant-...
    python starter_anthropic.py
"""

from __future__ import annotations

import os
import sys
import time
from typing import Any

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import anthropic

from starter import TraceContext, trace_span

MODEL = os.environ.get("MODEL", "claude-haiku-4-5")


def observable_agent_anthropic(question: str, ctx: TraceContext, client: Any = None) -> str:
    client = client or anthropic.Anthropic()
    with trace_span(ctx, "llm_call", model=MODEL):
        resp = client.messages.create(
            model=MODEL, max_tokens=300,
            messages=[{"role": "user", "content": question}],
        )
    # Anthropic usage 是精確的
    ctx.add_tokens(input_t=resp.usage.input_tokens, output_t=resp.usage.output_tokens)
    return " ".join(b.text for b in resp.content if b.type == "text")


if __name__ == "__main__":
    ctx = TraceContext(request_id=f"req_{int(time.time()*1000)}")
    answer = observable_agent_anthropic("What's 2+2?", ctx)
    print(f"answer: {answer}")
    print(f"trace: {ctx.summary()}")
    # Claude haiku ≈ $1/$5 per M tokens、簡單 query usage ≈ 10-30 token 雙向
    print(f"\n✅ 練習 3 (Anthropic) 通過 — token usage 精確、≈$0.0001/run")
