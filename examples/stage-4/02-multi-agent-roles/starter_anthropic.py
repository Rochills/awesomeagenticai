"""Stage 4 練習 2：多 agent 角色分配 — CrewAI + Anthropic（Path B）。

CrewAI 用 LiteLLM 底層、改成 "anthropic/claude-haiku-4-5" 字串即可切 backend。

跑法：
    pip install -r requirements.txt
    export ANTHROPIC_API_KEY=sk-ant-...
    python starter_anthropic.py

預算：3 agent × 短輸出 ≈ $0.005-0.01/run。Claude 對 multi-agent 互動穩很多。
"""

from __future__ import annotations

import os
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from starter import run

MODEL = os.environ.get("MODEL", "anthropic/claude-haiku-4-5")  # LiteLLM 格式


if __name__ == "__main__":
    topic = "react"
    print(f"❓ Topic: {topic}（using CrewAI + Anthropic {MODEL}）")
    print(f"   3 agents: Researcher → Writer → Critic（sequential）")
    print("-" * 60)
    result = run(topic, llm_model=MODEL)
    print(f"✅ Final (critic's verdict):\n{result['final']}")
    assert result["final"], "expected critic to produce a verdict"
    print("\n✅ 練習 2 (Anthropic path) 通過 — Claude 跑 3-agent crew、≈$0.005-0.01/run")
