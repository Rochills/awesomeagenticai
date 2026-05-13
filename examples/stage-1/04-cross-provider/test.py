"""
Stage 1 練習 4 自我驗證：用 mock 取代三家 SDK、不打 API。

驗證內容：
    - 沒設 key 的 provider 自動 skip、不會 crash
    - 設了 key 的 provider 正常 call、Reply dataclass 結構正確
    - 至少一家 provider 才能 pass
"""

from __future__ import annotations

import os
import sys
from unittest.mock import patch

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from starter import Reply, call_claude, call_openai, call_gemini, compare


def test_skip_when_no_key():
    """沒設任何 key 時、三個 call_xxx 都該回 None。"""
    with patch.dict(os.environ, {}, clear=True):
        assert call_claude("hi") is None
        assert call_openai("hi") is None
        assert call_gemini("hi") is None
    print("✅ test_skip_when_no_key")


def test_compare_returns_only_valid_replies():
    """compare() 跳過沒 key 的 provider、不會 raise。"""
    with patch.dict(os.environ, {}, clear=True):
        replies = compare("hi")
        assert replies == [], "沒任何 key 時、replies 應為空 list"
    print("✅ test_compare_returns_only_valid_replies")


def test_reply_dataclass_shape():
    """Reply 結構 ok。"""
    r = Reply(
        provider="X", model="x-1", text="hello",
        in_tokens=10, out_tokens=20, latency_ms=500,
    )
    assert r.provider == "X"
    assert r.in_tokens + r.out_tokens == 30
    print("✅ test_reply_dataclass_shape")


def test_compare_one_provider_set():
    """模擬：只設 ANTHROPIC_API_KEY、call_claude 被 mock 成回固定 Reply。"""
    fake_reply = Reply(
        provider="Anthropic", model="claude-haiku-4-5",
        text="AGI 跟 narrow AI 的差別…",
        in_tokens=20, out_tokens=50, latency_ms=800,
    )

    with patch.dict(os.environ, {"ANTHROPIC_API_KEY": "sk-fake"}, clear=True), \
         patch("starter.call_claude", return_value=fake_reply):
        replies = compare("test prompt")

    assert len(replies) == 1
    assert replies[0].provider == "Anthropic"
    assert replies[0].in_tokens == 20
    print("✅ test_compare_one_provider_set")


if __name__ == "__main__":
    test_skip_when_no_key()
    test_compare_returns_only_valid_replies()
    test_reply_dataclass_shape()
    test_compare_one_provider_set()
    print("\n🎉 全部通過 — Cross-provider 邏輯正確（skip-on-missing-key 已驗）")
