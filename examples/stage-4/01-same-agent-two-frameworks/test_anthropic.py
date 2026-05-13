"""Stage 4 練習 1 自我驗證 — Path B（Anthropic starter_anthropic.py）。

starter_anthropic.py 只是換 LLM backend、不改 build_graph 邏輯，所以共用 test.py 的測試。
這份只多驗：ChatAnthropic 可以被 build_graph 接受（不打 API、純 import 檢查）。
"""

from __future__ import annotations

import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def test_anthropic_import_ok():
    """ChatAnthropic import 通過、無需 API key（建構式不打 API）。"""
    from langchain_anthropic import ChatAnthropic
    assert ChatAnthropic is not None
    print("✅ test_anthropic_import_ok")


def test_starter_anthropic_module_ok():
    """starter_anthropic 模組可被 import、function 都存在。"""
    import starter_anthropic
    assert hasattr(starter_anthropic, "MODEL")
    print("✅ test_starter_anthropic_module_ok")


if __name__ == "__main__":
    test_anthropic_import_ok()
    test_starter_anthropic_module_ok()
    print("\n🎉 通過 — starter_anthropic.py 可載入（實際跑需要 ANTHROPIC_API_KEY）")
