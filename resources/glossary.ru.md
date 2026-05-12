# Glossary

> [繁體中文](./glossary.md) | [简体中文](./glossary.zh-Hans.md) | [English](./glossary.en.md) | **Русский**

> Карта обучения активно опирается на термины вроде LLM, RAG, MCP, agent. Незнакомые ищи здесь за 30 секунд и возвращайся к чтению этапа.
>
> Каждая запись даёт **минимально пригодное определение** (30–80 слов + указание этапа, где разбирается подробно) — не Wikipedia.

---

## 1. Базовые концепции

### LLM (Large Language Model)

GPT, Claude, Gemini — модели, принимающие текст на входе и выдающие текст на выходе. По сути чистая функция: input prompt → output text. **Сами по себе не лазают в веб, не помнят прошлые разговоры** — это надо подключать снаружи.

📍 Подробнее: [Этап 1](../stages/01-llm-basics.ru.md)

### Token (токен)

LLM видят **токены** (sub-word единицы), не символы. Грубо: 1 англ. слово ≈ 1.3 токена, 1 иероглиф ≈ 1.5–2 токена, 1 русское слово ≈ 2–3 токена. Цены LLM и context window'ы меряются в токенах. «1M-token context» ≈ 750k англ. слов.

📍 Подробнее: [Этап 1](../stages/01-llm-basics.ru.md)

### Context Window (окно контекста)

Максимум токенов, которые LLM «видит» за один вызов. Claude 200k, GPT-4o 128k, Gemini 2M. **Больше не всегда лучше** — за определённой длиной LLM «Lost in the Middle».

### Prompt (промпт)

Текст, который ты подаёшь LLM. **Prompt engineering** = дизайн этого текста, чтобы получить хорошие ответы. Базовая структура: system prompt (роль/правила) + user prompt (сам запрос).

📍 Подробнее: [Этап 2](../stages/02-prompt-engineering.ru.md)

### Few-shot / Zero-shot

- **Zero-shot**: спрашиваешь напрямую, без примеров.
- **Few-shot**: сначала даёшь 2–5 примеров input → output. **Few-shot обычно сильно повышает точность**, особенно для строгого формата.

### Chain-of-Thought (CoT)

Заставь LLM «подумать перед ответом» — добавь «Let's think step by step», и она выдаст рассуждение перед финальным ответом. **Обычно повышает точность** ценой большего числа токенов.

---

## 2. Agents / Tool Use

### Agent (агент)

Система, позволяющая LLM **вызывать внешние функции, видеть результаты и решать, что делать дальше**. Центральная тема этой карты. Разница: чистая LLM — это Q&A, agent — это «LLM + tools + loop».

📍 Подробнее: [Этап 3](../stages/03-tool-use-and-hello-agent.ru.md)

### Tool Use / Function Calling

Позволяет LLM вызывать функции, которые ты определил (DB lookup, math, browser, …). Вместо обычного текста LLM возвращает `{"function": "search", "args": {…}}`. Твой код исполняет, результат отдаёт обратно.

📍 Подробнее: [Этап 3](../stages/03-tool-use-and-hello-agent.ru.md)
📍 Как писать хорошие schemas: [Function Schema Design cheatsheet](schema-design-cheatsheet.ru.md)

### ReAct (Reasoning + Acting)

Классический agent-паттерн: **Thought → Action (вызов tool) → Observation (видишь результат) → Thought ...** цикл до завершения. Большинство agent-фреймворков реализуют это внутри.

📍 Подробнее: [Этап 3](../stages/03-tool-use-and-hello-agent.ru.md)

### Structured Output

Заставить LLM выдавать **JSON или другую фиксированную schema** вместо свободного текста. Все основные LLM API имеют `response_format` или аналог. Agent-фреймворки полагаются на это для связи LLM ↔ код.

### Agent Loop

Повторяющийся цикл «LLM → tool → результат → LLM». Завершение: LLM говорит «готово» / исчерпан step budget / достигнут cost cap.

---

## 3. Memory / Retrieval / RAG

### RAG (Retrieval-Augmented Generation)

«Сначала найди, потом генерируй». Поток: вопрос пользователя → embedding-поиск top-K релевантных кусков → засовываешь эти K кусков в промпт → LLM отвечает. **Решает две проблемы: LLM не знает твои приватные данные и знания устарели.**

📍 Подробнее: [Этап 6](../stages/06-memory-rag.ru.md)

### Vector DB / Embedding

Преобразование текста (или картинок) в вектор чисел, так что **семантически близкое сидит рядом** в векторном пространстве. Vector DB (Pinecone, Chroma, Qdrant и т. д.) хранят и эффективно ищут эти векторы. Ключевой компонент RAG.

📍 Подробнее: [Этап 6](../stages/06-memory-rag.ru.md)

### Semantic Search

Используй embeddings для сравнения «по смыслу», а не «по точному совпадению строки». «Как зарядить EV» может найти «туториал по аккумулятору электромобиля». Традиционный keyword search (BM25 и т. д.) так не умеет.

### Chunking

Разделение длинных документов на embedding-дружественные мелкие куски (обычно 200–1000 токенов). **Стратегия чанкинга напрямую влияет на качество RAG** — слишком мелкие куски теряют контекст, слишком длинные размывают релевантность. Распространённое: fixed-size, по абзацам, по структуре (по заголовкам).

### Hybrid Search

Запусти semantic search и keyword search вместе, слей и переранжируй. Обычно бьёт оба по отдельности. Дефолт для production-grade RAG.

### Reranking

После first-pass retrieval'а, который вытащил top-50, применяй более дорогую, но более точную модель (cross-encoder) для переранжирования до top-5 для LLM. Cohere Rerank, bge-reranker и т. д.

### Contextual Retrieval

Метод Anthropic 2024 — embed'ишь каждый chunk вместе с резюме документа, из которого он взят, чтобы «этот chunk по отдельности бессмыслен» не ломало retrieval.

📍 Подробнее: [Этап 6](../stages/06-memory-rag.ru.md)

---

## 4. Multi-Agent

### Multi-Agent

Несколько агентов, кооперирующихся над одной задачей. Распространённые паттерны:

- **Supervisor + Worker**: один агент планирует/распределяет, другие исполняют.
- **Swarm**: peer-агенты, без фиксированного supervisor'а.
- **Debate**: агенты спорят с разных позиций, потом приходят к консенсусу.

📍 Подробнее: [Этап 7](../stages/07-multi-agent-production.ru.md)

### Handoff

Один агент передаёт задачу другому. Добавляет «как передать контекст» и «кто разбирается с провалом» поверх простого function call.

### A2A (Agent-to-Agent) Protocol

Протокол Google для коммуникации agent ↔ agent. Брат MCP, но для agent-to-agent, а не agent-to-tool.

---

## 5. Экосистема Claude Code

### MCP (Model Context Protocol)

Открытый протокол Anthropic, позволяющий любому LLM-хосту (Claude Code, Cursor, твой собственный agent) обращаться к любому внешнему tool server через один интерфейс. Думай «**USB для LLM**».

📍 Подробнее: [Этап 5.2](../stages/05-claude-code-ecosystem.ru.md#52--mcp-model-context-protocol-foundation)

### Skills / SKILL.md

«Пакеты поведения» Claude Code. Skill — это папка с `SKILL.md`, говорящим «в каком контексте делать что, какие tools можно вызывать». Claude Code автоматически загружает подходящие skills по ситуации.

📍 Подробнее: [Этап 5.3](../stages/05-claude-code-ecosystem.ru.md#53--skills-claude-code-behavior-layer)

### Plugin / Marketplace

Пакуй несколько Skills + slash commands + hooks + MCP-конфиги в одну поставляемую единицу. **Marketplace** — каталог плагинов; пользователи `claude plugin install`, чтобы взять community-build'ы.

📍 Подробнее: [Этап 5.4](../stages/05-claude-code-ecosystem.ru.md#54--plugins--marketplaces)

### Slash Command

Команды внутри Claude Code, начинающиеся с `/` (`/help`, `/compact`, `/plan` и т. д.). Кастомизируются — бросаешь промпт в `.claude/commands/<name>.md` и он становится `/name`.

### CLAUDE.md

Markdown-файл в корне проекта, который Claude Code читает при каждом запуске. Project-level правила / конвенции / контекст (язык, стиль кода, файлы, которых нельзя касаться и т. д.).

### Hooks

Скрипты, запускаемые до/после действий Claude Code (pre-tool-use, post-tool-use, user-message-received и т. д.). Use cases: auto-commit при правках, logging, гейтинг поведения.

### Subagent

Спавнящийся agent из главной сессии Claude Code, со своим context window'ом, посвящён конкретной задаче. Например, «подними code-reviewer subagent на этот diff».

---

## 6. Production / Eval / Cost

### Eval (Evaluation Framework)

Прогон тестового набора по твоему agent'у с количественной оценкой accuracy / latency / cost. **Production-agent без eval не имеет тестов.** Распространённое: promptfoo, LangSmith, langfuse evals.

📍 Подробнее: [Этап 7](../stages/07-multi-agent-production.ru.md)

### Observability

Захват каждого внутреннего шага (какой LLM-вызов, какой tool, какой результат). Позволяет replay'ить, когда вылез баг. Распространённое: langfuse, Helicone, weave.

📍 Подробнее: [Этап 7](../stages/07-multi-agent-production.ru.md)

### Prompt Caching

LLM кэширует префикс промпта; при повторе только новый суффикс биллится по полной цене (Anthropic — 90% off cached, OpenAI — 50% off). Long-context повторные запросы дают большую экономию.

### Streaming

LLM возвращает токены по мере генерации (по одному) вместо ожидания полного ответа. Лучший UX (выглядит как печать); технически через SSE или chunked transfer. **Дефолт для production interactive apps**. Trade-offs: клиент должен обрабатывать partial responses; парсинг ReAct tool-call ждёт конца стрима.

### Batch API

Сгрести большое число LLM-запросов под отложенную (≤24ч) обработку. **Обычно 50% off (Anthropic, OpenAI)**. Хорошо для non-interactive: batch summarization, batch classification, eval suites, ETL pipelines. **Не используй для interactive chat** — latency неприемлемая.

### Token Cost / Inference Cost

За один LLM-вызов: input tokens × input price + output tokens × output price. Стоимость ReAct-цикла агента нарастает быстро — один grep по большой кодовой базе может съесть 100k токенов.

### Guardrails

Слой правил, не дающий LLM делать плохое — блок prompt injection, PII leakage, harmful output и т. д. NeMo Guardrails, Guardrails AI и т. д.

---

## 7. Buzzwords / Размытые термины

### CLI Agent

Агенты, бегущие в терминале (Claude Code, Codex, Aider, Gemini CLI и т. д.). Vs IDE-bound (Cursor, Continue) или web-based (ChatGPT, Claude.ai).

📍 Подробнее: [Track A A1](../tracks/cli/A1-cli-intro.ru.md), [`resources/cli-agents-guide.ru.md`](cli-agents-guide.ru.md)

### BYO API Key (Bring Your Own)

Инструмент, поддерживающий API-ключ от пользователя вместо встроенных подписок. Aider / OpenCode / goose — BYO; Claude Code / Codex по дефолту используют подписку.

### Local LLM / On-Device

Модели, бегущие на твоём железе (Ollama, llama.cpp, MLX, LocalAI и т. д.). Данные остаются локально — privacy-friendly, но возможности отстают от frontier-моделей.

📍 Подробнее: [Этап 1](../stages/01-llm-basics.ru.md)

### Quantization

Сжатие весов модели с fp16 до int8 / int4 для экономии памяти и роста скорости при небольшой потере точности. Пользователи локальных LLM видят это постоянно (Q4_K_M, Q8_0 и т. д.).

### Hallucination

LLM «уверенно утверждает ложь» — придумывает API, фабрикует числа и подаёт их как факт. Каждый production-agent нуждается в защите (RAG / structured output / eval / guardrails).

### Frontier Model

Текущий top-tier (GPT-5, Claude Sonnet 4.5, Gemini 2.5 Pro и т. д.). Frontier — для тяжёлых рассуждений; дешёвые мелкие модели — для простой классификации / перевода, чтобы экономить.

### Context Engineering

Когда дизайна одной фразы промпта перестаёт хватать и нужно динамически собирать **system prompt + tool definitions + memory + retrieved chunks + multi-turn history** — это и есть дизайн-дисциплина всего стека. **Следующий слой над prompt engineering.**

📍 Подробнее: [Закрытие этапа 2](../stages/02-prompt-engineering.ru.md) / [Этап 6](../stages/06-memory-rag.ru.md) / [Этап 7](../stages/07-multi-agent-production.ru.md)
📍 Дальше: [`Meirtz/Awesome-Context-Engineering`](https://github.com/Meirtz/Awesome-Context-Engineering)

### Harness Engineering

Дизайн toolchain'а для упаковки agent'а в production-систему — permissions, tool registry, memory layer, eval, observability, retry / circuit breaker. Claude Code, Cursor, OpenCode и т. д. — все они «harnesses». **Framework заворачивает LLM в agent; harness заворачивает agent в продукт.**

📍 Подробнее: обязательное чтение [Этапа 7](../stages/07-multi-agent-production.ru.md)
📍 Дальше: [`ai-boost/awesome-harness-engineering`](https://github.com/ai-boost/awesome-harness-engineering), [`ZhangHanDong/harness-engineering-from-cc-to-ai-coding`](https://github.com/ZhangHanDong/harness-engineering-from-cc-to-ai-coding)

---

## Термина здесь нет?

- Читай контент самого этапа: [Этап 5.2 MCP](../stages/05-claude-code-ecosystem.ru.md#52--mcp-model-context-protocol-foundation) / [5.3 Skills](../stages/05-claude-code-ecosystem.ru.md#53--skills-claude-code-behavior-layer) / [5.4 Plugins](../stages/05-claude-code-ecosystem.ru.md#54--plugins--marketplaces)
- Списки обязательного чтения в [Этапе 1](../stages/01-llm-basics.ru.md) / [Этапе 6](../stages/06-memory-rag.ru.md) / [Этапе 7](../stages/07-multi-agent-production.ru.md)
- Не нашёл? Открой issue или PR с новой записью.
