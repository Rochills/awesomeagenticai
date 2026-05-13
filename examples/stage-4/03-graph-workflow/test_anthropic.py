"""Stage 4 練習 3 — Path B 概念展示：圖結構跨 backend 一致。

跑法：python test_anthropic.py

這份只是 starter.py / test.py 的 Path B variant 確認——workflow 不依賴 LLM SDK、
所以兩條 path 跑出來一致。實際 production 在節點接 Claude 時、只改 respond_node。
"""

from __future__ import annotations

import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from starter_anthropic import run


def test_concept_workflow_runs():
    result = run("台北人口", approve=True)
    assert "PUBLISHED" in result["final"]
    print("✅ test_concept_workflow_runs")


def test_starter_anthropic_module_ok():
    import starter_anthropic
    assert hasattr(starter_anthropic, "run")
    print("✅ test_starter_anthropic_module_ok")


if __name__ == "__main__":
    test_concept_workflow_runs()
    test_starter_anthropic_module_ok()
    print("\n🎉 通過 — Path B concept demo 跑通")
