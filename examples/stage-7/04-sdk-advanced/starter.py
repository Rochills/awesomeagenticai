"""Stage 7 練習 4：SDK 進階 — Path A（Ollama 默認、$0、streaming）。

Production agent 兩個必備 SDK 進階 feature：
1. **Streaming**：邊產 token 邊回 UI（user perception 從 5 秒 → 0.5 秒就看到 token）
2. **Prompt caching**：Anthropic-specific、重複 long context 省 90% cost（Path B 才有）

跑法：
    pip install -r requirements.txt
    ollama pull qwen2.5:3b
    ollama serve
    python starter.py
"""

from __future__ import annotations

import os
import sys
import time
from typing import Any, Iterator

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from openai import OpenAI

MODEL = os.environ.get("MODEL", "qwen2.5:3b")
OLLAMA_BASE = os.environ.get("OLLAMA_API_BASE", "http://localhost:11434/v1")


def stream_response(prompt: str, llm: Any = None) -> Iterator[str]:
    """Yield each token chunk as it arrives."""
    llm = llm or OpenAI(base_url=OLLAMA_BASE, api_key="ollama")
    stream = llm.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        stream=True,
    )
    for chunk in stream:
        delta = chunk.choices[0].delta.content
        if delta:
            yield delta


def stream_to_string(prompt: str, llm: Any = None) -> dict:
    """Helper：consume streaming generator + 統計 latency。"""
    t0 = time.perf_counter()
    first_token_at = None
    chunks = []
    for delta in stream_response(prompt, llm=llm):
        if first_token_at is None:
            first_token_at = time.perf_counter() - t0
        chunks.append(delta)
    total_latency = time.perf_counter() - t0
    return {
        "text": "".join(chunks),
        "first_token_ms": (first_token_at or 0) * 1000,
        "total_latency_ms": total_latency * 1000,
        "chunk_count": len(chunks),
    }


if __name__ == "__main__":
    prompt = "Explain what a Python list comprehension is in 3 sentences."
    print(f"❓ {prompt}\n")
    print("(streaming token by token...)\n")

    t0 = time.perf_counter()
    for delta in stream_response(prompt):
        print(delta, end="", flush=True)
    total = time.perf_counter() - t0

    print(f"\n\n📊 Total: {total:.2f}s")
    print(f"✅ 練習 4 通過 — streaming SDK 跑通、$0/run")
    print("   UX 觀察：streaming 讓 user 早在 0.3-1 秒就看到第一個 token，不必等完整答案")
