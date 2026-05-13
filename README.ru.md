<div align="right">
  <a href="./README.md">繁體中文</a> | <a href="./README.zh-Hans.md">简体中文</a> | <a href="./README.en.md">English</a> | <strong>Русский</strong>
</div>

<div align="center">

![Карта обучения AI Agent](resources/diagrams/banner.en.png)

# awesome-agentic-ai-zh

</div>

[![License](https://img.shields.io/badge/license-MIT-blue)](LICENSE)
[![繁中](https://img.shields.io/badge/語言-繁體中文-red)](README.md)
[![简中](https://img.shields.io/badge/語言-简体中文-orange)](README.zh-Hans.md)
[![EN](https://img.shields.io/badge/lang-English-blue)](README.en.md)
[![RU](https://img.shields.io/badge/lang-Русский-green)](README.ru.md)
![GitHub stars](https://img.shields.io/github/stars/WenyuChiou/awesome-agentic-ai-zh?logo=github)
![GitHub forks](https://img.shields.io/github/forks/WenyuChiou/awesome-agentic-ai-zh?logo=github)

> **Русская версия. Канонический файл — zh-TW [README.md](README.md)**. Контент сначала курируется на zh-TW, эта страница — зеркало для русскоязычных читателей.

Карта обучения agentic AI — **от основ LLM до построения multi-agent систем**. Структурированный путь из 7 этапов: от «что такое LLM, как считаются токены» до multi-agent orchestration (оркестровки нескольких агентов) и локального развёртывания. На каждом этапе — обязательные демо, обязательное чтение и подборка проектов.

---

## 🎯 Зачем это нужно

Если ты хочешь изучить AI-приложения или вырасти от основ до multi-agent систем — **главная проблема не в нехватке ресурсов, а в непонимании с чего начать**. Awesome-списки на английском и китайском содержат сотни репозиториев, но без пути; люди, изучающие Claude Code, LangGraph или RAG, разбросаны по разным сообществам, используют разные термины и рекомендуют разные стартовые проекты.

Мы собрали **145+ отобранных проектов** в карту обучения «с нуля до продвинутых multi-agent», разбитую на **7 этапов**. Каждый этап чётко говорит, **что учить, какие упражнения делать, какие проекты изучать и какую самопроверку пройти перед следующим этапом**.

После основного пути ты переходишь от роли «**пользователь LLM**» к роли «**строитель agent-систем**» — способного проектировать multi-agent коллаборацию, писать свой MCP server и поставлять реальные agent-системы.

---

## 📋 Содержание

- [🎯 Зачем это нужно](#-зачем-это-нужно)
- [📚 Быстрый старт](#-быстрый-старт)
- [🗺️ Карта обучения (две дорожки)](#️-карта-обучения-две-дорожки)
- [💡 Как учиться](#-как-учиться)
- [📚 Связанные ресурсы](#-связанные-ресурсы)
- [🤝 Контрибьютинг](#-контрибьютинг)
- [🙏 Благодарности](#-благодарности)
- [🎓 Цитирование](#-цитирование)
- [License](#license)

---

## 📚 Быстрый старт

### 🚀 Первый раз с AI agents / никогда не писал код?

Начни здесь: **[`resources/setup-guide.ru.md`](resources/setup-guide.ru.md)** — 30–45 минут от нуля. Получишь API-ключ, установишь Python и запустишь первый LLM hello-world.

### Читать онлайн
- **[Карта обучения (две дорожки)](#️-карта-обучения-две-дорожки)** — прочитай этот раздел, чтобы выбрать дорожку A или B
- **[Этап 0: Foundations](stages/00-foundations.ru.md)** — уже знаешь Python / git / API? Сразу к этапу 1

### Локальный клон
```bash
git clone https://github.com/WenyuChiou/awesome-agentic-ai-zh.git
cd awesome-agentic-ai-zh
# Начни с stages/00-foundations.ru.md
```

### ✨ Что ты получишь

- 📖 **Полностью бесплатно** — MIT-лицензия, весь контент открыт
- 🗺️ **Две дорожки** — Track A (CLI Power User) для «использовать готовые CLI»; Track B (Agent Builder) для «собрать своё». Общий фундамент — этапы 0–2.
- 🛠️ **Обязательные практические упражнения** — 1–5 мини-проектов на этап (спецификации + критерии успеха, **код пишешь сам**, не готовые демо); просто читать — не считается
- 🎯 **145+ отобранных проектов** — каждый со звёздным рейтингом, целевой аудиторией, описанием чему учит и как запустить (включая локальные LLM-раннеры: Ollama, llama.cpp, LocalAI, MLX)
- 🌏 **Многоязычность** — канонический zh-TW, зеркала на английском, упрощённом китайском и русском
- 🎓 **Шире фреймворков: экосистема Claude Code** — MCP / Skills / Plugins / SDK, полный стек
- 🔬 **5 специализированных веток** — researcher / developer / teacher / knowledge worker / **everyday user**
- ⏱️ **Затраты времени, честно** — минимум 14–19 недель, реалистично 5–6 месяцев (5–8 ч/нед part-time)

---

## 🗺️ Карта обучения (две дорожки)

![Карта обучения AI Agent](resources/diagrams/learning-map.en.png)

После **этапов 0–2 (общий фундамент)** выбери дорожку по цели:

- **Track A — CLI Power User**: ты хочешь **ИСПОЛЬЗОВАТЬ** существующие CLI agents (Claude Code, Codex, OpenCode, Gemini CLI и т. д.), чтобы делать работу, а не строить агентов с нуля. 3 под-этапа (A1–A3).
- **Track B — Agent Builder**: ты хочешь **СОБРАТЬ** свой агент — выучить фреймворки, написать ReAct, спроектировать multi-agent систему. Основной путь — этапы 3–7.

Дорожки **не взаимоисключающие** — большинство сначала идёт по A, чтобы быстро набраться практики, затем возвращается к B за внутренностями (или наоборот). Этап 5 (Claude Code Ecosystem) общий для обеих дорожек.

### Общий фундамент (этапы 0–2)

| Этап | Тема | Ключевой контент | Время |
|---|---|---|---|
| **0** | [Foundations](stages/00-foundations.ru.md) | Python · CLI · git · API · JSON | 1–2 нед |
| **1** | [LLM Basics](stages/01-llm-basics.ru.md) | tokens · API · сравнение моделей · локальный LLM | 1 нед |
| **2** | [Prompt Engineering](stages/02-prompt-engineering.ru.md) | system prompts · few-shot · CoT | 1–2 нед |

### Track A — CLI Power User (использовать CLI для работы)

| Этап | Тема | Ключевой контент | Время |
|---|---|---|---|
| **A1** | [CLI Agent: введение и выбор](tracks/cli/A1-cli-intro.ru.md) | сравнение 7 CLI · установка · первый запуск | 1 нед |
| **A2** | [Паттерны CLI workflow](tracks/cli/A2-cli-workflow.ru.md) | CLAUDE.md · slash commands · multi-step decomposition | 1–2 нед |
| **A3** | [Интеграция и продакшен](tracks/cli/A3-cli-production.ru.md) | MCP-into-CLI · CI automation · cost / observability | 1–2 нед |

> **Общее время Track A**: 3–5 недель (с этапами 0–2: 6–8 недель). Основной справочник: [`resources/cli-agents-guide.ru.md`](resources/cli-agents-guide.ru.md).

### Track B — Agent Builder (собрать агента с нуля)

| Этап | Тема | Ключевой контент | Время |
|---|---|---|---|
| **3** ⭐ | [Tool Use & Hello Agent](stages/03-tool-use-and-hello-agent.ru.md) | function calling · ReAct · 5 практических упражнений | 2–3 нед |
| **4** | [Agent Frameworks](stages/04-agent-frameworks.ru.md) | LangGraph · AutoGen · CrewAI · Smolagents | 2–3 нед |
| **5** ⭐⭐ | [Claude Code Ecosystem](stages/05-claude-code-ecosystem.ru.md) | MCP · Skills · Plugins · Marketplace (общий для обеих дорожек) | 3–4 нед |
| **6** | [Memory · RAG · Advanced](stages/06-memory-rag.ru.md) | векторные БД · long-term memory · contextual retrieval | 2 нед |
| **7** | [Multi-Agent · Advanced](stages/07-multi-agent-production.ru.md) | multi-agent orchestration · eval · observability · advanced SDK | 2–4 нед |

> **Общее время Track B**: минимум **14–19 недель**, реалистично **5–6 месяцев** (5–8 ч/нед part-time)

> 💡 **Нужен конкретный сквозной пример?** [Собери первого AI agent за 7 шагов](walkthroughs/build-first-agent-in-7-steps.ru.md) — один и тот же Paper Summary Bot прослежен с этапа 1 до этапа 7, ~350 строк рабочего кода (**Track B**)

После основного пути — одна из 5 специализированных веток. **Не уверен, какую брать?**

![Дерево выбора ветки](resources/diagrams/branch-decision-tree.en.png)

> 💡 **Ветку Everyday User можно читать сразу, без прохождения основного пути** — она для тех, кто хочет использовать AI, без написания кода.

| Ветка | Для кого | Темы |
|---|---|---|
| 🔬 [Researcher](branches/for-researcher.ru.md) | Аспиранты, постдоки, PI | Lit triage · paper writing · multi-agent review |
| 💻 [Developer](branches/for-developer.ru.md) | Программисты | Cursor · Aider · CLI delegation · code review |
| 🎓 [Teacher](branches/for-teacher.ru.md) | Преподаватели, инструкторы | Lesson planning · слайды · feedback студентам · privacy / этика · prompt templates |
| 📊 [Knowledge Worker](branches/for-knowledge-worker.ru.md) | Консультанты, PM, аналитики | Email · meeting notes · автоматизация отчётов |
| 👥 [Everyday User](branches/for-everyday-users.ru.md) | Пользователи ChatGPT / Claude.ai | Ежедневное письмо · обучение · privacy · введение в CLI agent |

---

## 💡 Как учиться

Привет — будущий строитель agent-систем. Несколько советов перед стартом.

Эта карта обучения балансирует концепции и практику, помогая тебе **перейти от пользователя LLM к строителю agent-систем**. Предполагается **базовый Python**. До старта нужно:

- **Базовый Python** — писал функции, использовал API, читаешь JSON
- **Базовый git** — clone, commit, push
- **Мотивация учиться** — agents — самая быстро меняющаяся область AI в 2025+ и требует постоянных усилий

Если чего-то не хватает — пройди этап 0; если всё ок — **стартуй с этапа 1**.

Основной путь состоит из 4 частей:

- **Часть 1 (этапы 0–2): Foundations & LLM Basics** — Python / git / API, что такое LLM, дизайн промптов
- **Часть 2 (этапы 3–4): Собери своего агента** — от tool use до agents, изучи основные фреймворки
- **Часть 3 (этап 5): Claude Code Ecosystem** — MCP / Skills / Plugins, сердце пути
- **Часть 4 (этапы 6–7): Продвинутая интеграция** — memory / RAG / multi-agent коллаборация

После основного пути (14–19 недель) — выбери ветку.

Главный совет: **не пропускай практические упражнения**. Упражнения каждого этапа — «без них не выучишь»; пробежал глазами — застрянешь дальше.

Готов? [Старт с этапа 0](stages/00-foundations.ru.md).

---

## 📚 Связанные ресурсы

Полный блок связанных ресурсов (определения терминов + подборка MCP/Skill для повседневных инструментов + awesome-списки + ресурсы китайского сообщества) живёт в **[RESOURCES.ru.md](RESOURCES.ru.md)**, чтобы README оставался сфокусированным.

Частые быстрые ссылки:

- 🚀 **Никогда не писал код или первый раз с AI agents?** → [`resources/setup-guide.ru.md`](resources/setup-guide.ru.md) (30–45 минут от нуля)
- 📖 **Не знаешь термин?** (LLM, agent, RAG, token, MCP, Skill, vector DB, …) → [`resources/glossary.ru.md`](resources/glossary.ru.md) — 30+ частых терминов, по 30–80 слов определения + указание этапа, где он покрыт
- 🔑 **Что значат MCP / Skills / Plugins** → [RESOURCES.ru.md §три ключевых термина](RESOURCES.ru.md#three-core-terms-mcp--skills--plugins)
- 🔌 **Подключить Notion / Obsidian / Excel / GitHub и т. д.** → [RESOURCES.ru.md §интеграции с повседневными инструментами](RESOURCES.ru.md#daily-tool-integrations-mcp-servers--skills) или полный каталог из 62 записей [`resources/mcp-skills-catalog.ru.md`](resources/mcp-skills-catalog.ru.md)
- 🔬 **Research workflow + связка multi-LLM делегирования** → [RESOURCES.ru.md §research workflow](RESOURCES.ru.md#research-workflow-by-the-repo-maintainer)
- 📚 **Тематические awesome-списки / китайское сообщество** → [RESOURCES.ru.md §тематические списки](RESOURCES.ru.md#topic-based-awesome-lists)

---

## 🤝 Контрибьютинг

Этот репозиторий — обучающий документ по AI; если ты тоже собрал хорошие ресурсы, контрибьюты очень приветствуются:

- 🐛 **Bug reports** — неверный контент, битые ссылки, устаревшая инфа → открой Issue
- 💡 **Предложения** — пропущенный этап / новый проект в подборку → открой Issue для обсуждения
- 📝 **Улучшения** — уточнить контент этапа, исправить опечатки → прямой PR
- ✍️ **Добавить проект** — 1–3 новых проекта на этап с обоснованием «почему это учит данному этапу»
- 🌏 **Переводы** — улучшить английскую/русскую версию или перевести на другие языки
- 🌱 **Стать мейнтейнером этапа / ветки** — долгосрочный ревью конкретной области, см. [CONTRIBUTORS.md](CONTRIBUTORS.md)

Процесс PR и правила стиля: [CONTRIBUTING.md](CONTRIBUTING.md) + [resources/style-guide.ru.md](resources/style-guide.ru.md).

> 📅 **Хочешь увидеть, что зашло недавно?** → [`CHANGELOG.md`](CHANGELOG.md) (последние 14 дней).
> Внутренний прогресс phase rollout и launch checklist: [`.github/launch-checklist.md`](.github/launch-checklist.md) (внутренний документ мейнтейнера).

---

## 🙏 Благодарности

### Источники вдохновения

- [**Datawhale Hello-Agents**](https://github.com/datawhalechina/hello-agents) — образец систематической структуры agent-туториала; вдохновил наш дизайн глав + прогресса
- [**Datawhale community**](https://github.com/datawhalechina) — знаковое китайское ML-обучающее сообщество; несколько якорных проектов взяты оттуда
- [**liyupi/ai-guide**](https://github.com/liyupi/ai-guide) — крупнейший китайский «AI mega-guide» + Vibe Coding tutorial (покрывает Agent Skills / RAG / MCP / A2A / Harness Engineering). Этот репо — «структурированная карта», ai-guide — «хаб ресурсов вширь», они дополняют друг друга

### Связанные проекты

Другие списки в той же области — полезно листать параллельно при поиске конкретных инструментов:

- [`wong2/awesome-mcp-servers`](https://github.com/wong2/awesome-mcp-servers) — категоризированный каталог MCP servers
- [`punkpeye/awesome-mcp-servers`](https://github.com/punkpeye/awesome-mcp-servers) — ещё один каталог MCP servers
- [`hesreallyhim/awesome-claude-code`](https://github.com/hesreallyhim/awesome-claude-code) — список инструментов и плагинов Claude Code

Это чисто каталоги (листай и выбирай). Этот репо отличается тем, что в нём **порядок обучения с этапа 0 до продакшена**.

### Контрибьюторы

[![Contributors](https://contrib.rocks/image?repo=WenyuChiou/awesome-agentic-ai-zh)](https://github.com/WenyuChiou/awesome-agentic-ai-zh/graphs/contributors)

Новые контрибьюторы появляются выше автоматически. Полный список → [GitHub Contributors](https://github.com/WenyuChiou/awesome-agentic-ai-zh/graphs/contributors).

### Лично

- [@WenyuChiou](https://github.com/WenyuChiou) — мейнтейнер

---

## 🎓 Цитирование

Если эта карта обучения помогла твоему обучению или работе — пожалуйста, цитируй:

```bibtex
@misc{awesome_agentic_ai_zh_2026,
  title  = {awesome-agentic-ai-zh: A Structured Learning Roadmap for Agentic AI},
  author = {Chiou, Wenyu},
  year   = {2026},
  url    = {https://github.com/WenyuChiou/awesome-agentic-ai-zh},
  note   = {7-stage learning path from prerequisites to advanced multi-agent systems, with curated projects + hello-X demos. Multilingual (zh-TW / English / Russian).}
}
```

---

## 📈 История звёзд

[![Star History Chart](https://api.star-history.com/svg?repos=WenyuChiou/awesome-agentic-ai-zh&type=Date)](https://star-history.com/#WenyuChiou/awesome-agentic-ai-zh&Date)

---

## License

MIT. Поддерживает [@WenyuChiou](https://github.com/WenyuChiou).

<div align="center">
  <p>⭐ Если репо помог — поставь Star, это важно для итераций</p>
</div>
