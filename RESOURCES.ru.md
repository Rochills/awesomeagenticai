# Связанные ресурсы

> [繁體中文](./RESOURCES.md) | [简体中文](./RESOURCES.zh-Hans.md) | [English](./RESOURCES.en.md) | **Русский**

> [← Назад к главному README](README.ru.md)

Этот файл собирает: определения терминов, подборка MCP/Skill для повседневных инструментов, тематические awesome-списки, ресурсы китайского сообщества. Вынесено из главного README, чтобы тот оставался сфокусированным.

> 💡 **Не знаешь термин?** (LLM, agent, RAG, token, vector DB, …) → [`resources/glossary.ru.md`](resources/glossary.ru.md) — 30+ распространённых терминов с определениями по 30–80 слов

---

## Три ключевых термина: MCP / Skills / Plugins

README и stages часто ссылаются на эти три термина экосистемы Claude Code. Быстрые определения:

- **MCP (Model Context Protocol)** — открытый протокол Anthropic, позволяющий любому LLM-хосту (Claude Code, другим IDE, твоему собственному agent'у) общаться с любым внешним tool server'ом (filesystem, DB, API, твой сервис) через один интерфейс. Думай «USB для LLM». См. [Этап 5.2](stages/05-claude-code-ecosystem.ru.md#52--mcp-model-context-protocol-foundation).
- **Skills** — «bundle'ы поведения» Claude Code. Skill — это `SKILL.md`, описывающий «в каком контексте делать что, какие MCP-tools можно вызывать». Claude Code авто-обнаруживает их. См. [Этап 5.3](stages/05-claude-code-ecosystem.ru.md#53--skills-claude-code-behavior-layer).
- **Plugins / Marketplaces** — пакуй Skills, slash commands, hooks и MCP-конфиги в distribution-единицу, устанавливаемую командой или сообществом. Marketplace — каталог плагинов. См. [Этап 5.4](stages/05-claude-code-ecosystem.ru.md#54--plugins--marketplaces).

Практические упражнения живут в [Этапе 5](stages/05-claude-code-ecosystem.ru.md), [A3 в Track A](tracks/cli/A3-cli-production.ru.md) покрывает production-интеграцию.

---

## Интеграции с повседневными инструментами: MCP servers + Skills

Подключи Claude Code (или любой другой CLI agent) к приложениям, которыми уже пользуешься, без прыжков по окнам. Зрелые выборы ниже:

### Заметки / Knowledge Base

- [**MarkusPfundstein/mcp-obsidian**](https://github.com/MarkusPfundstein/mcp-obsidian) ★ 3.5k+ — Obsidian REST API plugin, позволяет LLM читать/писать в твоём vault
- [**makenotion/notion-mcp-server**](https://github.com/makenotion/notion-mcp-server) ★ 4k+ — Notion **официальный** MCP, query/create страниц, манипуляция databases
- [**PleasePrompto/notebooklm-skill**](https://github.com/PleasePrompto/notebooklm-skill) ★ 6k+ — NotebookLM Skill, citation-backed ответы из твоих загруженных доков
- [**teng-lin/notebooklm-py**](https://github.com/teng-lin/notebooklm-py) ★ 12k+ — неофициальный NotebookLM Python API + CLI, хорошо играет с Claude Code / Codex

### Office Documents (Word / Excel / PowerPoint / PDF)

- [**anthropics/skills**](https://github.com/anthropics/skills) ★ 129k+ — **официальные** Anthropic Skills со встроенной обработкой docx / xlsx / pptx / pdf
- [**tfriedel/claude-office-skills**](https://github.com/tfriedel/claude-office-skills) ★ 580+ — Office skills с automation-workflow'ами поверх официальных

### Google Workspace (Gmail / Docs / Drive / Calendar)

- [**taylorwilsdon/google_workspace_mcp**](https://github.com/taylorwilsdon/google_workspace_mcp) ★ 2.3k+ — полный Workspace-стек (Gmail, Calendar, Docs, Sheets, Slides, Drive) в одном сервере

### Dev Collaboration

- [**github/github-mcp-server**](https://github.com/github/github-mcp-server) ★ 29k+ — GitHub **официальный** MCP для issues / PRs / repos
- [**atlassian/atlassian-mcp-server**](https://github.com/atlassian/atlassian-mcp-server) ★ 650+ — Atlassian **официальный** Remote MCP (Jira, Confluence)
- [**jerhadf/linear-mcp-server**](https://github.com/jerhadf/linear-mcp-server) ★ 340+ — Linear MCP
- [**korotovsky/slack-mcp-server**](https://github.com/korotovsky/slack-mcp-server) ★ 1.5k+ — Slack MCP, работает без admin-permissions

### Research Workflow (от мейнтейнера репо)

- [**WenyuChiou/ai-research-skills**](https://github.com/WenyuChiou/ai-research-skills) ★ 60 — 14 research-workflow skills как 5-plugin marketplace
- [**WenyuChiou/research-hub**](https://github.com/WenyuChiou/research-hub) ★ 14 — Zotero + Obsidian + NotebookLM интеграционный workspace
- [**WenyuChiou/zotero-skills**](https://github.com/WenyuChiou/zotero-skills) ★ 16 — Zotero CLI skill
- [**WenyuChiou/codex-delegate**](https://github.com/WenyuChiou/codex-delegate) ★ 57 + [**gemini-delegate-skill**](https://github.com/WenyuChiou/gemini-delegate-skill) ★ 34 — multi-LLM делегационная пара

### Китайская экосистема

- [**leemysw/feishu-docx**](https://github.com/leemysw/feishu-docx) ★ 190+ — Feishu (Lark) docs / sheet / bitable ↔ Markdown с поддержкой Claude Skills

> Выше только highlights. **Полный каталог из 62 записей по категориям** (включая базы данных, browser automation, Figma, Excalidraw, Cloudflare, Stripe, academic-writing / multi-LLM delegation и т. д.) живёт в [`resources/mcp-skills-catalog.ru.md`](resources/mcp-skills-catalog.ru.md).

> Ищешь ещё каталоги MCP-серверов? См. [`wong2/awesome-mcp-servers`](https://github.com/wong2/awesome-mcp-servers) / [`punkpeye/awesome-mcp-servers`](https://github.com/punkpeye/awesome-mcp-servers) (категоризированы). Официальный MCP **Canva** ещё в early access — community-версии нестабильны; добавим, когда стабилизируется.

---

## Тематические awesome-списки

Этот репо **не заменяет** плоские awesome-списки. Если уже знаешь, какой инструмент нужен — эти более прямые:

### MCP-related

- [**modelcontextprotocol/servers**](https://github.com/modelcontextprotocol/servers) — официальные reference servers (filesystem, github, sqlite, git, fetch, memory, …)
- [**wong2/awesome-mcp-servers**](https://github.com/wong2/awesome-mcp-servers) — community MCP server каталог, по категориям (150+)
- [**punkpeye/awesome-mcp-servers**](https://github.com/punkpeye/awesome-mcp-servers) — ещё один каталог MCP-серверов

### Claude Code / Skills / Plugins-related

- [**hesreallyhim/awesome-claude-code**](https://github.com/hesreallyhim/awesome-claude-code) — Claude Code ресурсы (сейчас перестраивается)
- [**travisvn/awesome-claude-skills**](https://github.com/travisvn/awesome-claude-skills) — каталог Claude Skills
- [**anthropics/claude-plugins-official**](https://github.com/anthropics/claude-plugins-official) — официальный plugin marketplace template Anthropic; стартуй отсюда при упаковке своего plugin

### Китайскоязычное сообщество

- [**datawhalechina/hello-agents**](https://github.com/datawhalechina/hello-agents) — систематический agent-туториал Datawhale (zh-Hans)
- [**WangRongsheng/awesome-LLM-resources**](https://github.com/WangRongsheng/awesome-LLM-resources) — comprehensive zh-Hans LLM ресурсы (8k+ stars)
- [**AiHubCN/Awesome-Chinese-LLM**](https://github.com/AiHubCN/Awesome-Chinese-LLM) — каталог open-source китайских LLM

---

## Что ещё?

- Главный README: [README.ru.md](README.ru.md)
- Полный каталог MCP / Skill: [resources/mcp-skills-catalog.ru.md](resources/mcp-skills-catalog.ru.md)
- Руководство по сравнению CLI agent: [resources/cli-agents-guide.ru.md](resources/cli-agents-guide.ru.md)
- Style guide / contributing: [resources/style-guide.ru.md](resources/style-guide.ru.md), [CONTRIBUTING.md](CONTRIBUTING.md)
