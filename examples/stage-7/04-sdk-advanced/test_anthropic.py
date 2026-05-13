"""Stage 7 練習 4 — Anthropic streaming + cached_query mock."""

from __future__ import annotations

import sys
from types import SimpleNamespace
from unittest.mock import MagicMock

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from starter_anthropic import cached_query, stream_anthropic


def test_stream_anthropic_yields_text():
    """Mock Anthropic streaming context manager."""
    stream_obj = MagicMock()
    stream_obj.text_stream = iter(["Hello", " world"])
    stream_obj.__enter__ = MagicMock(return_value=stream_obj)
    stream_obj.__exit__ = MagicMock(return_value=False)

    client = MagicMock()
    client.messages.stream.return_value = stream_obj

    out = list(stream_anthropic("hi", client=client))
    assert out == ["Hello", " world"]
    print("✅ test_stream_anthropic_yields_text")


def test_cached_query_passes_cache_control():
    """確認 cache_control 真的傳進去 system param。"""
    client = MagicMock()
    client.messages.create.return_value = SimpleNamespace(
        content=[SimpleNamespace(type="text", text="ok")],
        usage=SimpleNamespace(
            input_tokens=10, output_tokens=2,
            cache_creation_input_tokens=2000, cache_read_input_tokens=0,
        ),
    )
    result = cached_query("Q?", "big system prompt", client=client)
    call_kwargs = client.messages.create.call_args.kwargs
    system_arg = call_kwargs["system"]
    assert isinstance(system_arg, list)
    assert system_arg[0]["cache_control"] == {"type": "ephemeral"}
    assert result["cache_creation_input_tokens"] == 2000
    print("✅ test_cached_query_passes_cache_control")


if __name__ == "__main__":
    test_stream_anthropic_yields_text()
    test_cached_query_passes_cache_control()
    print("\n🎉 通過 — streaming + caching API contract 正確")
