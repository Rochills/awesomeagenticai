# Этап 5 — Claude Code Ecosystem ⭐⭐

> [繁體中文](./05-claude-code-ecosystem.md) | [简体中文](./05-claude-code-ecosystem.zh-Hans.md) | [English](./05-claude-code-ecosystem.en.md) | **Русский**


⏱ **Оценка времени**: 3–4 недели (~15–25 часов)

> 💡 Этап крутится вокруг четырёх терминов (**MCP / Skills / Plugins / Marketplace**) → не знаком? См. [`resources/glossary.ru.md` §5](../resources/glossary.ru.md#5-экосистема-claude-code).

> 📌 **Этот этап используется обеими дорожками**:
> - **Track A (CLI Power User)**: A2 использует [5.1 (Claude Code basics)](#51--claude-code-basics); A3 использует [5.2 (MCP)](#52--mcp-model-context-protocol-foundation) + выборочно [5.3 (Skills)](#53--skills-claude-code-behavior-layer) и [5.4 (Plugins)](#54--plugins--marketplaces) (Упражнение CLI-12 в A3 учит упаковывать CLAUDE.md / команды в plugin). Угол чтения: «**как хорошо использовать Claude Code**»
> - **Track B (Agent Builder)**: проходит полный этап 5.1 → 5.4 как «**как Claude Code работает изнутри**» — deep dive

> ⚠️ **Этот этап — не путь для локального LLM.** Claude Code требует Anthropic API / OAuth и не может напрямую переключиться на Ollama или локальный endpoint. Для offline-работы, privacy-чувствительных файлов или избегания API-квот используй [`resources/cookbook.ru.md` Recipe 6](../resources/cookbook.ru.md#6-local-llm--cli-agent-quick-walkthrough) с BYO-LLM CLI agent'ом — OpenCode / goose / Aider / Hermes.

## Стек одним взглядом

Сверху вниз, каждый слой стоит на нижнем:

![Claude Code Ecosystem Stack](../resources/diagrams/stage5-stack.en.png)

Каждый слой добавляет одну способность:
- **API + SDK**: программный доступ к LLM
- **Tool Use**: LLM может вызывать функции, которые ты определил
- **MCP**: стандартизированный протокол, чтобы любой LLM-host мог использовать любой tool server
- **Skills**: behavior bundles для Claude Code, которые могут оборачивать MCP-tools
- **Plugins**: пакуй + поставляй Skills, hooks, commands, MCP-конфиги как одну единицу

Этап имеет 4 подсекции. **Делай в порядке** — каждая стоит на предыдущей.

```
5.1  Claude Code Basics       3-5 дней   (установка, slash commands, CLAUDE.md)
5.2  MCP — Protocol Layer     5-7 дней   (напиши первый MCP server)
5.3  Skills — Behavior Layer  5-7 дней   (напиши первый SKILL.md)
5.4  Plugins & Marketplaces   5-7 дней   (упакуй и поставь)
```

После этого этапа сможешь расширять Claude Code, писать свой MCP server и поставлять plugin marketplace.

---

## 5.1 — Claude Code Basics

### Цели обучения
- Установить Claude Code на свою ОС
- Использовать slash commands (`/help`, `/compact`, `/clear`, `/plan`)
- Понимать структуру директории `~/.claude/`
- Написать project-level `CLAUDE.md`, кастомизирующий поведение

### Обязательное чтение
1. [**Anthropic — Claude Code Quickstart**](https://docs.anthropic.com/en/docs/claude-code/quickstart) — официальный install guide
2. [**Anthropic — CLAUDE.md best practices**](https://docs.anthropic.com/en/docs/claude-code/memory) — как писать project memory
3. [**KimYx0207/Claude-Code-x-OpenClaw-Guide-Zh**](https://github.com/KimYx0207/Claude-Code-x-OpenClaw-Guide-Zh) — zh-Hans beginner guide

### Практические упражнения
- **Упражнение: Claude Code** — установка, запуск первой сессии, попроси Claude прочитать файл и суммаризировать
- **Упражнение: CLAUDE.md** — напиши project CLAUDE.md, понаблюдай за изменением поведения

### Подборка проектов
- [**anthropics/claude-code**](https://github.com/anthropics/claude-code) — официальный репо (issues, releases)
- [**KimYx0207/Claude-Code-x-OpenClaw-Guide-Zh**](https://github.com/KimYx0207/Claude-Code-x-OpenClaw-Guide-Zh) — zh-Hans walkthrough
- [**hesreallyhim/awesome-claude-code**](https://github.com/hesreallyhim/awesome-claude-code) — более широкий список ресурсов (сейчас перестраивается)

---

## 5.2 — MCP (Model Context Protocol) ⭐ Foundation

### Цели обучения
- Объяснить три абстракции MCP (Tools, Resources, Prompts)
- Подключить существующий MCP server к Claude Desktop или Claude Code
- Написать минимальный MCP server на Python, отдающий 1–2 tool'а
- Различать MCP server vs Tool Use vs Skills vs Plugins

### Обязательное чтение
1. [**Anthropic — Introducing MCP**](https://www.anthropic.com/news/model-context-protocol) — оригинальный анонс, концептуальный обзор
2. [**MCP Specification**](https://modelcontextprotocol.io/specification) — собственно spec протокола
3. [**Complete Guide to MCP in 2026**](https://dev.to/x4nent/complete-guide-to-mcp-model-context-protocol-in-2026-architecture-implementation-and-4a11) — implementation walkthrough

### Практические упражнения
- **Упражнение: MCP client** — установи `modelcontextprotocol/servers/filesystem` и подключи через Claude Desktop. Посмотри, как Claude читает твои файлы.
- **Упражнение: MCP server** — напиши Python MCP server, отдающий один tool (например, «convert temperature»). Подключи из Claude Code.
- **Упражнение: MCP в production** — подключи 2–3 MCP server'а в одной Claude-сессии и понаблюдай, как они координируются.

### Подборка проектов

> 💡 **Ищешь MCP-серверы для повседневных инструментов (Notion / Obsidian / Excel / Postgres / Playwright / Figma…)?**
> См. [`resources/mcp-skills-catalog.ru.md`](../resources/mcp-skills-catalog.ru.md) — 62 MCP server / Skill сгруппированы в 14 категорий со stars / license / audience. Раздел ниже остаётся сфокусирован на «**референсе для написания своего MCP server**» (официальные серверы + SDK).

#### [modelcontextprotocol/servers](https://github.com/modelcontextprotocol/servers) ⭐ Official

| Поле | Значение |
|---|---|
| Language | TypeScript / Python |
| Stars | ★ 85k+ |
| License | MIT |
| Recommendation | ⭐⭐⭐⭐⭐ |

**Чему учит**: 20+ reference MCP-серверов (filesystem, git, github, sqlite, time, fetch, memory, sequential thinking). Канонические примеры для написания своего.

**Лучше всего для**: Упражнение 1 и как референс. Прочти source `everything` server'а и `filesystem` server'а, чтобы понять протокол.

**Запуск**:
```bash
npx -y @modelcontextprotocol/server-filesystem /path/to/dir
# Или используй Python-серверы:
pip install mcp-server-fetch
```

---

#### [modelcontextprotocol/python-sdk](https://github.com/modelcontextprotocol/python-sdk)

| Поле | Значение |
|---|---|
| Language | Python |
| License | MIT |
| Recommendation | ⭐⭐⭐⭐⭐ |

**Чему учит**: официальный Python SDK для написания MCP-серверов. Используй для Упражнения 2.

**Запуск**:
```bash
pip install mcp
# Дальше следуй https://github.com/modelcontextprotocol/python-sdk#quickstart
```

---

#### [modelcontextprotocol/typescript-sdk](https://github.com/modelcontextprotocol/typescript-sdk)

| Поле | Значение |
|---|---|
| Language | TypeScript |
| License | MIT |
| Recommendation | ⭐⭐⭐⭐ |

**Чему учит**: TypeScript-эквивалент Python SDK. Бери, если предпочитаешь TS.

---

#### [wong2/awesome-mcp-servers](https://github.com/wong2/awesome-mcp-servers) ⭐ Каталог

| Поле | Значение |
|---|---|
| Format | Курируемый список |
| Recommendation | ⭐⭐⭐⭐⭐ |

**Чему учит**: каталог 150+ community MCP-серверов, организованных по категориям — search, code, cloud, communication, finance.

**Лучше всего для**: обнаружение существующих серверов перед написанием своего. Листай, когда есть конкретная tool-need.

**Заметки**: submission через их сайт (mcpservers.org).

---

#### [punkpeye/awesome-mcp-servers](https://github.com/punkpeye/awesome-mcp-servers)

| Поле | Значение |
|---|---|
| Recommendation | ⭐⭐⭐⭐ |

**Чему учит**: альтернативный каталог MCP-серверов с другой организацией (часто более актуальный).

**Лучше всего для**: cross-reference со списком wong2. Разные кураторы вытаскивают разные проекты.

---

#### [github/github-mcp-server](https://github.com/github/github-mcp-server)

| Поле | Значение |
|---|---|
| Recommendation | ⭐⭐⭐⭐ |

**Чему учит**: как структурирован реальный production MCP server. Официально поддерживается GitHub.

**Лучше всего для**: чтение source как reference implementation для production-grade MCP server.

---

#### [21st-dev/magic-mcp](https://github.com/21st-dev/magic-mcp)

| Поле | Значение |
|---|---|
| Stars | ★ 4.8k+ |
| License | NOASSERTION |
| Recommendation | ⭐⭐⭐ |

**Чему учит**: нетривиальный MCP server, создающий UI-компоненты. Показывает, как MCP может расширяться за пределы простого fetch'а данных.

**Лучше всего для**: вдохновение после Упражнения 2 — что могут креативные MCP-серверы.

---

## 5.3 — Skills (Claude Code Behavior Layer)

### Цели обучения
- Анатомия `SKILL.md` (YAML frontmatter + body)
- Когда skills auto-load (description matching)
- Как написать SKILL.md, решающий твою ежедневную задачу
- Использование подкаталогов `references/`, `scripts/`, `evals/`

### Обязательное чтение
1. [**Anthropic — Claude Skills documentation**](https://docs.anthropic.com/en/docs/claude-code/skills)
2. **Несколько примеров SKILL.md** из `anthropics/claude-code` или community marketplace'ов

### Практические упражнения
- **Упражнение: SKILL.md** — напиши 200-словный skill, решающий одну из твоих ежедневных задач
- **Упражнение: SKILL with references** — добавь `references/` markdown, из которого skill может подтягивать
- **Упражнение: SKILL eval** — добавь `evals/evals.json` с 3–5 self-test'ами

### Подборка проектов

> 💡 **Ищешь daily-use Skills (NotebookLM, Excalidraw, Office docs и т. д.)?**
> См. [`resources/mcp-skills-catalog.ru.md`](../resources/mcp-skills-catalog.ru.md) — сгруппированы по use case'ам, включает и Anthropic-официальные, и community Skills. Раздел ниже остаётся сфокусирован на «**референсном материале для написания своего Skill**» (спеки и showcase).

#### [anthropics/skills](https://github.com/anthropics/skills) ⭐ Official spec

| Поле | Значение |
|---|---|
| Stars | ★ 128k+ |
| License | NOASSERTION |
| Recommendation | ⭐⭐⭐⭐⭐ |

**Чему учит**: официальный Skills репо Anthropic — `spec/` (стандарт SKILL.md frontmatter), `template/` (стартовый scaffold), и `skills/` (reference implementations: pdf, docx, xlsx, pptx, skill-creator).

**Лучше всего для**: прочти это до написания своего SKILL.md — важная reference implementation для структуры и frontmatter'а SKILL.md.

**Заметки**: отличается от `anthropics/claude-code` — этот репо — выделенный Skills репо; тот — основной Claude Code репо. Более широкий стандарт Agent Skills — на [agentskills.io](https://agentskills.io).

---

#### [anthropics/claude-code](https://github.com/anthropics/claude-code)

| Поле | Значение |
|---|---|
| Recommendation | ⭐⭐⭐⭐ |

**Чему учит**: главный репо Claude Code — issues, releases и inline-примеры skills.

**Лучше всего для**: отслеживания новых фич, заведения багов, чтения release notes.

**Заметки**: на этом этапе (обучение Skills) этот репо стоит ниже `anthropics/skills` (⭐⭐⭐⭐⭐, официальная spec), поэтому рейтинг ⭐⭐⭐⭐. В ветках (позиционирован как end-user точка входа) увидишь ⭐⭐⭐⭐⭐ — тот же репо, audience-специфичная рамка.

---

#### [travisvn/awesome-claude-skills](https://github.com/travisvn/awesome-claude-skills)

| Поле | Значение |
|---|---|
| Recommendation | ⭐⭐⭐⭐ |

**Чему учит**: курируемый каталог Claude Skills по community.

**Лучше всего для**: обнаружение существующих skills перед написанием своего.

---

#### [obra/superpowers](https://github.com/obra/superpowers)

| Поле | Значение |
|---|---|
| Recommendation | ⭐⭐⭐⭐ |

**Чему учит**: 20+ обкатанных в бою skills (TDD, debugging, паттерны коллаборации) с командами `/brainstorm`, `/write-plan`, `/execute-plan` и skills-search tool'ом.

**Лучше всего для**: power-user setup. Читай SKILL.md source, чтобы учиться продвинутым паттернам.

---

#### [VoltAgent/awesome-agent-skills](https://github.com/VoltAgent/awesome-agent-skills)

| Поле | Значение |
|---|---|
| Stars | ★ 20k+ |
| License | MIT |
| Recommendation | ⭐⭐⭐ |

**Чему учит**: 1000+ agent skills, совместимых с Claude Code, Codex, Gemini CLI, Cursor. Cross-tool перспектива.

**Лучше всего для**: после того, как поймёшь SKILL.md, листай за идеями.

---

#### [alirezarezvani/claude-skills](https://github.com/alirezarezvani/claude-skills)

| Поле | Значение |
|---|---|
| Recommendation | ⭐⭐⭐ |

**Чему учит**: 232+ Claude Code skills по engineering, marketing, product, compliance.

**Лучше всего для**: domain-специфичные skill-примеры.

---

#### [mattpocock/skills](https://github.com/mattpocock/skills)

| Поле | Значение |
|---|---|
| Stars | ★ 61k+ |
| License | MIT |
| Recommendation | ⭐⭐⭐⭐ |

**Чему учит**: Matt Pocock (известный TypeScript-преподаватель) публикует свою настоящую `.claude/` директорию. Каждый SKILL.md короткий (10–50 строк) и не over-engineered.

**Лучше всего для**: видеть, как выглядят настоящие engineer-daily SKILL.md файлы. Отличный контр-пример к over-engineered 200-строчным skills.

---

#### [wshobson/agents](https://github.com/wshobson/agents)

| Поле | Значение |
|---|---|
| Stars | ★ 35k+ |
| License | MIT |
| Recommendation | ⭐⭐⭐⭐ |

**Чему учит**: комбинирование skills + subagents в multi-agent orchestration. **Идёт от single SKILL.md к паттерну agent-as-skill композиции.**

**Лучше всего для**: intermediate-учеников после нескольких SKILL.md — когда хочешь знать «как skills вызывают друг друга и превращаются в большие agent workflow'ы?»

---

## 5.4 — Plugins & Marketplaces

### Цели обучения
- Схема `plugin.json` (name, version, skills array, configuration)
- Схема `marketplace.json` (plugins array, source, metadata)
- Workflow `claude plugin marketplace add`
- Различать single-plugin bundle vs multi-plugin marketplace
- Опубликовать свой marketplace

### Обязательное чтение
1. [**Anthropic — Plugins documentation**](https://docs.anthropic.com/en/docs/claude-code/plugins)
2. **Прочти `plugin.json` и `marketplace.json` 2–3 marketplace'ов ниже**

### Практические упражнения
- **Упражнение: plugin install** — установи один из marketplace'ов ниже, посмотри как загружается
- **Упражнение: plugin.json** — упакуй SKILL.md, написанный в 5.3, в plugin
- **Упражнение: marketplace publish** — запушь на GitHub, установи через `claude plugin marketplace add`

### Подборка проектов

> 💡 **Хочешь увидеть, как другие пакуют plugins?** Несколько записей в [`resources/mcp-skills-catalog.ru.md`](../resources/mcp-skills-catalog.ru.md) (секции dev collab / design / monitoring) поставляются и как plugins (например, `timescale/pg-aiguide` — и MCP server, и plugin). Раздел ниже остаётся сфокусирован на «**шаблонах структуры marketplace**» как референсе.

#### [anthropics/claude-plugins-official](https://github.com/anthropics/claude-plugins-official) ⭐ Official

| Поле | Значение |
|---|---|
| Stars | ★ 18k+ |
| License | NOASSERTION (у каждого plugin своя лицензия; проверяй per plugin) |
| Recommendation | ⭐⭐⭐⭐⭐ |

**Чему учит**: официальный marketplace template Anthropic — `.claude-plugin/marketplace.json` стандартная схема, `plugins/` для inline-плагинов, и `external_plugins/` для плагинов, ссылающихся на внешние репо.

**Лучше всего для**: перед публикацией своего marketplace, это — официальный шаблон, который ты захочешь скопировать для вопроса **как должен выглядеть marketplace.json?**

**Заметки**: за пределами схемы, это также показывает, как Anthropic категоризирует свои официальные plugins (chrome-devtools, deepwiki, code-research, jam и т. д.).

---

#### [obra/superpowers-marketplace](https://github.com/obra/superpowers-marketplace)

| Поле | Значение |
|---|---|
| Stars | ★ 900+ |
| License | MIT |
| Recommendation | ⭐⭐⭐⭐ |

**Чему учит**: **минимальный marketplace-шаблон** — репо содержит только `.claude-plugin/marketplace.json` + README; source самих plugins живёт во внешних репо. Демонстрирует форму **curator-only marketplace** (куратор отбирает, не bundle'ит source).

**Лучше всего для**: построения marketplace «я курирую, другие пишут». Меньше, чем `anthropics/claude-plugins-official` — минимально жизнеспособный template.

---

#### [trailofbits/skills-curated](https://github.com/trailofbits/skills-curated)

| Поле | Значение |
|---|---|
| Stars | ★ 388 |
| License | CC-BY-SA-4.0 |
| Recommendation | ⭐⭐⭐ |

**Чему учит**: курируемый marketplace от известной security-фирмы Trail of Bits, сфокусированный на **supply-chain security** — каждый skill отревьюен, README документирует критерии.

**Лучше всего для**: ревьюеров и команд, заботящихся о supply-chain trust и желающих изучить модель **curator-vouches-for-safety**.

**Заметки**: мал по масштабу, но значим по рамке — показывает, что marketplace может быть больше, чем список, — он может быть trust-механизмом.

---

#### [anthropics/life-sciences](https://github.com/anthropics/life-sciences) (domain-специализированный пример)

| Поле | Значение |
|---|---|
| Stars | ★ 331 |
| License | NOASSERTION (у marketplace нет SPDX; каждый MCP server лицензируется своим провайдером) |
| Recommendation | ⭐⭐⭐ |

**Чему учит**: собственный пример **domain-специализированного marketplace** Anthropic (для life sciences / health) — показывает, как кроить `marketplace.json` под одну вертикаль вместо generic-каталога.

**Лучше всего для**: строителей вертикально-специфичных marketplace (healthcare, finance, legal, edu), желающих увидеть, как Anthropic с этим обходится.

**Заметки**: payload — bio-leaning MCP-серверы, но форма marketplace.json — собственно урок.

---

> **«Как опубликовать свой marketplace» туториала всё ещё нет** — самый надёжный ресурс сейчас — [официальные plugin docs Anthropic](https://docs.claude.com/en/docs/claude-code/plugins). Написал качественный walkthrough? PR welcome.

---

#### [rohitg00/awesome-claude-code-toolkit](https://github.com/rohitg00/awesome-claude-code-toolkit)

| Поле | Значение |
|---|---|
| Recommendation | ⭐⭐⭐ |

**Чему учит**: один из крупнейших community-каталогов Claude Code agents, skills, hooks и templates. Широкий охват по многим use case'ам.

**Лучше всего для**: после Упражнения 3 листай, чтобы увидеть, что есть.

---

## ✅ Самопроверка перед этапом 6

Можешь:
- [ ] Установить Claude Code и использовать 5 разных slash commands
- [ ] Подключить 2 MCP-сервера в одной Claude-сессии
- [ ] Написать свой MCP server на Python, отдающий 1 рабочий tool
- [ ] Написать `SKILL.md`, auto-load'ящийся по конкретной trigger-фразе
- [ ] Упаковать skills в plugin и опубликовать через `marketplace.json`
- [ ] Различать MCP / Skills / Plugins / SDK по их ролям

Если да → переходи к [Этапу 6 — Memory & RAG](06-memory-rag.ru.md).

## 💡 Bonus: после этого этапа

- Сабмить PR в [`anthropics/claude-cookbooks`](https://github.com/anthropics/claude-cookbooks) (мелкий фикс, обновление документации)
- Сабмить свой plugin в community marketplace
- Напиши blog post, сравнивающий твой hello-MCP server с одним из официальной коллекции `modelcontextprotocol/servers`
