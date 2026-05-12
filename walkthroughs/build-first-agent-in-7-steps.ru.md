# Собери первого AI Agent за 7 шагов

> [繁體中文](./build-first-agent-in-7-steps.md) | [简体中文](./build-first-agent-in-7-steps.zh-Hans.md) | [English](./build-first-agent-in-7-steps.en.md) | **Русский**

> [← Назад к README основного пути](../README.ru.md)

> 📌 **Это для Track B (Agent Builder)** — учит **написать agent с нуля**.
> Учащимся [Track A (CLI Power User)](../tracks/cli/A1-cli-intro.ru.md) **не обязательно гонять**; но чтение даёт глубокое понимание «**как агент собирается шаг за шагом от LLM API до production**» — опциональное продвинутое дополнение.

Это **конкретный cross-stage walkthrough** — один и тот же agent, прослежен с этапа 1 до этапа 7, с исполнимыми code-скелетами на каждом этапе.

> **Как это читать**: каждая секция расширяет предыдущую. Поздние сниппеты предполагают, что файлы ранних этапов в той же директории. Чтобы запустить:
> 1. Настрой окружение в этапе 0
> 2. Сохраняй каждый этап в новый файл (`step1_*.py`, `step2_*.py`, …)
> 3. Поздние этапы импортируют из ранних через `from step1_xxx import ...`
>
> Установи все зависимости разом: `pip install anthropic openai requests beautifulsoup4 langgraph langchain-anthropic langchain-core chromadb langfuse fastapi uvicorn pydantic`

Агент для постройки: **Paper Summary Bot** — по URL arXiv-статьи выдаёт 3-абзацное резюме + 5 ключевых слов + сравнение со related work.

Каждый этап **добавляет одну способность** к тому же агенту. К концу — multi-LLM, оснащённый памятью, deployable agent.

---

## 📋 Обзор

| Этап | Способность, которую добавляешь | Сложность кода |
|---|---|---|
| 0 | Окружение (Python, API key, git) | — |
| 1 | Первый LLM API call | ~10 строк |
| 2 | Написать профессиональный промпт | ~20 строк |
| 3 | Tool use: авто-fetch arXiv | ~80 строк |
| 4 | Переписать с framework + reflection | ~40 строк (framework абстрагирует loop) |
| 5 | Упаковать как Claude Code Skill | SKILL.md + 30 строк |
| 6 | Добавить RAG-память: сравнение с прошлыми статьями | ~60 строк |
| 7 | Добавить eval, observability, deploy | ~100 строк |

**Итого**: ~350 строк Python + structured config = конкретный пример, наблюдаемый от нуля до production.

---

## Этап 0 — Окружение

```bash
# Установка Python 3.11+
python --version

# Виртуальное окружение
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Установи все пакеты, используемые в этапах (one-time; позже не pip install)
pip install anthropic openai requests beautifulsoup4 \
            langgraph langchain-anthropic langchain-core \
            chromadb langfuse fastapi uvicorn pydantic

# Claude API key (получи на console.anthropic.com)
export ANTHROPIC_API_KEY="sk-ant-..."

# Init repo
mkdir paper-summary-bot && cd paper-summary-bot
git init
echo ".env\n.venv/\n__pycache__/" > .gitignore
```

**Чекпоинт**: `python -c "from anthropic import Anthropic; print('OK')"` должно работать без ошибок.

---

## Этап 1 — Первый LLM-вызов

```python
# step1_hello_llm.py
from anthropic import Anthropic

client = Anthropic()

response = client.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=500,
    messages=[{
        "role": "user",
        "content": "Explain ReAct agents in 3 sentences."
    }]
)

print(response.content[0].text)
print(f"\n--- Tokens: input={response.usage.input_tokens}, "
      f"output={response.usage.output_tokens} ---")
```

Запуск: `python step1_hello_llm.py`

**Что выучишь**: форма API-вызова, структура `messages`, как `usage` считает токены.

---

## Этап 2 — Профессиональный промпт

```python
# step2_paper_summary.py
from anthropic import Anthropic

client = Anthropic()

SYSTEM_PROMPT = """You are an academic paper summarization assistant. Your task:

1. Write a 3-paragraph summary describing: (a) motivation, (b) method, (c) results.
2. List 5 keywords.
3. Bullet 2-3 differences from mainstream approaches.

Format requirements:
- Each summary paragraph ≤ 60 words
- Keywords in English (technical terms)
- Total ≤ 300 words
- Don't fabricate; if not stated, say "not stated in the paper"."""

PAPER_TEXT = """[Paste paper abstract here]"""

response = client.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=800,
    system=SYSTEM_PROMPT,
    messages=[{"role": "user", "content": PAPER_TEXT}]
)

print(response.content[0].text)
```

**Что выучишь**: разделение system prompt vs user message, явные format-constraints, anti-hallucination через «say not stated».

---

## Этап 3 — Tool Use: авто-fetch статей

```python
# step3_tool_use.py
import requests
from anthropic import Anthropic
from step2_paper_summary import SYSTEM_PROMPT  # написан на предыдущем этапе

client = Anthropic()

# Определи tool
TOOLS = [{
    "name": "fetch_arxiv",
    "description": "Fetch arXiv paper abstract by URL",
    "input_schema": {
        "type": "object",
        "properties": {
            "arxiv_url": {"type": "string"}
        },
        "required": ["arxiv_url"]
    }
}]

def fetch_arxiv(arxiv_url: str) -> str:
    """Tool implementation."""
    arxiv_id = arxiv_url.split("/")[-1].replace(".pdf", "")
    api_url = f"http://export.arxiv.org/api/query?id_list={arxiv_id}"
    r = requests.get(api_url)
    # Упрощённо: реальная версия парсит XML
    return r.text[:5000]

# ReAct loop
def run_agent(user_query: str):
    messages = [{"role": "user", "content": user_query}]

    while True:
        response = client.messages.create(
            model="claude-sonnet-4-5",
            max_tokens=2000,
            tools=TOOLS,
            messages=messages,
            system=SYSTEM_PROMPT,  # из этапа 2
        )

        # Нет больше tool calls → готово
        if response.stop_reason == "end_turn":
            return response.content[-1].text

        # Обработай tool call
        tool_use = next(b for b in response.content if b.type == "tool_use")
        if tool_use.name == "fetch_arxiv":
            result = fetch_arxiv(**tool_use.input)
            messages.append({"role": "assistant", "content": response.content})
            messages.append({
                "role": "user",
                "content": [{
                    "type": "tool_result",
                    "tool_use_id": tool_use.id,
                    "content": result,
                }]
            })

# Запуск
print(run_agent("Summarize this paper: https://arxiv.org/abs/2210.03629"))
```

**Что выучишь**: синтаксис tool-schema, механика ReAct loop, `stop_reason` для завершения, `tool_result` round-trip.

**Это самый большой прыжок этапа 3 — твой код переходит от «зову LLM» к «LLM зовёт мой код».**

---

## Этап 4 — Framework + Reflection

> **Установка**: `pip install langgraph langchain-anthropic langchain-core`

Перепиши с LangGraph и добавь self-review ноду:

```python
# step4_langgraph.py
from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import create_react_agent
from langgraph.graph.message import add_messages
from langchain_anthropic import ChatAnthropic
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage

@tool
def fetch_arxiv(arxiv_url: str) -> str:
    """Fetch arXiv paper abstract."""
    import requests
    arxiv_id = arxiv_url.split("/")[-1].replace(".pdf", "")
    r = requests.get(f"http://export.arxiv.org/api/query?id_list={arxiv_id}")
    return r.text[:5000]

class State(TypedDict):
    messages: Annotated[list, add_messages]
    revisions: int  # ограничь loop

llm = ChatAnthropic(model="claude-sonnet-4-5")
react_agent = create_react_agent(llm, tools=[fetch_arxiv])

MAX_REVISIONS = 2

def reflect(state: State) -> State:
    """Пусть LLM проревьюит предыдущее резюме и решит, переделывать ли."""
    last_summary = state["messages"][-1].content

    # Явный yes/no verdict вместо keyword-matching текста
    review_prompt = (
        f"Does the following summary satisfy: 3 paragraphs, each ≤60 words, "
        f"5 English keywords, no fabrication?\n\n"
        f"{last_summary}\n\n"
        "Reply with PASS or NEEDS_REVISION only — no explanation."
    )
    verdict = llm.invoke(review_prompt).content.strip().upper()

    return {
        "messages": [HumanMessage(content=f"[Reviewer verdict: {verdict}]")],
        "revisions": state.get("revisions", 0) + 1,
    }

def should_continue(state: State) -> str:
    """Решает, циклиться к agent или завершиться."""
    last_msg = state["messages"][-1].content
    if state["revisions"] >= MAX_REVISIONS:
        return END  # достигнут предел, выходим безусловно
    if "NEEDS_REVISION" in last_msg:
        return "agent"  # переделать
    return END  # PASS → выход

# Построй граф
graph = StateGraph(State)
graph.add_node("agent", react_agent)
graph.add_node("reflect", reflect)
graph.add_edge("agent", "reflect")
graph.add_conditional_edges("reflect", should_continue, {"agent": "agent", END: END})
graph.set_entry_point("agent")
app = graph.compile()

# Запуск
result = app.invoke({
    "messages": [HumanMessage(content="Summarize https://arxiv.org/abs/2210.03629")],
    "revisions": 0,
})
print(result["messages"][-1].content)
```

**Что выучишь**: что framework абстрагирует (while loop, message-структура, tool registration), как определять conditional ветви с правильным завершением, как reflection-паттерн позволяет агенту само-корректироваться в bounded числе раундов (без бесконечного loop'а).

**Заметка**: после этапа 4 мы больше не показываем внутренности LangGraph state — поздние этапы относятся к LangGraph-агенту как к чёрному ящику.

---

## Этап 5 — Project Skill в Claude Code

> Этот шаг **не** Python — это переупаковка логики этапов 1–4 в **project skill** для Claude Code, который Claude загружает нативно. С чётким `description` Claude автоматически триггерит его, когда пользователь упоминает релевантный запрос.

В твоём репо создай:

```
your-repo/
└── .claude/
    └── skills/
        └── paper-summary/
            └── SKILL.md
```

Контент `SKILL.md`:

```markdown
---
name: paper-summary
description: Summarize arXiv papers. Trigger when the user pastes an arXiv URL, mentions a paper ID (e.g. 2210.03629), or asks "summarize this paper / 摘要論文". Output: 3-paragraph summary + 5 keywords + differences from mainstream.
---

# Paper Summary Skill

## What this does
Summarize an arXiv paper into 3 structured paragraphs + keywords + difference points.

## When Claude should use this
The user:
- Pastes an arXiv URL (`https://arxiv.org/abs/...` or `arxiv.org/pdf/...`)
- Mentions a specific paper (title or ID) and asks for a summary
- Asks "how does this paper differ from other approaches"

## How to do it
1. Fetch paper content from the URL (use Claude Code's built-in WebFetch tool; or Read tool if a PDF is attached)
2. Apply this prompt structure:
   - Motivation (≤60 words)
   - Method (≤60 words)
   - Results (≤60 words)
   - 5 English keywords
   - 2-3 differences from mainstream
3. If something isn't stated, say "not stated in the paper" — never fabricate

## References
- `references/example-summaries.md` — 3 example outputs in the target style
```

После размещения **открой Claude Code в этом репо** — project-level skills авто-загружаются (install не нужен). Claude триггерит skill, когда вход совпадает с `description`.

Чтобы проверить: вставь `https://arxiv.org/abs/2210.03629` в Claude Code сессии, смотри, отвечает ли Claude в твоём формате.

**Что выучишь**: разница между project skills и plugin marketplace skills (этот project-level, активен как только ты в репо; plugins — отдельный distribution-слой); `description` — discovery-механизм (не магическое поле `trigger_phrases`); как `references/` расширяет skill более длинными примерами.

**Дальше**: если хочешь упаковать этот skill как share'абельный plugin (чтобы другие могли установить в свой Claude Code), см. [Этап 5.4 Plugins & Marketplaces](../stages/05-claude-code-ecosystem.ru.md#54--plugins--marketplaces). Этот walkthrough не покрывает plugin-упаковку.

---

## Этап 6 — RAG Memory

Сделай агента **помнящим статьи, которые видел**, сравнивая новые с прошлыми.

```python
# step6_memory.py
import chromadb
from chromadb.utils import embedding_functions
from langchain_anthropic import ChatAnthropic

llm = ChatAnthropic(model="claude-sonnet-4-5")

# Локальная vector DB
chroma = chromadb.PersistentClient(path="./paper_memory")
embed_fn = embedding_functions.DefaultEmbeddingFunction()
collection = chroma.get_or_create_collection(
    name="papers",
    embedding_function=embed_fn,
)

def store_paper(arxiv_id: str, summary: str):
    """Сохрани резюме в vector DB."""
    collection.add(
        documents=[summary],
        ids=[arxiv_id],
        metadatas=[{"arxiv_id": arxiv_id}],
    )

def find_similar(query_summary: str, top_k: int = 3) -> list[dict]:
    """Найди top 3 наиболее похожих прошлых статей."""
    results = collection.query(query_texts=[query_summary], n_results=top_k)
    return [
        {"id": id_, "summary": doc}
        for id_, doc in zip(results["ids"][0], results["documents"][0])
    ]

# Модифицируй агента этапа 4 — добавь compare_with_memory шаг:
def compare_with_memory(state):
    new_summary = state["messages"][-1].content
    similar = find_similar(new_summary, top_k=3)

    if not similar:
        return {"comparison": "(no related papers in DB)"}

    compare_prompt = f"""New paper summary: {new_summary}

Top 3 similar papers in DB:
{chr(10).join(f"- {p['id']}: {p['summary'][:200]}" for p in similar)}

List 2-3 unique contributions of the new paper not covered above."""

    response = llm.invoke(compare_prompt)

    # Сохрани новую статью в memory
    store_paper(arxiv_id="...", summary=new_summary)

    return {"comparison": response.content}
```

Вшей `compare_with_memory` в граф этапа 4:

```python
# step6_memory.py (продолжение)
from step4_langgraph import State, react_agent, reflect, should_continue, MAX_REVISIONS
from langgraph.graph import StateGraph, END

graph = StateGraph(State)
graph.add_node("agent", react_agent)
graph.add_node("reflect", reflect)
graph.add_node("compare", compare_with_memory)  # новая нода
graph.add_edge("agent", "reflect")
graph.add_conditional_edges("reflect", should_continue, {"agent": "agent", END: "compare"})
graph.add_edge("compare", END)
graph.set_entry_point("agent")
app_with_memory = graph.compile()
```

**Что выучишь**: как использовать vector DB, embeddings + similarity-запросы, перевод агента из «stateless» в «stateful», дизайн persistent-хранения и как расширять граф новой нодой без переписывания ранней логики.

---

## Этап 7 — Eval + Observability + Deploy

### 7.1 Eval (`promptfoo`)

> **Установка**: `npm install -g promptfoo`

Python-провайдер Promptfoo ожидает callable-функцию, не module variable. Поэтому оборачиваем тонкий provider:

```python
# eval_provider.py
"""Promptfoo Python provider — функция, вызываемая promptfoo."""
from step2_paper_summary import SYSTEM_PROMPT
from step3_tool_use import run_agent  # ReAct loop этапа 3


def call_api(prompt: str, options: dict, context: dict) -> dict:
    """Promptfoo передаёт vars (context['vars']) + prompt."""
    paper_url = context["vars"]["paper_url"]
    output = run_agent(f"Summarize this paper: {paper_url}")
    return {"output": output}
```

```yaml
# promptfooconfig.yaml
prompts:
  - "Summarize: {{paper_url}}"

providers:
  - id: file://eval_provider.py
    label: paper-summary-agent

tests:
  - description: "ReAct paper"
    vars:
      paper_url: "https://arxiv.org/abs/2210.03629"
    assert:
      - type: contains
        value: "Reasoning"
      - type: llm-rubric
        value: "Output contains 5 English keywords, each paragraph ≤ 60 words"
  - description: "RAG paper"
    vars:
      paper_url: "https://arxiv.org/abs/2104.08663"
    assert:
      - type: contains
        value: "retrieval"
```

Запуск: `promptfoo eval && promptfoo view`

### 7.2 Observability (`langfuse`)

> **Установка**: `pip install langfuse`
> **Env vars** (получи на [cloud.langfuse.com](https://cloud.langfuse.com)):
> ```bash
> export LANGFUSE_PUBLIC_KEY="pk-lf-..."
> export LANGFUSE_SECRET_KEY="sk-lf-..."
> export LANGFUSE_HOST="https://cloud.langfuse.com"  # или твой self-hosted URL
> ```

```python
# step7_observability.py
from langfuse.decorators import observe
from step3_tool_use import run_agent  # агент из ранних этапов

@observe(name="paper-summary-agent")
def run_paper_agent(arxiv_url: str) -> str:
    return run_agent(f"Summarize {arxiv_url}")

if __name__ == "__main__":
    out = run_paper_agent("https://arxiv.org/abs/2210.03629")
    print(out)
```

После запуска смотри per-call trace, cost, latency и tool use в dashboard Langfuse.

### 7.3 Deploy (Docker + FastAPI)

> **Установка**: `pip install fastapi uvicorn pydantic`

```python
# main.py
from fastapi import FastAPI
from pydantic import BaseModel
from step7_observability import run_paper_agent  # обёрнутый Langfuse'ом

app = FastAPI()

class PaperRequest(BaseModel):
    arxiv_url: str

@app.post("/summarize")
def summarize(req: PaperRequest):
    return {"summary": run_paper_agent(req.arxiv_url)}
```

```text
# requirements.txt
anthropic
requests
langgraph
langchain-anthropic
langchain-core
chromadb
langfuse
fastapi
uvicorn
pydantic
```

```dockerfile
# Dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

```bash
docker build -t paper-summary-bot .
docker run -p 8000:8000 \
  -e ANTHROPIC_API_KEY=$ANTHROPIC_API_KEY \
  -e LANGFUSE_PUBLIC_KEY=$LANGFUSE_PUBLIC_KEY \
  -e LANGFUSE_SECRET_KEY=$LANGFUSE_SECRET_KEY \
  paper-summary-bot
# Или деплой на Cloud Run / Fly.io / Railway / свой K8s
```

**Что выучишь**: eval как regression-тест, observability для дебага задеплоенных агентов, перевод агента из скрипта в сервис.

---

## ✅ После полного walkthrough'а сможешь:

- [ ] Построить ReAct agent с нуля (этап 3)
- [ ] Переписать с framework и добавить продвинутые паттерны (этап 4)
- [ ] Упаковать агента как Claude Code skill (этап 5)
- [ ] Добавить RAG-память, чтобы агент был stateful (этап 6)
- [ ] Написать eval'ы + подключить observability + задеплоить (этап 7)

**Этот пример — ~350 строк Python** — больше, чем типичный framework-пример, но каждая строка — то, что реально используешь.

---

## 🚧 Продвинутые расширения

Если хочешь глубже, этот paper-summary-bot может расшириться в:

- **Multi-agent paper review**: два агента играют поддерживающего vs adversarial reviewer'а, третий — area chair → for-researcher ветка
- **Conference report generator**: по conference proceedings URL производит per-track high-level резюме → knowledge-worker ветка
- **Topic trend tracker**: еженедельный arXiv-сканер, сравнивает новые статьи с существующей памятью, производит weekly digest → personal-assistant ветка

Каждое отображается на специализированную ветку.

---

## 💡 Поддержка этого walkthrough'а

Этот пример будет эволюционировать — SDK-интерфейсы меняются, фреймворки развиваются, best practices сдвигаются. Если что-то ломается:

1. Открой issue с точной ошибкой + твоё окружение (Python-версия, версии пакетов)
2. PR-фиксы должны объяснять «зачем это изменение»
3. Не рефактори этот файл для демо только своего любимого фреймворка — это **multi-framework learning** пример
