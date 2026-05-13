"""Stage 7 練習 4：SDK 進階 — Path B（Anthropic streaming + prompt caching）。

Anthropic 額外的兩個 production 殺手 feature：
1. **Streaming**：跟 OpenAI 類似、但 content blocks 結構不同
2. **Prompt caching**：cache_control={"type": "ephemeral"}、重複 long context（system / tools）
   省 90% cost。第一次寫入有 25% premium、之後 5 分鐘內每次省 90%。

跑法：
    pip install -r requirements.txt
    export ANTHROPIC_API_KEY=sk-ant-...
    python starter_anthropic.py
"""

from __future__ import annotations

import os
import sys
import time
from typing import Any, Iterator

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import anthropic

MODEL = os.environ.get("MODEL", "claude-haiku-4-5")


def stream_anthropic(prompt: str, client: Any = None) -> Iterator[str]:
    client = client or anthropic.Anthropic()
    with client.messages.stream(
        model=MODEL,
        max_tokens=300,
        messages=[{"role": "user", "content": prompt}],
    ) as stream:
        for text in stream.text_stream:
            yield text


def cached_query(question: str, large_system_prompt: str, client: Any = None) -> dict:
    """示範 prompt caching：第一次 call 沒 cache、第二次 hit cache、看 usage 差異。"""
    client = client or anthropic.Anthropic()

    resp = client.messages.create(
        model=MODEL,
        max_tokens=200,
        system=[
            {
                "type": "text",
                "text": large_system_prompt,
                "cache_control": {"type": "ephemeral"},   # ← key
            }
        ],
        messages=[{"role": "user", "content": question}],
    )

    usage = resp.usage
    return {
        "answer": " ".join(b.text for b in resp.content if b.type == "text"),
        "input_tokens": usage.input_tokens,
        "cache_creation_input_tokens": getattr(usage, "cache_creation_input_tokens", 0),
        "cache_read_input_tokens": getattr(usage, "cache_read_input_tokens", 0),
        "output_tokens": usage.output_tokens,
    }


if __name__ == "__main__":
    # Demo 1: streaming
    print("=== Streaming demo ===")
    print("(token by token...)\n")
    t0 = time.perf_counter()
    for delta in stream_anthropic("Explain Python list comprehension in 3 sentences."):
        print(delta, end="", flush=True)
    print(f"\n[took {time.perf_counter()-t0:.2f}s]\n")

    # Demo 2: prompt caching（同 system prompt 2 次、第二次省 90% input cost）
    print("=== Prompt caching demo ===")
    big_system = "You are a helpful assistant. " + ("This is reference material. " * 200)  # ~2000 tokens
    r1 = cached_query("What's 2+2?", big_system)
    print(f"Call 1 (cache miss): input={r1['input_tokens']}, cache_create={r1['cache_creation_input_tokens']}, cache_read={r1['cache_read_input_tokens']}")
    r2 = cached_query("What's 3+3?", big_system)
    print(f"Call 2 (cache hit):  input={r2['input_tokens']}, cache_create={r2['cache_creation_input_tokens']}, cache_read={r2['cache_read_input_tokens']}")

    if r2["cache_read_input_tokens"] > 0:
        print(f"\n✅ Cache 命中！第二次只算 {r2['input_tokens']} input + {r2['cache_read_input_tokens']} cache-read（cache-read 只算 10% 價）")
    print(f"\n✅ 練習 4 (Anthropic) 通過 — streaming + prompt caching、Claude {MODEL}")
