"""練習 6：Schema 設計 — Good schema（Path A、Ollama 默認）。

清楚的工具用途、正確型別、必填欄位與 enum 收斂。小 model（qwen2.5:3b）也能穩定
選到 `convert_temperature`。對照 `starter_bad.py`。

跑法：
    pip install -r requirements.txt
    ollama pull qwen2.5:3b
    ollama serve
    python starter_good.py
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


def process_data(data: list[dict], operation: str) -> dict:
    if operation == "count_rows":
        return {"rows": len(data)}
    if operation == "list_columns":
        return {"columns": sorted({key for row in data for key in row})}
    return {"error": "unknown operation", "retry_hint": "use count_rows or list_columns"}


def convert_temperature(value: float, unit: str) -> dict:
    if unit == "celsius":
        return {"value": round(value * 9 / 5 + 32, 2), "unit": "fahrenheit"}
    if unit == "fahrenheit":
        return {"value": round((value - 32) * 5 / 9, 2), "unit": "celsius"}
    return {"error": "unsupported unit", "retry_hint": "unit must be celsius or fahrenheit"}


# Good schema: 用途明確、正確型別、required、enum
TOOLS_SPEC = [
    {
        "type": "function",
        "function": {
            "name": "process_data",
            "description": "Use only to summarize structured JSON table rows. Do not use for temperature conversion.",
            "parameters": {
                "type": "object",
                "properties": {
                    "data": {"type": "array", "items": {"type": "object"}, "description": "Rows to inspect"},
                    "operation": {"type": "string", "enum": ["count_rows", "list_columns"]},
                },
                "required": ["data", "operation"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "convert_temperature",
            "description": "Use this when the user asks to convert temperatures between Fahrenheit and Celsius.",
            "parameters": {
                "type": "object",
                "properties": {
                    "value": {"type": "number", "description": "Temperature value to convert"},
                    "unit": {"type": "string", "enum": ["celsius", "fahrenheit"], "description": "Unit of the input value"},
                },
                "required": ["value", "unit"],
            },
        },
    },
]

TOOL_IMPL = {
    "process_data": lambda i: process_data(i["data"], i["operation"]),
    "convert_temperature": lambda i: convert_temperature(i["value"], i["unit"]),
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
    print(f"❓ 問題：{question}（using Ollama {MODEL}、GOOD schema）")
    result = select_and_run(question)
    print(f"   tool: {result['tool']}")
    print(f"   tool_input: {result.get('tool_input')}")
    print(f"   observation: {result['observation']}")

    assert result["tool"] == "convert_temperature", f"預期 convert_temperature、得到 {result['tool']}"
    print("✅ Good schema starter 通過 — qwen2.5:3b 在清楚的 schema 上穩定挑對 tool、$0/run")
