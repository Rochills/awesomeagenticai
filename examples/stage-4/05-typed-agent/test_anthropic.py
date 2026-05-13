"""Stage 4 練習 5 — Path B 載入檢查。

實測請跑 starter_anthropic.py 配 ANTHROPIC_API_KEY。
"""

from __future__ import annotations

import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def test_anthropic_model_importable():
    from pydantic_ai.models.anthropic import AnthropicModel
    assert AnthropicModel is not None
    print("✅ test_anthropic_model_importable")


def test_starter_anthropic_loadable():
    import starter_anthropic
    assert hasattr(starter_anthropic, "MODEL")
    assert "claude" in starter_anthropic.MODEL
    print("✅ test_starter_anthropic_loadable")


if __name__ == "__main__":
    test_anthropic_model_importable()
    test_starter_anthropic_loadable()
    print("\n🎉 通過 — Path B 可載入（實測需 ANTHROPIC_API_KEY）")
