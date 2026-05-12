# Руководство по сравнению CLI Agents

> [繁體中文](./cli-agents-guide.md) | [简体中文](./cli-agents-guide.zh-Hans.md) | [English](./cli-agents-guide.en.md) | **Русский**

> [← Назад к README основного пути](../README.ru.md)

> 📌 **Это reference-документ** (глубокое сравнение, логика выбора, ловушки, рекомендуемые setup'ы).
> Первый раз с CLI agents, нужен пошаговый onboarding → см. [`tracks/cli/A1-cli-intro.ru.md`](../tracks/cli/A1-cli-intro.ru.md) (первая остановка Track A).
> Уже используешь один, хочешь решить / сравнить / апгрейднуть → оставайся здесь.

Cross-branch референс, общий для Track A (A1–A3) + всех 5 специализированных веток: **как выбрать между Claude Code / Codex / OpenCode / Gemini CLI / goose / Aider / Hermes Agent?** Каждая ветка ссылается на CLI agents, но ни одна ветка не «владеет» этим сравнением, поэтому оно живёт в `resources/`.

---

## 📋 7 основных terminal CLI agents

Включены только terminal-based CLI agents. IDE-based агенты (Cursor / Cline / Continue) живут в [for-developer](../branches/for-developer.ru.md). Первые 6 цифр верифицированы через `gh api` 2026-05-06; Hermes Agent — 2026-05-10.

| Tool | Provider | License | Основной LLM | Auth / Pricing | Stars |
|---|---|---|---|---|---|
| [Claude Code](https://github.com/anthropics/claude-code) | Anthropic (официальный) | NOASSERTION | Claude | Claude subscription **ИЛИ** API-ключ Anthropic Console | ★ 120k+ |
| [Codex](https://github.com/openai/codex) | OpenAI (официальный) | Apache-2.0 | GPT-семейство | Вход через ChatGPT-аккаунт **ИЛИ** OpenAI API key | ★ 80k+ |
| [OpenCode](https://github.com/sst/opencode) | community (репо теперь `anomalyco/opencode`) | MIT | Любой (multi-provider) | BYO API key, или встроенный OpenCode Zen hosted | ★ 155k+ |
| [Gemini CLI](https://github.com/google-gemini/gemini-cli) | Google (официальный) | Apache-2.0 | Gemini | Щедрый free tier, платный сверх квоты | ★ 103k+ |
| [goose](https://github.com/block/goose) | Agentic AI Foundation (репо теперь `aaif-goose/goose`) | Apache-2.0 | 15+ провайдеров (вкл. Ollama) | BYO API key, или существующая Claude / ChatGPT / Gemini подписка через ACP | ★ 43k+ |
| [Aider](https://github.com/Aider-AI/aider) | Aider-AI (community) | Apache-2.0 | Любой | BYO API key | ★ 44k+ |
| [Hermes Agent](https://github.com/NousResearch/hermes-agent) | Nous Research | MIT | 200+ через OpenRouter / NVIDIA NIM / Zhipu GLM / Kimi / Xiaomi MiMo / MiniMax / HF / OpenAI | BYO API key (multi-provider) | ★ 142k+ |

---

## 🎯 Что выбрать? Решай по use case

### Писать статьи / литература / research
**Top pick**: Claude Code (длинный контекст, сильное reasoning, хорошая устойчивость к hallucination). Gemini CLI — альтернатива; его миллион-токенов контекст подходит для whole-PDF / whole-dataset workflow'ов.

### Писать код / рефакторить кодовую базу
**Top pick**: Aider (git-native — авто-коммит каждого изменения, легко откатить) или Claude Code. OpenCode подходит, когда нужно переключаться между LLM.

### Privacy / offline / без облака
**Top pick**: goose или OpenCode + локальный Ollama. Оба поддерживают BYO LLM и подключаются к `http://localhost:11434/v1` (Ollama по дефолту).

### Уже подписан на ChatGPT Plus / Pro
**Top pick**: Codex — тот же аккаунт, без отдельного биллинга.

### Хочешь 1M-токенов длинный контекст + Google-экосистему
**Top pick**: Gemini CLI. Щедрый free tier и длинный контекст — дифференциаторы. Заметь: интеграция Google-сервисов (Gmail / Drive / Docs) идёт через MCP-расширения, не built-in коннекторы — тот же setup-паттерн, что у других CLI.

### Хочешь избежать vendor lock-in
**Top pick**: OpenCode > goose > Aider. Ни один не привязывает к конкретному провайдеру; модели взаимозаменяемы.

### Первый раз ставишь CLI agent — нужен простейший старт
**Top pick**: Claude Code. Широкая экосистема, механизм CLAUDE.md для version-controlled промптов, много community-ресурсов, когда натыкаешься на проблемы.

### Хочешь, чтобы он работал на cloud VM, общался через Telegram / Slack / Discord, с китайскими LLM как primary
**Top pick**: Hermes Agent. Три дифференциатора:
- **Отвязан от твоего ноутбука** — agent работает на $5 VPS / Modal serverless / Vercel Sandbox; ты пишешь ему из Telegram / Discord / Slack / WhatsApp / Signal
- **Model-neutral** — поддерживает GLM / Kimi / Xiaomi MiMo / MiniMax, совпадает с записями каталога §11 Chinese-ecosystem
- **Встроенный self-improving skill loop + cron scheduler** — agent автономно генерирует skills из взаимодействия, рафинирует их между сессиями, гоняет scheduled jobs без присмотра
- ⚠️ Self-evolving skills — фронтирная фича без независимого аудита; для production-задач стартуй с low-stakes экспериментов

---

## 📝 Портируемые промпты между CLI

Если хочешь промпты, работающие через CLI-инструменты (или хочешь переключаться без переписывания), следуй принципам:

1. **Явно указывай пути файлов** — «modify `src/auth.py`» бьёт «modify that auth file»
2. **Проси multi-step разбиение** — «first list a plan, then act after I confirm» работает в каждом CLI
3. **Избегай CLI-специфичной магии** — `/init` `/compact` — Claude-Code-специфичные; у OpenCode их нет
4. **Используй `.cursorrules` / `CLAUDE.md` / `AGENTS.md` для постоянных предпочтений** — Claude Code читает `CLAUDE.md`, Codex читает `AGENTS.md`, OpenCode читает `OPENCODE.md`, **контент может быть тем же**
5. **Чётко обозначай scope ревью** — «review only my diff» vs «review the whole repo»

Cross-CLI промпты обычно на 5–10% многословнее, чем CLI-специфичные, но плюс — переключаешься без переписывания.

---

## ⚠️ Распространённые ловушки

### Обработка путей файлов
- Windows использует обратные слэши (`C:\Users\...`); большинство CLI переводят внутри, но иногда путаются
- Рекомендация: в git-bash / WSL используй forward слэши, избегай странных кавычек

### Различия git-интеграции
- **Aider** авто-коммитит каждое изменение (by design, не баг)
- **Claude Code / Codex / OpenCode / goose** не авто-коммитят по дефолту — вручную или через промпт

### Дефолтный sandbox (каждый CLI отличается; проверяй официальные доки перед использованием)
- **Claude Code**: bash пишет по дефолту в cwd; читает шире (кроме deny-rule путей)
- **Codex**: в version-controlled папках рекомендуется `Auto` (workspace-write + on-request escalation); в non-git папках — `read-only`
- **goose / OpenCode**: относительно permissive — добавляй явные sandbox / approval-правила; не полагайся на дефолты

### Накопление token cost
- Запуск `grep` по большой кодовой базе может съесть 100k+ токенов
- Суммаризация длинного PDF может попасть в 500k токенов (Gemini справляется; другие инструменты должны быть cost-aware)
- Рекомендация: оценивай стоимость перед каждой операцией; ставь месячный cap

### Multi-CLI session interference
- Два CLI в одном репо (например, Claude Code + Aider) могут race-condition'ить правки файлов
- Рекомендация: один репо, один CLI (если только реально не нужен параллелизм)

---

## 🔧 Реальные setup'ы

Три распространённых комбинации; выбери подходящий:

### Setup A: Claude Code primary + OpenCode backup
- Claude Code обрабатывает 90% ежедневной работы (код, доки, debug)
- OpenCode + Ollama для privacy-чувствительных данных (медицинские, финансовые)
- Один промпт, работает в обоих

### Setup B: Codex (GPT) + Aider (Claude) mix
- Codex обрабатывает мелкие задачи в рамках квоты ChatGPT Plus
- Aider с Claude API key обрабатывает большие рефакторинги (git-native commit удобен)
- Раздельный биллинг, без интерференции

### Setup C: Gemini CLI primary (сценарии long-context)
- Whole PDF / whole codebase подаётся разом
- Добавь Aider для сценариев, требующих точного git diff
- Подходит scholar'ам, knowledge worker'ам

### Setup D: Hermes Agent + локальный Ollama (multi-platform + китайские LLM + offline)
- **Hermes Agent** работает на low-cost VPS или твоей машине как multi-platform agent-gateway
- **LLM endpoint** может быть Ollama (`http://localhost:11434/v1`) или сменён на провайдеров вроде z.ai GLM / Kimi
- **Chat entrypoint** может быть Telegram / Slack / Discord; Hermes маршрутизирует platform-сообщения в agent workflow
- **Когда нужен ноль зависимости от Anthropic / OpenAI**, этот setup подходит для offline, privacy-чувствительных и low-cost повторяющихся экспериментов
- Пошаговый walkthrough: [`resources/cookbook.ru.md` Recipe 6](cookbook.ru.md#6-local-llm--cli-agent-quick-walkthrough)

---

## Связь с ветками

У разных аудиторий разные CLI-потребности:

- **[for-developer](../branches/for-developer.ru.md)**: см. также IDE-based agents (Cursor, Cline, Continue)
- **[for-everyday-users](../branches/for-everyday-users.ru.md)** Tier 2: CLI — продвинутый вариант; сначала попробуй Tier 0 / 1 (Web / Desktop App)
- **[for-researcher](../branches/for-researcher.ru.md)**: см. также paper-специфичные инструменты (paper-qa, gpt-researcher, ChatPaper)
- **[for-knowledge-worker](../branches/for-knowledge-worker.ru.md)**: см. также workflow-автоматизацию (n8n, Make)
- **[for-teacher](../branches/for-teacher.ru.md)**: CLI продвинутый для учителей; стартуй с prompt-библиотек

---

## Заметки по поддержке

- Stars / license / pushed_at 7 CLI-инструментов рефрешатся ежеквартально через `bash scripts/refresh-stars.py`
- Рынок CLI движется быстро — новые инструменты требуют оценки перед включением (планка: 30k+ stars, активная поддержка, true CLI, не IDE)
- Сравнительная таблица намеренно опускает колонки «сильные / слабые стороны» — избегая субъективного bias и оставляя эту работу секции use-case'ов + собственному суждению читателя
