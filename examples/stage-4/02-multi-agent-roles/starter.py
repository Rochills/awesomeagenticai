"""Stage 4 練習 2：多 agent 角色分配 — CrewAI + Ollama（Path A、默認）。

3 個 agent 各有角色：
- Researcher 找資料（用 search tool）
- Writer 寫稿（拿 researcher 的結果寫成 blog 段落）
- Critic 審稿（檢查 factual + tone）

這個情境 CrewAI 最拿手——hierarchical / sequential delegation 是 CrewAI 的招牌。

跑法：
    pip install -r requirements.txt
    ollama pull qwen2.5:3b
    ollama serve
    python starter.py

驗證：
    python test.py

預算：$0/run（Ollama）。對照 Anthropic 版見 starter_anthropic.py。

⚠️ 注意：3 個 agent 走 sequential、qwen2.5:3b 可能會繞較久（30-90 秒）。
"""

from __future__ import annotations

import os
import sys
from typing import Any

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from crewai import Agent, Crew, Process, Task
from crewai.tools import tool

MODEL = os.environ.get("MODEL", "ollama/qwen2.5:3b")
OLLAMA_BASE = os.environ.get("OLLAMA_API_BASE", "http://localhost:11434")


# === Tool ===

@tool("search")
def search(query: str) -> str:
    """Search a (fake, offline) knowledge base."""
    db = {
        "react": "ReAct (Reasoning+Acting, Yao et al. 2022) is the foundational agent pattern: think→act→observe loop.",
        "langgraph": "LangGraph is a graph-based agent orchestration framework by LangChain, focuses on state + checkpointing.",
        "crewai": "CrewAI is a role-based multi-agent framework — define Agent/Task/Crew, run with kickoff().",
    }
    return db.get(query.strip().lower(), f"no entry for {query}")


# === Crew 設計 ===

def build_crew(topic: str, llm_model: str = MODEL) -> Crew:
    os.environ["OPENAI_API_BASE"] = f"{OLLAMA_BASE}/v1"
    os.environ["OPENAI_API_KEY"] = "ollama"

    researcher = Agent(
        role="Researcher",
        goal=f"Find concise factual info about {topic} from the knowledge base.",
        backstory="You search a knowledge base and return raw factual entries.",
        tools=[search],
        llm=llm_model,
        verbose=False,
        allow_delegation=False,
    )
    writer = Agent(
        role="Writer",
        goal=f"Write a 2-sentence blog intro about {topic}.",
        backstory="You take the researcher's findings and write engaging blog copy.",
        llm=llm_model,
        verbose=False,
        allow_delegation=False,
    )
    critic = Agent(
        role="Critic",
        goal="Verify the writer's blog intro is factually grounded in the researcher's data + check tone.",
        backstory="You're a strict editor who flags hallucinations and tone issues.",
        llm=llm_model,
        verbose=False,
        allow_delegation=False,
    )

    research_task = Task(
        description=f"Search for `{topic}` and report what you find.",
        expected_output="A 1-2 sentence factual entry from the knowledge base.",
        agent=researcher,
    )
    write_task = Task(
        description="Write a 2-sentence blog intro using the researcher's findings.",
        expected_output="A 2-sentence intro paragraph.",
        agent=writer,
        context=[research_task],
    )
    critic_task = Task(
        description="Check if the writer's intro is factually grounded in the researcher's data. "
                    "Report PASS or list issues.",
        expected_output="Either 'PASS: [intro]' or 'ISSUES: [list]'.",
        agent=critic,
        context=[research_task, write_task],
    )

    return Crew(
        agents=[researcher, writer, critic],
        tasks=[research_task, write_task, critic_task],
        process=Process.sequential,
        verbose=False,
    )


def run(topic: str, llm_model: str = MODEL) -> dict:
    crew = build_crew(topic, llm_model=llm_model)
    result = crew.kickoff()
    return {"final": str(result), "topic": topic}


if __name__ == "__main__":
    topic = "react"
    print(f"❓ Topic: {topic}（using CrewAI + Ollama {MODEL}）")
    print(f"   3 agents: Researcher → Writer → Critic（sequential）")
    print("-" * 60)
    result = run(topic)
    print(f"✅ Final (critic's verdict):\n{result['final']}")
    assert result["final"], "expected critic to produce a verdict"
    print("\n✅ 練習 2 通過 — 3-agent crew 跑完、$0/run")
