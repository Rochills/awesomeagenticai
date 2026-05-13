# Для обычных пользователей — специализированная ветка

> [繁體中文](./for-everyday-users.md) | [简体中文](./for-everyday-users.zh-Hans.md) | [English](./for-everyday-users.en.md) | **Русский**

> 🚀 **Никогда не писал код и не ставил Python?** Начни с [`resources/setup-guide.ru.md` §A-C](../resources/setup-guide.ru.md) (около 30 минут с нуля), потом возвращайся. Если уже знаешь Python и есть API-ключ — пропусти.

> [← Назад к README основного пути](../README.ru.md) · Сюда **не обязательно проходить весь основной путь** — эта ветка для тех, кто **просто хочет ИСПОЛЬЗОВАТЬ AI, не строить агентов**.

## Use cases

- Писать email, организовывать заметки, шлифовать cover letter
- Учиться новому (читать английские статьи, осваивать язык, повторять материал)
- Research и сравнение (путешествия, товары, школы)
- Повседневный поток (рецепты, расписания, todo-листы)
- Privacy-чувствительные сценарии: медкарты, личные финансы (→ локальный LLM)

## С чего начать: 4 tier'а по «насколько глубоко хочешь нырять»

```
Tier 0: Web / Mobile App  (рекомендуемый старт)
   ↓
Tier 1: Desktop App  (апгрейд, когда нужно работать с локальными файлами)
   ↓
Tier 2: CLI Agent  (готов выучить немного command line; автоматизация повседневных потоков)
   ↓
Tier 3: Local LLM  (privacy-чувствительность, экономия, offline)
```

**Большинство остаётся на Tier 0 / Tier 1** — Tier 2–3 для особых потребностей или обучения.

---

## 🎯 Подборка проектов

### Tier 0 — Web / Mobile App ⭐ Entry-level

#### [Claude.ai](https://claude.ai) ⭐⭐⭐⭐⭐
Официальный интерфейс Anthropic. Лучше для long-form письма, глубоких дискуссий, сложных вопросов — стиль ответов более сдержанный, меньше склонен к hallucination.

#### [ChatGPT](https://chatgpt.com) ⭐⭐⭐⭐⭐
Официальный интерфейс OpenAI. Самая большая экосистема (GPTs, Custom Instructions, Voice mode). Стандартный общий выбор.

#### [Gemini](https://gemini.google.com) ⭐⭐⭐⭐
Предложение Google. Длинный context window (миллионы токенов) — особенно хорош, когда бросаешь весь PDF и спрашиваешь. Интегрирован с Google-сервисами (Gmail, Docs).

#### [Perplexity](https://perplexity.ai) ⭐⭐⭐⭐
Поисковик × LLM — каждый ответ цитирует источники. Лучше ChatGPT для сценариев «нужна актуальная инфа».

---

### Tier 1 — Desktop App

#### [Claude Desktop](https://claude.ai/download) ⭐⭐⭐⭐⭐
Шире, чем web-версия: drag-and-drop файлов, чтение локальных файлов, сохранение длинного контекста разговора. **Также шлюз в MCP-экосистему** — можно подключить Slack / Gmail / Calendar серверы.

#### [ChatGPT Desktop](https://openai.com/chatgpt/desktop) ⭐⭐⭐⭐
Desktop-версия ChatGPT. Задавай вопросы по скриншотам, голосовой режим, интеграция с другими приложениями.

---

### Tier 2 — CLI Agents (продвинутые пользователи, готовые учить command line)

> Эти инструменты позиционируются для разработчиков, но **обычные пользователи тоже могут их использовать** — например, batch-переименование файлов, уборка папки Downloads, авто-написание weekly review, суммаризация PDF в Markdown.
>
> Нужно подробное сравнение? См. [`resources/cli-agents-guide.ru.md`](../resources/cli-agents-guide.ru.md) — семь основных CLI agents бок-о-бок, рекомендации по use case'ам, частые ловушки, реальные setup'ы.
>
> Нужен пошаговый onboarding? См. [`tracks/cli/A1-cli-intro.ru.md`](../tracks/cli/A1-cli-intro.ru.md) — первая остановка Track A, от установки до первой задачи.
>
> Хочешь подвязать CLI agent к Notion / Obsidian / Excel / Google docs / и т. д.? См. [`resources/mcp-skills-catalog.ru.md`](../resources/mcp-skills-catalog.ru.md) — 62 MCP server / Skill, сгруппированных по use case'ам.

#### [anthropics/claude-code](https://github.com/anthropics/claude-code) ⭐⭐⭐⭐⭐
★ 120k+ — официальный CLI agent Anthropic. Читает/пишет файлы, запускает команды, обрабатывает multi-step задачи. **Самый дружелюбный к новичку CLI-инструмент для обычных пользователей.**

#### [openai/codex](https://github.com/openai/codex) ⭐⭐⭐⭐⭐

| Поле | Значение |
|---|---|
| Stars | ★ 80k+ |
| License | Apache-2.0 |

**Чему учит**: облегчённый terminal coding agent от OpenAI. Та же категория, что Claude Code, но использует модели OpenAI.

**Лучше всего для**: людей, уже подписанных на ChatGPT Plus / Pro и желающих использовать тот же аккаунт в терминале.

#### [sst/opencode](https://github.com/sst/opencode) ⭐⭐⭐⭐⭐

| Поле | Значение |
|---|---|
| Stars | ★ 155k+ |
| License | MIT |

**Чему учит**: open-source coding agent, **не привязанный к конкретному LLM-провайдеру** — используй Claude, GPT, Gemini или локальный Ollama, на твой выбор. Поддерживается сообществом, быстрая итерация.

**Лучше всего для**: self-hoster'ов; людей, не желающих vendor lock-in; всех, кто переключается между несколькими LLM.

#### [google-gemini/gemini-cli](https://github.com/google-gemini/gemini-cli) ⭐⭐⭐⭐

| Поле | Значение |
|---|---|
| Stars | ★ 103k+ |
| License | Apache-2.0 |

**Чему учит**: официальный Gemini CLI agent от Google. Приводит длинный контекст Gemini и интеграцию с Google-экосистемой в терминал.

**Лучше всего для**: тяжёлых пользователей Google-экосистемы (Gmail, Drive, Docs).

---

### Tier 3 — Local LLM (privacy / offline / cost)

#### [Ollama](https://github.com/ollama/ollama) ⭐⭐⭐⭐⭐
★ 170k+ — одна команда — и локальный LLM работает. Применяй, когда privacy-чувствительные данные (медкарты, контракты, семейные разговоры) не должны покидать машину. См. [Этап 1 — Local LLM](../stages/01-llm-basics.ru.md).

#### [LM Studio](https://lmstudio.ai/)
Closed-source, но самый дружелюбный к новичку вариант — drag-and-drop UI, без command line. Mac / Windows / Linux.

---

### Библиотека промптов

#### [f/awesome-chatgpt-prompts](https://github.com/f/awesome-chatgpt-prompts) ⭐⭐⭐⭐
★ 161k+ — поддерживаемый сообществом мега-каталог промптов. «Act as a translator / résumé consultant / chef...» в сотнях ролей. **Застрял с чего начать — листай тут.**

---

## Обязательное чтение

1. [**Anthropic — How to write effective prompts**](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/overview) — читается без кода
2. [**OpenAI — Prompting Guide**](https://platform.openai.com/docs/guides/prompt-engineering) — параллельный официальный документ

Если хочешь глубже — см. [Этап 2 — Prompt Engineering](../stages/02-prompt-engineering.ru.md), там более системный подход.

## Workflow'ы, которые можешь собрать

Это шаблоны — адаптируй под себя:

- **Weekly journal**: расскажи Claude.ai, что сделал на этой неделе, попроси организовать в журнал + ключевые пункты на следующую неделю
- **Email triage**: вставляй неотвеченные письма в Claude каждое утро, проси категоризировать как «ответить сейчас / сегодня / на этой неделе / пропустить»
- **Изучение языка**: voice-режим — разговор с ChatGPT на целевом языке; пусть отмечает грамматические ошибки
- **Batch-уборка файлов**: Claude Code переименует и перегруппирует все файлы в твоей папке Downloads по дате + теме
- **Local privacy chat**: Ollama с qwen2.5:7b — задавай медицинские / юридические / финансовые вопросы, не отправляя данные в облако

## Tier-рекомендации для обычных пользователей

90% сценариев: **оставайся на Tier 0** — Claude.ai или ChatGPT web. Без установки, без оплаты (free tier'ы лимитированы, но хватает для повседневности).

5% апгрейдятся до Tier 1: работа с локальными файлами, длинный история разговора, подключение MCP-серверов.

5% апгрейдятся до Tier 2–3: реальные потребности автоматизации (например, делаешь одно и то же 100 раз в день) или privacy-чувствительные данные, которым нельзя в облако.

**Не давай никому тянуть тебя к преждевременному апгрейду** — для большинства Tier 0 достаточно. Tier 2–3 — инструменты, не маркеры статуса.

## Community notes

Особенно приветствуются контрибьюты:

- Domain-специфичные prompt-шаблоны (кулинария, фитнес, изучение языка)
- Дружелюбные к китайскому чат-инструменты (китайские LLM, локализованные обёртки)
- Privacy / safety best practices (какие данные OK отправлять / какие нет)

См. [CONTRIBUTING.md](../CONTRIBUTING.md).
