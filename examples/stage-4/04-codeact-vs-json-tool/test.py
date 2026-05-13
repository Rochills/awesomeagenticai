"""Stage 4 練習 4 自我驗證 — CodeAct tool 邏輯 + agent 建構。

Smolagents 整個 agent.run() 會實際執行 Python code、純 mock 困難。
這份只驗：(1) tool function 邏輯、(2) build_agent 可建構、(3) max_steps 等預設正確。

要實測請跑 starter.py 配 Ollama。
"""

from __future__ import annotations

import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from starter import build_agent, calculator, lookup_fact


def test_calculator_basic():
    fn = getattr(calculator, "func", None) or getattr(calculator, "forward", None) or calculator
    # Smolagents @tool decorator wraps; the underlying callable can be reached via .forward or direct call
    try:
        result = fn("2 + 3") if callable(fn) and fn is not calculator else calculator("2 + 3")
    except TypeError:
        # If tool wrapper expects dict
        result = calculator(expression="2 + 3")
    assert "5" in str(result), f"expected 5, got {result}"
    print("✅ test_calculator_basic")


def test_calculator_rejects_injection():
    try:
        out = calculator(expression="__import__('os').system('ls')")
    except TypeError:
        out = calculator("__import__('os').system('ls')")
    assert "error" in str(out)
    print("✅ test_calculator_rejects_injection")


def test_lookup_fact_basic():
    try:
        out = lookup_fact(query="Taipei population")
    except TypeError:
        out = lookup_fact("Taipei population")
    assert "2602000" in str(out)
    print("✅ test_lookup_fact_basic")


def test_build_agent_ok():
    """確認 build_agent 能組出 CodeAgent、且 max_steps 預設合理。"""
    # 不真打 API：傳一個 mock model
    class FakeModel:
        def __call__(self, *a, **kw): return ""
    agent = build_agent(model=FakeModel())
    assert hasattr(agent, "run"), "expected CodeAgent.run method"
    assert agent.max_steps == 4, f"expected max_steps=4, got {agent.max_steps}"
    print("✅ test_build_agent_ok")


if __name__ == "__main__":
    test_calculator_basic()
    test_calculator_rejects_injection()
    test_lookup_fact_basic()
    test_build_agent_ok()
    print("\n🎉 通過 — Smolagents tool + agent 結構正確（實測需 Ollama）")
