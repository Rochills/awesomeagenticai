"""Stage 4 練習 3：圖式 workflow — LangGraph + Ollama（Path A、默認）。

LangGraph 最拿手：條件分支 + human-in-the-loop + checkpointing。

任務：「研究 → 寫稿 → 人類審核 → 發佈」
- classify_node 看 query 決定 search_needed
- 條件分支：need_search=True → search_node、否則直接 respond_node
- HITL：respond_node 前 interrupt、等人類 approve
- final_node 標記完成

跑法：
    pip install -r requirements.txt
    ollama pull qwen2.5:3b
    ollama serve
    python starter.py

驗證：
    python test.py
"""

from __future__ import annotations

import os
import sys
from typing import Any, Literal

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import END, START, StateGraph
from typing_extensions import TypedDict

MODEL = os.environ.get("MODEL", "qwen2.5:3b")


class State(TypedDict):
    query: str
    needs_search: bool
    search_result: str
    draft: str
    approved: bool
    final: str


# === Nodes ===

def classify_node(state: State) -> dict:
    """看 query 決定要不要 search。簡化邏輯：含關鍵字「人口 / 天氣 / 最新」就 search。"""
    q = state["query"].lower()
    needs = any(k in q for k in ["人口", "weather", "天氣", "latest", "最新", "current"])
    return {"needs_search": needs}


def search_node(state: State) -> dict:
    db = {
        "taipei": "Taipei population ~2.6M (2024)",
        "台北": "Taipei population ~2.6M (2024)",
        "weather": "sunny 25°C",
        "天氣": "sunny 25°C",
    }
    q = state["query"].lower()
    for k, v in db.items():
        if k in q:
            return {"search_result": v}
    return {"search_result": "no data"}


def respond_node(state: State) -> dict:
    """寫 draft。實際用 LLM，這裡簡化用 template 演示流程。"""
    if state.get("search_result"):
        return {"draft": f"Based on search: {state['search_result']}"}
    return {"draft": f"Direct answer to: {state['query']}"}


def final_node(state: State) -> dict:
    if state.get("approved"):
        return {"final": f"PUBLISHED: {state['draft']}"}
    return {"final": f"REJECTED (human said no): {state['draft']}"}


def should_search(state: State) -> Literal["search", "respond"]:
    return "search" if state["needs_search"] else "respond"


# === Graph build ===

def build_graph(checkpointer: Any = None) -> Any:
    g = StateGraph(State)
    g.add_node("classify", classify_node)
    g.add_node("search", search_node)
    g.add_node("respond", respond_node)
    g.add_node("final", final_node)

    g.add_edge(START, "classify")
    g.add_conditional_edges("classify", should_search, {"search": "search", "respond": "respond"})
    g.add_edge("search", "respond")
    g.add_edge("respond", "final")
    g.add_edge("final", END)

    # HITL：在 final 之前 interrupt、讓人類在 state 改 approved
    return g.compile(checkpointer=checkpointer, interrupt_before=["final"])


def run(query: str, approve: bool = True) -> dict:
    """跑一輪含 HITL 的 workflow。`approve` 模擬人類審核決定。"""
    checkpointer = InMemorySaver()
    graph = build_graph(checkpointer=checkpointer)
    config = {"configurable": {"thread_id": "demo"}}

    # 第一段：跑到 final 之前停（interrupt_before=["final"]）
    state_before = graph.invoke({"query": query, "approved": False}, config=config)
    print(f"   draft（等待 approval）: {state_before.get('draft', '<none>')}")

    # HITL：人類審核——更新 state.approved
    graph.update_state(config, {"approved": approve})

    # 第二段：繼續跑完
    state_after = graph.invoke(None, config=config)
    return state_after


if __name__ == "__main__":
    print(f"❓ Workflow: classify → [search?] → respond → [HITL] → final（using {MODEL}）")
    print("-" * 60)

    print("\n[Case 1] query 含「台北人口」、需要 search、人類 approve=True")
    r1 = run("台北人口是多少？", approve=True)
    print(f"   final: {r1['final']}")
    assert "PUBLISHED" in r1["final"]

    print("\n[Case 2] query 不需 search、人類 approve=False")
    r2 = run("解釋一下 Python 是什麼", approve=False)
    print(f"   final: {r2['final']}")
    assert "REJECTED" in r2["final"]

    print("\n✅ 練習 3 通過 — LangGraph 圖式 workflow + HITL checkpoint、$0/run")
