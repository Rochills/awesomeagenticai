"""練習 6：Schema 設計 — Good schema（Path B、Anthropic Claude）。

清楚的工具用途、正確型別、必填欄位與 enum 收斂。模型穩定選到 `convert_temperature`。
對照 `starter_bad_anthropic.py`。

跑法：
    pip install -r requirements.txt
    export ANTHROPIC_API_KEY=sk-ant-...
    python starter_good_anthropic.py

預算：每次 ≈ $0.0005（claude-haiku-4-5、單輪 call）。
Ollama 版本見 starter_good.py。
"""

from __future__ import annotations

import os, sys
from typing import Any

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import anthropic

MODEL = os.environ.get("MODEL", "claude-haiku-4-5")


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


TOOLS_SPEC = [
    {
        "name": "process_data",
        "description": "Use only to summarize structured JSON table rows. Do not use for temperature conversion.",
        "input_schema": {
            "type": "object",
            "properties": {
                "data": {"type": "array", "items": {"type": "object"}, "description": "Rows to inspect"},
                "operation": {"type": "string", "enum": ["count_rows", "list_columns"]},
            },
            "required": ["data", "operation"],
        },
    },
    {
        "name": "convert_temperature",
        "description": "Use this when the user asks to convert temperatures between Fahrenheit and Celsius.",
        "input_schema": {
            "type": "object",
            "properties": {
                "value": {"type": "number", "description": "Temperature value to convert"},
                "unit": {"type": "string", "enum": ["celsius", "fahrenheit"], "description": "Unit of the input value"},
            },
            "required": ["value", "unit"],
        },
    },
]

TOOL_IMPL = {"process_data": lambda i: process_data(i["data"], i["operation"]), "convert_temperature": lambda i: convert_temperature(i["value"], i["unit"])}


def select_and_run(question: str, client: Any = None) -> dict:
    client = client or anthropic.Anthropic()
    resp = client.messages.create(model=MODEL, max_tokens=512, tools=TOOLS_SPEC, messages=[{"role": "user", "content": question}])
    calls = [b for b in resp.content if getattr(b, "type", None) == "tool_use"]
    if not calls:
        return {"tool": None, "tool_input": {}, "observation": None}
    call = calls[0]
    args = dict(call.input)
    return {"tool": call.name, "tool_input": args, "observation": TOOL_IMPL[call.name](args)}


if __name__ == "__main__":
    result = select_and_run("Convert 32 Celsius to Fahrenheit.")
    print(result)
    # === 自我檢查 ===
    assert result["tool"] == "convert_temperature", f"expected convert_temperature, got {result['tool']}"
    print("Stage 3 exercise 6 good-schema starter check passed")
