> [繁體中文](./setup-guide.md) | [简体中文](./setup-guide.zh-Hans.md) | [English](./setup-guide.en.md) | **Русский**

# 🚀 С нуля — Setup Guide для людей без бэкграунда разработки

> [← Назад к главному README](../README.ru.md)

> Ожидаемое время: 30–45 минут. Получишь первый API-ключ, установишь Python / uv и запустишь первый LLM hello world.
> Этот гайд для тех, кто хочет учить AI agents, но раньше не писал код. Если уже знаешь Python, git и CLI — переходи сразу к [Этапу 1](../stages/01-llm-basics.ru.md).

## Сначала выбери уровень входа

Упорядочено от поверхностного к глубокому по объёму setup'а. **Никогда не трогал LLM? Начни с 1️⃣**.

### 1️⃣ Web (самое простое, бесплатный tier, ноль setup'а)

Открой браузер, набери URL — готово. **Лучшее место для старта в первый раз**. Бесплатного тира обычно хватает на неделю экспериментов.

| Сервис | URL | Заметки |
|---|---|---|
| **Claude** | https://claude.ai | Anthropic. У free tier есть дневные лимиты; Pro — $20/мес |
| **ChatGPT** | https://chatgpt.com | OpenAI. Free GPT-5 (базовый); Plus — $20/мес |
| **Gemini** | https://gemini.google.com | Google. Щедрый free tier, интеграция с приложениями Google |
| **Le Chat** | https://chat.mistral.ai | Mistral (EU open-source LLM лаборатория). Бесплатно, фокус на privacy |

### 2️⃣ Desktop-приложение (бесплатно, лучше интеграция между приложениями)

Нативные приложения для macOS / Windows — добавляют системный шорткат, интеграцию с буфером обмена / скриншотами, drag-and-drop файлов.

| Приложение | Скачать | Платформа |
|---|---|---|
| **Claude Desktop** | https://claude.ai/download | macOS / Windows |
| **ChatGPT Desktop** | https://openai.com/chatgpt/download | macOS / Windows |
| **Gemini** | Нативного desktop-приложения пока нет | (используй web) |
| **LM Studio** | https://lmstudio.ai | macOS / Windows / Linux — запускает локальные LLM как desktop-приложение; $0, но нужен GPU/RAM |

### 3️⃣ IDE со встроенным AI (пишешь код с AI-сайдкиком)

Живёт внутри редактора кода — ты пишешь код как обычно, AI рядом подсказывает / редактирует / отвечает на вопросы. **Лучше всего подходит, если уже пишешь код и хочешь AI-native IDE**.

| Инструмент | Скачать | Тип |
|---|---|---|
| **Cursor** | https://cursor.com | Самостоятельный IDE (fork VS Code) |
| **Windsurf** | https://codeium.com/windsurf | Самостоятельный IDE (от Codeium) |
| **Cline** | https://cline.bot | Расширение для VS Code (agentic-стиль) |
| **Continue** | https://continue.dev | Расширение для VS Code / JetBrains (open-source) |
| **Roo Code** | https://github.com/RooCodeInc/Roo-Code | Расширение для VS Code (fork Cline, активное сообщество) |
| **Zed** | https://zed.dev | Самостоятельный редактор со встроенным AI-ассистентом |
| **GitHub Copilot** | https://github.com/features/copilot | Расширение для нескольких IDE (VS Code / JetBrains / и т. д.) |

→ Подробное сравнение → [`branches/for-developer.ru.md`](../branches/for-developer.ru.md)

### 4️⃣ CLI agent (терминал, может читать/писать файлы, запускать shell, управлять git)

Агенты, живущие в терминале — даёшь один промпт (например, «отрефактори этот модуль»), агент читает файлы, редактирует их, запускает команды, делает коммиты. **Более автономен, чем IDE-режим, справляется с multi-step задачами**, но setup тяжелее (нужен Node.js или Python; см. §B / §D ниже).

| CLI Agent | Install / Docs | Основной LLM |
|---|---|---|
| **Claude Code** | https://docs.anthropic.com/en/docs/claude-code/quickstart | Claude |
| **Codex CLI** | https://github.com/openai/codex | GPT-семейство |
| **Gemini CLI** | https://github.com/google-gemini/gemini-cli | Gemini |
| **OpenCode** | https://github.com/sst/opencode | Любой (multi-provider) |
| **goose** | https://block.github.io/goose | Любой |
| **Aider** | https://aider.chat | Любой (git-native) |
| **Hermes Agent** | https://github.com/NousResearch/hermes-agent | 200+ (model-neutral) |

→ Полное сравнение 7 CLI → [`cli-agents-guide.ru.md`](cli-agents-guide.ru.md)
→ Подробная первая установка Claude Code → [§D](#d--install-claude-code-for-the-first-time-about-10-minutes-needed-for-stage-5--for-developer) ниже

> 💡 **IDE vs CLI — как выбрать?** Хочешь AI рядом, пока пишешь код → IDE. Хочешь дать один промпт и пусть агент выполнит multi-step задачу → CLI. Многие используют оба.

### 5️⃣ API + пишешь свой код (самое продвинутое)

Хочешь скриптовать на Python, гонять batch-задачи, интегрировать LLM в своё приложение/автоматизацию? §A–C ниже — для тебя.

> 💡 **Что такое API key?** Пароль, позволяющий программе обращаться к модели. Относись к нему как к платёжной информации.

---

## §A — Получи первый API key (около 10 минут)

### Anthropic Claude (Рекомендуется первым)

1. Открой https://console.anthropic.com/
2. Зарегистрируйся через Google, GitHub или email.
3. После входа найди **API Keys**, выбери **Create Key**.
4. **Сразу скопируй ключ**. Большинство платформ показывают его только один раз.
5. Положи в локальный password manager или ненадолго в локальный текстовый файл; следующий раздел перенесёт его в `.env`.

> ⚠️ **Три правила API-ключа**
> - **Не вставляй** в чаты, групповые чаты, email или скриншоты.
> - **Не загружай** в git; GitHub может обнаружить и отозвать его.
> - **Не храни** как plain text в облачном диске; синхронизация увеличивает экспозицию.

### Другие варианты LLM

- **OpenAI**: https://platform.openai.com/api-keys
  ChatGPT Plus и API-доступ — разные вещи; подписчикам Plus всё равно нужен API-ключ.
- **Google AI Studio**: https://aistudio.google.com/
  Удобно для пробы Gemini API. Free-квота зависит от региона и состояния аккаунта.
- **Локальные модели Ollama**: API-ключ не нужен. Для локального пути см. [Cookbook Recipe 6](cookbook.ru.md#6-local-llm--cli-agent-quick-walkthrough).

---

## §B — Установка локального окружения (около 10 минут)

### Установи Python 3.10+

- **macOS**: открой Terminal и запусти `brew install python@3.12`. Если Homebrew не установлен — начни с https://brew.sh.
- **Windows**: скачай инсталлятор с https://www.python.org/downloads/ и убедись, что **Add Python to PATH** отмечен.
- **Linux**: на Ubuntu — `sudo apt install python3 python3-venv`; на Fedora — `sudo dnf install python3`.
- **Проверка**: macOS / Linux: `python3 --version`; Windows: `py --version`. Нужен `Python 3.10` или новее.

### Установи uv

uv — инструмент управления пакетами Python. Для этого гайда воспринимай его как «установи нужные пакеты, потом запусти этот скрипт».

```bash
# macOS / Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows PowerShell
irm https://astral.sh/uv/install.ps1 | iex
```

Проверка:

```bash
uv --version
```

### Создай первый `.env` файл

В папке, где хочешь запускать скрипт, создай файл `.env`:

```bash
ANTHROPIC_API_KEY=sk-ant-...вставь скопированный ключ
```

`.env` — место, где живут локальные секреты. Программа может его прочитать, но загружать на GitHub нельзя.

### Добавь `.gitignore`

В той же папке создай `.gitignore`:

```gitignore
.env
__pycache__/
*.pyc
```

Это удерживает git от записи твоего `.env`.

---

## §C — Запусти первый `hello-claude.py` (около 5 минут)

Создай `hello-claude.py`:

```python
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()
client = Anthropic()  # Автоматически читает ANTHROPIC_API_KEY

msg = client.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=100,
    messages=[{"role": "user", "content": "Hello, who are you?"}],
)

print(msg.content[0].text)
```

Запусти:

```bash
uv run --with anthropic --with python-dotenv python hello-claude.py
```

Если Claude представился — API-ключ, Python и пакеты работают.

### Частые ошибки

| Ошибка | Вероятная причина | Фикс |
|---|---|---|
| `401 Unauthorized` | API-ключ отсутствует или с опечаткой | Скопируй заново из §A, проверь имя файла `.env` и значение |
| `429 Rate limit` | Слишком много запросов слишком быстро | Подожди несколько секунд или минут и повтори |
| `connection refused` | Проблема сети или firewall | Проверь сеть, корпоративный firewall или firewall в учебном заведении |
| `ModuleNotFoundError` | Пакет не установлен | Убедись, что запустил ровно команду `uv run --with ...` выше |

---

## §D — Первая установка Claude Code (около 10 минут; нужно для этапа 5 / for-developer)

### Сначала установи Node.js

- **macOS / Linux**: запусти `brew install node` или скачай с https://nodejs.org.
- **Windows**: скачай инсталлятор с https://nodejs.org.
- **Проверка**: запусти `node --version`; v18 или новее — достаточно.

### Установи Claude Code

```bash
npm install -g @anthropic-ai/claude-code
```

### Первая аутентификация

```bash
claude
```

При первом запуске обычно выбираешь между:

- **Claude subscription**: войди через аккаунт Claude.ai. Самый простой путь для новичков.
- **API key**: вставь ключ, созданный в §A.

### Создай первый `CLAUDE.md`

Создай `CLAUDE.md` в корне проекта. Claude Code читает его при запуске, чтобы понять, как ты хочешь получать помощь.

```markdown
# Кто ты
Я [твоё имя], [твоё поле, например учитель / исследователь / писатель].

# Стиль кода
- Пиши комментарии на русском, код — на английском
- Предпочитай type hints при написании функций
- Не коммить автоматически; я сам запущу git add

# Не делай так
- Не лезь в веб без явного разрешения
- Не модифицируй `.env` или `.gitignore`
- Не удаляй папки, включая подпапки
```

---

## §E — Первый пример Skill (около 5 минут; нужно для этапа 5.3)

Skill — это переиспользуемый пакет промптов для Claude Code. Когда твоё сообщение совпадает с описанием, Claude Code автоматически загружает эту инструкцию.

Создай `.claude/skills/hello-skill/SKILL.md`:

```markdown
---
name: hello-skill
description: First hello skill. Trigger when the user says "請打招呼", "say hi", or "поздоровайся".
---

Когда пользователь просит поздороваться, верни три вещи:

1. Скажи привет один раз на русском и один раз на английском
2. Упомяни сегодняшнюю дату по системному времени
3. Дай одно маленькое ежедневное напоминание, случайно выбрав из категорий: здоровье / обучение / настроение
```

Запусти `claude`, набери `say hi` (или `поздоровайся`). Если Claude вернул три пункта — Skill загрузился.

> Глубже про дизайн Skills — см. [Этап 5.3 — Skills](../stages/05-claude-code-ecosystem.ru.md#53--skills-claude-code-behavior-layer).
> Готовые примеры copy-and-run — [Cookbook](cookbook.ru.md).

---

## Куда дальше

| Текущее состояние | Следующий шаг |
|---|---|
| Хочешь понять LLM, API и токены | [Этап 1 — LLM Basics](../stages/01-llm-basics.ru.md) |
| Хочешь выбрать ветку по роли | [Everyday users](../branches/for-everyday-users.ru.md) / [Teachers](../branches/for-teacher.ru.md) / [Knowledge workers](../branches/for-knowledge-worker.ru.md) / [Researchers](../branches/for-researcher.ru.md) / [Developers](../branches/for-developer.ru.md) |
| Хочешь всю экосистему Claude Code | [Этап 5 — Claude Code Ecosystem](../stages/05-claude-code-ecosystem.ru.md) |
| Хочешь локальные LLM без облачного ключа | [Cookbook Recipe 6](cookbook.ru.md#6-local-llm--cli-agent-quick-walkthrough) |
| Хочешь сравнить CLI agents | [CLI Agents Comparison Guide](cli-agents-guide.ru.md) |
| Термин непонятен | [Glossary](glossary.ru.md) |
