# Cookbook — переводи концепции в исполнимые рецепты

> [繁體中文](./cookbook.md) | [简体中文](./cookbook.zh-Hans.md) | [English](./cookbook.en.md) | **Русский**

> Этап 5 (Claude Code Ecosystem) говорит про «Концепции» и «Доступные инструменты» вместе с [`mcp-skills-catalog.ru.md`](mcp-skills-catalog.ru.md). Этот cookbook заполняет промежуток: «**как собрать**». Каждый рецепт — пошаговый гид + sample-код + распространённые ловушки, спроектирован на 30–50 минут.
>
> Это не reference и не туториал — это рецепт. Бери нужный и начинай готовить.

---

## 📋 Содержание

1. [Напиши первый Skill (анатомия SKILL.md)](#1-write-your-first-skill)
2. [Напиши первый MCP Server (Python SDK)](#2-write-your-first-mcp-server)
3. [Office Docs Workflow](#3-office-docs-workflow)
4. [NotebookLM Workflow](#4-notebooklm-workflow)
5. [Zotero Workflow](#5-zotero-workflow)
6. [Local LLM + CLI Agent quick walkthrough](#6-local-llm--cli-agent-quick-walkthrough)

---

## 1. Write Your First Skill

> Skill — это папка, содержащая `SKILL.md`, который Claude Code автоматически обнаруживает при запуске и загружает контекстуально. Минимально жизнеспособная версия запускается с 50 строк кода.

### Зачем

Разница между написанием Skill и добавлением нескольких инструкций в промпт:
- Skills **per-domain** — не загрязняют все разговоры.
- Их можно паковать и шарить между проектами или командами.
- Claude решает, когда их загрузить (по совпадению description с контекстом).

### Шаги

#### Шаг 1: Создай папку Skill

Skills могут лежать в двух местах (в зависимости от scope user-level / project-level):

```bash
# User-level (общий для всех проектов)
mkdir -p ~/.claude/skills/my-first-skill
cd ~/.claude/skills/my-first-skill

# Или Project-level (срабатывает только в этом репо)
mkdir -p .claude/skills/my-first-skill
cd .claude/skills/my-first-skill
```

#### Шаг 2: Напиши `SKILL.md`

Минимальный рабочий шаблон:

```markdown
---
name: my-first-skill
description: When the user asks for [SPECIFIC SITUATION], use this skill to [WHAT IT DOES]. Examples include [2-3 trigger phrases]. Do NOT use for [WHAT IT'S NOT FOR].
---

# My First Skill

You are now in the [domain] context.

## When the user asks X, do these steps:

1. First, [action A]
2. Then, [action B]
3. Verify with [check]

## Don't do:

- [anti-pattern 1]
- [anti-pattern 2]

## Reference

- (optional) link to a doc / paper / API spec
```

Конкретный пример: «Organize Python imports by PEP 8 order»

```markdown
---
name: python-import-organizer
description: When the user pastes Python code or asks to clean up imports / format code / sort imports, organize the imports following PEP 8 + isort order: stdlib first, then third-party, then local. Do NOT use for non-Python code.
---

# Python Import Organizer

When the user wants Python imports cleaned up:

1. Group imports into 3 sections: stdlib / third-party / local
2. Within each group, sort alphabetically
3. Add a blank line between groups
4. Remove unused imports (only if user explicitly asks; otherwise just sort)

## Don't:
- Don't change function code, only the import block
- Don't auto-remove imports without asking
```

#### Шаг 3: Тест

```bash
# Перезапусти Claude Code (чтобы пере-discover'ил skills)
# Дай trigger-фразу в разговоре
# например, "Help me organize the imports in this Python code."
# Понаблюдай, следует ли Claude шагам в SKILL.md
```

#### Шаг 4 (advanced): добавь Evals

Добавь `evals/evals.json` внутрь папки skill:

```json
{
  "evals": [
    {
      "input": "Organize the imports in this Python code: import os
import requests
from mypackage import foo",
      "expected_behavior": ["Group by stdlib / third-party / local", "Sort alphabetically"]
    }
  ]
}
```

Дальше можно использовать инструменты вроде promptfoo для batch-тестов.

### Распространённые ловушки

| Симптом | Причина | Решение |
|---|---|---|
| Claude никогда не триггерит мой skill | `description` слишком generic, не совпадает с user queries | Добавь 2–3 конкретных trigger-фразы в `description` (например, «when the user asks X / Y / Z») |
| Триггерит, но ведёт себя неправильно | Шаги skill в `SKILL.md` слишком абстрактны | Поменяй на numbered list, каждый шаг — чёткое действие |
| Триггерит, когда не должен | `description` слишком broad, совпадает с нерелевантными запросами | Добавь «Do NOT use for X», чтобы сузить scope |

### Дальнейшее чтение

- См. [Этап 5.3](../stages/05-claude-code-ecosystem.ru.md#53--skills-claude-code-behavior-layer) для детального объяснения анатомии Skill.
- Смотри официальные skill-шаблоны в [`anthropics/skills`](https://github.com/anthropics/skills) (для docx / xlsx / pptx и т. д.) как примеры.
- Упаковка нескольких skills в plugin → [Этап 5.4](../stages/05-claude-code-ecosystem.ru.md#54--plugins--marketplaces)

---

## 2. Write Your First MCP Server

> MCP server — отдельный процесс, отдающий tools / resources / prompts LLM-хосту (Claude Desktop / Claude Code). Минимально рабочая версия — меньше 50 строк Python.

### Зачем

- Skills — для «роли + правил» Claude; MCP — для «**внешних функций**» Claude.
- Skills не могут читать файлы или звать API; MCP могут (любой инструмент, который можно заскриптить).
- Skills работают только внутри Claude Code; MCP могут использоваться любым LLM-хостом (включая кастомных agents).

### Шаги

#### Шаг 1: Установи официальный SDK

```bash
pip install mcp
```

#### Шаг 2: Напиши `server.py`

Минимальный шаблон echo-tool:

```python
# server.py
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

app = Server("hello-mcp")

@app.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="echo",
            description="Echo the input text back to the user.",
            inputSchema={
                "type": "object",
                "properties": {
                    "text": {
                        "type": "string",
                        "description": "Text to echo back",
                    }
                },
                "required": ["text"],
            },
        )
    ]

@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    if name == "echo":
        return [TextContent(type="text", text=f"Echo: {arguments['text']}")]
    raise ValueError(f"Unknown tool: {name}")

async def main():
    async with stdio_server() as (read, write):
        await app.run(read, write, app.create_initialization_options())

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
```

#### Шаг 3: Конфигурация в Claude Desktop / Code

**Claude Desktop**: правь `~/Library/Application Support/Claude/claude_desktop_config.json` (macOS) или `%APPDATA%\Claude\claude_desktop_config.json` (Windows):

```json
{
  "mcpServers": {
    "hello-mcp": {
      "command": "python",
      "args": ["/absolute/path/to/server.py"]
    }
  }
}
```

**Claude Code**: используй команду `claude mcp add`:

```bash
claude mcp add hello-mcp python /absolute/path/to/server.py
```

#### Шаг 4: Перезапусти Claude Desktop / Code и тестируй

```
Ты: echo "hello world" to me
Claude отвечает (с иконкой tool call): Echo: hello world
```

### Распространённые ловушки

| Симптом | Причина | Решение |
|---|---|---|
| Claude Desktop не видит tool | `server.py` не стартанул | Запусти `python server.py` прямо в терминале и проверь `stderr` на ошибки |
| Tool в списке, но вызов падает | Неправильный формат `inputSchema` (missing `required` fields, wrong `type`) | См. [`schema-design-cheatsheet.ru.md`](schema-design-cheatsheet.ru.md) |
| Claude не проактивно зовёт tool | `description` слишком generic | Уточни `description` до конкретных trigger-фраз вроде «When the user asks X, use this tool» |
| stdio vs SSE? | `stdio` — для локальной desktop-интеграции; `SSE` — для remote/web | Для первого сервера всегда используй `stdio`. |

### Дальнейшее чтение

- См. [Этап 5.2](../stages/05-claude-code-ecosystem.ru.md#52--mcp-model-context-protocol-foundation) для полного введения в MCP.
- Смотри официальные примеры в [`modelcontextprotocol/servers`](https://github.com/modelcontextprotocol/servers) (например, filesystem, github, sqlite, time).
- Для production-серверов см. [Stage 5.2 "Practice: MCP in production"](../stages/05-claude-code-ecosystem.ru.md#52--mcp-model-context-protocol-foundation) и примеры `~/.claude/skills/` в [`anthropics/claude-code`](https://github.com/anthropics/claude-code).

---

## 3. Office Docs Workflow

> Используй Claude для чтения и записи Word / Excel / PowerPoint / PDF без установки лишних инструментов — официальный репо [`anthropics/skills`](https://github.com/anthropics/skills) уже их включает.

### Зачем

Частые сценарии:
- Генерация Word / PPT из Markdown / outline.
- Суммаризация / извлечение данных из множества PDF / Excel.
- Правка полученных `.docx` (например, добавление track changes, переформатирование).
- Cross-reference таблиц для отчётов.

Не нужно парсить XML или искать туториалы для `python-docx` / `openpyxl` — `anthropics/skills` уже всё покрывает.

### Шаги

#### Шаг 1: Установи Skills

Простейший способ — клонировать официальный Anthropic skills репо в user-level skill-директорию:

```bash
# User-level (для всех проектов)
git clone https://github.com/anthropics/skills.git ~/.claude/skills/anthropic-skills
```

Альтернативно — `claude plugin install`, если упаковано как plugin.

#### Шаг 2: Перезапусти Claude Code

- `skills/docx/` → Read/write DOCX
- `skills/xlsx/` → Read/write Excel
- `skills/pptx/` → Read/write PowerPoint
- `skills/pdf/` → Read PDF

Claude автоматически загрузит нужный skill по запросу.

#### Шаг 3: Практические prompt-шаблоны

**Сгенерируй PPT из outline**:
```
Read my outline.md, and generate a PPT based on this structure:
- 1 title slide
- 1 slide per H2, with bullet points condensed from H3 content
- 1 conclusion slide

Save as ./output/presentation.pptx
```

**Прочитай Excel и суммаризируй**:
```
Read the first sheet of ./data/sales-2023.xlsx, calculate the total Q4 sales for each region,
and write it into ./output/q4-summary.md using a markdown table format.
```

**Правка DOCX**:
```
Read ./doc/draft.docx, change all instances of "使用者" to "用户" (zh-Hans translation),
and save as ./doc/draft.zh-Hans.docx, preserving the original track changes.
```

**Чтение PDF и извлечение информации**:
```
Read ./papers/research.pdf, extract the abstract, main contributions, and limitations,
and write each into separate markdown sections in ./notes/research-summary.md.
```

### Распространённые ловушки

| Симптом | Причина | Решение |
|---|---|---|
| Skill не триггерится | Неправильный путь репо | Убедись, что `SKILL.md` лежит на уровне вроде `~/.claude/skills/anthropic-skills/skills/docx/SKILL.md` |
| У сгенерированной PPT уродский стиль | Не дан design reference | Добавь «Use ./template.pptx as a style reference» в промпт |
| Большие PDF не дочитываются | Ограничение context window | Используй [`SylphxAI/pdf-reader-mcp`](https://github.com/SylphxAI/pdf-reader-mcp) (в 5–10 раз быстрее) |
| Excel-формулы теряются | `docx` skill не обрабатывает формулы | Прямо в промпте «preserve formulas, do not hard-code values» до открытия файла |

### Дальнейшее чтение

- Каталог §2 [`mcp-skills-catalog.ru.md` §2 Office Documents](mcp-skills-catalog.ru.md#2-office-documents-word--excel--powerpoint--pdf): улучшенные office skills / отдельный MCP для Excel / PPT.
- Office workflow на китайском: [`leemysw/feishu-docx`](https://github.com/leemysw/feishu-docx) для Feishu / Lark docs ↔ Markdown.

---

## 4. NotebookLM Workflow

> NotebookLM — RAG-on-your-docs инструмент Google. **У Claude Code нет официальной интеграции с NotebookLM**, но есть два зрелых community-решения.

### Зачем

Сильные стороны NotebookLM:
- Автоматически индексирует до 50 загруженных PDF.
- Даёт Q&A с цитатами (каждый ответ ссылается на документ и номер страницы).
- Генерирует резюме, mind maps или podcast-style audio overview.

Слабость: используется через web-интерфейс NotebookLM, что отрывает его от других workflow'ов (Claude Code, Obsidian, Zotero).

Два решения мостят этот разрыв:
1. **PleasePrompto/notebooklm-skill** (Skill, browser automation)
2. **teng-lin/notebooklm-py** (Python API + CLI)

### Выбор между двумя решениями

| Сценарий | Выбирай | Почему |
|---|---|---|
| Эпизодически запрашивать NotebookLM из Claude Code | `PleasePrompto/notebooklm-skill` | Один промпт в Claude Code; простая настройка. |
| Batch-операции (например, создать 100 notebooks, импортировать документы массово) | `teng-lin/notebooklm-py` | Python API для программного исполнения. |
| Избежать поломки из-за изменений Google policy | (Ждать официального Google API) | Оба решения неофициальные, могут ломаться. |

### Решение A: PleasePrompto/notebooklm-skill

#### Шаг 1: Клонируй в skills-директорию

```bash
git clone https://github.com/PleasePrompto/notebooklm-skill ~/.claude/skills/notebooklm
```

#### Шаг 2: первый запуск требует Google login (browser automation)

Следуй README репо для настройки OAuth или login-cookies.

#### Шаг 3: Практические промпты

```
Search my NotebookLM notebooks for ones related to "LLM Agents 2024".
Find all paragraphs mentioning "tool use" and organize them into a comparison table,
including the filename and page number for each source.
```

### Решение B: teng-lin/notebooklm-py

```bash
pip install notebooklm-py
```

Пример:

```python
from notebooklm import NotebookLM
nlm = NotebookLM()  # OAuth flow

# Создай notebook
nb = nlm.create_notebook("My Research")

# Batch-импорт PDF
for pdf in glob.glob("papers/*.pdf"):
    nb.add_source(pdf)

# Q&A
answer = nb.query("What are the main contributions?")
print(answer.text)
print(answer.citations)
```

### Распространённые ловушки

| Симптом | Причина | Решение |
|---|---|---|
| Внезапно перестало работать | Google поменял внутренний API | Проверь issue tracker; жди community-апдейтов |
| Q&A-ответы расплывчатые | Слишком много source'ов залито, retrieval неточен | Разбей на несколько notebook'ов (каждый < 50 source'ов) |
| Плохая поддержка китайского | UI по дефолту английский | Поменяй настройки NotebookLM на zh-Hant |

### Дальнейшее чтение

- Каталог §1 [`mcp-skills-catalog.ru.md` §1 Notes / Knowledge Base](mcp-skills-catalog.ru.md#1-notes--knowledge-base)
- Полный research workspace: интегрируй NotebookLM + Zotero + Obsidian через [`WenyuChiou/research-hub`](https://github.com/WenyuChiou/research-hub).

---

## 5. Zotero Workflow

> Zotero управляет твоей литературой. С [`WenyuChiou/zotero-skills`](https://github.com/WenyuChiou/zotero-skills) Claude Code может напрямую искать, добавлять, категоризировать и тегировать ссылки.

### Зачем

Классические pain points research workflow:
- «Где эта статья?» — Zotero её хранит, но требует переключения окна.
- «Дай мне summaries всех статей про transformers» — нужен ручной отбор, экспорт, потом подача в LLM.
- «Какие теги поставить этой статье?» — вручную.

`zotero-skills` превращает это в single-промпты в Claude Code.

### Отличие от zotero-gpt

| Инструмент | Роль | Лучше всего для |
|---|---|---|
| [`MuiseDestiny/zotero-gpt`](https://github.com/MuiseDestiny/zotero-gpt) | Zotero plugin (чат **внутри** Zotero) | Задавать LLM вопросы при чтении статей без переключения окон. |
| [`WenyuChiou/zotero-skills`](https://github.com/WenyuChiou/zotero-skills) | Claude Code skill (оперирует Zotero **снаружи**) | Главным образом используя Claude Code для написания статей / literature review. |

Они дополняют друг друга, не взаимоисключающие; можно поставить оба.

### Шаги

#### Шаг 1: Включи Zotero Local API

Desktop-приложение Zotero не включает API по дефолту. Включи:
- **Edit → Preferences → Advanced → Config Editor**
- Найди `extensions.zotero.httpServer.enabled` и поставь `true`.
- Найди `extensions.zotero.httpServer.port`; по дефолту `23119`.

#### Шаг 2: Клонируй zotero-skills

```bash
git clone https://github.com/WenyuChiou/zotero-skills ~/.claude/skills/zotero-skills
```

Следуй README репо для настройки, включая конфигурацию API-ключа для write-операций через Web API.

#### Шаг 3: Практические промпты

**Поиск литературы**:
```
Search my Zotero library for all papers published after 2023 related to multi-agent systems,
sort them by cited count, and output as a markdown table.
```

**Автоматическая категоризация**:
```
Review the 50 papers in my "Inbox" collection in Zotero, automatically create sub-collections based on topics
(e.g., "RAG", "Tool Use", "Multi-Agent"), and move the papers into them.
```

**Тегирование статей**:
```
Read this paper in my Zotero (after reviewing its attached PDF),
extract 5 keywords from the abstract to use as tags.
```

**Организация цитат для paper writing**:
```
My paper draft is in ./paper/v3.tex. Find all \cite{} entries, compare them against my Zotero library,
and export any missing BibTeX entries as a .bib file for me.
```

### Распространённые ловушки

| Симптом | Причина | Решение |
|---|---|---|
| Skill триггерится, но запрос падает | Zotero не запущен / API не включён | Запусти Zotero desktop + подтверди, что порт 23119 слушает |
| Write-операции (add/move) падают | Local API read-only; нужен Web API | Сконфигурируй Web API-ключ ([zotero.org/settings/keys](https://www.zotero.org/settings/keys)) |
| Collection-структура становится беспорядочной | Промпт для авто-категоризации не имел directory structure-контекста | Дай Claude существующее collection tree в промпте перед просьбой категоризировать. |

### Дальнейшее чтение

- Полный research workspace: интегрируй Zotero + Obsidian + NotebookLM через [`WenyuChiou/research-hub`](https://github.com/WenyuChiou/research-hub).
- Академическое paper writing: [`WenyuChiou/academic-writing-skills`](https://github.com/WenyuChiou/academic-writing-skills).
- Подборка 14 research workflow skills: [`WenyuChiou/ai-research-skills`](https://github.com/WenyuChiou/ai-research-skills).

---

## 6. Local LLM + CLI Agent quick walkthrough

> Примерно за 30 минут подключи настройку локальной модели этапа 1 к CLI agent этапа 5: полезно для offline-работы, конфиденциальных файлов и экспериментов, где не хочется тратить API-квоту.

### Зачем

Этап 1 учит local LLM runtime'ам — Ollama / llama.cpp / vLLM. Этап 5 учит экосистеме Claude Code, MCP, Skills и Plugins. Распространённое непонимание между ними: **Claude Code не local LLM runner**. Claude Code требует Anthropic OAuth / API-credential'ы; не может напрямую переключить model endpoint на Ollama или другой локальный endpoint.

Если цель — «local LLM + CLI agent», выбери CLI, поддерживающий BYO LLM. **OpenCode / goose / Aider / Hermes Agent** могут подключиться к OpenAI-compatible endpoint'у или Ollama-провайдеру. Этот рецепт даёт короткий путь, чтобы провалидировать модель, агент и одну реальную задачу.

### Шаги

#### Шаг 1: Ollama + модель (10 минут)

```bash
# Установка Ollama: https://ollama.com
ollama pull qwen2.5:3b
# На 16GB+ RAM можно попробовать: ollama pull qwen2.5:7b
ollama serve
```

Подтверди, что OpenAI-compatible API отвечает:

```bash
curl http://localhost:11434/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model":"qwen2.5:3b","messages":[{"role":"user","content":"Explain ReAct agents in 3 sentences."}]}'
```

#### Шаг 2: Выбери один CLI agent и подключи к Ollama (10 минут)

**OpenCode**: хорош, когда хочешь переключение провайдеров + локальные модели.

```bash
npm install -g opencode-ai
opencode auth login   # выбери Ollama, endpoint http://localhost:11434/v1
opencode
```

**goose**: имеет Ollama-провайдера, прямолинеен для local-agent экспериментов.

```bash
# Инструкции по установке: https://block.github.io/goose
goose configure       # выбери Ollama, model qwen2.5:3b
goose session start
```

**Aider**: git-native, полезен для мелких code-правок внутри репо.

```bash
pip install aider-chat
aider --model ollama/qwen2.5:3b --no-show-model-warnings
```

**Hermes Agent**: полезен на VPS, когда Telegram / Slack / Discord должен быть front door для агента.

```bash
curl -fsSL https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh | bash
hermes model set ollama:qwen2.5:3b
hermes
```

#### Шаг 3: Запусти одну реальную мелкую задачу (10 минут)

Не останавливайся на «hello world». Выбери задачу, касающуюся файлов, суммаризации, таблиц или поиска:

- Найди 5 PDF в `~/Downloads`, потом извлеки one-sentence summary и метод для каждой статьи.
- Прочитай первые 3 колонки `data.csv`, выведи Markdown-таблицу и отметь column issues.
- Поищи в `~/notes/` абзацы за последние 7 дней, упоминающие `agent safety`, потом сделай из них checklist.

Понаблюдай за тремя вещами:

- **Скорость**: мелкие локальные модели часто в 2–5 раз медленнее API-моделей.
- **Качество**: 3B / 7B модели обычно отстают от Claude по reasoning, длинному контексту и сложному коду.
- **Стоимость**: token cost = `$0`, но тратишь локальный RAM / VRAM и питание.

#### Шаг 4: Сравни с Claude Code (5 минут)

| Измерение | Claude Code | OpenCode + Ollama |
|---|---|---|
| LLM | Anthropic hosted | Локальная модель |
| Стоимость | Подписка или per-token | `$0` token cost |
| Скорость | Обычно стабильнее | Hardware-dependent, часто в 2–5 раз медленнее |
| Privacy | Контент уходит в Anthropic | Контент остаётся локально |
| Reasoning ceiling | Сильнее с Claude 4.5+ | Зависит от локальной модели |
| Лучший сценарий | Сложные кодовые базы, длинный контекст, надёжный reasoning | Приватные файлы, offline-демо, low-cost повторяющиеся эксперименты |

### Важное ограничение: Claude Code не может напрямую использовать локальный LLM

Claude Code на сейчас требует Anthropic OAuth / API-credential'ы и не имеет официальной настройки замены модели на Ollama или локальный endpoint. Можно увидеть эксперименты с proxy / API-shim онлайн, но это не официально поддерживаемый путь; стабильность и совместимость — на твоей стороне валидации.

Для локальной LLM-работы относись к «Claude Code» и «BYO-LLM CLI agents» как к раздельным инструментам: используй Claude Code, когда нужно качество Claude; используй OpenCode / goose / Aider / Hermes для локальных, offline, конфиденциальных или low-cost экспериментов.

### Распространённые ловушки

| Проблема | Причина | Фикс |
|---|---|---|
| `connection refused` | Ollama-сервер не запущен в фоне | Запусти `ollama serve` в другом терминале |
| Вывод модели фрагментарный или слабый | 3B-модель слишком мала | Попробуй `qwen2.5:7b` или `deepseek-r1:7b` |
| CLI agent не редактирует файлы | Локальная модель слишком слаба или промпт недо-уточнён | Сузь задачу, назови файлы, определи критерии успеха |
| Memory / OOM | Модель превышает RAM / VRAM | Стартуй с `qwen2.5:3b`, потом двигайся к 7B; включи swap при необходимости |

### Дальнейшее чтение

- Этап 1 [Local LLM упражнение](../stages/01-llm-basics.ru.md#упражнение-local-llm): trade-off'ы Ollama / llama.cpp / vLLM
- [`cli-agents-guide.ru.md`](cli-agents-guide.ru.md): как выбирать между 7 CLI agents
- README Hermes Agent: настройка multi-platform gateway для Telegram / Discord / Slack и провайдеров

---

## Не находишь нужный рецепт?

- См. [Этап 5](../stages/05-claude-code-ecosystem.ru.md) для полной концепции.
- См. [`mcp-skills-catalog.ru.md`](mcp-skills-catalog.ru.md) для comprehensive списка инструментов.
- См. [`schema-design-cheatsheet.ru.md`](schema-design-cheatsheet.ru.md) для деталей написания tool schemas.
- См. [`cli-agents-guide.ru.md`](cli-agents-guide.ru.md) для сравнения 7 популярных CLI agents.

Хочешь новый рецепт? Открой issue или сабмить PR. Формат рецепта: **Why + Steps + Sample Prompt + Common Pitfalls + Further Reading**.
