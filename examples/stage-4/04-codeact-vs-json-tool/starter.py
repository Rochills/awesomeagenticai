"""Stage 4 練習 4：CodeAct（Smolagents）vs JSON tool — Path A（Ollama 默認）。

CodeAct pattern：agent 產生 Python 程式碼當 action（不是 JSON tool call）。
HuggingFace Smolagents 是這條路線的代表——LLM 寫 `result = calculator(...)` 一句一句執行。

跟練習 1 / 3 用的 JSON tool 路線對照：
- JSON tool: LLM 回 `{"name": "calculator", "arguments": {"expression": "..."}}`
- CodeAct:   LLM 回 ```python\nresult = calculator(expression="...")\nprint(result)\n```

跑法：
    pip install -r requirements.txt
    ollama pull qwen2.5:3b
    ollama serve
    python starter.py

驗證：
    python test.py

⚠️ 注意：Smolagents 對小 model 比較吃力（要產正確 Python syntax）。
qwen2.5:3b 可能會產出有 syntax error 的 code、agent 自己迭代修。Claude 較穩。
"""

from __future__ import annotations

import os
import sys
from typing import Any

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from smolagents import CodeAgent, OpenAIServerModel, tool

MODEL = os.environ.get("MODEL", "qwen2.5:3b")
OLLAMA_BASE = os.environ.get("OLLAMA_API_BASE", "http://localhost:11434/v1")


# === Tools ===

@tool
def calculator(expression: str) -> str:
    """Safe arithmetic calculator (whitelist + - * / parentheses).

    Args:
        expression: Arithmetic expression to evaluate, e.g. '2 + 3 * (4 - 1)'.
    """
    allowed = set("0123456789.+-*/() ")
    if any(c not in allowed for c in expression):
        return "error: only basic arithmetic allowed"
    try:
        return str(eval(expression, {"__builtins__": {}}, {}))  # noqa: S307
    except Exception as e:  # noqa: BLE001
        return f"error: {e}"


@tool
def lookup_fact(query: str) -> str:
    """Look up a fact (population / physical constants, etc.).

    Args:
        query: Fact key to look up, e.g. 'taipei population' or 'speed of light'.
    """
    db = {
        "taipei population": "2602000",
        "new york population": "8336000",
        "speed of light": "299792458",
    }
    return db.get(query.strip().lower(), f"unknown: {query}")


def build_agent(model: Any = None) -> CodeAgent:
    model = model or OpenAIServerModel(
        model_id=MODEL, api_base=OLLAMA_BASE, api_key="ollama",
    )
    return CodeAgent(tools=[calculator, lookup_fact], model=model, max_steps=4)


def run(question: str, model: Any = None) -> dict:
    agent = build_agent(model=model)
    result = agent.run(question)
    return {"final": str(result)}


if __name__ == "__main__":
    question = "Find Taipei population, divide by New York population, give the ratio."
    print(f"❓ Question: {question}（using Smolagents + Ollama {MODEL}）")
    print("   CodeAct pattern: agent will WRITE PYTHON CODE that calls tools")
    print("-" * 60)
    result = run(question)
    print(f"\n✅ Final: {result['final']}")
    assert result["final"], "expected non-empty answer"
    print("✅ 練習 4 通過 — Smolagents CodeAct、$0/run")
    print("   對照練習 1 / 3 的 JSON tool 寫法、看兩種路線怎麼解同題")
