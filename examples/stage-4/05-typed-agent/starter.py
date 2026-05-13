"""Stage 4 練習 5：型別安全 agent — Pydantic AI + Ollama（Path A、默認）。

Pydantic AI 把「structured output」變成型別系統的一級成員：
- Agent 回傳必須 conform to Pydantic model
- runtime validation 自動跑（譬如 confidence 必須是 float、不是 string）
- 失敗時 LLM 會被告知 schema、retry 再 produce

任務：問問題、agent 回 `{"answer": str, "confidence": float, "sources": [str]}`。

跑法：
    pip install -r requirements.txt
    ollama pull qwen2.5:3b
    ollama serve
    python starter.py

驗證：
    python test.py

⚠️ 注意：Pydantic AI 對 model 的 instruction following 要求高。
qwen2.5:3b 可能多 retry 才產對 schema、Claude haiku 通常一次過。
"""

from __future__ import annotations

import os
import sys
from typing import Any

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from pydantic import BaseModel, Field
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider

MODEL = os.environ.get("MODEL", "qwen2.5:3b")
OLLAMA_BASE = os.environ.get("OLLAMA_API_BASE", "http://localhost:11434/v1")


# === Schema：agent 強制要回這個 shape ===

class AnswerWithConfidence(BaseModel):
    """Structured answer the agent must produce."""
    answer: str = Field(description="The actual answer text.")
    confidence: float = Field(ge=0.0, le=1.0, description="Confidence score 0-1.")
    sources: list[str] = Field(description="Sources or references used.")


def build_agent(model: Any = None) -> Agent:
    if model is None:
        model = OpenAIModel(
            MODEL,
            provider=OpenAIProvider(base_url=OLLAMA_BASE, api_key="ollama"),
        )
    return Agent(
        model=model,
        output_type=AnswerWithConfidence,
        system_prompt=(
            "You answer questions. ALWAYS return a structured answer with "
            "an 'answer' text, a 'confidence' float (0.0 to 1.0), and a list of 'sources'. "
            "If you don't know, set confidence low and explain in answer."
        ),
    )


def run(question: str, model: Any = None) -> AnswerWithConfidence:
    agent = build_agent(model=model)
    result = agent.run_sync(question)
    return result.output


if __name__ == "__main__":
    question = "What is the population of Taipei?"
    print(f"❓ Q: {question}（using Pydantic AI + Ollama {MODEL}）")
    print("-" * 60)
    answer = run(question)
    print(f"  answer:     {answer.answer}")
    print(f"  confidence: {answer.confidence}")
    print(f"  sources:    {answer.sources}")

    # Pydantic 已經保證 type 正確、這裡只 sanity check
    assert isinstance(answer.confidence, float)
    assert 0.0 <= answer.confidence <= 1.0
    assert isinstance(answer.sources, list)
    print("\n✅ 練習 5 通過 — Pydantic AI 強制 structured output、$0/run")
    print("   schema validation 在 runtime 自動跑、LLM 不能偷懶")
