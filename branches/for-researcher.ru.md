# Для исследователей — специализированная ветка

> [繁體中文](./for-researcher.md) | [简体中文](./for-researcher.zh-Hans.md) | [English](./for-researcher.en.md) | **Русский**

> 🚀 **Первый раз ставишь Python или делаешь API-ключ?** Начни с [`resources/setup-guide.ru.md` §A-C](../resources/setup-guide.ru.md). Эта ветка предполагает, что ты можешь запустить Python-скрипт, есть API-ключ, умеешь git.

> [← Назад к README основного пути](../README.ru.md) · Сюда — после **A3 в Track A** или **этапа 7 в Track B**. Применять agentic AI к research workflow.

## Use cases

- Literature triage и сборка матриц
- Извлечение «памяти» статьи (claims, figures, citations)
- Multi-agent paper review (peer-review паттерны)
- Верификация NotebookLM brief'ов
- Автоматизация reference manager'ов

## Подборка проектов

> 💡 **Хочешь подвязать Claude Code к NotebookLM, Obsidian, Notion, Excel, PDF, Excalidraw и другим research-инструментам?** 62 интеграции в [`resources/mcp-skills-catalog.ru.md`](../resources/mcp-skills-catalog.ru.md) (по use case'ам). Раздел ниже держит research-специфичные инструменты и marketplace'ы.

### Research workflow marketplace'ы

#### [flonat/claude-research](https://github.com/flonat/claude-research) ⭐⭐⭐

Claude Code инфраструктура для PhD-исследователей — skills, agents, hooks, rules для академических workflow. Сильный фокус на LaTeX/bibliography.

---

### Literature RAG / Q&A

#### [Future-House/paper-qa](https://github.com/Future-House/paper-qa) ⭐⭐⭐⭐⭐

| Поле | Значение |
|---|---|
| Stars | ★ 8k+ |
| License | Apache-2.0 |

**Чему учит**: высокоточный RAG над PDF-документами с grounded цитированием на уровне предложений в каждом ответе.

**Лучше всего для**: исследователей, пишущих literature reviews, которым нужно «каждый ответ должен быть прослеживаем до источника». Строже generic RAG.

---

#### [assafelovic/gpt-researcher](https://github.com/assafelovic/gpt-researcher) ⭐⭐⭐⭐

| Поле | Значение |
|---|---|
| Stars | ★ 27k+ |
| License | Apache-2.0 |

**Чему учит**: автономный deep-research agent — planner + multi-source crawl + синтез отчёта. Дай ему тему — получи markdown / PDF brief.

**Лучше всего для**: исследователей, которым нужно быстро прощупать новые темы и сделать research-brief.

---

### Outline & Writing

#### [stanford-oval/storm](https://github.com/stanford-oval/storm) ⭐⭐⭐⭐

| Поле | Значение |
|---|---|
| Stars | ★ 28k+ |
| License | MIT |

**Чему учит**: multi-perspective outline-then-write pipeline — агент сначала генерирует outline с разных углов, потом раскрывает в Wikipedia-стиль статью. От Stanford OVAL.

**Лучше всего для**: освоения **outline-driven writing**. Хорош для topic-brief'ов с нуля; ближайший open-source аналог структурированного report-flow NotebookLM.

**Заметки**: последний push больше 6 месяцев назад — проверь дату последнего коммита, прежде чем полагаться.

---

#### [kaixindelele/ChatPaper](https://github.com/kaixindelele/ChatPaper) ⭐⭐⭐⭐⭐ (для китайскоязычных)

| Поле | Значение |
|---|---|
| Language | Chinese + Python |
| Stars | ★ 19k+ |
| License | NOASSERTION (кастомная non-commercial) |

**Чему учит**: полный arXiv workflow для китайских исследователей — paper summary + перевод + полировка + генерация ответов рецензентам. Поддерживается китайской командой; дефолты дружелюбны к китайскоязычным workflow'ам.

**Лучше всего для**: китайских аспирантов, ищущих entry-level paper-инструмент с китайским фокусом.

**Заметки**: лицензия — custom non-commercial — прочитай оригинальные условия перед использованием; обычная практика — research / personal use, но условия проверь сам.

---

### Интеграции с citation manager'ами

#### [MuiseDestiny/zotero-gpt](https://github.com/MuiseDestiny/zotero-gpt) ⭐⭐⭐⭐

| Поле | Значение |
|---|---|
| Stars | ★ 7k+ |
| License | AGPL-3.0 |

**Чему учит**: LLM-плагин для Zotero — чат с твоей библиотекой, суммаризация выделенного, генерация inline-заметок.

**Лучше всего для**: heavy-пользователей Zotero, желающих AI прямо в reading workflow без переключения инструментов.

**Заметки**: AGPL-3.0 (copyleft) — производные продукты, поставляющие модификации, должны следовать условиям.

---

### Research workflow Skills (от мейнтейнера репо)

> Skills / workspace'ы, которые мейнтейнер репо [@WenyuChiou](https://github.com/WenyuChiou) (Lehigh CEE PhD candidate) использует ежедневно в research. Здесь — чтобы другие исследователи могли подобрать напрямую. Полные записи в [`resources/mcp-skills-catalog.ru.md` §13-§14](../resources/mcp-skills-catalog.ru.md#13-research-workflow-skills-academic--paper--lit).

#### [WenyuChiou/ai-research-skills](https://github.com/WenyuChiou/ai-research-skills) ⭐⭐⭐⭐⭐

★ 60 · MIT — 14 Claude Code skills, покрывающих полный research pipeline (lit triage, research design, project context, manuscript writing, multi-AI delegation), упакованных как 5-plugin marketplace. Одна команда — всё установлено.

#### [WenyuChiou/research-hub](https://github.com/WenyuChiou/research-hub) ⭐⭐⭐⭐

★ 14 · MIT — Zotero + Obsidian + NotebookLM triple-workspace интеграция с CLI / MCP / REST / dashboard интерфейсами. Must-see для исследователей, использующих все три.

#### [WenyuChiou/zotero-skills](https://github.com/WenyuChiou/zotero-skills) ⭐⭐⭐⭐

★ 16 — Zotero CLI skill: search / add / classify / annotate. Дополняет zotero-gpt (chat внутри Zotero); этот позволяет Claude Code оперировать Zotero снаружи.

#### [WenyuChiou/academic-writing-skills](https://github.com/WenyuChiou/academic-writing-skills) ⭐⭐⭐

★ 2 · MIT — строгий skill для написания / ревизии / submission'а академической статьи. Автоматизирует banned-word аудит, figure-text coupling, submission checklist. Per-paper `journal_format` / `style_overrides` для кастомизации.

#### [WenyuChiou/codex-delegate](https://github.com/WenyuChiou/codex-delegate) ⭐⭐⭐⭐⭐ + [WenyuChiou/gemini-delegate-skill](https://github.com/WenyuChiou/gemini-delegate-skill) ⭐⭐⭐⭐

★ 57 + ★ 34 · MIT — связка multi-LLM делегирования. Research-сценарий: Claude как планировщик + Codex исполняет имплементацию (код / figures / tables) + Gemini пишет длинную форму (китайские отчёты, английские секции статей). Практическая реализация концепции multi-agent из этапа 7.

---

### Multi-Agent для research

#### [langchain-ai/open_deep_research](https://github.com/langchain-ai/open_deep_research) ⭐⭐⭐⭐⭐

| Поле | Значение |
|---|---|
| Stars | ★ 11k+ |
| License | MIT |

**Чему учит**: open-source Deep Research — поддерживает single-agent и supervisor + multi-researcher архитектуры (multi-agent путь сейчас в `src/legacy/`), параллельный поиск, citation-grounded синтез отчётов. Прочный референс для «LLM-agent, авто-производящий cited brief».

**Лучше всего для**: исследователей, строящих workflow «agent авто-генерирует cited brief». Прочный open-source выбор, когда нужна поддерживаемая reference implementation.

**Заметки**: зависит от LangGraph + search tools (нужен API-ключ).

---

#### [SakanaAI/AI-Scientist-v2](https://github.com/SakanaAI/AI-Scientist-v2) ⭐⭐⭐⭐

| Поле | Значение |
|---|---|
| Stars | ★ 6k+ |
| License | The AI Scientist Source Code License (source-available, non-commercial + manuscript-disclosure clause) |

**Чему учит**: end-to-end multi-agent science-цикл: ideate → code → experiment → write → peer-review. Research-реализация Sakana AI «AI пишет полную ML-статью».

**Лучше всего для**: исследователей, желающих увидеть «как выглядит swarm агентов, прокручивающий полный research lifecycle». Архитектурный референс, не production-инструмент.

**Заметки**: выходы demo-уровня (не field-ready), смещение в сторону ML/CS-домена. Лицензия — кастомный source-available (с manuscript-disclosure clause) — прочитай LICENSE перед использованием.

---

> Всё ещё не хватает: активно поддерживаемой peer-review автоматизации, conference-review пайплайнов. Если собрал или знаешь такое — открой PR.

## Обязательное чтение

1. [The Effortless Academic — Claude Code beginner guides](https://effortlessacademic.com/claude-code-and-cowork-for-academics-beginner-guide-part-1/)
2. [Pedro Sant'Anna — Researcher setup guide](https://paulgp.substack.com/p/getting-started-with-claude-code)

## Workflow'ы для освоения

- **Literature triage**: используй `paper-qa` для grounded Q&A над PDF-библиотекой, потом `gpt-researcher` для авто-генерации brief'ов, вывод в Obsidian / Notion
- **Outline-driven writing**: `storm` для авто-генерации multi-perspective outline'а по теме, потом руками разворачивай в формальные секции
- **Chinese paper workflow**: `ChatPaper` для summary / перевода / полировки, потом human review
- **Zotero in-app AI**: установи `zotero-gpt`, задавай вопросы или суммаризируй выделенное прямо в reading flow
