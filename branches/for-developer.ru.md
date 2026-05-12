# Для разработчиков — специализированная ветка

> [繁體中文](./for-developer.md) | [简体中文](./for-developer.zh-Hans.md) | [English](./for-developer.en.md) | **Русский**

> 🚀 **Первый раз ставишь Claude Code или пишешь `CLAUDE.md` / `SKILL.md`?** Быстрый setup guide — [`resources/setup-guide.ru.md` §D-E](../resources/setup-guide.ru.md). Если уже знаешь — пропускай.

> [← Назад к README основного пути](../README.ru.md) · Сюда — после **A3 в Track A** или **этапа 7 в Track B**. Применять agentic AI к coding workflow.

## Use cases

- AI pair programming (Cursor, Aider, Claude Code, Cline, Continue)
- Автоматизация code review
- Генерация тестов
- Multi-agent coding-задачи (planning + execution)
- Интеграция с IDE и governance в CI

## Подборка проектов

> Шесть основных CLI agents (Claude Code / Codex / OpenCode / Gemini CLI / goose / Aider / Hermes Agent) сравниваются бок-о-бок в [`resources/cli-agents-guide.ru.md`](../resources/cli-agents-guide.ru.md). Новичок в CLI agents, нужен пошаговый onboarding → [`tracks/cli/A1-cli-intro.ru.md`](../tracks/cli/A1-cli-intro.ru.md) (первая остановка Track A). Ищешь MCP / Skill интеграции, чтобы подвязать CLI к ежедневным инструментам (GitHub, Linear, Atlassian, Postgres, Playwright, Figma…) → [`resources/mcp-skills-catalog.ru.md`](../resources/mcp-skills-catalog.ru.md) (62 записи по категориям). Ниже — только ключевые позиции, которые разработчик должен знать.

### Coding Agents

#### [Cursor](https://www.cursor.com/) ⭐⭐⭐⭐⭐
AI pair-programmer, интегрированный в редактор. Индустриальный стандарт AI-ассистированного кодинга.

#### [Aider-AI/aider](https://github.com/Aider-AI/aider) ⭐⭐⭐⭐⭐
★ 44k+ · Apache-2.0 — git-aware CLI pair-programmer. Редактирует файлы прямо в твоём репозитории и сам пишет коммиты. **Open-source эталон «git-native AI редактирования».** Model-agnostic.

#### [anthropics/claude-code](https://github.com/anthropics/claude-code) ⭐⭐⭐⭐⭐
★ 120k+ — официальный agentic coding ассистент Anthropic. Skills + plugins экосистема.

#### [cline/cline](https://github.com/cline/cline) ⭐⭐⭐⭐⭐
★ 61k+ · Apache-2.0 — VS Code расширение, автономный in-IDE agent: tool use, браузер, step-by-step approval. **Первый выбор для пользователей VS Code, желающих IDE-native agentic dev.**

#### [continuedev/continue](https://github.com/continuedev/continue) ⭐⭐⭐⭐
★ 33k+ · Apache-2.0 — source-controlled AI checks, гоняемые в CI. Представляет **team / governance** угол coding agents.

#### [OpenHands (бывший OpenDevin)](https://github.com/All-Hands-AI/OpenHands) ⭐⭐⭐⭐
★ 72k+ · MIT — open-source автономный software development agent. Более агрессивный дизайн, чем Aider / Claude Code — agent живёт в своём sandbox и автономно коммитит. Лучший для сценариев «брось ему весь issue».

#### [block/goose](https://github.com/block/goose) ⭐⭐⭐⭐
★ 43k+ · Apache-2.0 — Open-source, расширяемый AI agent, идущий дальше кодо-подсказок — install / execute / edit / test, с любым LLM. Поддерживает несколько LLM провайдеров и MCP, поставляется как desktop app, CLI и API. (Репозиторий теперь резолвится в `aaif-goose/goose`.)

#### [RooCodeInc/Roo-Code](https://github.com/RooCodeInc/Roo-Code) ⭐⭐⭐⭐
★ 23k+ · Apache-2.0 — VS Code coding agent с моделью «**команда специализированных режимов**». Отличается от single-agent потока Cline.

### Code Review

#### [obra/superpowers](https://github.com/obra/superpowers) ⭐⭐⭐⭐
20+ обкатанных в бою skills, включая TDD-паттерны, debugging, паттерны коллаборации. Хороший источник для дизайна code-review skill.

## Workflow'ы, которые надо освоить

- **AI pair programming**: выбери один из Claude Code / Cursor / Cline для повседневной работы
- **Git-native AI редактирование**: погоняй Aider неделю, привыкни к ритму «AI правит → коммит → ревью»
- **AI checks в CI**: используй Continue, чтобы подвязать AI-проверки к PR-пайплайну
- **Генерация тестов**: напиши skill / промпт, генерирующий pytest-тесты из сигнатуры функции
- **Автоматизация code review**: GitHub Action, вызывающий Claude API на каждом PR

### 3 конкретных workflow-рецепта

**1. AI Pair Programming (ежедневный ритм)**
1. Стартуй фичу → `git checkout -b feature/xxx`
2. Передай задачу Claude Code / Cursor — **заставь сначала написать план** (не нырять сразу в код)
3. Прочитай план, скорректируй курс → только потом одобряй кодинг
4. Когда готово: запусти тесты + lint → сам ревьюь diff (**не принимай вслепую**)
5. Commit message пиши сам или дай AI черновик и отредактируй перед коммитом

**2. Aider Git-Native Flow (ближе всего к «работаю в паре с AI»)**
```bash
# Внутри репозитория
aider --model anthropic/claude-sonnet-4-20250514

# Запрос на естественном языке
> Add a timezone parameter to parse_date in utils.py, default UTC

# Aider правит + коммитит автоматически. Откат:
> /undo  # отменяет последний AI-коммит
```

**3. Claude code review на PR (GitHub Action)**

`.github/workflows/claude-review.yml`:
```yaml
on:
  pull_request:
jobs:
  review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
      - name: Run Claude review
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
        run: |
          # Use anthropics/claude-code-action or your own script
          # Get git diff, run prompt, post results back to PR
```
Источник: официальный GitHub Action [`anthropics/claude-code-action`](https://github.com/anthropics/claude-code-action).

## Частые ловушки (анти-паттерны)

| ❌ Не делай | ✅ Делай вместо |
|---|---|
| Дать AI пушить прямо в main | Всегда через PR → ревью → merge |
| Слепо принимать большие рефакторинг-diff'ы | Разбей на куски < 50 LOC, ревьюй каждый |
| Отдать `.env` / API-ключи AI | Используй механизм исключений: Cursor `.cursorignore` / Aider `.aiderignore` / Claude Code `permissions.deny` в `.claude/settings.json` |
| Дать AI свободно запускать shell против production-кода | Sandbox + permission whitelist |
| Принимать AI-сгенерированные тесты на веру | Запусти coverage + умышленно сломай unit, чтобы убедиться, что тесты ловят это |
| Заметить неправильное направление через много коммитов | **Plan-first** режим: ревьюй план до любого кодинга |

## Путь апгрейда tier'ов

- **Tier 0**: Cursor / Claude Desktop — IDE chat, без agents
- **Tier 1**: Claude Code / Cline / OpenCode — CLI с доступом к файловой системе и CLAUDE.md, всё ещё human-in-the-loop
- **Tier 2**: Пиши свои Skills + MCP-серверы — пакуй свой dev-workflow в общие командные skills
- **Tier 3**: Auto-running agents в CI + production observability — дорога в [Этап 7](../stages/07-multi-agent-production.ru.md)

> Tier 0–1 покрывает ~90% разработчиков. **Прежде чем уходить в Tier 2+, проверь ROI**: инвестиции оправданы, только если команда большая, потоки повторяющиеся и инциденты необратимые.

## Другие ветки тоже подойдут

Ветки, сильно пересекающиеся с разработчиками:

- **ML-исследования / написание статей** → [Researcher branch](./for-researcher.ru.md)
- **Подвязать Notion / Linear / Atlassian / Postgres / Figma к своему CLI** → [`resources/mcp-skills-catalog.ru.md`](../resources/mcp-skills-catalog.ru.md)
- **Написать свой Skill / MCP server** → [Этап 5](../stages/05-claude-code-ecosystem.ru.md) + [`resources/cookbook.ru.md`](../resources/cookbook.ru.md)
- **Детали дизайна schema** → [`resources/schema-design-cheatsheet.ru.md`](../resources/schema-design-cheatsheet.ru.md)
- **CLI с нуля** → [Track A](../tracks/cli/A1-cli-intro.ru.md) (A1 → A2 → A3)

## Community note

Особенно приветствуются контрибьюты:

- IDE-специфичные config-шаблоны (Cursor `.cursorrules`, Claude Code `CLAUDE.md` для Python / Go / Rust и т. д.)
- Language-специфичные Skills (Python / TypeScript / Rust / Go best-practice паттерны)
- Кейсы интеграции CI / pre-commit hooks
- **Multi-developer team governance** — обмен Skills между разработчиками, permission design, cost tracking

См. [CONTRIBUTING.md](../CONTRIBUTING.md).
