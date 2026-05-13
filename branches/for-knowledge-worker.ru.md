# Для knowledge workers — специализированная ветка

> [繁體中文](./for-knowledge-worker.md) | [简体中文](./for-knowledge-worker.zh-Hans.md) | [English](./for-knowledge-worker.en.md) | **Русский**

> 🚀 **Совсем без бэкграунда разработки?** Начни с [`resources/setup-guide.ru.md` §A-D](../resources/setup-guide.ru.md) (30–45 минут с нуля). Дальнейшие упоминания «Claude Code», «MCP» и «Skills» в этой ветке опираются на §D-настройку.

> [← Назад к README основного пути](../README.ru.md) · Сюда — после **A3 в Track A** или **этапа 7 в Track B**. Применять agentic AI к офисной / knowledge work.

## Use cases

- Email triage и черновики
- Meeting notes → action items
- Агрегация отчётов из нескольких источников
- Research / market intelligence
- Decision-support workflow'ы

## Подборка проектов

> 💡 **Хочешь подвязать свой AI agent к Notion / Gmail / Outlook / Slack / Excel / Lark?** 62 MCP server / Skill интеграции — в [`resources/mcp-skills-catalog.ru.md`](../resources/mcp-skills-catalog.ru.md) (сгруппированы по use case'ам). Раздел ниже сфокусирован на workflow / integration-platform инструментах.

### Workflow-инструменты

#### [n8n](https://github.com/n8n-io/n8n) ⭐⭐⭐⭐
Self-host-платформа автоматизации workflow со встроенной AI-интеграцией; визуальный node-based редактор.

**Лучше всего для**: когда нужен «клей» между множеством SaaS-инструментов (Slack + Gmail + Notion + AI).

---

#### [Make.com](https://www.make.com/) (бывший Integromat)
Hosted workflow automation. Сильные AI-интеграционные ноды.

---

### Skills для knowledge workers

#### [obra/superpowers](https://github.com/obra/superpowers) ⭐⭐⭐⭐

Skills для brainstorming, planning и принятия решений.

---

### Knowledge management / Personal AI

#### [khoj-ai/khoj](https://github.com/khoj-ai/khoj) ⭐⭐⭐⭐

| Поле | Значение |
|---|---|
| Stars | ★ 34k+ |
| License | AGPL-3.0 |

**Чему учит**: self-hosted «второй мозг» — чат с web + локальными доками, расписание автоматизаций, кастомные агенты.

**Лучше всего для**: тех, кто хочет self-hosted personal knowledge base + AI-ассистент.

**Заметки**: AGPL-3.0 (copyleft).

---

#### [lobehub/lobe-chat](https://github.com/lobehub/lobe-chat) ⭐⭐⭐⭐⭐

| Поле | Значение |
|---|---|
| Stars | ★ 76k+ |
| License | LobeHub Community License (Apache-2.0 база + commercial conditions) |

**Чему учит**: deployable multi-agent chat-платформа — plugin marketplace, knowledge bases, team collaboration. Один из представительных вариантов self-hosted AI workspace.

**Лучше всего для**: self-host'а коллаборативного chat workspace.

**Заметки**: для коммерческого использования нужно проверить дополнительные условия LobeHub Community License.

---

#### [langflow-ai/langflow](https://github.com/langflow-ai/langflow) ⭐⭐⭐⭐

| Поле | Значение |
|---|---|
| Stars | ★ 147k+ |
| License | MIT |

**Чему учит**: визуальная платформа разработки AI-agent — drag-and-drop дизайн agent-flow на нодах, со встроенным API + деплоем MCP-сервера. Более agent-сфокусированная, чем n8n (n8n — generic workflow).

**Лучше всего для**: knowledge worker'ов, которые предпочли бы соединять ноды, а не писать Python; или тех, кто проектирует agent-flow для передачи в команду.

---

#### [Mintplex-Labs/anything-llm](https://github.com/Mintplex-Labs/anything-llm) ⭐⭐⭐⭐⭐

| Поле | Значение |
|---|---|
| Stars | ★ 60k+ |
| License | MIT |

**Чему учит**: all-in-one приватный RAG workspace — заливай документы, строй агентов, MCP-совместимый, по дефолту on-device. **Self-hosted альтернатива NotebookLM**.

**Лучше всего для**: knowledge worker'ов, желающих инструмент в стиле NotebookLM, self-hosted, без отправки данных в облако.

---

### MCP-серверы, полезные knowledge worker'ам

#### Communication MCP-серверы ⭐⭐⭐⭐
Slack / Gmail / Discord и т. д. Оригинальные Anthropic-hosted reference серверы были реорганизованы в 2025; community-поддерживаемые серверы теперь живут в [**punkpeye/awesome-mcp-servers**](https://github.com/punkpeye/awesome-mcp-servers#communication) и [**wong2/awesome-mcp-servers**](https://github.com/wong2/awesome-mcp-servers). Листай эти списки за актуальными Slack / Gmail / Drive / Calendar MCP-серверами.

---

## Workflow'ы для сборки

- **Ежедневный email triage**: сканируй inbox → категоризируй → черновики ответов на ревью → mark read
- **Meeting → action items**: transcript → ключевые решения + action items → назначь + запости
- **Weekly report agregation**: подтяни метрики из N инструментов → синтезируй → email-сводка
- **Research / market intel**: вопрос → поиск по нескольким источникам → перекрёстная валидация → memo

## Tier-рекомендации

Большинству knowledge worker'ов стоит стартовать с **Tier 0** (Claude.ai web), апгрейдиться до **Tier 1** (Claude Desktop с MCP), когда нужны повторяющиеся workflow'ы над local/cloud файлами.

**Tier 3+ (CLI / SDK) — overkill для большинства задач knowledge worker'а.** Не дай себя уговорить.

## Чтение

- [How I Turned Claude Code Into My Personal AI Agent OS](https://aimaker.substack.com/p/how-i-turned-claude-code-into-personal-ai-agent-operating-system-for-writing-research-complete-guide) — кейс knowledge worker'а
