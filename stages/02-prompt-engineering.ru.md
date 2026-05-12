# Этап 2 — Prompt Engineering

> [繁體中文](./02-prompt-engineering.md) | [简体中文](./02-prompt-engineering.zh-Hans.md) | [English](./02-prompt-engineering.en.md) | **Русский**


⏱ **Оценка времени**: 1–2 недели (~5–12 часов)

> 👋 **Пришёл с [этапа 1](01-llm-basics.ru.md)?** Хорошо — умеешь звать API. Следующие 5–12 часов: пиши переиспользуемые структурированные промпты, используй few-shot и chain-of-thought для трудных reasoning-задач, количественно оценивай улучшение промпта через eval'ы. **Прыгнул прямо сюда?** Убедись, что можешь вызвать LLM API и оценить стоимость в токенах — если нет, вернись на [Этап 1](01-llm-basics.ru.md).

> 💡 Незнакомый термин? (prompt / few-shot / CoT / system prompt / …) → см. [`resources/glossary.ru.md`](../resources/glossary.ru.md).

## 📌 Цели обучения

После этого этапа сможешь:
- Писать структурированные промпты (role + task + format + examples)
- Применять few-shot prompting и знать, когда это помогает
- Использовать chain-of-thought (CoT) для reasoning-задач
- Итеративно дорабатывать промпт и измерять улучшение
- Распознавать, когда prompting упирается в потолок (нужны tools / agents)

## 🚪 Условия входа

Уже должен:
- Уметь звать LLM API (этап 1)
- Уметь парсить / итерировать API-ответы

## 📚 Обязательное чтение

1. [**Anthropic Prompt Engineering Guide**](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/overview) — официальный, хорошо организованный
2. [**OpenAI Prompt Engineering**](https://platform.openai.com/docs/guides/prompt-engineering) — точка зрения OpenAI
3. [**dair-ai Prompt Engineering Guide**](https://www.promptingguide.ai/) — академический вкус, в глубину
4. [**Anthropic — Prompting Best Practices**](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/be-clear-and-direct) — be clear and direct

## 🛠 Практические упражнения

### Упражнение: System Prompt
Одно и то же user message, три разных system prompt'а. Понаблюдай, как меняется личность / формат вывода.

### Упражнение: Few-Shot
Выбери задачу классификации. Запусти 0-shot, потом 3-shot. Замерь разницу accuracy.

### Упражнение: CoT
Выбери математическую word-задачу. Сравни:
- Голый промпт
- Голый промпт + «Let's think step by step»
- Голый промпт + worked example с CoT

### Упражнение: Iterative Refinement
Возьми расплывчатый промпт, дорабатывай 5 раз. Трекай итерации. Заметь, какие изменения улучшают качество.

## 🎯 Подборка проектов

### [dair-ai/Prompt-Engineering-Guide](https://github.com/dair-ai/Prompt-Engineering-Guide)

| Поле | Значение |
|---|---|
| Stars | ★ 60k+ |
| License | MIT |
| Recommendation | ⭐⭐⭐⭐⭐ |

**Чему учит**: end-to-end prompt engineering от основ до продвинутого (CoT, ToT, ReAct, RAG). Академический вкус, но практический.

**Лучше всего для**: референс. Пролистай один раз, возвращайся, когда нужна конкретная техника.

---

### [f/awesome-chatgpt-prompts](https://github.com/f/awesome-chatgpt-prompts)

| Поле | Значение |
|---|---|
| Stars | ★ 130k+ |
| License | CC0 |
| Recommendation | ⭐⭐⭐ |

**Чему учит**: сотни role-based промптов. Паттерны «Act as a [role]...».

**Лучше всего для**: вдохновение, когда застрял. Не копируй дословно — адаптируй паттерны.

---

### [PromptingGuide.ai](https://www.promptingguide.ai/)

**Чему учит**: тот же контент, что dair-ai на GitHub, но в формате сайта с живыми примерами.

**Лучше всего для**: чтения с мобильного.

---

### [microsoft/prompt-engine](https://github.com/microsoft/prompt-engine)

| Recommendation | ⭐⭐⭐ |
|---|---|

**Чему учит**: TypeScript-библиотека для управления промптами в масштабе (templating, conversation history).

**Лучше всего для**: когда начинаешь управлять многими промптами в production.

---

### [microsoft/promptflow](https://github.com/microsoft/promptflow)

| Поле | Значение |
|---|---|
| Stars | ★ 10k+ |
| Recommendation | ⭐⭐⭐ |

**Чему учит**: визуальный дизайн промптов + evaluation tooling.

**Лучше всего для**: команд, строящих prompt-heavy приложения с eval-потребностями.

---

### [GoogleCloudPlatform/generative-ai](https://github.com/GoogleCloudPlatform/generative-ai)

| Recommendation | ⭐⭐⭐ |
|---|---|

**Чему учит**: cookbook от Google Cloud по prompt'ингу (notebooks, фокус на PaLM/Gemini).

**Лучше всего для**: cross-vendor перспектива, если используешь стек Google.

---

### [Anthropic Cookbook — Prompt patterns](https://github.com/anthropics/anthropic-cookbook)

Уже упомянут в этапе 1. Конкретно `misc/prompt_caching.ipynb` и `multimodal/` notebooks учат продвинутым prompt-паттернам.

---

### [stanfordnlp/dspy](https://github.com/stanfordnlp/dspy)

| Поле | Значение |
|---|---|
| Language | Python |
| Stars | ★ 34k+ |
| License | MIT |
| Recommendation | ⭐⭐⭐⭐⭐ |

**Чему учит**: Prompt-as-code — определяй signatures + modules, оптимизируй промпты через компиляторы / teleprompters вместо ручной настройки f-string'ов. Естественный мостик с этапа 2 на этап 3. От Stanford NLP.

**Лучше всего для**: читателей, закончивших гайд dair-ai и спросивших «как масштабировать промпты за пределами hard-coded строк?»

**Заметки**: это framework, не туториал — выше learning bar, чем prompt-engineering-guide. Пара с официальным сайтом туториалов dspy.ai.

---

### [NirDiamant/Prompt_Engineering](https://github.com/NirDiamant/Prompt_Engineering)

| Поле | Значение |
|---|---|
| Language | Python / Jupyter |
| Stars | ★ 7k+ |
| License | NOASSERTION (кастомные условия, research/non-commercial — читай перед использованием) |
| Recommendation | ⭐⭐⭐⭐ |

**Чему учит**: 22 prompt-engineering техники как запускаемые Jupyter notebooks (zero-shot → CoT → ReAct → constitutional). Винтаж 2025, более hands-on, чем dair-ai.

**Лучше всего для**: учеников, предпочитающих «run-and-learn». Каждая техника — отдельный notebook, бери что интересно.

---

## 🔭 За пределами prompts: context engineering

Когда обнаруживаешь, что **одного промпта уже не хватает** покрыть проблему — и нужно динамически собирать system prompt + retrieved chunks + memory + tool definitions + multi-turn history — ты вырос из prompt engineering в **context engineering**. Это следующий слой над.

**Не пытайся учить сейчас**, просто знай направление:

- Сначала столкнёшься в [Этапе 6 (Memory · RAG)](06-memory-rag.ru.md) (какие данные идут в промпт)
- Полностью встретишься в [Этапе 7 (Multi-Agent · Production)](07-multi-agent-production.ru.md) (бюджет context window, memory layering, observability)

Дальнейшее чтение (опционально, когда захочешь копнуть глубже):

- [`Meirtz/Awesome-Context-Engineering`](https://github.com/Meirtz/Awesome-Context-Engineering) (★ 3k+) — comprehensive survey от prompt engineering до production agents
- [`Windy3f3f3f3f/how-claude-code-works`](https://github.com/Windy3f3f3f3f/how-claude-code-works) (★ 2k+) — внутренности Claude Code, включает главу про context engineering

## ✅ Самопроверка перед этапом 3

Можешь:
- [ ] Написать промпт с system message + user message + 3 example messages (few-shot)
- [ ] Продемонстрировать улучшение accuracy с CoT на reasoning-задаче
- [ ] Итеративно дорабатывать промпт 5 раз, трекая каждую версию
- [ ] Определить, когда prompting — не тот инструмент (и нужен tool use)

Если да → переходи к [Этапу 3 — Tool Use & Agent Intro](03-tool-use-and-hello-agent.ru.md). Это самый важный этап — не пробегай мимо промптов, но и не залипай тут.
