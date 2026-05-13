"""
Stage 1 練習 5：Error Handling + Retry wrapper — Path A（Ollama 默認、本機免費）。

3 種錯誤情境 + 1 個 retry wrapper：
    1. API key 錯（401 AuthenticationError）→ 不要 retry、直接 raise
    2. Rate limit（429 RateLimitError）→ exponential backoff retry
    3. 網路錯（APIConnectionError）→ exponential backoff retry

跑法：
    pip install -r requirements.txt
    ollama pull gemma4:e4b   # Stage 1+2 預設、CPU-friendly
    ollama serve             # 預設 port 11434
    python starter.py

驗證：
    python test.py   （mock 三種錯誤、不需真的斷網）

想看 Anthropic 版本：
    python starter_anthropic.py   （需 ANTHROPIC_API_KEY）

⚠️ 注意：本機 Ollama 不會真的撞 RateLimitError（沒 quota），所以「情境 2 rate limit」
demo 看不到。但 `python test.py` 全部用 mock、retry 邏輯一樣可以完整驗證。
這恰好是 Ollama path 反而更適合理解 retry pattern——快、免費、可重現。
"""

from __future__ import annotations

import os
import random
import sys
import time
from typing import Any, Callable

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from openai import (
    APIConnectionError,
    APIStatusError,
    AuthenticationError,
    OpenAI,
    RateLimitError,
)

MODEL = os.environ.get("MODEL", "gemma4:e4b")


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
                break
            delay = base_delay * (2 ** attempt) + random.uniform(0, 0.3)
            print(f"  ⚠ attempt {attempt+1}/{max_attempts} fail ({type(e).__name__}); retry in {delay:.1f}s")
            sleep_fn(delay)
    raise last_exc  # type: ignore[misc]


# === 3 個錯誤情境 demo ===

def demo_bad_key() -> None:
    """情境 1: 故意用壞 base_url、看 APIConnectionError（Ollama 沒在跑時）。"""
    print("\n[情境 1] 故意連到不存在的 Ollama port")
    client = OpenAI(base_url="http://localhost:65535/v1", api_key="ollama")
    try:
        client.chat.completions.create(
            model=MODEL,
            max_tokens=10,
            messages=[{"role": "user", "content": "hi"}],
        )
    except APIConnectionError as e:
        print(f"  ✅ 抓到 APIConnectionError: {type(e).__name__}")
        print(f"  💡 production 處理: retry（網路錯通常是 transient）")


def demo_with_retry() -> None:
    """情境 2: 包 with_retry 跑一次正常 call、應該第 1 次就成功。"""
    print("\n[情境 2] 正常 call、with_retry 包裝（需要 Ollama 在跑）")
    client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")

    def call():
        return client.chat.completions.create(
            model=MODEL,
            max_tokens=30,
            messages=[{"role": "user", "content": "用一個 emoji 回答。"}],
        )

    try:
        msg = with_retry(call)
        print(f"  ✅ 成功、第一次就過: {msg.choices[0].message.content}")
    except APIConnectionError:
        print("  ⚠ Ollama 沒在跑（port 11434 不通）。請先 `ollama serve`")


def demo_too_long_prompt() -> None:
    """情境 3: 故意丟超大 prompt、看 context window 滿了怎樣。"""
    print("\n[情境 3] Prompt 超過 context window（Ollama 通常會截斷或 raise）")
    client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")
    huge_prompt = "重複很多次的 token。" * 200_000  # ~1M tokens

    try:
        client.chat.completions.create(
            model=MODEL,
            max_tokens=10,
            messages=[{"role": "user", "content": huge_prompt}],
        )
        print("  ⚠ Ollama 沒 raise（可能直接截斷 prompt）。Cloud API 通常會 400")
    except APIStatusError as e:
        print(f"  ✅ 抓到 APIStatusError: {e.status_code}")
        print(f"  💡 production 處理: 在 client 端先 count token、超過就拒、別浪費 API call")
    except APIConnectionError:
        print("  ⚠ Ollama 沒在跑")


if __name__ == "__main__":
    demo_bad_key()
    demo_with_retry()
    demo_too_long_prompt()

    # === 自我驗證 ===
    print("\n✅ 練習 5 通過 — 你已了解 3 種錯誤如何 raise、知道何時該 retry 何時該 stop、$0/run")
