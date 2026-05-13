"""Stage 7 練習 1：Multi-Agent 辯論 — Path A（Ollama 默認、$0）。

2 個 agent 對同一個問題持相反立場辯論、第 3 個 judge agent 評分。
這個 pattern（debate / peer review）可以**降低單一 LLM 的 bias**——production
高賭注決策（policy / 醫療 / 法律 review）常用。

跑法：
    pip install -r requirements.txt
    ollama pull qwen2.5:3b
    ollama serve
    python starter.py
"""

from __future__ import annotations

import os
import sys
from typing import Any

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from openai import OpenAI

MODEL = os.environ.get("MODEL", "qwen2.5:3b")
OLLAMA_BASE = os.environ.get("OLLAMA_API_BASE", "http://localhost:11434/v1")


def llm_call(system: str, user: str, llm: Any = None) -> str:
    llm = llm or OpenAI(base_url=OLLAMA_BASE, api_key="ollama")
    resp = llm.chat.completions.create(
        model=MODEL,
        messages=[{"role": "system", "content": system}, {"role": "user", "content": user}],
    )
    return resp.choices[0].message.content or ""


def debate(question: str, llm: Any = None) -> dict:
    """3-agent debate：pro / con / judge。"""
    pro_argument = llm_call(
        system="You argue the PRO position on the user's question. Be concise (2-3 sentences).",
        user=question, llm=llm,
    )
    con_argument = llm_call(
        system="You argue the CON position on the user's question. Be concise (2-3 sentences).",
        user=question, llm=llm,
    )
    judge_verdict = llm_call(
        system="You are a neutral judge. Read both arguments below and pick the stronger one. "
               "Reply with: WINNER=PRO or WINNER=CON, then 1-sentence reasoning.",
        user=f"Question: {question}\n\nPRO: {pro_argument}\n\nCON: {con_argument}",
        llm=llm,
    )
    return {"question": question, "pro": pro_argument, "con": con_argument, "judge": judge_verdict}


if __name__ == "__main__":
    q = "Should small teams use a framework (LangGraph/CrewAI) or build agents from scratch?"
    print(f"❓ Question: {q}\n")
    result = debate(q)
    print(f"PRO:    {result['pro']}\n")
    print(f"CON:    {result['con']}\n")
    print(f"Judge:  {result['judge']}")
    assert "WINNER" in result["judge"].upper()
    print("\n✅ 練習 1 通過 — 3-agent debate 跑通、$0/run")
