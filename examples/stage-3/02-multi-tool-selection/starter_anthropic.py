"""練習 2：多工具選擇 — Path B（Anthropic Claude）。

讓 Claude 在 3 個 tool（web_search / calculator / calendar_lookup）裡選一個執行。
重點：tool schema 的 description 越精準、模型選對的機率越高。

跑法：
    pip install -r requirements.txt
    export ANTHROPIC_API_KEY=sk-ant-...
    python starter_anthropic.py

預算：每次 ≈ $0.0005（claude-haiku-4-5、單輪 call）。
Ollama 版本見 starter.py（本機 $0）。
"""

from __future__ import annotations

import os
import sys
from typing import Any

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import anthropic

MODEL = os.environ.get("MODEL", "claude-haiku-4-5")


def web_search(query: str) -> str:
    return f"search result: {query} -> Anthropic tool use docs and examples"


def calculator(expression: str) -> str:
    allowed = set("0123456789.+-*/() ")
    if any(ch not in allowed for ch in expression):
        return "error: calculator only accepts basic arithmetic"
    try:
        return str(eval(expression, {"__builtins__": {}}, {}))  # noqa: S307
    except Exception as exc:  # noqa: BLE001
        return f"error: {exc}"


def calendar_lookup(date: str) -> str:
    events = {"2026-05-13": "10:00 Stage 3 review, 15:00 agent study group", "tomorrow": "10:00 Stage 3 review, 15:00 agent study group"}
    return events.get(date.strip(), f"no events found for {date}")


def tool_schema(name: str, description: str, field: str, field_description: str) -> dict:
    return {"name": name, "description": description, "input_schema": {"type": "object", "properties": {field: {"type": "string", "description": field_description}}, "required": [field]}}


TOOLS_SPEC = [
    tool_schema("web_search", "Search current or external information not in the prompt.", "query", "Search query"),
    tool_schema("calculator", "Evaluate basic arithmetic with +, -, *, /, and parentheses.", "expression", "Math expression"),
    tool_schema("calendar_lookup", "Look up events for a specific date or relative day.", "date", "Date to inspect"),
]

TOOL_IMPL = {
    "web_search": lambda args: web_search(args["query"]),
    "calculator": lambda args: calculator(args["expression"]),
    "calendar_lookup": lambda args: calendar_lookup(args["date"]),
}


def run_tool_selection(question: str, client: Any = None) -> dict:
    client = client or anthropic.Anthropic()
    resp = client.messages.create(
        model=MODEL,
        max_tokens=512,
        tools=TOOLS_SPEC,
        messages=[{"role": "user", "content": question}],
    )
    text = " ".join(getattr(b, "text", "") for b in resp.content if getattr(b, "type", None) == "text")
    tool_calls = [b for b in resp.content if getattr(b, "type", None) == "tool_use"]
    if not tool_calls:
        return {"tool": None, "thought": text, "observation": None}
    call = tool_calls[0]
    args = dict(call.input)
    observation = TOOL_IMPL.get(call.name, lambda _: f"error: unknown tool {call.name}")(args)
    return {"tool": call.name, "tool_input": args, "thought": text, "observation": observation}


if __name__ == "__main__":
    result = run_tool_selection("What is (19 * 42) - 8? Use the best available tool.")
    print(result)

    # === 自我檢查 ===
    assert result["tool"] == "calculator", f"expected calculator, got {result['tool']}"
    assert result["observation"] and not result["observation"].startswith("error:")
    print("Stage 3 exercise 2 starter check passed")
