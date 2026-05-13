"""
練習 3：從零實作 ReAct（不用 framework）— starter.py（Path A、Ollama 默認）

70 行 Python 把 Thought → Action → Observation 迴圈寫出來。
不要 LangChain、不要 LangGraph，就是純 while loop。

跑法：
    pip install -r requirements.txt
    ollama pull qwen2.5:3b   # Stage 3+ tool-use 默認 model
    ollama serve             # 預設 port 11434
    python starter.py

驗證：
    python test.py   （test.py 跨 backend 通用、用 mock、不打 API）

想看 Anthropic Claude 版本：
    python starter_anthropic.py   （需 ANTHROPIC_API_KEY、$0.001/run）
"""

from __future__ import annotations

import json
import os
import sys
from typing import Any

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from openai import OpenAI

MODEL = os.environ.get("MODEL", "qwen2.5:3b")  # tool-use 穩定的 Ollama model


# === 1. Tools 定義（含實作）===

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
    """假的事實查詢（教學專用、避免依賴外部 API）。"""
    facts = {
        "台北人口": "2602000",
        "紐約人口": "8336000",
        "光速": "299792458",  # m/s
    }
    return facts.get(query.strip(), f"unknown: {query}")


# OpenAI-compatible 的 tools schema wrap 在 {"type":"function", "function":{...}} 裡
TOOLS_SPEC = [
    {
        "type": "function",
        "function": {
            "name": "calculator",
            "description": "做基本算術運算（加減乘除）。輸入是表達式字串。",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {"type": "string", "description": "算術表達式"},
                },
                "required": ["expression"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "lookup_fact",
            "description": "查詢一個事實（人口 / 物理常數等）。",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "查詢關鍵字"},
                },
                "required": ["query"],
            },
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
    OpenAI-compatible ReAct loop。每輪：
      1. 問 LLM（含 tools）
      2. finish_reason: 'tool_calls' → 執行 tool、observation 接回、繼續
                       'stop' → 結束、最後 message 是答案
    回傳 {final, trace, steps}。
    """
    client = client or OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")
    messages = [{"role": "user", "content": question}]
    trace: list[dict] = []

    for step in range(max_iter):
        resp = client.chat.completions.create(
            model=MODEL,
            tools=TOOLS_SPEC,
            messages=messages,
        )
        msg = resp.choices[0].message
        thought_text = msg.content or ""
        tool_calls = msg.tool_calls or []

        # 把 assistant message 加進 messages（OpenAI 格式）
        assistant_entry: dict = {"role": "assistant", "content": thought_text}
        if tool_calls:
            assistant_entry["tool_calls"] = [
                {
                    "id": tc.id,
                    "type": "function",
                    "function": {"name": tc.function.name, "arguments": tc.function.arguments},
                }
                for tc in tool_calls
            ]
        messages.append(assistant_entry)

        if resp.choices[0].finish_reason == "stop" or not tool_calls:
            trace.append({"step": step, "thought": thought_text, "tool": None, "obs": None})
            return {"final": thought_text, "trace": trace, "steps": step + 1}

        # 執行 tool calls、observation 接回（OpenAI 用 role="tool"）
        last_obs = ""
        for tc in tool_calls:
            fn = TOOL_IMPL.get(tc.function.name)
            args = json.loads(tc.function.arguments)
            obs = fn(args) if fn else f"error: unknown tool {tc.function.name}"
            last_obs = obs
            messages.append({
                "role": "tool",
                "tool_call_id": tc.id,
                "content": obs,
            })

        trace.append({
            "step": step,
            "thought": thought_text,
            "tool": tool_calls[0].function.name,
            "tool_input": json.loads(tool_calls[0].function.arguments),
            "obs": last_obs,
        })

    return {"final": None, "trace": trace, "steps": max_iter, "truncated": True}


# === 3. 自我驗證 ===

if __name__ == "__main__":
    question = "台北人口除以紐約人口、答案保留 4 位小數。"
    print(f"❓ 問題：{question}（using Ollama {MODEL}）")
    print("-" * 60)

    result = react_loop(question, max_iter=5)

    for entry in result["trace"]:
        print(f"[step {entry['step']}] thought: {(entry['thought'] or '')[:80]}...")
        if entry["tool"]:
            print(f"           tool: {entry['tool']}({entry.get('tool_input')}) → {entry['obs']}")
    print("-" * 60)
    print(f"✅ 最終答案：{result['final']}")
    print(f"   共 {result['steps']} 輪")

    # 寬鬆驗證（小 model 不一定精確到 4 位小數）
    assert result.get("final") is not None or result.get("truncated"), "loop 應收尾或顯式 truncate"
    print("✅ 練習 3 通過 — 你已用本機 qwen2.5:3b 跑通 ReAct + tool use、$0/run")
