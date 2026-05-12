# Индекс `resources/`

<div align="right">
  <a href="./README.md">繁體中文</a> | <a href="./README.zh-Hans.md">简体中文</a> | <a href="./README.en.md">English</a> | <strong>Русский</strong>
</div>

> Это **reference area** репо: вспомогательный материал, лежащий вне основного пути и предназначенный открываться по необходимости. У каждого файла своя отдельная роль.

---

## 7 референсов + когда их читать

| Файл | Роль | Когда читать | Строки |
|---|---|---|---|
| [`glossary.ru.md`](glossary.ru.md) | **30-секундное определение термина** | Натыкаешься на термины вроде LLM / RAG / token / agent / vector DB / streaming / batch API при чтении этапа | ~210 |
| [`cli-agents-guide.ru.md`](cli-agents-guide.ru.md) | **7 CLI agents в сравнении** | Первый раз выбираешь между Claude Code / Codex / OpenCode / Gemini CLI / goose / Aider / Hermes Agent | ~134 |
| [`mcp-skills-catalog.ru.md`](mcp-skills-catalog.ru.md) | **Каталог 62 интеграций** | Хочешь подключить Claude Code к Notion / Obsidian / Excel / Postgres / Slack / другим реальным инструментам | ~775 |
| [`schema-design-cheatsheet.ru.md`](schema-design-cheatsheet.ru.md) | **5 правил function-schema + 5 анти-паттернов** | Пишешь tool schema / MCP server schema / function calling, а LLM выбирает не тот tool или не те аргументы | ~159 |
| [`cookbook.ru.md`](cookbook.ru.md) | **6 пошаговых рецептов** | Хочешь построить первый Skill / MCP server / Office-интеграцию / NotebookLM-flow / Zotero-flow / локальный LLM за 30–50 минут | ~620 |
| [`setup-guide.ru.md`](setup-guide.ru.md) | **Setup guide с нуля** | Без бэкграунда разработки; первый раз делаешь API-ключ, ставишь Python или используешь Claude Code | ~400 |
| [`style-guide.ru.md`](style-guide.ru.md) | **Правила формата и формулировок перед PR** | Хочешь контрибьютить в репо, добавлять записи или улучшать переводы | ~338 |

Вместе это ~2500 строк референса. Звучит много, но **каждый файл читается в своё время**. Не читай всё сразу — открывай нужный на 30 секунд — 45 минут.

---

## Entry points: «Что я пытаюсь сделать?»

### 🆕 Никогда не писал код / первый раз настраиваю AI agent

→ [`setup-guide.ru.md`](setup-guide.ru.md) (30–45 минут с нуля)

### 🆕 Только начинаю учить AI agents

Никакой референс сначала не нужен. **Стартуй с главного [README](../README.ru.md) → [Этап 0](../stages/00-foundations.ru.md)**. Когда термин неясен — вернись к [`glossary.ru.md`](glossary.ru.md).

### 🛠 Нужно выбрать CLI agent

→ [`cli-agents-guide.ru.md`](cli-agents-guide.ru.md) (CLI-сравнение + рекомендации по use case'ам)

### 🔌 Хочу подключить Claude Code к tool X (Notion / Excel / Postgres / и т. д.)

→ [`mcp-skills-catalog.ru.md`](mcp-skills-catalog.ru.md) (62 интеграции в 14 категориях)

### 🍳 Хочу построить первый Skill / MCP server / Word-интеграцию

→ [`cookbook.ru.md`](cookbook.ru.md) (6 пошаговых рецептов)

### 📐 Написал tool schema, а LLM ей не следует

→ [`schema-design-cheatsheet.ru.md`](schema-design-cheatsheet.ru.md) (5 правил + 5 анти-паттернов)

### 📚 Наткнулся на неясный термин в этапе

→ [`glossary.ru.md`](glossary.ru.md) (30–80 слов на термин + указание этапа для углубления)

### 🤝 Хочу отправить PR / перевести / добавить новую запись

→ [`style-guide.ru.md`](style-guide.ru.md) + [`../CONTRIBUTING.md`](../CONTRIBUTING.md)

---

## Дубликация?

Дубликация намеренна только там, где помогает навигации. Роли остаются раздельными:

- **glossary** — 30-секундный lookup, текст этапа — 3–5-минутное чтение, cookbook — 30–50-минутная сборка.
- **schema-design-cheatsheet** пересекается с cookbook §2, но cheatsheet объясняет правила schema, а cookbook поднимает сервер.
- **cli-agents-guide** — comparison reference; **mcp-skills-catalog** — каталог tool-интеграций.
- **setup-guide** — для людей с нуля; этап 0 предполагает готовность следовать learning path.

---

## Покрытие языков

| Файл | zh-TW (canonical) | zh-Hans | English | Русский |
|---|---|---|---|---|
| glossary | ✅ | ✅ | ✅ | ✅ |
| cli-agents-guide | ✅ | ✅ | ✅ | ✅ |
| mcp-skills-catalog | ✅ | ✅ | ✅ | ✅ |
| schema-design-cheatsheet | ✅ | ✅ | ✅ | ✅ |
| cookbook | ✅ | ✅ | ✅ | ✅ |
| setup-guide | ✅ | ✅ | ✅ | ✅ |
| style-guide | ✅ | ✅ | ✅ | ✅ |

---

## Стандарты добавления нового референса

Новый reference-файл не должен добавляться легко. Он должен:

1. **Не дублировать существующую роль** из таблицы выше.
2. **Решать проблему, которую основной путь не покрывает хорошо**. Если 50 строк в этапе X покроют — клади в этот этап.
3. **Ожидать 3+ cross-references** из этапов или веток. Если служит только одному этапу — оставь в этом этапе.

Возможные будущие референсы:

- `cost-calculator-guide.md`: cross-provider pricing. Этап 1 пока покрывает достаточно.
- `troubleshooting-guide.md`: common error runbook. Существующего материала хватает, пока не прибудет больше community-репортов.
- `prompt-patterns-guide.md`: CoT / few-shot template library. Этап 2 уже покрывает основы; более глубокая версия может подождать community PR'ов.
