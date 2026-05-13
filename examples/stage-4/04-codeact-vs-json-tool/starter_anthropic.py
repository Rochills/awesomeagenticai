"""Stage 4 練習 4：CodeAct（Smolagents）— Path B（Anthropic Claude via LiteLLM）。

Smolagents 的 LiteLLMModel 可以打 Claude，model_id 用 LiteLLM 格式。

跑法：
    pip install -r requirements.txt
    export ANTHROPIC_API_KEY=sk-ant-...
    python starter_anthropic.py

預算：CodeAct 通常多步、每次 ≈ $0.005-0.02（claude-haiku-4-5）。
Claude 寫 Python code 比 qwen2.5:3b 穩很多。
"""

from __future__ import annotations

import os
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from smolagents import LiteLLMModel

from starter import run

MODEL = os.environ.get("MODEL", "anthropic/claude-haiku-4-5")


if __name__ == "__main__":
    question = "Find Taipei population, divide by New York population, give the ratio."
    print(f"❓ Question: {question}（using Smolagents + Anthropic {MODEL}）")
    print("-" * 60)
    model = LiteLLMModel(model_id=MODEL)
    result = run(question, model=model)
    print(f"\n✅ Final: {result['final']}")
    assert result["final"]
    print("✅ 練習 4 (Anthropic path) 通過 — Claude 寫 Python code 比小 model 穩很多")
