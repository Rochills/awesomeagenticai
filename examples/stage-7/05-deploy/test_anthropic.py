"""Stage 7 練習 5 — Anthropic FastAPI endpoint test。"""

from __future__ import annotations

import sys
from types import SimpleNamespace
from unittest.mock import MagicMock, patch

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import anthropic
from fastapi.testclient import TestClient

from starter_anthropic import app

client = TestClient(app)


def test_health_anthropic():
    r = client.get("/health")
    assert r.status_code == 200
    print("✅ test_health_anthropic")


def test_chat_anthropic_happy_path():
    fake_resp = SimpleNamespace(
        content=[SimpleNamespace(type="text", text="Hi!")],
        usage=SimpleNamespace(input_tokens=10, output_tokens=2),
    )
    with patch("starter_anthropic.anthropic.Anthropic") as mock_cls:
        mock_cls.return_value.messages.create.return_value = fake_resp
        r = client.post("/chat", json={"message": "hello"})
    assert r.status_code == 200
    body = r.json()
    assert body["answer"] == "Hi!"
    assert body["input_tokens"] == 10
    assert body["output_tokens"] == 2
    print("✅ test_chat_anthropic_happy_path")


def test_chat_anthropic_429_on_rate_limit():
    with patch("starter_anthropic.anthropic.Anthropic") as mock_cls:
        mock_cls.return_value.messages.create.side_effect = anthropic.RateLimitError(
            message="rate limited", response=MagicMock(status_code=429), body=None,
        )
        r = client.post("/chat", json={"message": "hi"})
    assert r.status_code == 429
    print("✅ test_chat_anthropic_429_on_rate_limit")


if __name__ == "__main__":
    test_health_anthropic()
    test_chat_anthropic_happy_path()
    test_chat_anthropic_429_on_rate_limit()
    print("\n🎉 通過 — Anthropic FastAPI endpoint 正確")
