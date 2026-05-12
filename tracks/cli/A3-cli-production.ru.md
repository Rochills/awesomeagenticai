# A3 — Интеграция и продакшен

> [繁體中文](./A3-cli-production.md) | [简体中文](./A3-cli-production.zh-Hans.md) | [English](./A3-cli-production.en.md) | **Русский**

> [← A2 — CLI Workflow Patterns](A2-cli-workflow.ru.md) · **Track A: CLI Power User** — Остановка 3 (финальная)

⏱ **Оценка времени**: 1–2 недели (~8–15 часов)

После того как CLI работает гладко, следующий шаг: **подвязать его в реальный workflow**. MCP server интеграция, CI-автоматизация, cost / observability. После этой остановки CLI больше не личный инструмент — он часть workflow команды.

## 📌 Цели обучения

- Подключить 1–3 MCP-сервера к своему CLI (Slack / Gmail / внутренний API / БД)
- Настроить GitHub Actions для авто-запуска Claude Code (PR review, release notes и т. д.)
- Добавить observability (trace, cost, latency) в CLI workflow'ы
- Спланировать cost-budget — знать примерно, во сколько токенов обходится большая задача

## 📚 Обязательное чтение

1. [**Этап 5.2 — MCP (Model Context Protocol)**](../../stages/05-claude-code-ecosystem.ru.md#52--mcp-model-context-protocol-foundation) — концепция MCP и основы
2. [**Anthropic — Prompt Caching**](https://www.anthropic.com/news/prompt-caching) — ключевой трюк для снижения cost на 90%
3. [**Этап 7 — секция Observability**](../../stages/07-multi-agent-production.ru.md#observability) — langfuse / Helicone / weave
4. [**`resources/cli-agents-guide.ru.md`** §«Распространённые ловушки»](../../resources/cli-agents-guide.ru.md) — самые частые production-проблемы с CLI

## 🛠 Практические упражнения

### Упражнение CLI-9: MCP server, подключённый к CLI
Следуя [Упражнению MCP client этапа 5.2](../../stages/05-claude-code-ecosystem.ru.md#52--mcp-model-context-protocol-foundation), подключи как минимум один полезный MCP-сервер к CLI:
- `filesystem` server → пусть CLI читает файлы вне дефолтного scope'а
- `github` server → пусть читает PR / issues напрямую
- Custom server → подключи свой внутренний API / БД

Успех: в CLI-разговоре спроси «есть ли в моём PR конфликты?» и пусть CLI ответит через MCP (без открытия браузера).

### Упражнение CLI-10: GitHub Actions + CLI
Напиши `.github/workflows/cli-review.yml`:
- Trigger: PR opened / synchronize
- Run: в GH Actions runner запусти Claude Code (или Codex), подай ему `git diff` + твой `.claude/commands/review.md`
- Output: PR comment

Успех: открой новый PR, увидь review-комментарий за 1–2 минуты.

> Точки старта: официальный Anthropic [`claude-code-action`](https://github.com/anthropics/claude-code-action); у Codex есть GitHub App и CLI режимы.

### Упражнение CLI-11: Cost tracking
Запусти ежедневную задачу. **Спрогнозируй** использование токенов сначала, потом реально запусти и проверь usage. Разрыв обычно большой (обычно недооцениваешь).
- Математика: input tokens + output tokens × цена модели каждое
- Подключи langfuse или Helicone ([Этап 7 Observability](../../stages/07-multi-agent-production.ru.md#observability)) для tracing
- Понаблюдай: какая подзадача жрёт больше всего токенов? Не шлёшь ли ненужный длинный контекст?

### Упражнение CLI-12: Skill / plugin team sharing
Упакуй свои `.claude/commands/` и `CLAUDE.md` в plugin, публикуй на internal marketplace или GitHub. Тиммейты делают `claude plugin install` и получают тот же workflow.
- Skill / plugin детали в [Этапе 5.3 + 5.4](../../stages/05-claude-code-ecosystem.ru.md)
- Шаблон: [anthropics/claude-plugins-official](https://github.com/anthropics/claude-plugins-official)

## 🎯 Подборка проектов

### Коллекция MCP server'ов (CLI-friendly)

> 💡 **Ищешь MCP, подключающие к ежедневным инструментам** (Notion / Obsidian / Excel / Postgres / Playwright / Slack / Linear / Figma…): см. [`resources/mcp-skills-catalog.ru.md`](../../resources/mcp-skills-catalog.ru.md) — 62 записи, сгруппированных по категориям, каждая со stars / license / audience. Список ниже — для «написать свой MCP server / найти reference implementation».

#### [modelcontextprotocol/servers](https://github.com/modelcontextprotocol/servers) ⭐⭐⭐⭐⭐
★ 85k+ — официальные reference-серверы. filesystem, github, sqlite, git, time, fetch, memory, sequential-thinking.
> См. [Этап 5.2](../../stages/05-claude-code-ecosystem.ru.md#52--mcp-model-context-protocol-foundation).

#### [wong2/awesome-mcp-servers](https://github.com/wong2/awesome-mcp-servers)
Community MCP server каталог. 150+ серверов категоризировано.

---

### CI Integration Patterns

#### [anthropics/claude-code-action](https://github.com/anthropics/claude-code-action)
Официальный GitHub Action шаблон. PR review, issue triage, auto-fix.

#### [continuedev/continue](https://github.com/continuedev/continue) ⭐⭐⭐⭐
★ 33k+ — подвяжи AI-проверки в CI; enforce в PR pipeline.
> Полное введение в [`branches/for-developer.ru.md`](../../branches/for-developer.ru.md).

---

### Observability + Cost

#### [langfuse/langfuse](https://github.com/langfuse/langfuse) ⭐⭐⭐⭐⭐
★ 26k+ — open-source LLM observability. Trace, cost, sessions в одном месте.
> См. [Этап 7 Observability](../../stages/07-multi-agent-production.ru.md#observability).

#### [Helicone](https://github.com/Helicone/helicone) ⭐⭐⭐⭐
★ 5k+ — proxy-based monitoring. Просто поменяй `base_url` — получаешь logging + caching.

#### [promptfoo/promptfoo](https://github.com/promptfoo/promptfoo) ⭐⭐⭐⭐⭐
★ 20k+ — eval-фреймворк. Гоняй regression-тесты перед промоушеном CLI workflow'ов в production.
> См. [Этап 7 Eval](../../stages/07-multi-agent-production.ru.md#evaluation-фреймворки).

---

### Production CLI Workflow шаблоны

#### [obra/superpowers](https://github.com/obra/superpowers) ⭐⭐⭐⭐
★ 178k+ — production-ready skill коллекция. Посмотри, как кто-то делает полный CLI workflow.

#### [obra/superpowers-marketplace](https://github.com/obra/superpowers-marketplace)
★ 900+ — минимальный marketplace-шаблон. Референс при упаковке CLI workflow команды.

## ✅ Полная самопроверка Track A

Можешь:
- [ ] Имеешь минимум 1 MCP server, подключённый к ежедневному CLI
- [ ] Имеешь минимум 1 CI workflow, авто-гоняющий CLI agent
- [ ] Назвать грубые token / cost / latency для какой-то конкретной задачи
- [ ] Упаковал свои CLAUDE.md / commands хотя бы раз (даже только для себя)
- [ ] Знаешь, какие задачи заслуживают observability, а какие нет

Если да → **Track A завершён**. Выбери [специализированную ветку](../../README.ru.md#️-карта-обучения-две-дорожки) и продолжай (researcher / developer / teacher / knowledge-worker / everyday-users).

Хочешь глубже про «**как написать свой CLI agent**» (не использовать готовые) → прыгай к [Track B этап 3](../../stages/03-tool-use-and-hello-agent.ru.md). Track A и Track B дополняют друг друга.

## 💡 Что дальше

После Track A ты CLI power user. Выборы следующей фазы:

1. **Углуби CLI workflow** (продолжай уточнять setup)
   - Подпишись на Anthropic / OpenAI changelogs
   - Ежеквартальный review [`resources/cli-agents-guide.ru.md`](../../resources/cli-agents-guide.ru.md) на новые инструменты
   - Шарь CLAUDE.md / skills с командой

2. **Переходи к Track B** (учись писать свой agent)
   - Этапы 3–4: tool use + фреймворки
   - Этап 5: deep dive во внутренности Claude Code
   - Этап 7: пиши свою multi-agent систему

3. **Иди по специализированной ветке** (применяй CLI к конкретному домену)
   - Researcher / developer / knowledge-worker / teacher / everyday-users
   - Каждая ветка использует то, что выучил в Track A
