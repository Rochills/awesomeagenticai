"""Stage 7 練習 2：Eval — Path B（Claude）。

跟 starter.py 同流程、agent + judge 都用 Claude。

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

from starter import EVAL_CASES, eval_substring, run_eval

MODEL = os.environ.get("MODEL", "claude-haiku-4-5")


def agent_answer_anthropic(question: str, instruction: str = "", client: Any = None) -> str:
    client = client or anthropic.Anthropic()
    system = "Answer concisely (1-2 sentences). " + instruction
    resp = client.messages.create(
        model=MODEL, max_tokens=200, system=system,
        messages=[{"role": "user", "content": question}],
    )
    return " ".join(b.text for b in resp.content if b.type == "text")


if __name__ == "__main__":
    out = run_eval(EVAL_CASES, agent_answer_anthropic, eval_substring)
    for r in out["results"]:
        mark = "✅" if r["passed"] else "❌"
        print(f"   {mark} [{r['id']}] {r['output']}")
    print(f"\nPass: {out['pass_count']}/{out['total']} ({out['pass_rate']:.0%})")
    print(f"✅ 練習 2 (Anthropic) 通過 — {MODEL}、5 cases × ≈$0.0005 = ≈$0.003/run")
