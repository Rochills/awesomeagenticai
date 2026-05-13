"""Stage 7 練習 1：Multi-Agent 辯論 — Path B（Anthropic Claude）。

Multi-agent debate 對 model 質量敏感——3 個 agent 都要能持住自己的立場、Claude 比 qwen 穩。

跑法：
    pip install -r requirements.txt
    export ANTHROPIC_API_KEY=sk-ant-...
    python starter_anthropic.py
"""

from __future__ import annotations

import os
import sys
from typing import Any

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import anthropic

MODEL = os.environ.get("MODEL", "claude-haiku-4-5")


def llm_call_anthropic(system: str, user: str, client: Any = None) -> str:
    client = client or anthropic.Anthropic()
    resp = client.messages.create(
        model=MODEL, max_tokens=300, system=system,
        messages=[{"role": "user", "content": user}],
    )
    return " ".join(b.text for b in resp.content if b.type == "text")


def debate_anthropic(question: str, client: Any = None) -> dict:
    pro = llm_call_anthropic(
        "You argue the PRO position on the user's question. Be concise (2-3 sentences).",
        question, client=client,
    )
    con = llm_call_anthropic(
        "You argue the CON position on the user's question. Be concise (2-3 sentences).",
        question, client=client,
    )
    judge = llm_call_anthropic(
        "You are a neutral judge. Reply with: WINNER=PRO or WINNER=CON, then 1-sentence reasoning.",
        f"Question: {question}\n\nPRO: {pro}\n\nCON: {con}",
        client=client,
    )
    return {"question": question, "pro": pro, "con": con, "judge": judge}


if __name__ == "__main__":
    q = "Should small teams use a framework or build from scratch?"
    print(f"❓ {q}\n")
    r = debate_anthropic(q)
    for k in ("pro", "con", "judge"):
        print(f"{k.upper()}: {r[k]}\n")
    print(f"✅ 練習 1 (Anthropic) 通過 — Claude {MODEL}、≈$0.003/run（3 個 LLM call）")
