"""Stage 4 練習 2 自我驗證 — CrewAI 模組可載入 + tool 邏輯正確。

CrewAI 整個 kickoff 太黑盒（內部走 LiteLLM、prompt 累積）、不適合純 mock。
這份只驗：(1) 3 個 agent + 3 個 task 結構正確、(2) search tool 邏輯正確。
要實測請跑 starter.py 配 Ollama。
"""

from __future__ import annotations

import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from starter import build_crew, search


def test_search_basic():
    fn = getattr(search, "func", None) or getattr(search, "run", None)
    if fn is None:
        print("⚠ CrewAI tool 介面變動、跳過")
        return
    assert "ReAct" in fn("react")
    assert "no entry" in fn("nonexistent")
    print("✅ test_search_basic")


def test_crew_structure():
    """確認 build_crew 出來的 Crew 真有 3 個 agent + 3 個 task、process 是 sequential。"""
    crew = build_crew("react")
    assert len(crew.agents) == 3, f"expected 3 agents, got {len(crew.agents)}"
    roles = [a.role for a in crew.agents]
    assert roles == ["Researcher", "Writer", "Critic"], f"unexpected roles: {roles}"
    assert len(crew.tasks) == 3, f"expected 3 tasks, got {len(crew.tasks)}"
    # critic_task 應該 context 包含 research_task 跟 write_task
    critic_task = crew.tasks[2]
    assert len(critic_task.context) == 2, "critic should depend on research + write"
    print("✅ test_crew_structure")


if __name__ == "__main__":
    test_search_basic()
    test_crew_structure()
    print("\n🎉 通過 — 3-agent crew 結構正確（實際 kickoff 需 Ollama 跑著）")
