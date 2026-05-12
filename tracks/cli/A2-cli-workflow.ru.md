# A2 — Паттерны CLI Workflow

> [繁體中文](./A2-cli-workflow.md) | [简体中文](./A2-cli-workflow.zh-Hans.md) | [English](./A2-cli-workflow.en.md) | **Русский**

> [← A1 — CLI Intro](A1-cli-intro.ru.md) · **Track A: CLI Power User** — Остановка 2

⏱ **Оценка времени**: 1–2 недели (~8–15 часов)

После установки CLI и первых задач следующий вопрос: **как сделать CLI консистентным, повторяемым, share'абельным?** Эта остановка покрывает workflow-паттерны — превращая «я перепечатываю тот же промпт каждый раз» в «настроил один раз, CLI делает правильно автоматически».

## 📌 Цели обучения

- Написать production-grade `CLAUDE.md` / `AGENTS.md` (не 1-строчный note — 30–50-строчный рабочий спек)
- Спроектировать переиспользуемые slash commands / кастомные промпты
- Декомпозировать multi-step задачи на те, что CLI может исполнить end-to-end
- Спроектировать промпты, портируемые между CLI

## 📚 Обязательное чтение

1. [**Anthropic — CLAUDE.md best practices**](https://docs.anthropic.com/en/docs/claude-code/memory) ⭐
2. [**Этап 2 — Prompt Engineering**](../../stages/02-prompt-engineering.ru.md) — workflow-дизайн и prompt-дизайн — две стороны одной монеты
3. [**Этап 5.1 — Claude Code Basics**](../../stages/05-claude-code-ecosystem.ru.md#51--claude-code-basics) — детали slash command
4. [**`resources/cli-agents-guide.ru.md`** §«Портируемые промпты между CLI»](../../resources/cli-agents-guide.ru.md) — принципы portable-промптов

## 🛠 Практические упражнения

### Упражнение CLI-5: напиши production CLAUDE.md
Твой CLAUDE.md должен как минимум содержать:
- **Persona**: «Ты senior Python инженер / academic writing assistant / и т. д.»
- **Repo context**: какой проект, какой стек, какие конвенции
- **Не делай**: не трогай main, не двигай секреты, не авто-коммит
- **Как делать вещи**: сначала plan, тесты перед commit, type hints
- **Частые команды**: как гонять тесты, lint, deploy

Закоммить в git. В следующий раз, когда тиммейт клонирует репо, его Claude Code автоматически загрузит конвенции.

### Упражнение CLI-6: первая slash command
Напиши `.claude/commands/review.md` (или эквивалент твоего CLI):
```markdown
---
name: review
description: Review staged changes for security + style
---

Run this flow:
1. `git diff --cached` to get staged changes
2. Look for: hard-coded secrets, SQL injection, type errors
3. Check against the style rules in CLAUDE.md
4. Output: PASS / or list of specific changes needed
```
После этого каждый `/review` запускает тот же поток.

### Упражнение CLI-7: декомпозиция multi-step задачи
Дай CLI сложную задачу («переведи эти 50 markdown-файлов на английский + добавь frontmatter + перенеси в en/ subdirectory»).
- Первый раз: брось всю задачу целиком → понаблюдай, как делает, где ошибается
- Второй раз: предварительно декомпозируй на 5 подзадач, давай по одной → понаблюдай разницу
- Урок: CLI как ты — слишком большие задачи нужно декомпозировать; слишком мелкие ведут к over-orchestration

### Упражнение CLI-8: портируемый промпт
Напиши промпт, работающий в Claude Code. **Запусти тот же промпт в Codex / OpenCode / Gemini CLI** — что нужно поменять? Частые открытия:
- file path конвенции отличаются (cwd vs absolute)
- дефолты shell-execution permission отличаются
- «plan-first» промптинг нужен явно в одних, по дефолту в других

Скомпилируй это в свой cheat sheet.

## 🎯 Подборка проектов

### Примеры CLAUDE.md

#### [Официальные доки Anthropic](https://docs.anthropic.com/en/docs/claude-code/memory)
официальное — Claude Code memory / CLAUDE.md doc'и, включая best practices.

#### [obra/superpowers](https://github.com/obra/superpowers) ⭐⭐⭐⭐
★ 178k+ — не просто skill-коллекция, но и production CLAUDE.md шаблон. Прочти полную структуру `.claude/`.

#### [mattpocock/skills](https://github.com/mattpocock/skills) ⭐⭐⭐⭐
★ 59k+ — daily skill-библиотека практика. Структура `.claude/` — отличный референс.

> Больше примеров skill / SKILL.md в [Этапе 5.3 — Skills](../../stages/05-claude-code-ecosystem.ru.md#53--skills-claude-code-behavior-layer).

---

### Slash Commands / кастомные промпты

#### [anthropics/claude-plugins-official](https://github.com/anthropics/claude-plugins-official) ⭐ Official
★ 18k+ — официальный plugin marketplace. Commands / skills каждого plugin'а служат примерами slash command.

#### [hesreallyhim/awesome-claude-code](https://github.com/hesreallyhim/awesome-claude-code)
Community-курируемые Claude Code ресурсы. Листай примеры slash command'ов.

---

### Референсы дизайна промптов

#### [f/awesome-chatgpt-prompts](https://github.com/f/awesome-chatgpt-prompts) ⭐⭐⭐⭐
★ 161k+ — начато для ChatGPT, но ~90% паттернов работают в CLI.

#### Этап 2 — Prompt Engineering full list
[Full list](../../stages/02-prompt-engineering.ru.md#-подборка-проектов) — DSPy, Prompt-Engineering-Guide и т. д.

---

### Multi-CLI паттерны

#### [`resources/cli-agents-guide.ru.md`](../../resources/cli-agents-guide.ru.md) §«Три распространённые комбинации»
Смотри Setup A / B / C и попробуй подходящий.

## ✅ Самопроверка перед A3

Можешь:
- [ ] Написал минимум 1 CLAUDE.md для production / work репо (не demo-репо)
- [ ] Написал минимум 2 slash command'а, которыми реально пользуешься
- [ ] Запустил тот же промпт в 2 разных CLI и знаешь различия
- [ ] Сформулировать «какие задачи стоит декомпозировать, а какие нет»

Если да → переходи к [A3 — Интеграция и продакшен](A3-cli-production.ru.md).

Если нет → CLAUDE.md только на demo-репо — это впустую; иди напиши для реального репо сначала.

## 💡 Частые ловушки

- **CLAUDE.md слишком длинный**: больше 100 строк — и CLI авто-truncate'ит / игнорирует заднюю половину. Sweet spot: 30–60 строк.
- **Slash command написан как «do X, Y, Z, A, B» в одном предложении**: CLI пропускают шаги. Перепиши как numbered list с критерием успеха per step.
- **Over-portable**: у каждого CLI свои сильные стороны; не выкидывай specifics из промпта только ради cross-CLI.
- **«я уже всё это знаю, не нужно записывать»**: CLAUDE.md — для будущего тебя (и новых тиммейтов), не для текущего тебя.
