"""Stage 6 練習 3 — Path B concept demo 載入檢查。"""

from __future__ import annotations

import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def test_loadable():
    import starter_anthropic
    assert hasattr(starter_anthropic, "compare_strategies")
    print("✅ test_loadable")


if __name__ == "__main__":
    test_loadable()
    print("\n🎉 通過")
