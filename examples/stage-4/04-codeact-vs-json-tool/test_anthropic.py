"""Stage 4 練習 4 — Path B 載入檢查。

Smolagents 整個 CodeAct 太重、純 mock 困難。實測請跑 starter_anthropic.py 配 ANTHROPIC_API_KEY。
"""

from __future__ import annotations

import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def test_litellm_model_importable():
    from smolagents import LiteLLMModel
    assert LiteLLMModel is not None
    print("✅ test_litellm_model_importable")


def test_starter_anthropic_loadable():
    import starter_anthropic
    assert hasattr(starter_anthropic, "MODEL")
    assert "anthropic/" in starter_anthropic.MODEL
    print("✅ test_starter_anthropic_loadable")


if __name__ == "__main__":
    test_litellm_model_importable()
    test_starter_anthropic_loadable()
    print("\n🎉 通過 — Path B 可載入（實測需 ANTHROPIC_API_KEY）")
