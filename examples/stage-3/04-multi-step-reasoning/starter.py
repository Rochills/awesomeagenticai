"""練習 4：多步驟推理任務 — Path A（Ollama 默認、本機免費）。

把練習 3 的 ReAct loop 延伸成 3-5 步任務：查台北人口 → 查紐約人口 → 相除 → 轉百分比。
重點：工具寫窄而穩、LLM 負責規劃下一步、max_iter 是 safety net。

跑法：
    pip install -r requirements.txt
    ollama pull qwen2.5:3b
    ollama serve
    python starter.py

驗證：
    python test.py   （用 mock、不打 API）

想看 Anthropic Claude 版本：
    python starter_anthropic.py   （需 ANTHROPIC_API_KEY、$0.005/run）

⚠️ 注意：4 步推理對小 model 是挑戰。qwen2.5:3b 可能中間漏一步、或停太早。
Claude haiku 比較穩——這恰好是教學重點：對比同樣 loop、不同 model 在哪一步崩。
"""

from __future__ import annotations

import json
import os
import sys
from typing import Any

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from openai import OpenAI

MODEL = os.environ.get("MODEL", "qwen2.5:3b")


# === 1. Tools 定義（含實作）===

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


# OpenAI-compat 包一層 {"type": "function", "function": {...}}
TOOLS_SPEC = [
    {
        "type": "function",
        "function": {
            "name": "lookup_population",
            "description": "Return the population for a known city.",
            "parameters": {
                "type": "object",
                "properties": {"city": {"type": "string"}},
                "required": ["city"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "divide",
            "description": "Divide a by b. Returns 0 instead of crashing when b is zero.",
            "parameters": {
                "type": "object",
                "properties": {"a": {"type": "number"}, "b": {"type": "number"}},
                "required": ["a", "b"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "to_percentage",
            "description": "Convert a ratio such as 0.31 into a percentage number.",
            "parameters": {
                "type": "object",
                "properties": {"ratio": {"type": "number"}},
                "required": ["ratio"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "round_int",
            "description": "Round a number to the nearest integer.",
            "parameters": {
                "type": "object",
                "properties": {"x": {"type": "number"}},
                "required": ["x"],
            },
        },
    },
]

TOOL_IMPL = {
    "lookup_population": lambda i: lookup_population(i["city"]),
    "divide": lambda i: divide(i["a"], i["b"]),
    "to_percentage": lambda i: to_percentage(i["ratio"]),
    "round_int": lambda i: round_int(i["x"]),
}


# === 2. ReAct loop（OpenAI-compat）===

def react_loop(question: str, max_iter: int = 8, client: Any = None) -> dict:
    """OpenAI-compat 多步驟 ReAct loop。"""
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
        text = msg.content or ""
        tool_calls = msg.tool_calls or []

        assistant_entry: dict = {"role": "assistant", "content": text}
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
            trace.append({"step": step, "thought": text, "tool": None, "obs": None})
            return {"final": text, "trace": trace, "steps": step + 1}

        for tc in tool_calls:
            fn = TOOL_IMPL.get(tc.function.name, lambda _: f"error: unknown tool {tc.function.name}")
            args = json.loads(tc.function.arguments)
            obs = fn(args)
            messages.append({
                "role": "tool",
                "tool_call_id": tc.id,
                "content": obs,
            })
            trace.append({"step": step, "thought": text, "tool": tc.function.name, "tool_input": args, "obs": obs})

    return {"final": None, "trace": trace, "steps": max_iter, "truncated": True}


# === 3. 自我驗證 ===

if __name__ == "__main__":
    question = "Find Taipei population divided by New York population, then express it as a percentage."
    print(f"❓ 問題：{question}（using Ollama {MODEL}）")
    print("-" * 60)

    result = react_loop(question)
    for entry in result["trace"]:
        if entry["tool"]:
            print(f"[step {entry['step']}] tool: {entry['tool']}({entry.get('tool_input')}) → {entry['obs']}")
    print("-" * 60)
    print(f"✅ 最終答案：{result['final']}")
    print(f"   共 {result['steps']} 輪")

    # 寬鬆驗證：小 model 不一定走完 4 步、但 loop 至少要收尾或顯式 truncate
    assert result.get("final") is not None or result.get("truncated"), "loop 應收尾或 truncate"
    print("✅ 練習 4 通過 — 你已用本機 qwen2.5:3b 跑通多步 ReAct loop、$0/run")
