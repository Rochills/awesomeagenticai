"""Stage 4 練習 3 自我驗證 — LangGraph workflow（無 LLM、純圖邏輯）。

跑法：
    python test.py

驗證內容：
    - classify_node 正確判斷 needs_search
    - 條件分支正確 routing（search vs respond 兩條路）
    - HITL：interrupt_before=['final'] + update_state(approved=...) 起作用
    - approve=True → PUBLISHED、approve=False → REJECTED
"""

from __future__ import annotations

import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from starter import classify_node, run, search_node, should_search


def test_classify_needs_search():
    assert classify_node({"query": "台北人口"})["needs_search"] is True
    assert classify_node({"query": "解釋一下 Python"})["needs_search"] is False
    assert classify_node({"query": "current weather"})["needs_search"] is True
    print("✅ test_classify_needs_search")


def test_search_node():
    out = search_node({"query": "taipei population"})
    assert "2.6M" in out["search_result"]
    out2 = search_node({"query": "unknown topic"})
    assert "no data" in out2["search_result"]
    print("✅ test_search_node")


def test_should_search_routing():
    assert should_search({"needs_search": True}) == "search"
    assert should_search({"needs_search": False}) == "respond"
    print("✅ test_should_search_routing")


def test_hitl_approve_true_publishes():
    """搜尋路徑 + 人類 approve=True → PUBLISHED。"""
    result = run("台北人口", approve=True)
    assert "PUBLISHED" in result["final"]
    assert "2.6M" in result["draft"]  # draft 引用了 search result
    print("✅ test_hitl_approve_true_publishes")


def test_hitl_approve_false_rejects():
    """非搜尋路徑 + 人類 approve=False → REJECTED。"""
    result = run("解釋 Python", approve=False)
    assert "REJECTED" in result["final"]
    assert "Direct answer" in result["draft"]
    print("✅ test_hitl_approve_false_rejects")


def test_branching_skips_search():
    """非搜尋路徑時、search_result 應該不存在或空。"""
    result = run("解釋 Python", approve=True)
    assert not result.get("search_result"), f"預期無 search_result、得到 {result.get('search_result')}"
    print("✅ test_branching_skips_search")


if __name__ == "__main__":
    test_classify_needs_search()
    test_search_node()
    test_should_search_routing()
    test_hitl_approve_true_publishes()
    test_hitl_approve_false_rejects()
    test_branching_skips_search()
    print("\n🎉 全部通過 — LangGraph 圖結構 + 條件分支 + HITL 邏輯正確")
