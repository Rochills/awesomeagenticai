"""Stage 4 練習 3：圖式 workflow — LangGraph（Path B、概念展示）。

這個 starter 的 workflow 不打 LLM API（節點都是 deterministic 邏輯 / template）、
所以 Path A 跟 Path B **跑出來一樣**。重點是「**圖結構 + checkpointing + HITL**
邏輯本身**完全跨 backend**」。

實際 production 把 `respond_node` 換成真的 LLM call 即可——`ChatAnthropic(model="claude-haiku-4-5")`
或 `ChatOpenAI(base_url="...")` 都能塞進來。

跑法：
    pip install -r requirements.txt
    python starter_anthropic.py
"""

from __future__ import annotations

import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from starter import run

if __name__ == "__main__":
    print("ℹ️ 這份 workflow 不打 LLM、純展示 LangGraph 圖結構 + HITL。")
    print("   要在節點裡接 Anthropic Claude，把 respond_node 改成：")
    print('     from langchain_anthropic import ChatAnthropic')
    print('     llm = ChatAnthropic(model="claude-haiku-4-5")')
    print('     draft = llm.invoke(state["query"]).content')
    print("-" * 60)
    r = run("台北人口", approve=True)
    print(f"final: {r['final']}")
    assert r["final"]
    print("✅ 練習 3 (Anthropic concept) 通過 — 圖結構跨 backend 一致")
