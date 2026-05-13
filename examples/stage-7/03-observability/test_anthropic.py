"""Stage 7 練習 3 — Anthropic mock test。"""

from __future__ import annotations

import sys
from types import SimpleNamespace
from unittest.mock import MagicMock

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from starter import TraceContext
from starter_anthropic import observable_agent_anthropic


def test_observable_anthropic_records_precise_tokens():
    client = MagicMock()
    client.messages.create.return_value = SimpleNamespace(
        content=[SimpleNamespace(type="text", text="42")],
        usage=SimpleNamespace(input_tokens=15, output_tokens=2),
    )
    ctx = TraceContext("req_1")
    out = observable_agent_anthropic("2+2?", ctx, client=client)
    assert "42" in out
    assert ctx.total_tokens["input"] == 15
    assert ctx.total_tokens["output"] == 2
    print("✅ test_observable_anthropic_records_precise_tokens")


if __name__ == "__main__":
    test_observable_anthropic_records_precise_tokens()
    print("\n🎉 通過")
