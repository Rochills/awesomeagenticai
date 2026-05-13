"""Stage 7 練習 5 自我驗證 — FastAPI endpoint + error handling。
"""

from __future__ import annotations

import sys
from types import SimpleNamespace
from unittest.mock import MagicMock, patch

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from fastapi.testclient import TestClient
from openai import APIConnectionError

from starter import app, agent_call

client = TestClient(app)


def test_health_endpoint():
    r = client.get("/health")
    assert r.status_code == 200
    body = r.json()
    assert body["status"] == "ok"
    assert "model" in body
    print("✅ test_health_endpoint")


def test_chat_endpoint_happy_path():
    """Mock 上游 LLM、確認 /chat 回 ChatResponse shape。"""
    fake_resp = SimpleNamespace(
        choices=[SimpleNamespace(message=SimpleNamespace(content="Hello!"))]
    )
    with patch("starter.OpenAI") as mock_openai:
        mock_openai.return_value.chat.completions.create.return_value = fake_resp
        r = client.post("/chat", json={"message": "hi"})
    assert r.status_code == 200
    body = r.json()
    assert body["answer"] == "Hello!"
    assert "request_id" in body
    assert body["latency_ms"] >= 0
    print("✅ test_chat_endpoint_happy_path")


def test_chat_returns_503_on_upstream_unavailable():
    """模擬 Ollama down、回 503 而非 500。"""
    with patch("starter.OpenAI") as mock_openai:
        mock_openai.return_value.chat.completions.create.side_effect = APIConnectionError(
            request=MagicMock()
        )
        r = client.post("/chat", json={"message": "hi"})
    assert r.status_code == 503
    assert "unavailable" in r.json()["detail"].lower()
    print("✅ test_chat_returns_503_on_upstream_unavailable")


def test_chat_validates_input_schema():
    """缺 message field、應該 422 Unprocessable Entity（FastAPI 自動驗 Pydantic schema）。"""
    r = client.post("/chat", json={})
    assert r.status_code == 422
    print("✅ test_chat_validates_input_schema")


def test_agent_call_unit():
    """agent_call function 單元測試（無 HTTP）。"""
    fake_resp = SimpleNamespace(
        choices=[SimpleNamespace(message=SimpleNamespace(content="ok"))]
    )
    llm = MagicMock()
    llm.chat.completions.create.return_value = fake_resp
    out = agent_call("hi", max_tokens=100, llm=llm)
    assert out == "ok"
    print("✅ test_agent_call_unit")


if __name__ == "__main__":
    test_health_endpoint()
    test_chat_endpoint_happy_path()
    test_chat_returns_503_on_upstream_unavailable()
    test_chat_validates_input_schema()
    test_agent_call_unit()
    print("\n🎉 全部通過 — FastAPI agent endpoint 邏輯正確")
