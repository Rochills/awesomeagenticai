"""練習 6：Schema 設計 — Bad schema（Path A、Ollama 默認）。

故意保留 anti-pattern：description 太模糊、參數都用 string、沒有 required、沒有 enum。
小 model（qwen2.5:3b）對 schema 質量比大 model 更敏感——壞 schema 在 Claude haiku
上可能還能猜對、在 qwen2.5:3b 上幾乎必錯。對照 `starter_good.py`。

跑法：
    pip install -r requirements.txt
    ollama pull qwen2.5:3b
    ollama serve
    python starter_bad.py
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


def process_data(data: str = "") -> str:
    return f"processed generic data: {data}"


def convert_temperature(value: str = "") -> str:
    return f"converted something from: {value}"


# Anti-pattern: description 太短、params 都 string、無 required、無 enum
TOOLS_SPEC = [
    {
        "type": "function",
        "function": {
            "name": "process_data",
            "description": "Process data.",
            "parameters": {"type": "object", "properties": {"data": {"type": "string"}}},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "convert_temperature",
            "description": "Convert a value.",
            "parameters": {
                "type": "object",
                "properties": {"value": {"type": "string"}, "unit": {"type": "string"}},
            },
        },
    },
]

TOOL_IMPL = {
    "process_data": lambda i: process_data(i.get("data", "")),
    "convert_temperature": lambda i: convert_temperature(i.get("value", "")),
}


def select_and_run(question: str, client: Any = None) -> dict:
    client = client or OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")
    resp = client.chat.completions.create(
        model=MODEL,
        tools=TOOLS_SPEC,
        messages=[{"role": "user", "content": question}],
    )
    msg = resp.choices[0].message
    tool_calls = msg.tool_calls or []
    if not tool_calls:
        return {"tool": None, "tool_input": {}, "observation": None}
    call = tool_calls[0]
    args = json.loads(call.function.arguments)
    return {"tool": call.function.name, "tool_input": args, "observation": TOOL_IMPL[call.function.name](args)}


if __name__ == "__main__":
    question = "Convert 32 Celsius to Fahrenheit."
    print(f"❓ 問題：{question}（using Ollama {MODEL}、BAD schema）")
    result = select_and_run(question)
    print(f"   tool: {result['tool']}")
    print(f"   observation: {result['observation']}")

    # 寬鬆驗證：bad schema 不保證選對 tool、但至少要產出一個 tool call
    assert result["tool"] is not None, "even bad schema should produce an observable selection"
    if result["tool"] != "convert_temperature":
        print("⚠ 小 model + 壞 schema → 預期會挑錯。對照 starter_good.py 看修正後的差異")
    print("✅ Bad schema starter 跑通 — 對照 starter_good.py")
