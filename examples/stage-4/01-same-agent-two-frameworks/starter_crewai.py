"""Stage 4 練習 1：同一個 agent、CrewAI 版本對照（Ollama 預設）。

跟 starter.py (LangGraph) 同一個任務：search + summarize。
看程式碼風格差異——CrewAI 用 Agent + Task 抽象、LangGraph 用 StateGraph + node。

跑法：
    pip install -r requirements.txt   # 含 crewai
    ollama pull qwen2.5:3b
    ollama serve
    python starter_crewai.py

預算：$0/run。要切 Anthropic 改 LLM_PROVIDER env var（CrewAI 用 LiteLLM 底層）。

⚠️ 注意：CrewAI 對小 model（qwen2.5:3b）較吃力，可能會多繞幾步。Claude / sonnet 較穩。
"""

from __future__ import annotations

import os
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from crewai import Agent, Crew, Task
from crewai.tools import tool

MODEL = os.environ.get("MODEL", "ollama/qwen2.5:3b")  # LiteLLM 格式
OLLAMA_BASE = os.environ.get("OLLAMA_API_BASE", "http://localhost:11434")


@tool("search")
def search(query: str) -> str:
    """Search a (fake, offline) knowledge base for a topic."""
    db = {
        "taipei": "Taipei is the capital of Taiwan, population ~2.6M, known for night markets.",
        "react agent": "ReAct (Reasoning + Acting) is an agent pattern: think → act → observe loop.",
    }
    return db.get(query.strip().lower(), f"no entry for {query}")


def build_crew(query: str) -> Crew:
    """CrewAI 風格：一個 agent + 一個 task。"""
    os.environ["OPENAI_API_BASE"] = f"{OLLAMA_BASE}/v1"
    os.environ["OPENAI_API_KEY"] = "ollama"

    researcher = Agent(
        role="Researcher",
        goal="Find and summarize the requested topic.",
        backstory="You search a knowledge base and give concise summaries.",
        tools=[search],
        llm=MODEL,
        verbose=False,
    )
    task = Task(
        description=query,
        expected_output="A 1-2 sentence summary based on search results.",
        agent=researcher,
    )
    return Crew(agents=[researcher], tasks=[task], verbose=False)


def run(query: str) -> dict:
    crew = build_crew(query)
    result = crew.kickoff()
    return {"final": str(result), "steps": None}


if __name__ == "__main__":
    query = "summarize what you know about Taipei"
    print(f"❓ Query: {query}（using CrewAI + Ollama {MODEL}）")
    print("-" * 60)
    result = run(query)
    print(f"✅ Final: {result['final']}")
    assert result["final"], "expected non-empty summary"
    print("✅ CrewAI 版本通過 — 同樣任務、不同 framework、$0/run")
    print("   對照 starter.py（LangGraph）看程式碼風格差異")
