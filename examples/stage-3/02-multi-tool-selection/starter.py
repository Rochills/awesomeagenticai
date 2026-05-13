"""練習 2：多工具選擇 — Path A（Ollama 默認、本機免費）。

讓本機 qwen2.5:3b 在 3 個 tool（web_search / calculator / calendar_lookup）裡選一個。
重點不是工具強不強，是觀察 schema 的 description / 參數 / required 如何引導模型選對。

跑法：
    pip install -r requirements.txt
    ollama pull qwen2.5:3b   # Stage 3+ tool-use 默認 model
    ollama serve             # 預設 port 11434
    python starter.py

驗證：
    python test.py   （用 mock、不打 API）

想看 Anthropic Claude 版本：
    python starter_anthropic.py   （需 ANTHROPIC_API_KEY、$0.0005/run）
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
    events = {
        "2026-05-13": "10:00 Stage 3 review, 15:00 agent study group",
        "tomorrow": "10:00 Stage 3 review, 15:00 agent study group",
    }
    return events.get(date.strip(), f"no events found for {date}")


# OpenAI-compat 的 tools schema 要包一層 {"type": "function", "function": {...}}
def _wrap(name: str, description: str, field: str, field_description: str) -> dict:
    return {
        "type": "function",
        "function": {
            "name": name,
            "description": description,
            "parameters": {
                "type": "object",
                "properties": {field: {"type": "string", "description": field_description}},
                "required": [field],
            },
        },
    }


TOOLS_SPEC = [
    _wrap("web_search", "Search current or external information not in the prompt.", "query", "Search query"),
    _wrap("calculator", "Evaluate basic arithmetic with +, -, *, /, and parentheses.", "expression", "Math expression"),
    _wrap("calendar_lookup", "Look up events for a specific date or relative day.", "date", "Date to inspect"),
]

TOOL_IMPL = {
    "web_search": lambda args: web_search(args["query"]),
    "calculator": lambda args: calculator(args["expression"]),
    "calendar_lookup": lambda args: calendar_lookup(args["date"]),
}


# === 2. 單輪 tool selection ===

def run_tool_selection(question: str, client: Any = None) -> dict:
    """單輪 call：LLM 看完 question + tools 後選一個 tool 呼叫，本地執行 observation 接回去。"""
    client = client or OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")
    resp = client.chat.completions.create(
        model=MODEL,
        tools=TOOLS_SPEC,
        messages=[{"role": "user", "content": question}],
    )
    msg = resp.choices[0].message
    text = msg.content or ""
    tool_calls = msg.tool_calls or []
    if not tool_calls:
        return {"tool": None, "thought": text, "observation": None}
    call = tool_calls[0]
    args = json.loads(call.function.arguments)
    fn = TOOL_IMPL.get(call.function.name, lambda _: f"error: unknown tool {call.function.name}")
    return {"tool": call.function.name, "tool_input": args, "thought": text, "observation": fn(args)}


# === 3. 自我驗證 ===

if __name__ == "__main__":
    question = "What is (19 * 42) - 8? Use the best available tool."
    print(f"❓ 問題：{question}（using Ollama {MODEL}）")
    result = run_tool_selection(question)
    print(f"   tool: {result['tool']}")
    print(f"   tool_input: {result.get('tool_input')}")
    print(f"   observation: {result['observation']}")

    assert result["tool"] == "calculator", f"預期 calculator、得到 {result['tool']}"
    assert result["observation"] and not result["observation"].startswith("error:")
    print("✅ 練習 2 通過 — 你已用本機 qwen2.5:3b 跑通 multi-tool selection、$0/run")
