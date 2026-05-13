"""Stage 4 練習 1 CrewAI 對照版自我驗證。

只驗 import + tool function 邏輯。CrewAI 整個 Crew.kickoff() 太黑盒、不適合純 mock；
要實測請跑 starter_crewai.py 配 Ollama。
"""

from __future__ import annotations

import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from starter_crewai import search


def test_search_tool_basic():
    """CrewAI tool 包裝後仍可被 .run / .func 直接呼叫做單元測。"""
    fn = getattr(search, "func", None) or getattr(search, "run", None)
    if fn is None:
        print("⚠ CrewAI tool 介面變動、跳過 unit test")
        return
    assert "Taipei" in fn("Taipei")
    print("✅ test_search_tool_basic (CrewAI tool wrapper)")


def test_crewai_module_ok():
    import starter_crewai
    assert hasattr(starter_crewai, "build_crew")
    assert hasattr(starter_crewai, "MODEL")
    print("✅ test_crewai_module_ok")


if __name__ == "__main__":
    test_search_tool_basic()
    test_crewai_module_ok()
    print("\n🎉 通過 — CrewAI 對照版可載入（實測需要 Ollama 跑著）")
