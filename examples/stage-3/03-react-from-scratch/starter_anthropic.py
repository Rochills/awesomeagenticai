"""
練習 3：從零實作 ReAct（不用 framework）— starter.py

目的：用 ~70 行 Python 把 Thought → Action → Observation 迴圈寫出來。
不要 LangChain、不要 LangGraph，就是純 while loop。

跑法：
    pip install -r requirements.txt
    export ANTHROPIC_API_KEY=sk-ant-...
    python starter.py

驗證：
    python test.py  （用 mock、不花 API 錢）
"""

from __future__ import annotations

import json
import os
import sys
from typing import Any

# Windows cp950 console 無法印 emoji / 中文、強制 UTF-8
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import anthropic

MODEL = os.environ.get("MODEL", "claude-haiku-4-5")  # 想換 sonnet 改這行

# === 1. Tools 定義（含實作） ===

def tool_calculator(expression: str) -> str:
    """安全的計算器：只允許 + - * / 跟數字。"""
    allowed = set("0123456789.+-*/() ")
    if any(c not in allowed for c in expression):
        return f"error: 表達式含不允許字元（{expression}）"
    try:
        return str(eval(expression))  # noqa: S307 — 已用 whitelist
    except Exception as e:  # noqa: BLE001
        return f"error: {e}"


def tool_lookup_fact(query: str) -> str:
    """假的事實查詢（避免依賴外部 API、教學專用）。"""
    facts = {
        "台北人口": "2602000",
        "紐約人口": "8336000",
        "光速": "299792458",  # m/s
    }
    return facts.get(query.strip(), f"unknown: {query}")


TOOLS_SPEC = [
    {
        "name": "calculator",
        "description": "做基本算術運算（加減乘除）。輸入是表達式字串，例如 '3 * (5+2)'。",
        "input_schema": {
            "type": "object",
            "properties": {
                "expression": {"type": "string", "description": "算術表達式"},
            },
            "required": ["expression"],
        },
    },
    {
        "name": "lookup_fact",
        "description": "查詢一個事實（人口 / 物理常數等）。輸入是查詢關鍵字、回傳一個字串答案或 'unknown: ...'。",
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "查詢關鍵字（如「台北人口」、「光速」）"},
            },
            "required": ["query"],
        },
    },
]

TOOL_IMPL = {
    "calculator": lambda inp: tool_calculator(inp["expression"]),
    "lookup_fact": lambda inp: tool_lookup_fact(inp["query"]),
}


# === 2. ReAct loop ===

def react_loop(question: str, max_iter: int = 6, client: Any = None) -> dict:
    """
    純 while 迴圈、每輪：
      1. 問 LLM（含 tools）
      2. 看 stop_reason：tool_use → 執行工具、把結果加進 messages、繼續
                       end_turn → 完成、回傳最終答案
    回傳 {final, trace}。trace 紀錄每輪 (thought, tool, obs)。
    """
    client = client or anthropic.Anthropic()
    messages = [{"role": "user", "content": question}]
    trace: list[dict] = []

    for step in range(max_iter):
        resp = client.messages.create(
            model=MODEL,
            max_tokens=1024,
            tools=TOOLS_SPEC,
            messages=messages,
        )

        # 收 thought（assistant 的 text block）跟 tool call
        thought_text = " ".join(b.text for b in resp.content if b.type == "text")
        tool_calls = [b for b in resp.content if b.type == "tool_use"]

        # 把 assistant 整個 response 加進 messages（給下一輪 context）
        messages.append({"role": "assistant", "content": resp.content})

        if resp.stop_reason == "end_turn" or not tool_calls:
            # 已收尾、最後一段 text 就是答案
            trace.append({"step": step, "thought": thought_text, "tool": None, "obs": None})
            return {"final": thought_text, "trace": trace, "steps": step + 1}

        # 執行所有 tool call、把 observation 接回去
        tool_results = []
        last_obs = ""
        for call in tool_calls:
            fn = TOOL_IMPL.get(call.name)
            obs = fn(call.input) if fn else f"error: unknown tool {call.name}"
            last_obs = obs
            tool_results.append({"type": "tool_result", "tool_use_id": call.id, "content": obs})
        messages.append({"role": "user", "content": tool_results})

        trace.append({
            "step": step,
            "thought": thought_text,
            "tool": tool_calls[0].name,
            "tool_input": dict(tool_calls[0].input),
            "obs": last_obs,
        })

    # 跑滿 max_iter 還沒收尾
    return {"final": None, "trace": trace, "steps": max_iter, "truncated": True}


# === 3. 自我驗證（跑真 API） ===

if __name__ == "__main__":
    question = "台北人口除以紐約人口、答案保留 4 位小數。"
    print(f"❓ 問題：{question}")
    print("-" * 60)

    result = react_loop(question, max_iter=5)

    for entry in result["trace"]:
        print(f"[step {entry['step']}] thought: {entry['thought'][:80]}...")
        if entry["tool"]:
            print(f"           tool: {entry['tool']}({entry.get('tool_input')}) → {entry['obs']}")
    print("-" * 60)
    print(f"✅ 最終答案：{result['final']}")
    print(f"   共 {result['steps']} 輪")

    # === 自我驗證 ===
    assert result.get("final") is not None, "預期 react_loop 在 max_iter 內收尾"
    assert "0.3" in (result["final"] or ""), f"預期答案含 0.3xxx（2602000/8336000≈0.3122）"
    print("✅ 練習 3 通過 — ReAct loop 自己連用了 lookup_fact 跟 calculator")
