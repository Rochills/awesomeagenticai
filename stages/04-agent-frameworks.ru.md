# Этап 4 — Agent Frameworks

> [繁體中文](./04-agent-frameworks.md) | [简体中文](./04-agent-frameworks.zh-Hans.md) | [English](./04-agent-frameworks.en.md) | **Русский**


⏱ **Оценка времени**: 2–3 недели (~10–15 часов)

> 💡 Незнакомый термин? (framework / supervisor / worker / handoff / …) → [`resources/glossary.ru.md`](../resources/glossary.ru.md).

Ты построил ReAct agent с нуля (этап 3). Теперь учи, что фреймворки делают за тебя. **Выбери один для глубокого изучения**, остальные просто пролистай, чтобы знать, когда переключиться.

## 📌 Цели обучения

После этого этапа сможешь:
- Сравнить 5 основных agent-фреймворков (LangGraph, AutoGen, CrewAI, Smolagents, OpenAI Agents SDK)
- Выбрать правильный framework для задачи
- Построить один и тот же agent в 2 фреймворках и почувствовать разницу
- Распознать, когда стоит уйти от фреймворков и писать с нуля

## 🚪 Условия входа

Уже должен:
- Закончить все 5 hello-X проектов этапа 3
- Построить ReAct с нуля (Упражнение 3)
- Чувствовать себя уверенно с async Python (фреймворки опираются на async)

⚠️ **Memory primer (заглянь вперёд, если нужно)**: некоторые фичи фреймворков опираются на концепции memory — LangGraph использует checkpointing (state persistence), CrewAI передаёт результаты задач между агентами (легковесная memory). [Этап 6 — Memory & RAG](06-memory-rag.ru.md) покрывает это как следует. Не обязательно читать сначала, но если фича framework'а кажется загадочной — ответ там.

## 📚 Обязательное чтение

1. [**Anthropic — Building Effective Agents**](https://www.anthropic.com/engineering/building-effective-agents) — когда использовать фреймворки vs raw API
2. [**LangChain — Conceptual Guide: Agents**](https://python.langchain.com/docs/concepts/agents/) — agent-абстракции
3. [**Best Multi-Agent Frameworks 2026 comparison**](https://gurusup.com/blog/best-multi-agent-frameworks-2026) — текущее рыночное позиционирование
4. **Quickstart одного фреймворка** — выбери LangGraph или CrewAI; пройди их официальный туториал end-to-end

## 🛠 Практические упражнения

### Упражнение 1: Тот же agent, два фреймворка
Построй один и тот же простой agent (search + summarize) в:
- LangGraph
- CrewAI
Сравни строки кода, опыт дебага и где они прячут сложность.

### Упражнение 2: Multi-agent распределение ролей
Используй CrewAI, чтобы построить 2–3 agent'ов с разными ролями, работающих над одной задачей. (CrewAI лучший для этого.)

### Упражнение 3: Graph-based workflow
Используй LangGraph, чтобы построить workflow с branching-логикой и human-in-the-loop checkpoint'ом. (LangGraph лучший для этого.)

### Упражнение 4: CodeAct vs JSON tool
Построй Smolagents-agent, пишущий Python-код как actions (CodeAct-паттерн), сравни с JSON tool-call маршрутом из Упражнения 1. Задай тот же вопрос, понаблюдай, как два маршрута решают по-разному.

### Упражнение 5: Type-safe agent
Используй Pydantic AI, чтобы построить agent, возвращающий structured output (например, спрашиваешь, получаешь `{ "answer": str, "confidence": float, "sources": [str] }`). Понаблюдай, как Pydantic schema validation не даёт агенту срезать углы или галлюцинировать структуру.

## 🎯 Подборка проектов

### [LangGraph](https://github.com/langchain-ai/langgraph) ⭐ Production-grade

| Поле | Значение |
|---|---|
| Language | Python / TypeScript |
| Stars | ★ 31k+ |
| License | MIT |
| Recommendation | ⭐⭐⭐⭐⭐ |

**Чему учит**: graph-based agent orchestration. State management, checkpointing, human-in-the-loop, time-travel debugging.

**Лучше всего для**: production multi-agent систем, где нужны audit trails и rollback. Enterprise-grade.

**Заметки**: сильное enterprise-внедрение с 2025 (audit trails, replay-friendly graph model). Круче learning curve, чем у CrewAI, но окупается в production. Парь с LangSmith для observability.

**Запуск**:
```bash
pip install langgraph langchain-anthropic
# Tutorial: https://langchain-ai.github.io/langgraph/tutorials/introduction/
```

---

### [CrewAI](https://github.com/crewAIInc/crewAI) ⭐ Самый низкий learning curve

| Поле | Значение |
|---|---|
| Language | Python |
| Stars | ★ 50k+ |
| License | MIT |
| Recommendation | ⭐⭐⭐⭐ |

**Чему учит**: role-based multi-agent design. «Crews» агентов с разными ролями, работающие над общими целями.

**Лучше всего для**: быстрое прототипирование multi-agent систем. ~20 строк до рабочего crew. Отлично для пайплайнов вида «research → writer → reviewer».

**Заметки**: самый низкий learning curve. Но: нет встроенного checkpointing для long-running workflow'ов, ограниченный контроль над agent-to-agent коммуникацией, грубое error handling. Хорошо для прототипов; LangGraph — для production.

---

### [Microsoft AutoGen / AG2](https://github.com/microsoft/autogen)

| Поле | Значение |
|---|---|
| Language | Python |
| Stars | ★ 57k+ |
| License | CC-BY-4.0 (заметь: лицензия для документации; код отдельно) |
| Recommendation | ⭐⭐⭐⭐ |

**Чему учит**: conversational multi-agent команды. Агенты взаимодействуют через multi-turn разговоры. Сильные group-chat паттерны координации.

**Лучше всего для**: multi-agent debate, brainstorming, peer review паттернов. Исследовательская родословная Microsoft.

**Заметки**: AG2 (v0.4 rewrite) приносит async-first исполнение и event-driven core. Оригинальный AutoGen (v0.2) — то, что используют большинство туториалов. Учитывай раскол по версиям.

---

### [Hugging Face Smolagents](https://github.com/huggingface/smolagents)

| Поле | Значение |
|---|---|
| Language | Python |
| Stars | ★ 27k+ |
| License | Apache 2.0 |
| Recommendation | ⭐⭐⭐⭐ |

**Чему учит**: код-пишущие agents (CodeAct-паттерн) — агенты генерируют Python-код вместо JSON tool calls. Философия ≤1000 LOC.

**Лучше всего для**: экосистем локальных LLM и HuggingFace-интеграций. Другая дизайн-философия, которую стоит понимать.

**Заметки**: ставка HF: agents должны быть мелкими. Их CodeAct-подход интеллектуально отличается. Сравни с JSON-tool подходом, чтобы увидеть trade-off'ы.

---

### [OpenAI Agents SDK](https://github.com/openai/openai-agents-python)

| Поле | Значение |
|---|---|
| Language | Python |
| License | MIT |
| Recommendation | ⭐⭐⭐⭐ |

**Чему учит**: официальный agent SDK от OpenAI. Hand-offs между агентами, structured outputs, OpenAI-native эргономика.

**Лучше всего для**: если ты привязан к экосистеме OpenAI. Лёгкий, плотная интеграция с GPT-4-серией.

**Заметки**: новый игрок (конец 2025). Менее обкатан, чем LangGraph, но очень чистый. Стоит наблюдать, как мужает.

---

### [LlamaIndex Agents](https://github.com/run-llama/llama_index)

| Поле | Значение |
|---|---|
| Language | Python |
| Stars | ★ 49k+ |
| License | MIT |
| Recommendation | ⭐⭐⭐ |

**Чему учит**: агенты, плотно интегрированные с RAG. Если твоему агенту нужен тяжёлый document/data retrieval — LlamaIndex естественный выбор.

**Лучше всего для**: document-heavy agent-приложений. Research assistant, knowledge worker agents.

**Заметки**: сильнее в retrieval, чем в orchestration. Не выбор для чистой orchestration; идеальна для retrieval-heavy работы.

---

### [Pydantic AI](https://github.com/pydantic/pydantic-ai)

| Поле | Значение |
|---|---|
| Language | Python |
| License | MIT |
| Recommendation | ⭐⭐⭐ |

**Чему учит**: type-safe agent framework, использующий Pydantic для structured outputs. Сильные гарантии валидации.

**Лучше всего для**: production-команд, желающих runtime type safety + structured outputs по дефолту.

**Заметки**: новее альтернатив. Родословная Pydantic-команды даёт уверенность в API-дизайне.

---

### [agentscope-ai/agentscope](https://github.com/agentscope-ai/agentscope)

| Поле | Значение |
|---|---|
| Language | Python |
| Stars | ★ 24k+ |
| License | Apache 2.0 |
| Recommendation | ⭐⭐⭐ |

**Чему учит**: multi-agent платформа с сильным visualization-инструментарием. «Build and run agents you can see, understand, and trust».

**Лучше всего для**: исследователей, желающих визуальный дебаг multi-agent потоков.

**Заметки**: меньше внедрения в западном community, но технически крепко. Сильный observability-инструментарий.

---

### [LangChain](https://github.com/langchain-ai/langchain)

| Поле | Значение |
|---|---|
| Language | Python / TypeScript |
| Stars | ★ 135k+ |
| License | MIT |
| Recommendation | ⭐⭐⭐ |

**Чему учит**: оригинальный «всё в одном мешке» framework. Chains, agents, memory, retrievers, всё вместе.

**Лучше всего для**: быстрые прототипы, где нужно склеить много кусков.

**Заметки**: многие пере-используют LangChain. Специально для agent orchestration — предпочитай LangGraph (его наследник). LangChain лучший как retrieval + chaining-клей, не agent orchestration.

---

### [microsoft/semantic-kernel](https://github.com/microsoft/semantic-kernel)

| Поле | Значение |
|---|---|
| Language | C# / Python / Java |
| Stars | ★ 27k+ |
| License | MIT |
| Recommendation | ⭐⭐⭐⭐ |

**Чему учит**: enterprise SDK паттерн Microsoft (kernels + plugins + planners) — **поддерживает C# / Python / Java с официальными SDK**, один из немногих agent-фреймворков со всеми тремя.

**Лучше всего для**: разработчиков в Microsoft-стек работах или всем, кому нужны agents в .NET / Java окружениях.

**Заметки**: более тяжёлые абстракции, чем у smolagents — не для новичка первой недели. Стоит рассматривать для enterprise-окружений, нуждающихся в .NET / Java покрытии.

---

### [agno-agi/agno](https://github.com/agno-agi/agno)

| Поле | Значение |
|---|---|
| Language | Python |
| Stars | ★ 39k+ |
| License | Apache-2.0 |
| Recommendation | ⭐⭐⭐⭐ |

**Чему учит**: multi-modal agent runtime + control plane — за пределами просто *постройки* агентов, покрывает serving, monitoring и governance. 2025-native agent-платформа.

**Лучше всего для**: толкать agents к «serveable + observable» без полного стека LangGraph + LangSmith. Также ок для prototype-фазы быстрого дизайна.

**Заметки**: этап 4 для agent API, этап 7 для runtime / monitoring стороны.

---

### [BerriAI/litellm](https://github.com/BerriAI/litellm) (не framework — cross-stage infra)

| Поле | Значение |
|---|---|
| Language | Python |
| Stars | ★ 45k+ |
| License | MIT (с отдельной лицензией для директории `enterprise/`) |
| Recommendation | ⭐⭐⭐⭐ |

**Чему учит**: provider-agnostic SDK + AI gateway — **вызывай 100+ LLM через OpenAI-shaped API**, с cost tracking, fallbacks, guardrails.

**Лучше всего для**: агентов, переключающихся между Claude / GPT / Gemini / open-source моделями без переписывания кода.

**Заметки**: строго говоря не agent framework — это provider-abstraction layer, на котором сидят фреймворки. Списан в этап 4, потому что multi-provider agent-работа часто его требует; deploy этапа 7 тоже его касается. Директория `enterprise/` лицензирована отдельно.

---

## ✅ Самопроверка перед этапом 5

Можешь:
- [ ] Построить один и тот же agent в LangGraph И CrewAI
- [ ] Выбрать правильный framework для задачи (production vs prototype)
- [ ] Объяснить LangGraph checkpoint vs CrewAI task delegation
- [ ] Определить, когда CodeAct (Smolagents) лучше JSON-tool
- [ ] Решить, когда уйти от фреймворков и использовать raw API

Если да → переходи к [Этапу 5 — Claude Code Ecosystem](05-claude-code-ecosystem.ru.md).

## 💡 Стратегическая заметка

Не пытайся выучить ВСЕ. Выбери **один production-grade (LangGraph)** и **один quick-prototype (CrewAI)** и иди вглубь. Просматривай README остальных, чтобы знать, что они существуют.
