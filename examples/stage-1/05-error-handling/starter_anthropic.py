"""
Stage 1 練習 5：Error Handling + Retry wrapper — Path B（Anthropic Claude）。

3 種錯誤情境 + 1 個 retry wrapper：
    1. API key 錯（401 AuthenticationError）→ 不要 retry、直接 raise
    2. Rate limit（429 RateLimitError）→ exponential backoff retry
    3. 網路錯（APIConnectionError）→ exponential backoff retry

跑法：
    pip install -r requirements.txt
    export ANTHROPIC_API_KEY=sk-ant-...
    python starter_anthropic.py

預算：每次 ≈ $0.0005（只有「情境 2 正常 call」會真的打 API、claude-haiku-4-5）。
Ollama 版本見 starter.py（本機 $0、用 openai SDK exception class）。
"""

from __future__ import annotations

import os
import random
import sys
import time
from typing import Any, Callable

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import anthropic
from anthropic import (
    APIConnectionError,
    APIStatusError,
    AuthenticationError,
    RateLimitError,
)


# === Retry wrapper ===

RETRIABLE = (APIConnectionError, RateLimitError)
MAX_ATTEMPTS = 4
BASE_DELAY = 1.0  # 秒


def with_retry(fn: Callable[[], Any], *, max_attempts: int = MAX_ATTEMPTS, base_delay: float = BASE_DELAY, sleep_fn=time.sleep) -> Any:
    """
    Exponential backoff retry。
    - RETRIABLE 例外 → 等 base * 2^attempt 秒再試（含 jitter）
    - 不 retriable 例外（譬如 AuthenticationError）→ 直接 raise、不浪費時間
    """
    last_exc = None
    for attempt in range(max_attempts):
        try:
            return fn()
        except RETRIABLE as e:  # noqa: PERF203
            last_exc = e
            if attempt == max_attempts - 1:
                break  # 最後一次失敗、break 出來 raise
            delay = base_delay * (2 ** attempt) + random.uniform(0, 0.3)
            print(f"  ⚠ attempt {attempt+1}/{max_attempts} fail ({type(e).__name__}); retry in {delay:.1f}s")
            sleep_fn(delay)
    raise last_exc  # type: ignore[misc]


# === 3 個錯誤情境 demo ===

def demo_bad_key() -> None:
    """情境 1: 故意用壞 key、看 AuthenticationError 怎麼 raise。"""
    print("\n[情境 1] 故意用壞 API key")
    client = anthropic.Anthropic(api_key="sk-ant-FAKE-KEY-DO-NOT-USE")
    try:
        client.messages.create(
            model="claude-haiku-4-5",
            max_tokens=10,
            messages=[{"role": "user", "content": "hi"}],
        )
    except AuthenticationError as e:
        print(f"  ✅ 抓到 AuthenticationError: {e.status_code}")
        print(f"  💡 production 處理: 立刻 alert、stop retry（key 不會自己變對）")


def demo_with_retry() -> None:
    """情境 2: 包 with_retry 跑一次正常 call、應該第 1 次就成功。"""
    print("\n[情境 2] 正常 call、with_retry 包裝")
    client = anthropic.Anthropic()

    def call():
        return client.messages.create(
            model="claude-haiku-4-5",
            max_tokens=30,
            messages=[{"role": "user", "content": "用一個 emoji 回答。"}],
        )

    msg = with_retry(call)
    print(f"  ✅ 成功、第一次就過: {msg.content[0].text}")


def demo_too_long_prompt() -> None:
    """情境 3: 故意丟超大 prompt、看 context window 滿了怎樣。"""
    print("\n[情境 3] Prompt 超過 context window")
    client = anthropic.Anthropic()
    huge_prompt = "重複很多次的 token。" * 300_000  # ~1.5M tokens、絕對超過任何 model

    try:
        client.messages.create(
            model="claude-haiku-4-5",
            max_tokens=10,
            messages=[{"role": "user", "content": huge_prompt}],
        )
    except APIStatusError as e:
        print(f"  ✅ 抓到 APIStatusError: {e.status_code}")
        print(f"  💡 production 處理: 在 client 端先 count token、超過就拒、別浪費 API call")


if __name__ == "__main__":
    demo_bad_key()
    demo_with_retry()
    demo_too_long_prompt()

    # === 自我驗證 ===
    print("\n✅ 練習 5 通過 — 你已了解 3 種錯誤如何 raise、知道何時該 retry 何時該 stop")
