"""Stage 4 練習 5：型別安全 agent — Pydantic AI + Anthropic（Path B）。

Pydantic AI 對 Anthropic 是一級支援、用 'anthropic:claude-haiku-4-5' 字串即可建 model。

跑法：
    pip install -r requirements.txt
    export ANTHROPIC_API_KEY=sk-ant-...
    python starter_anthropic.py

預算：每次 ≈ $0.001（claude-haiku-4-5）。Claude 對 structured output 穩很多——
schema validation retry 機率小、實際 token 成本通常比 qwen2.5:3b 還少。
"""

from __future__ import annotations

import os
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from pydantic_ai.models.anthropic import AnthropicModel

from starter import run

MODEL = os.environ.get("MODEL", "claude-haiku-4-5")


if __name__ == "__main__":
    question = "What is the population of Taipei?"
    print(f"❓ Q: {question}（using Pydantic AI + Anthropic {MODEL}）")
    print("-" * 60)
    model = AnthropicModel(MODEL)
    answer = run(question, model=model)
    print(f"  answer:     {answer.answer}")
    print(f"  confidence: {answer.confidence}")
    print(f"  sources:    {answer.sources}")
    assert isinstance(answer.confidence, float)
    print("\n✅ 練習 5 (Anthropic path) 通過 — Claude structured output 穩、≈$0.001/run")
