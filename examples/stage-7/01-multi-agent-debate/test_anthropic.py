"""Stage 7 練習 1 — Anthropic mock test。"""

from __future__ import annotations

import sys
from types import SimpleNamespace
from unittest.mock import MagicMock

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from starter_anthropic import debate_anthropic


def test_debate_anthropic_3_calls():
    client = MagicMock()
    responses = ["pro", "con", "WINNER=CON. Better reasoning."]
    client.messages.create.side_effect = [
        SimpleNamespace(content=[SimpleNamespace(type="text", text=r)]) for r in responses
    ]
    result = debate_anthropic("Q?", client=client)
    assert client.messages.create.call_count == 3
    assert "WINNER=CON" in result["judge"]
    print("✅ test_debate_anthropic_3_calls")


if __name__ == "__main__":
    test_debate_anthropic_3_calls()
    print("\n🎉 通過")
