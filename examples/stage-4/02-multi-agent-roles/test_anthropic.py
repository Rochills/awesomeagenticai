"""Stage 4 練習 2 自我驗證 — Path B import + module-load check。

CrewAI multi-agent kickoff 太黑盒、純 mock 困難。實測請跑 starter_anthropic.py 配 ANTHROPIC_API_KEY。
"""

from __future__ import annotations

import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def test_starter_anthropic_loadable():
    import starter_anthropic
    assert hasattr(starter_anthropic, "MODEL")
    assert "anthropic/" in starter_anthropic.MODEL, f"預期 LiteLLM 格式 anthropic/...、得到 {starter_anthropic.MODEL}"
    print("✅ test_starter_anthropic_loadable")


def test_run_function_imported():
    """starter_anthropic 重用 starter.run，並注入 anthropic model name。"""
    from starter_anthropic import run
    assert callable(run)
    print("✅ test_run_function_imported")


if __name__ == "__main__":
    test_starter_anthropic_loadable()
    test_run_function_imported()
    print("\n🎉 通過 — Anthropic path 可載入（實測需 ANTHROPIC_API_KEY）")
