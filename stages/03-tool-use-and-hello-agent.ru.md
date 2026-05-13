# Этап 3 — Tool Use & Agent Intro ⭐

> [繁體中文](./03-tool-use-and-hello-agent.md) | [简体中文](./03-tool-use-and-hello-agent.zh-Hans.md) | [English](./03-tool-use-and-hello-agent.en.md) | **Русский**


⏱ **Оценка времени**: 2–3 недели (~10–20 часов)

> 💡 Этап насыщен терминами (agent / tool use / function calling / ReAct / structured output / …) → см. [`resources/glossary.ru.md` §2](../resources/glossary.ru.md#2-agents--tool-use).

Это самый важный этап. **Ты не понимаешь agents, пока не построил один.** Не пропускай hello-X демо.

## 📌 Цели обучения

После этого этапа сможешь:
- Объяснить, почему LLM нужны tools: без них модель не может надёжно получать свежие данные, выполнять действия и проверять внешний мир
- Определить tool schema так, чтобы LLM корректно выбрала и вызвала tool
- Построить single-step ReAct agent с нуля (без фреймворков)
- Построить multi-step ReAct agent, решающий, когда остановиться
- Распознавать, когда задаче нужен tool use vs. plain prompting

## 🚪 Условия входа

Уже должен:
- Иметь рабочий доступ Claude / OpenAI / Gemini API (этап 1)
- Чувствовать себя уверенно в основах prompt engineering (этап 2)
- Уметь написать Python-функцию, принимающую JSON-вход и возвращающую JSON

## 📚 Обязательное чтение

1. [**Anthropic — Tool Use**](https://docs.anthropic.com/en/docs/agents-and-tools/tool-use/overview) — официальный гайд
2. [**ReAct: Synergizing Reasoning and Acting in Language Models**](https://arxiv.org/abs/2210.03629) — Yao et al. 2022, фундаментальная статья. Прочитай хотя бы abstract и Section 3.
3. [**OpenAI — Function Calling**](https://platform.openai.com/docs/guides/function-calling) — формат function-calling, референс
4. [**Build an agent from scratch**](https://shafiqulai.github.io/blogs/blog_3.html) — narrative walkthrough

## 🛠 Практические упражнения (6 штук)

### Упражнение 1: Function Calling (один tool, один вызов)
Дай Claude один tool (фейковый weather API) и один вопрос («Идёт ли дождь в Тайбэе?»). Посмотри, как Claude вызывает tool, получает результат и отвечает.

### Упражнение 2: Multi-Tool Selection
Дай Claude три tool'а (search, calculator, calendar) и задачу. Посмотри, как Claude выбирает нужный tool. Заметь, когда Claude делает неправильный выбор.

### Упражнение 3: ReAct с нуля (без фреймворка)
Реализуй цикл Thought → Action → Observation в 50–80 строках Python. Без LangChain, без LangGraph. Просто `while not done: thought; action; observation; ...`.

### Упражнение 4: Multi-Step Reasoning Task
Задача, требующая 3–5 tool-вызовов подряд. Например: «Найди население Тайбэя, потом подели на население Нью-Йорка, и переведи отношение в проценты». Каждый шаг использует разный tool.

### Упражнение 5: Error Handling
Сделай так, чтобы tool падал (network error, invalid input). Понаблюдай, как агент восстанавливается (или нет). Добавь retry-логику.

### Упражнение 6: Function schema design (исправь плохую schema)
**Начни с намеренно плохой schema** — расплывчатый `description` («processes data»), все params типизированы как `string`, нет разделения required/optional, отсутствует `enum`, где он должен быть. Посмотри, как LLM выбирает неправильный tool / передаёт неправильные args. Потом чини по кусочкам:
- Перепиши `description`, чтобы LLM понимал *когда* звать этот tool (не docstring-стиль)
- Используй правильные типы (number / boolean / enum / array); явно описывай required
- Сжимай нечёткие поля с `enum` (например `unit: "celsius" | "fahrenheit"` вместо `unit: string`)
- Сделай ошибки восстанавливаемыми: возвращай `{"error": "...", "retry_hint": "..."}`, чтобы LLM мог retry'ить умно

> 💡 Подробная шпаргалка: [`resources/schema-design-cheatsheet.ru.md`](../resources/schema-design-cheatsheet.ru.md) — 5 золотых правил + 5 распространённых анти-паттернов.

## 🎯 Подборка проектов

### [Anthropic — Tool Use Cookbook](https://github.com/anthropics/anthropic-cookbook/tree/main/tool_use)

| Поле | Значение |
|---|---|
| Language | Python |
| License | MIT |
| Recommendation | ⭐⭐⭐⭐⭐ |

**Чему учит**: каждый tool-use паттерн, поддерживаемый Claude — single tool, multi-tool, parallel calls, structured output extraction.

**Лучше всего для**: Упражнений 1 и 2. Стартуй отсюда.

**Запуск**:
```bash
git clone https://github.com/anthropics/anthropic-cookbook
cd anthropic-cookbook/tool_use
jupyter notebook customer_service_agent.ipynb
```

---

### [Anthropic — Quickstarts](https://github.com/anthropics/anthropic-quickstarts)

| Поле | Значение |
|---|---|
| Language | Python / TypeScript |
| Stars | ★ 16k+ |
| License | MIT |
| Recommendation | ⭐⭐⭐⭐⭐ |

**Чему учит**: официальный hands-on starter kit от Anthropic. Три deployable agent-шаблона: `financial-data-analyst` (data analysis agent), `customer-support-agent` и `computer-use-demo` (Claude управляет экраном).

**Лучше всего для**: после Упражнений 1/2, когда хочешь увидеть «как выглядит реальное приложение» из канонического источника. Отполированнее community-имплементаций, с правильным deployment setup'ом.

**Заметки**: каждый шаблон — самодостаточная подпапка — бери один и запускай. Computer-use demo особенно стоит изучить как один из немногих официальных примеров GUI-управляющего agent'а.

---

### [pguso/ai-agents-from-scratch](https://github.com/pguso/ai-agents-from-scratch)

| Поле | Значение |
|---|---|
| Language | Python |
| License | MIT |
| Recommendation | ⭐⭐⭐⭐⭐ |

**Чему учит**: строй agents с локальными LLM и НУЛЁМ фреймворков. ReAct, function calling, memory — всё с нуля. Спроектировано демистифицировать то, что фреймворки прячут.

**Лучше всего для**: Упражнение 3 (ReAct с нуля). Самый чистый «no-framework» референс.

**Заметки**: использует локальный Ollama — работает без API-стоимости. Внимательно читай README — педагогическая структура отличная.

---

### [arunpshankar/react-from-scratch](https://github.com/arunpshankar/react-from-scratch)

| Поле | Значение |
|---|---|
| Language | Python |
| License | Apache-2.0 |
| Last update | ⚠️ Май 2025 (замедляется) |
| Recommendation | ⭐⭐⭐⭐ |

**Чему учит**: вариации и реализации ReAct-паттерна, оптимизированы под Gemini.

**Лучше всего для**: альтернатива Упражнению 3, если предпочитаешь Gemini. Покрывает варианты ReAct + Reflection + Self-consistency.

---

### [mattambrogi/agent-implementation](https://github.com/mattambrogi/agent-implementation)

| Поле | Значение |
|---|---|
| Language | Python |
| License | MIT |
| Last update | ⚠️ Stale (январь 2024) — оставлен как educational toy reference |
| Recommendation | ⭐⭐⭐ |

**Чему учит**: минимальная реализация ReAct agent'а. Ультра-урезано (~150 строк) для обучения.

**Лучше всего для**: чтение source построчно. Используй как референс, когда застрял в Упражнении 3.

---

### [lsdefine/GenericAgent](https://github.com/lsdefine/GenericAgent)

| Поле | Значение |
|---|---|
| Language | 中文 + Python |
| Stars | ★ 9k+ |
| License | MIT |
| Recommendation | ⭐⭐⭐⭐ |

**Чему учит**: минимальный self-evolving agent framework — core ~3K строк кода, agent растит skill tree из seed'а. Поддерживает Claude / Gemini / Kimi / MiniMax. Активная разработка.

**Лучше всего для**: альтернатива Упражнений 3/4 для читателей, желающих более «минимальный но полный» framework-референс. Хорошая середина между toy от mattambrogi и полным LangGraph.

---

### [HelloAgents (jjyaoao)](https://github.com/jjyaoao/HelloAgents) — ветка `learn_version`

| Поле | Значение |
|---|---|
| Language | 中文 (zh-Hans) + Python |
| License | CC BY-NC-SA 4.0 |
| Recommendation | ⭐⭐⭐⭐⭐ для zh-читателей |

**Чему учит**: teaching-oriented multi-agent practice framework, преподаётся chapter-by-chapter, в паре с [туториалом Datawhale Hello-Agents](https://github.com/datawhalechina/hello-agents). 16 возможностей (tool response, context engineering, session persistence, sub-agents, circuit breaker, observability и т. д.) — материал чтобы *учить* production-паттерны, не готовый production-ready продукт сам по себе.

**Лучше всего для**: китайскоязычных учеников. **Переключись на ветку `learn_version`** для туториал-aligned версии.

**Заметки**: лицензия CC BY-NC-SA — non-commercial. Контент туториала на zh-Hans; технический контент переносится к zh-TW читателям нормально.

**Запуск**:
```bash
pip install hello-agents
git clone -b learn_version https://github.com/jjyaoao/HelloAgents
```

---

### [datawhalechina/hello-agents](https://github.com/datawhalechina/hello-agents)

| Поле | Значение |
|---|---|
| Language | 中文 (zh-Hans) |
| License | CC BY-NC-SA |
| Recommendation | ⭐⭐⭐⭐⭐ для zh-читателей |

**Чему учит**: companion-туториал к HelloAgents. Multi-chapter walkthrough от «что такое agent» до production-паттернов.

**Лучше всего для**: китайскоязычных учеников, желающих структурированный туториал параллельно с кодом.

**Заметки**: парь это с веткой `learn_version` репо HelloAgents выше.

---

### [QuantaLogic/quantalogic](https://github.com/quantalogic/quantalogic)

| Поле | Значение |
|---|---|
| Language | Python |
| License | Apache-2.0 |
| Recommendation | ⭐⭐⭐ |

**Чему учит**: ReAct agent, генерирующий Python-код вместо JSON tool-calls. Другой дизайн-выбор — agent пишет код как действия.

**Лучше всего для**: после Упражнения 3. Сравни CodeAct (код как action) vs JSON tool calls.

---

### [HuggingFace Smolagents](https://github.com/huggingface/smolagents)

| Поле | Значение |
|---|---|
| Language | Python |
| Stars | ★ 27k+ |
| License | Apache 2.0 |
| Recommendation | ⭐⭐⭐⭐ |

**Чему учит**: smol agents (≤1000 LOC). Код-пишущие агенты, исполняющие Python вместо JSON tool calls.

**Лучше всего для**: альтернатива Упражнению 5. Особенно хорош для экспериментов с локальными LLM.

**Заметки**: позиция HF: agents должны быть мелкими. Их code-action подход интеллектуально отличается от JSON-tool. Стоит сравнить.

---

### [LangChain — ReAct Agent Template](https://github.com/langchain-ai/react-agent)

| Поле | Значение |
|---|---|
| Language | Python |
| License | MIT |
| Recommendation | ⭐⭐⭐ |

**Чему учит**: как framework абстрагирует ReAct-паттерн. Шаблон для LangGraph Studio.

**Лучше всего для**: после Упражнения 3 (сначала собери с нуля). Потом сравни, что фреймворки делают за тебя.

---

### [Anthropic — Building Effective Agents (blog post)](https://www.anthropic.com/engineering/building-effective-agents)

| Поле | Значение |
|---|---|
| Format | Статья |
| Recommendation | ⭐⭐⭐⭐⭐ |

**Чему учит**: собственный гайд Anthropic о том, когда использовать agents (vs. workflow'ы), частые паттерны и ловушки. Обязательное чтение перед этапом 4.

**Лучше всего для**: концептуальная рамка. Читай после Упражнения 3, но до изучения фреймворков.

---

## ✅ Самопроверка перед этапом 4

Можешь:
- [ ] Определить tool schema (name + description + JSON schema input/output)
- [ ] Реализовать ReAct loop в <100 строках Python без фреймворка
- [ ] Объяснить, зачем agent'у условие выхода «я закончил»
- [ ] Сравнить CodeAct (код как action) vs JSON-tool подход
- [ ] Распознать, когда задаче не нужен agent

Если да → переходи к [Этапу 4 — Agent Frameworks](04-agent-frameworks.ru.md).

Если нет → запусти Упражнение 3 ещё раз. Не пропускай. Фреймворки этапа 4 будут мистифицировать тебя, если ты не понимаешь, что они абстрагируют.
