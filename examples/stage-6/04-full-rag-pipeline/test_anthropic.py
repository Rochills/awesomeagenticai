"""Stage 6 練習 4 — Path B 自我驗證（mock Anthropic client）。
"""

from __future__ import annotations

import sys
from types import SimpleNamespace
from unittest.mock import MagicMock

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from starter_anthropic import generate_anthropic


def make_anthropic_client(answer: str):
    client = MagicMock()
    block = SimpleNamespace(type="text", text=answer)
    client.messages.create.return_value = SimpleNamespace(content=[block])
    return client


def test_generate_anthropic_uses_context():
    client = make_anthropic_client("Python 3.11+.")
    answer = generate_anthropic("Python version?", ["We use Python 3.11+."], client=client)
    call_args = client.messages.create.call_args
    prompt = call_args.kwargs["messages"][0]["content"]
    assert "Python 3.11" in prompt
    assert answer == "Python 3.11+."
    print("✅ test_generate_anthropic_uses_context")


if __name__ == "__main__":
    test_generate_anthropic_uses_context()
    print("\n🎉 Path B mock test 通過")
