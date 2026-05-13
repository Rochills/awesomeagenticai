"""練習 6：Schema 設計 — Bad schema（Path B、Anthropic Claude）。

故意保留 anti-pattern：description 太模糊、參數都用 string、沒有 required、沒有 enum。
模型很容易把溫度轉換誤判給 `process_data`。對照 `starter_good_anthropic.py`。

跑法：
    pip install -r requirements.txt
    export ANTHROPIC_API_KEY=sk-ant-...
    python starter_bad_anthropic.py

預算：每次 ≈ $0.0005（claude-haiku-4-5、單輪 call）。
Ollama 版本見 starter_bad.py。
"""

from __future__ import annotations

import os
import sys
from typing import Any

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import anthropic

MODEL = os.environ.get("MODEL", "claude-haiku-4-5")


def process_data(data: str = "") -> str:
    return f"processed generic data: {data}"


def convert_temperature(value: str = "") -> str:
    return f"converted something from: {value}"


TOOLS_SPEC = [
    {
        "name": "process_data",
        "description": "Process data.",
        "input_schema": {"type": "object", "properties": {"data": {"type": "string"}}},
    },
    {
        "name": "convert_temperature",
        "description": "Convert a value.",
        "input_schema": {"type": "object", "properties": {"value": {"type": "string"}, "unit": {"type": "string"}}},
    },
]

TOOL_IMPL = {
    "process_data": lambda i: process_data(i.get("data", "")),
    "convert_temperature": lambda i: convert_temperature(i.get("value", "")),
}


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
    assert result["tool"] is not None, "even bad schema should produce an observable selection"
    print("Stage 3 exercise 6 bad-schema starter check passed")
