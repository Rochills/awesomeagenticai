# A1 — CLI Agent: введение и выбор

> [繁體中文](./A1-cli-intro.md) | [简体中文](./A1-cli-intro.zh-Hans.md) | [English](./A1-cli-intro.en.md) | **Русский**

> [← Назад к README основного пути](../../README.ru.md) · **Track A: CLI Power User** — Остановка 1

⏱ **Оценка времени**: 1 неделя (~5–10 часов)

После этапов 0–2 ты хочешь использовать существующие CLI agents для реальной работы — а не писать ReAct loop с нуля. Этот track для тебя. Первая остановка: **выбери CLI agent и запусти его**.

## 📌 Цели обучения

- Знать разницу между 7 mainstream CLI agents (Claude Code / Codex / OpenCode / Gemini CLI / goose / Aider / Hermes Agent)
- Выбрать первый CLI-инструмент исходя из сценария
- Завершить install + auth + первую реальную задачу (не hello world)
- Знать, когда переключаться / добавить второй CLI

## 🚪 Условия входа

Уже должен:
- Закончить Упражнение CLI этапа 0 (базовая command-line грамотность)
- Иметь Claude / OpenAI / Google аккаунт (платный не обязателен)
- Чувствовать себя уверенно в prompt-дизайне (этап 2)

## 📚 Обязательное чтение

1. [**`resources/cli-agents-guide.ru.md`**](../../resources/cli-agents-guide.ru.md) ⭐ — основной референс этого track'а. 7 mainstream CLI agents бок-о-бок, use-case picks, реальные setup'ы
2. [**Anthropic — Claude Code Quickstart**](https://docs.anthropic.com/en/docs/claude-code/quickstart) — официальная установка
3. [**OpenAI — Codex Quickstart**](https://github.com/openai/codex/blob/main/README.md) — Codex install + auth

## 🛠 Практические упражнения (делать, не просто читать)

### Упражнение CLI-1: установка + первый запуск
Следуй quickstart выбранного CLI. **Не пиши «hello world»** — дай ему реальную задачу, которую планировал сделать сегодня, например «организуй мою Downloads-папку, передвинь все PDF в ~/Documents/PDFs». Понаблюдай, как он декомпозирует задачу и какие confirmations спрашивает.

### Упражнение CLI-2: встроенный system prompt-файл CLI
- Claude Code → напиши `CLAUDE.md` в корне репо
- Codex → напиши `AGENTS.md`
- Gemini CLI → напиши `GEMINI.md`
- goose / OpenCode → см. доки каждого инструмента

Положи 3 вещи: «твоя persona / предпочитаемый стиль кода / чего нельзя делать». Запусти задачу и понаблюдай за behavioural-различиями.

### Упражнение CLI-3: запусти второй CLI параллельно
Установи второй CLI (рекомендую Codex или OpenCode как backup). Запусти тот же промпт и сравни стиль вывода, скорость, стоимость. **Не выбирать победителя — а понять, что «разные CLI решают одну проблему под разным углом».**

### Упражнение CLI-4: auth corner cases
Намеренно сломай API-ключ (один неверный символ) и посмотри, как CLI выдаст ошибку. Потом «правильный ключ, но неверное имя модели». Production usage наткнётся на auth-проблемы — наступи на них сейчас.

## 🎯 Подборка проектов

### 7 mainstream CLI Agents

Детальное сравнение (stars, license, сильные стороны, рекомендуемые use case'ы) в [`resources/cli-agents-guide.ru.md`](../../resources/cli-agents-guide.ru.md). Быстрые entry points здесь:

#### [anthropics/claude-code](https://github.com/anthropics/claude-code) ⭐⭐⭐⭐⭐
★ 120k+ — рекомендуемый первый CLI agent. Встроенная SKILL / plugin экосистема, CLAUDE.md prompt-система, самые полные community-ресурсы.

#### [openai/codex](https://github.com/openai/codex) ⭐⭐⭐⭐⭐
★ 80k+ — top pick, если уже подписан на ChatGPT Plus / Pro; тот же аккаунт работает в терминале.

#### [sst/opencode](https://github.com/sst/opencode) ⭐⭐⭐⭐⭐
★ 155k+ — open-source, не привязан к LLM-провайдеру, самая быстрая community-итерация. Выбирай для self-hosting или no vendor lock-in.

#### [google-gemini/gemini-cli](https://github.com/google-gemini/gemini-cli) ⭐⭐⭐⭐
★ 103k+ — когда нужен 1M-token длинный контекст для больших кодовых баз / больших PDF.

#### [block/goose](https://github.com/block/goose) ⭐⭐⭐⭐
★ 43k+ — поддержка 15+ провайдеров (вкл. Ollama); используй существующие Claude / ChatGPT / Gemini подписки. Теперь по адресу `aaif-goose/goose` (AAIF / Linux Foundation).

#### [Aider-AI/aider](https://github.com/Aider-AI/aider) ⭐⭐⭐⭐⭐
★ 44k+ — git-native, авто-commit / branch. Выбирай, когда хочешь чистый git workflow с code-правками.

#### [NousResearch/hermes-agent](https://github.com/NousResearch/hermes-agent) ⭐⭐⭐⭐⭐
★ 142k+ — self-improving agent от Nous Research. Три дифференциатора: (1) agent работает на cloud VM, ты пишешь ему из Telegram / Discord / Slack / WhatsApp / Signal; (2) model-neutral — поддерживает GLM / Kimi / Xiaomi MiMo / MiniMax и другие китайские LLM; (3) встроенный cron-scheduler + autonomous skill-evolution loop. ⚠️ self-improving skills — frontier-фича без независимого аудита — стартуй в low-stakes контекстах.

---

### Смежные инструменты

#### [LM Studio](https://lmstudio.ai/)
Closed-source desktop app — drag-and-drop UI для локальных LLM. Попробуй сначала, если на Windows / Mac и хочешь local LLM без command line.

#### [Ollama](https://github.com/ollama/ollama)
★ 170k+ — local LLM runner; хорошо работает в паре с OpenCode / goose (и любым инструментом с OpenAI-совместимым base_url). См. [секцию Local LLM этапа 1](../../stages/01-llm-basics.ru.md).

## ✅ Самопроверка перед A2

Можешь:
- [ ] Сформулировать core-разницу между 7 mainstream CLI (3–4 без подглядывания в таблицу)
- [ ] Имеешь рабочий основной CLI (установлен, аутентифицирован, запустил 5+ реальных задач)
- [ ] Написал свой `CLAUDE.md` / `AGENTS.md` / `GEMINI.md`
- [ ] Запустил второй CLI хотя бы раз, знаешь различия в стиле

Если да → переходи к [A2 — CLI Workflow Patterns](A2-cli-workflow.ru.md).

Если нет → не пропускай. Sloppy CLI-использование — не productive CLI-использование; сделай упражнения CLI-1/2 ещё минимум 3 раза.

## 💡 Напоминание учащимся Track A

CLI agent — не «то же самое с другим UI», как Claude.ai / ChatGPT web — он может читать/писать файлы на твоей машине, запускать shell-команды, модифицировать git. Эта capability-разница заслуживает осторожности **перед использованием**:
- Неделя 1: ревьюй план перед исполнением (или используй `--dry-run`)
- Не давай CLI коммитить прямо в production кодовые базы пока
- Положи sensitive data (ключи, контракты, медкарты) в `.cursorignore` / `.claudeignore`, чтобы исключить
