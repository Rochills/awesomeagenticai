"""練習 4：多步驟推理任務 — Path B（Anthropic Claude）。

把練習 3 的 ReAct loop 延伸成 3-5 步任務：查台北人口 → 查紐約人口 → 相除 → 轉百分比。
工具負責執行小動作、LLM 負責規劃下一步。

跑法：
    pip install -r requirements.txt
    export ANTHROPIC_API_KEY=sk-ant-...
    python starter_anthropic.py

預算：每次 ≈ $0.005（claude-haiku-4-5、5 輪 messages 累積）。
Ollama 版本見 starter.py（本機 $0、但小 model 在多步任務上可能漏步）。
"""

from __future__ import annotations

import os
import sys
from typing import Any

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import anthropic

MODEL = os.environ.get("MODEL", "claude-haiku-4-5")


def lookup_population(city: str) -> str:
    data = {"taipei": 2_602_000, "new york": 8_336_000, "empty city": 0}
    return str(data.get(city.strip().lower(), 0))


def divide(a: float, b: float) -> str:
    b = float(b)
    return "0" if b == 0 else str(float(a) / b)


def to_percentage(ratio: float) -> str:
    return f"{float(ratio) * 100:.2f}"


def round_int(x: float) -> str:
    return str(round(float(x)))


TOOLS_SPEC = [
    {"name": "lookup_population", "description": "Return the population for a known city.", "input_schema": {"type": "object", "properties": {"city": {"type": "string"}}, "required": ["city"]}},
    {"name": "divide", "description": "Divide a by b. Returns 0 instead of crashing when b is zero.", "input_schema": {"type": "object", "properties": {"a": {"type": "number"}, "b": {"type": "number"}}, "required": ["a", "b"]}},
    {"name": "to_percentage", "description": "Convert a ratio such as 0.31 into a percentage number.", "input_schema": {"type": "object", "properties": {"ratio": {"type": "number"}}, "required": ["ratio"]}},
    {"name": "round_int", "description": "Round a number to the nearest integer.", "input_schema": {"type": "object", "properties": {"x": {"type": "number"}}, "required": ["x"]}},
]

TOOL_IMPL = {
    "lookup_population": lambda i: lookup_population(i["city"]),
    "divide": lambda i: divide(i["a"], i["b"]),
    "to_percentage": lambda i: to_percentage(i["ratio"]),
    "round_int": lambda i: round_int(i["x"]),
}


def react_loop(question: str, max_iter: int = 8, client: Any = None) -> dict:
    client = client or anthropic.Anthropic()
    messages = [{"role": "user", "content": question}]
    trace: list[dict] = []
    for step in range(max_iter):
        resp = client.messages.create(model=MODEL, max_tokens=1024, tools=TOOLS_SPEC, messages=messages)
        text = " ".join(getattr(b, "text", "") for b in resp.content if getattr(b, "type", None) == "text")
        calls = [b for b in resp.content if getattr(b, "type", None) == "tool_use"]
        messages.append({"role": "assistant", "content": resp.content})
        if resp.stop_reason == "end_turn" or not calls:
            trace.append({"step": step, "thought": text, "tool": None, "obs": None})
            return {"final": text, "trace": trace, "steps": step + 1}
        results = []
        for call in calls:
            args = dict(call.input)
            obs = TOOL_IMPL.get(call.name, lambda _: f"error: unknown tool {call.name}")(args)
            results.append({"type": "tool_result", "tool_use_id": call.id, "content": obs})
            trace.append({"step": step, "thought": text, "tool": call.name, "tool_input": args, "obs": obs})
        messages.append({"role": "user", "content": results})
    return {"final": None, "trace": trace, "steps": max_iter, "truncated": True}


if __name__ == "__main__":
    result = react_loop("Find Taipei population divided by New York population, then express it as a percentage.")
    print(result)

    # === 自我檢查 ===
    assert result["final"] is not None, "expected the loop to reach end_turn"
    assert any(str(n) in result["final"] for n in range(28, 35)), "expected a final answer near 31%"
    print("Stage 3 exercise 4 starter check passed")
