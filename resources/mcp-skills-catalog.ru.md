# MCP / Skills Integration Catalog

> [繁體中文](./mcp-skills-catalog.md) | [简体中文](./mcp-skills-catalog.zh-Hans.md) | [English](./mcp-skills-catalog.en.md) | **Русский**

> Подключи Claude Code (или любой другой CLI agent) к приложениям, которыми уже пользуешься, без прыжков между окнами. Эта страница — курируемый индекс 62 MCP-серверов / Claude Skills / интеграций, сгруппированных по сценариям (включая research-workflow + multi-LLM-делегирование выделенные секции).

---

## Как пользоваться каталогом

- **Ищешь MCP конкретного инструмента**: прыгай в соответствующую секцию ниже
- **Хочешь знать, что такое MCP / Skills / Plugins**: сначала см. [README «Три ключевых термина»](../README.ru.md#три-ключевых-термина-mcp--skills--plugins), потом [Этап 5 — Claude Code Ecosystem](../stages/05-claude-code-ecosystem.ru.md)
- **Хочешь практические упражнения (install + test)**: см. [Этап 5.2 (MCP)](../stages/05-claude-code-ecosystem.ru.md#52--mcp-model-context-protocol-foundation) и [Этап 5.3 (Skills)](../stages/05-claude-code-ecosystem.ru.md#53--skills-claude-code-behavior-layer)

### Направление включения (не строгие правила)

- **Сначала официальное**: Anthropic / vendor-publish'нутые MCP / Skill обычно ранжируются выше
- **Stars — сигнал, не фильтр**: community-репо около 100+ обычно поддерживаются, но «niche but useful» репо принимаются через PR с фразой о причине
- **Метаданные, где возможно**: stars / license подтягиваются через `gh api`; refresh когда угодно
- **Избегать (не запрещено)**: archived, long-stale, unclear-license репо — niche-инструменты могут быть исключениями

### Индекс

1. [Заметки / Knowledge Base](#1-notes--knowledge-base) (7)
2. [Office Documents (Word / Excel / PowerPoint / PDF)](#2-office-documents-word--excel--powerpoint--pdf) (6)
3. [Google Workspace](#3-google-workspace) (2)
4. [Microsoft 365](#4-microsoft-365) (3)
5. [Dev Collaboration (GitHub / Atlassian / Slack…)](#5-dev-collaboration-github--atlassian--slack) (6)
6. [Databases](#6-databases) (7)
7. [Browser Automation / Web Scraping](#7-browser-automation--web-scraping) (4)
8. [Design (Figma / Excalidraw)](#8-design-figma--excalidraw) (3)
9. [Monitoring / Observability](#9-monitoring--observability) (3)
10. [Media / Streaming (YouTube / Spotify)](#10-media--streaming-youtube--spotify) (3)
11. [Китайская экосистема](#11-chinese-language-ecosystem) (7)
12. [Прочее распространённое (Cloudflare / Stripe…)](#12-other-common-cloudflare--stripe) (2)
13. [Research Workflow Skills](#13-research-workflow-skills-academic--paper--lit) (4)
14. [Multi-LLM Delegation Skills](#14-multi-llm-delegation-skills) (3)

---

## 1. Notes / Knowledge Base

### [makenotion/notion-mcp-server](https://github.com/makenotion/notion-mcp-server) ⭐⭐⭐⭐⭐

| Поле | Значение |
|---|---|
| Stars | ★ 4k+ |
| License | NOASSERTION |
| Rating | ⭐⭐⭐⭐⭐ (**официальный**) |

**Что делает**: официальный MCP-сервер Notion — query страниц, создание страниц, манипуляция databases.
**Аудитория**: heavy-пользователи Notion для note-taking / project management / wikis — пусть LLM подтягивает данные и пишет страницы напрямую.
**Заметки**: требует Notion integration token; поддерживает read-only и read-write режимы.

### [MarkusPfundstein/mcp-obsidian](https://github.com/MarkusPfundstein/mcp-obsidian) ⭐⭐⭐⭐

| Поле | Значение |
|---|---|
| Stars | ★ 3.5k+ |
| License | MIT |
| Rating | ⭐⭐⭐⭐ (community, самый популярный) |

**Что делает**: read/write твоего Obsidian vault через Obsidian REST API community plugin.
**Аудитория**: heavy-пользователи Obsidian, желающие Claude Code для организации ежедневных заметок, auto-link, поиска между файлами.
**Заметки**: требует [Local REST API](https://github.com/coddingtonbear/obsidian-local-rest-api) плагин в Obsidian.

### [PleasePrompto/notebooklm-skill](https://github.com/PleasePrompto/notebooklm-skill) ⭐⭐⭐⭐

| Поле | Значение |
|---|---|
| Stars | ★ 6k+ |
| License | NOASSERTION |
| Rating | ⭐⭐⭐⭐ |

**Что делает**: Claude Code Skill, использующий browser automation для query'ев в NotebookLM с citation-backed ответами.
**Аудитория**: люди, управляющие статьями / research-заметками в NotebookLM, желающие запрашивать из Claude Code одним промптом.
**Заметки**: требует аутентификации через Google account.

### [teng-lin/notebooklm-py](https://github.com/teng-lin/notebooklm-py) ⭐⭐⭐⭐

| Поле | Значение |
|---|---|
| Stars | ★ 12k+ |
| License | NOASSERTION |
| Rating | ⭐⭐⭐⭐ |

**Что делает**: неофициальный NotebookLM Python API + CLI + agentic skill; шире по фичам, чем skill выше, включая возможности, не выставленные в web UI.
**Аудитория**: люди, делающие программные / batch-операции над NotebookLM (авто-создание notebook'ов, bulk-импорт документов).
**Заметки**: неофициальный; может ломаться с изменениями Google policy — проверяй issue tracker.

### [ergut/mcp-logseq](https://github.com/ergut/mcp-logseq) ⭐⭐⭐

| Поле | Значение |
|---|---|
| Stars | ★ 264 |
| License | MIT |
| Rating | ⭐⭐⭐ |

**Что делает**: read/write Logseq graph через Logseq Local HTTP API.
**Аудитория**: пользователи Logseq, автоматизирующие daily journals, cross-page links, backlink queries.
**Заметки**: включи HTTP API Logseq (Settings → Features → HTTP API).

### [skridlevsky/graphthulhu](https://github.com/skridlevsky/graphthulhu) ⭐⭐⭐

| Поле | Значение |
|---|---|
| Stars | ★ 147 |
| License | MIT |
| Rating | ⭐⭐⭐ (покрывает и Logseq + Obsidian) |

**Что делает**: 39 tools — навигация, поиск, анализ, написание, journals, flashcards, whiteboards.
**Аудитория**: люди, использующие и Logseq, и Obsidian, не желающие два MCP-сервера.
**Заметки**: community-проект; широкая tool-поверхность, но каждый tool относительно базовый.

### [ankimcp/anki-mcp-server](https://github.com/ankimcp/anki-mcp-server) ⭐⭐⭐

| Поле | Значение |
|---|---|
| Stars | ★ 254 |
| License | MIT |
| Rating | ⭐⭐⭐ |

**Что делает**: create / query / batch-edit Anki decks через AnkiConnect.
**Аудитория**: люди, использующие Anki для языков / медицины / права — пусть LLM авто-генерирует карточки из учебного материала.
**Заметки**: требует Anki Desktop + аддон [AnkiConnect](https://ankiweb.net/shared/info/2055492159).

---

## 2. Office Documents (Word / Excel / PowerPoint / PDF)

### [anthropics/skills](https://github.com/anthropics/skills) ⭐⭐⭐⭐⭐

| Поле | Значение |
|---|---|
| Stars | ★ 129k+ |
| License | NOASSERTION |
| Rating | ⭐⭐⭐⭐⭐ (**официально**, must-install) |

**Что делает**: официальный Agent Skills репо Anthropic — включает docx / xlsx / pptx / pdf processing skills.
**Аудитория**: каждый пользователь Claude Code — `claude skill install`, и Claude может читать/писать Office-файлы напрямую.
**Заметки**: это коллекция Skills, не MCP; живёт в Skills-системе Stage 5.3.

### [haris-musa/excel-mcp-server](https://github.com/haris-musa/excel-mcp-server) ⭐⭐⭐⭐⭐

| Поле | Значение |
|---|---|
| Stars | ★ 3.8k+ |
| License | MIT |
| Rating | ⭐⭐⭐⭐⭐ (самый популярный community Excel MCP) |

**Что делает**: манипуляция Excel-файлами через MCP — read / write / modify ячеек, формул, sheets.
**Аудитория**: люди, работающие с Excel-отчётами ежедневно, желающие LLM-driven data filling и cleanup.
**Заметки**: Python-based, зависит от openpyxl.

### [GongRzhe/Office-PowerPoint-MCP-Server](https://github.com/GongRzhe/Office-PowerPoint-MCP-Server) ⭐⭐⭐⭐

| Поле | Значение |
|---|---|
| Stars | ★ 1.7k+ |
| License | MIT |
| Rating | ⭐⭐⭐⭐ |

**Что делает**: манипуляция PPT через python-pptx — создание decks, правка слайдов, вставка изображений, смена layouts.
**Аудитория**: люди, желающие, чтобы LLM авто-генерировал deck'и из outline / Markdown (консультанты, лекторы, студенты).
**Заметки**: пересекается с pptx skill из `anthropics/skills`; используй, когда официального не хватает.

### [SylphxAI/pdf-reader-mcp](https://github.com/SylphxAI/pdf-reader-mcp) ⭐⭐⭐⭐

| Поле | Значение |
|---|---|
| Stars | ★ 688 |
| License | MIT |
| Rating | ⭐⭐⭐⭐ (high-throughput PDF) |

**Что делает**: высокоскоростной PDF-парсер MCP, ~5–10× быстрее pdf skill из `anthropics/skills` (по их заявлению).
**Аудитория**: люди, делающие batch-чтение статей / контрактов / отчётов.
**Заметки**: параллельная обработка; заметно на больших PDF.

### [tfriedel/claude-office-skills](https://github.com/tfriedel/claude-office-skills) ⭐⭐⭐

| Поле | Значение |
|---|---|
| Stars | ★ 590 |
| License | NOASSERTION |
| Rating | ⭐⭐⭐ (Office skill add-on) |

**Что делает**: расширяет `anthropics/skills` Office workflow'ами, которые тот не покрывает (автоматизация, advanced formatting).
**Аудитория**: люди, считающие официальные docx/xlsx/pptx skills слишком coarse-grained.
**Заметки**: дополняет `anthropics/skills`, не заменяет.

### [kreuzberg-dev/kreuzberg](https://github.com/kreuzberg-dev/kreuzberg) ⭐⭐⭐⭐

| Поле | Значение |
|---|---|
| Stars | ★ 8.2k+ |
| License | NOASSERTION |
| Rating | ⭐⭐⭐⭐ |

**Что делает**: фреймворк парсинга 97+ форматов документов, Rust-ядро. Даёт MCP server + REST API + CLI.
**Аудитория**: инженеры cross-format batch-парсинга, заботящиеся о throughput.
**Заметки**: покрывает экзотические форматы вроде HWP, ODT и т. д., не только PDF / Office.

---

## 3. Google Workspace

### [taylorwilsdon/google_workspace_mcp](https://github.com/taylorwilsdon/google_workspace_mcp) ⭐⭐⭐⭐⭐

| Поле | Значение |
|---|---|
| Stars | ★ 2.3k+ |
| License | MIT |
| Rating | ⭐⭐⭐⭐⭐ (один сервер, всё Google) |

**Что делает**: Gmail, Calendar, Docs, Sheets, Slides, Drive, Chat, Forms, Tasks, Search — всё в одном MCP-сервере.
**Аудитория**: heavy-пользователи Google Workspace — ответы на email, scheduling, написание docs, манипуляция sheets — всё из одного сервера.
**Заметки**: OAuth-настройка чуть запутана, но делается один раз; самое полное покрытие Google-инструментов.

### [xing5/mcp-google-sheets](https://github.com/xing5/mcp-google-sheets) ⭐⭐⭐⭐

| Поле | Значение |
|---|---|
| Stars | ★ 844 |
| License | MIT |
| Rating | ⭐⭐⭐⭐ (только Sheets) |

**Что делает**: сфокусированная Google Sheets / Drive интеграция — создание sheets, правка ячеек, query формул.
**Аудитория**: люди, использующие только Google Sheets, не желающие full Workspace MCP.
**Заметки**: уже по scope, чем `google_workspace_mcp`, но проще в настройке.

---

## 4. Microsoft 365

### [Softeria/ms-365-mcp-server](https://github.com/Softeria/ms-365-mcp-server) ⭐⭐⭐⭐

| Поле | Значение |
|---|---|
| Stars | ★ 681 |
| License | MIT |
| Rating | ⭐⭐⭐⭐ (full M365) |

**Что делает**: M365 + Office сервисы через Microsoft Graph API — Outlook, Teams, OneDrive, SharePoint.
**Аудитория**: enterprise M365-пользователи, желающие LLM-driven ответы на email, calendar lookups, OneDrive-операции.
**Заметки**: требует Azure AD app registration; корпоративные IT-policies могут блокировать.

### [ryaker/outlook-mcp](https://github.com/ryaker/outlook-mcp) ⭐⭐⭐

| Поле | Значение |
|---|---|
| Stars | ★ 363 |
| License | NOASSERTION |
| Rating | ⭐⭐⭐ (только Outlook) |

**Что делает**: Outlook mail / calendar через Graph API.
**Аудитория**: люди, которым нужен только Outlook, не остальное из M365.
**Заметки**: уже scope, чем `ms-365-mcp-server`.

### [merill/lokka](https://github.com/merill/lokka) ⭐⭐⭐

| Поле | Значение |
|---|---|
| Stars | ★ 244 |
| License | MIT |
| Rating | ⭐⭐⭐ |

**Что делает**: M365 + Microsoft Graph admin-операции — Entra (AD), Intune и т. д.
**Аудитория**: M365 system admins, управляющие tenants / users / policies.
**Заметки**: полезнее IT-админам, чем end-юзерам.

---

## 5. Dev Collaboration (GitHub / Atlassian / Slack…)

### [github/github-mcp-server](https://github.com/github/github-mcp-server) ⭐⭐⭐⭐⭐

| Поле | Значение |
|---|---|
| Stars | ★ 29.5k+ |
| License | MIT |
| Rating | ⭐⭐⭐⭐⭐ (**официальный**) |

**Что делает**: официальный GitHub MCP — issues / PRs / repos / Actions / Codespaces.
**Аудитория**: каждый пользователь GitHub; как только Claude Code подвязан, PR review, issue triage, release notes — всё работает.
**Заметки**: **must-install для Упражнения CLI-9 в Track A A3**.

### [sooperset/mcp-atlassian](https://github.com/sooperset/mcp-atlassian) ⭐⭐⭐⭐⭐

| Поле | Значение |
|---|---|
| Stars | ★ 5.1k+ |
| License | MIT |
| Rating | ⭐⭐⭐⭐⭐ (самый популярный community Atlassian) |

**Что делает**: Confluence + Jira в одном MCP, гибче официального remote.
**Аудитория**: пользователи Atlassian, считающие официальный remote-сервер слишком ограничительным.
**Заметки**: выбирай этот ИЛИ `atlassian/atlassian-mcp-server` (официальный) в зависимости от IT-policy.

### [atlassian/atlassian-mcp-server](https://github.com/atlassian/atlassian-mcp-server) ⭐⭐⭐⭐

| Поле | Значение |
|---|---|
| Stars | ★ 650+ |
| License | Apache-2.0 |
| Rating | ⭐⭐⭐⭐ (**официальный**) |

**Что делает**: официальный Remote MCP Atlassian, безопасное подключение к Jira / Confluence.
**Аудитория**: компании с enterprise Atlassian + IT-policies, требующими официальный tooling.
**Заметки**: remote-модель с официальным SLA.

### [korotovsky/slack-mcp-server](https://github.com/korotovsky/slack-mcp-server) ⭐⭐⭐⭐

| Поле | Значение |
|---|---|
| Stars | ★ 1.6k+ |
| License | MIT |
| Rating | ⭐⭐⭐⭐ (не нужны admin permissions) |

**Что делает**: Slack MCP — DM, group DM, channel messages, со встроенной логикой history fetch.
**Аудитория**: individual-пользователи (не Slack admin'ы), желающие LLM-Slack интеграцию.
**Заметки**: не нужны admin tokens; использует user-level OAuth.

### [jerhadf/linear-mcp-server](https://github.com/jerhadf/linear-mcp-server) ⭐⭐⭐⭐

| Поле | Значение |
|---|---|
| Stars | ★ 344 |
| License | NOASSERTION |
| Rating | ⭐⭐⭐⭐ |

**Что делает**: Linear (issue tracker) MCP — query issues, создание issues, смена статуса.
**Аудитория**: разработчики, управляющие sprints / backlogs в Linear.
**Заметки**: требует Linear API key.

### [SaseQ/discord-mcp](https://github.com/SaseQ/discord-mcp) ⭐⭐⭐

| Поле | Значение |
|---|---|
| Stars | ★ 298 |
| License | MIT |
| Rating | ⭐⭐⭐ |

**Что делает**: Discord MCP — read/write channel-сообщений, управление серверами.
**Аудитория**: мейнтейнеры, ведущие OSS / community Discord-серверы.
**Заметки**: требует Discord bot token; следи за rate limits.

### [safishamsi/graphify](https://github.com/safishamsi/graphify) ⭐⭐⭐⭐⭐

| Поле | Значение |
|---|---|
| Stars | ★ 44k+ |
| License | MIT |
| Rating | ⭐⭐⭐⭐⭐ |

**Что делает**: AI coding skill, превращающий кодовые базы / SQL schemas / R scripts / shell-скрипты / доки / статьи / изображения / видео в queryable knowledge graph. Работает в Claude Code, Codex, OpenCode, Cursor, Gemini CLI.
**Аудитория**: инженеры / исследователи, анализирующие большие кодовые базы, трекинг cross-file ссылок или вопросы по «app code + DB schema + infra» вместе.
**Заметки**: cross-cutting инструмент — подходит и для dev collaboration (понимание существующих кодовых баз), и для research workflow (превращение любого артефакта в граф). Застрял на большой кодовой базе — используй graphify для извлечения структуры, потом отдай Claude'у для reasoning'а.

---

## 6. Databases

### [googleapis/mcp-toolbox](https://github.com/googleapis/mcp-toolbox) ⭐⭐⭐⭐⭐

| Поле | Значение |
|---|---|
| Stars | ★ 15k+ |
| License | Apache-2.0 |
| Rating | ⭐⭐⭐⭐⭐ (**Google официально**, multi-DB) |

**Что делает**: cross-DB MCP-сервер — MySQL / PostgreSQL / Cloud SQL / Spanner / BigQuery.
**Аудитория**: инженеры, гоняющие БД на Google Cloud, или всем, кому нужна multi-engine поддержка.
**Заметки**: open-source + Google-поддерживаемый; production-grade выбор.

### [bytebase/dbhub](https://github.com/bytebase/dbhub) ⭐⭐⭐⭐⭐

| Поле | Значение |
|---|---|
| Stars | ★ 2.7k+ |
| License | MIT |
| Rating | ⭐⭐⭐⭐⭐ (community multi-DB) |

**Что делает**: zero-dependency, token-efficient multi-DB MCP — Postgres, MySQL, SQL Server, MariaDB, SQLite.
**Аудитория**: инженеры, не желающие Google Cloud SDK и нуждающиеся в cross-OSS-DB поддержке.
**Заметки**: пересекается с `googleapis/mcp-toolbox`, но легче.

### [supabase-community/supabase-mcp](https://github.com/supabase-community/supabase-mcp) ⭐⭐⭐⭐⭐

| Поле | Значение |
|---|---|
| Stars | ★ 2.7k+ |
| License | Apache-2.0 |
| Rating | ⭐⭐⭐⭐⭐ (**Supabase official-community**) |

**Что делает**: подключение Supabase (Postgres, Auth, Storage, Edge Functions) к LLM.
**Аудитория**: full-stack разработчики, использующие Supabase как backend.
**Заметки**: официально community-поддерживаемый.

### [timescale/pg-aiguide](https://github.com/timescale/pg-aiguide) ⭐⭐⭐⭐

| Поле | Значение |
|---|---|
| Stars | ★ 1.7k+ |
| License | Apache-2.0 |
| Rating | ⭐⭐⭐⭐ (Postgres coding aid) |

**Что делает**: MCP-сервер + Claude-плагин, помогающий LLM писать лучший PostgreSQL код.
**Аудитория**: Postgres-heavy SQL-писатели / DBA.
**Заметки**: сфокусирован на «LLM пишет лучший SQL», не просто query execution.

### [benborla/mcp-server-mysql](https://github.com/benborla/mcp-server-mysql) ⭐⭐⭐⭐

| Поле | Значение |
|---|---|
| Stars | ★ 1.6k+ |
| License | MIT |
| Rating | ⭐⭐⭐⭐ (read-only MySQL) |

**Что делает**: read-only MySQL MCP — пусть LLM видит schemas, гоняет запросы.
**Аудитория**: сценарии, где LLM должен анализировать production-БД, но никогда не модифицировать.
**Заметки**: read-only — это safety-фича, не ограничение.

### [mongodb-js/mongodb-mcp-server](https://github.com/mongodb-js/mongodb-mcp-server) ⭐⭐⭐⭐

| Поле | Значение |
|---|---|
| Stars | ★ 1k+ |
| License | Apache-2.0 |
| Rating | ⭐⭐⭐⭐ (**MongoDB официально**) |

**Что делает**: MCP-сервер для MongoDB и MongoDB Atlas Cluster.
**Аудитория**: инженеры, использующие MongoDB / Atlas.
**Заметки**: `mongodb-js` — официальная GitHub-org MongoDB.

### [redis/mcp-redis](https://github.com/redis/mcp-redis) ⭐⭐⭐⭐

| Поле | Значение |
|---|---|
| Stars | ★ 504 |
| License | MIT |
| Rating | ⭐⭐⭐⭐ (**Redis официально**) |

**Что делает**: официальный Redis MCP — natural-language операции над Redis и Redis Stack (Vector / Search / JSON).
**Аудитория**: люди, использующие Redis как cache / vector DB / queue.
**Заметки**: официально поддерживается; включает vector search.

---

## 7. Browser Automation / Web Scraping

### [microsoft/playwright-mcp](https://github.com/microsoft/playwright-mcp) ⭐⭐⭐⭐⭐

| Поле | Значение |
|---|---|
| Stars | ★ 32k+ |
| License | Apache-2.0 |
| Rating | ⭐⭐⭐⭐⭐ (**Microsoft официально**) |

**Что делает**: Playwright MCP-сервер — пусть LLM открывает браузеры, кликает кнопки, заполняет формы, скрейпит страницы.
**Аудитория**: всем, делающим E2E-автоматизацию, cross-site интеграцию, скрейпинг за логином.
**Заметки**: официальный Playwright; самый надёжный. **Первый выбор для Claude Code + web-автоматизация**.

### [ChromeDevTools/chrome-devtools-mcp](https://github.com/ChromeDevTools/chrome-devtools-mcp) ⭐⭐⭐⭐⭐

| Поле | Значение |
|---|---|
| Stars | ★ 38k+ |
| License | Apache-2.0 |
| Rating | ⭐⭐⭐⭐⭐ (**Chrome официально**) |

**Что делает**: выставляет Chrome DevTools coding-агентам — performance, network, console traces — всё доступно LLM.
**Аудитория**: разработчики, дебажащие фронтенд-баги, делающие web performance-анализ.
**Заметки**: хорошо работает в паре с Playwright MCP — один управляет браузером, другой наблюдает.

### [firecrawl/firecrawl-mcp-server](https://github.com/firecrawl/firecrawl-mcp-server) ⭐⭐⭐⭐⭐

| Поле | Значение |
|---|---|
| Stars | ★ 6.2k+ |
| License | MIT |
| Rating | ⭐⭐⭐⭐⭐ (**Firecrawl официально**) |

**Что делает**: официальный MCP Firecrawl — large-scale web-скрейпинг + поиск + structured extraction.
**Аудитория**: люди, скрейпящие большие объёмы web-данных для training / RAG / research.
**Заметки**: требует Firecrawl API key (есть free tier).

### [browserbase/mcp-server-browserbase](https://github.com/browserbase/mcp-server-browserbase) ⭐⭐⭐⭐

| Поле | Значение |
|---|---|
| Stars | ★ 3.3k+ |
| License | Apache-2.0 |
| Rating | ⭐⭐⭐⭐ (**Browserbase официально**) |

**Что делает**: официальный MCP Browserbase, паррится со Stagehand для cloud-based browser-автоматизации.
**Аудитория**: люди, у которых local browser-automation слишком тяжёлая / нужны parallel cloud-сессии.
**Заметки**: коммерческий сервис (есть free tier); дополняет Playwright MCP (local vs cloud).

---

## 8. Design (Figma / Excalidraw)

### [GLips/Figma-Context-MCP](https://github.com/GLips/Figma-Context-MCP) ⭐⭐⭐⭐⭐

| Поле | Значение |
|---|---|
| Stars | ★ 14.6k+ |
| License | MIT |
| Rating | ⭐⭐⭐⭐⭐ (самый популярный Figma MCP) |

**Что делает**: подаёт Figma layout-инфо coding-агентам — читает дизайн-файлы, выставляет component-структуру, позволяет Cursor / Claude Code генерировать соответствующие React-компоненты.
**Аудитория**: front-end разработчики, идущие от Figma-дизайнов к component-коду.
**Заметки**: требует Figma access token; must-install для design-to-code workflow'ов.

### [excalidraw/excalidraw-mcp](https://github.com/excalidraw/excalidraw-mcp) ⭐⭐⭐⭐⭐

| Поле | Значение |
|---|---|
| Stars | ★ 4.3k+ |
| License | NOASSERTION |
| Rating | ⭐⭐⭐⭐⭐ (**Excalidraw официально**) |

**Что делает**: streamable Excalidraw MCP — пусть LLM рисует архитектурные диаграммы и flowcharts напрямую.
**Аудитория**: всем, пишущим design docs / system architecture / flowcharts, желающим, чтобы Claude рисовал из текста.
**Заметки**: официальный Excalidraw; вывод импортируется прямо в Excalidraw для правки.

### [yctimlin/mcp_excalidraw](https://github.com/yctimlin/mcp_excalidraw) ⭐⭐⭐⭐

| Поле | Значение |
|---|---|
| Stars | ★ 1.9k+ |
| License | MIT |
| Rating | ⭐⭐⭐⭐ (альтернатива Excalidraw) |

**Что делает**: MCP-сервер + Claude Code Skill, real-time canvas sync, create / edit / export.
**Аудитория**: люди, которым нужен real-time canvas sync и программное оперирование.
**Заметки**: дополняет официальный; community-поддерживаемый.

### [pbakaus/impeccable](https://github.com/pbakaus/impeccable) ⭐⭐⭐⭐⭐

| Поле | Значение |
|---|---|
| Stars | ★ 25k+ |
| License | Apache-2.0 |
| Rating | ⭐⭐⭐⭐⭐ |

**Что делает**: «**The design language that makes your AI harness better at design.**» Vocabulary / pattern set, помогающий AI-агентам производить UI / visual вывод, уходящий от generic «AI-generated» ощущения.
**Аудитория**: разработчики, использующие AI для генерации UI / mockup'ов / visual-дизайнов, получающие generic-результаты; front-end + AI workflow'ы.
**Заметки**: не MCP-сервер и не Skill-bundle — это **design language** референс. Подай AI higher-quality design vocabulary, и он произведёт лучший вывод.

---

## 9. Monitoring / Observability

### [grafana/mcp-grafana](https://github.com/grafana/mcp-grafana) ⭐⭐⭐⭐⭐

| Поле | Значение |
|---|---|
| Stars | ★ 3k+ |
| License | Apache-2.0 |
| Rating | ⭐⭐⭐⭐⭐ (**Grafana официально**) |

**Что делает**: официальный MCP Grafana — query dashboards / metrics / alerts из LLM.
**Аудитория**: SRE / DevOps, использующие Grafana для метрик.
**Заметки**: «почему эта dashboard-линия упала?» — спроси, и LLM подтянет метрики для ответа.

### [getsentry/sentry-mcp](https://github.com/getsentry/sentry-mcp) ⭐⭐⭐⭐

| Поле | Значение |
|---|---|
| Stars | ★ 677 |
| License | NOASSERTION |
| Rating | ⭐⭐⭐⭐ (**Sentry официально**) |

**Что делает**: query Sentry error events / issues / traces из LLM.
**Аудитория**: инженеры, использующие Sentry для production-ошибок.
**Заметки**: «покажи stack trace этой ошибки за прошлую неделю» — работает прямо в Claude Code.

### [winor30/mcp-server-datadog](https://github.com/winor30/mcp-server-datadog) ⭐⭐⭐

| Поле | Значение |
|---|---|
| Stars | ★ 142 |
| License | Apache-2.0 |
| Rating | ⭐⭐⭐ (community Datadog) |

**Что делает**: Datadog API MCP — monitors / logs / metrics.
**Аудитория**: пользователи Datadog, пока нет официального Datadog MCP.
**Заметки**: вероятно будет заменён, когда Datadog выкатит официальный MCP.

---

## 10. Media / Streaming (YouTube / Spotify)

### [varunneal/spotify-mcp](https://github.com/varunneal/spotify-mcp) ⭐⭐⭐⭐

| Поле | Значение |
|---|---|
| Stars | ★ 599 |
| License | MIT |
| Rating | ⭐⭐⭐⭐ |

**Что делает**: подключение LLM к Spotify — play tracks, управление playlist'ами, query истории.
**Аудитория**: всем, интегрирующим playback control или text → music workflow'ы с Claude Code.
**Заметки**: требует Spotify Premium (API-ограничение).

### [kimtaeyoon83/mcp-server-youtube-transcript](https://github.com/kimtaeyoon83/mcp-server-youtube-transcript) ⭐⭐⭐⭐

| Поле | Значение |
|---|---|
| Stars | ★ 534 |
| License | MIT |
| Rating | ⭐⭐⭐⭐ (YouTube transcripts) |

**Что делает**: подтягивает YouTube video transcripts в LLM для summary / перевода / RAG.
**Аудитория**: люди, использующие видео как учебный материал, batch-суммаризирующие YouTube-контент.
**Заметки**: зависит от YouTube auto-captions; не-английские transcripts — попадание-промах.

### [ZubeidHendricks/youtube-mcp-server](https://github.com/ZubeidHendricks/youtube-mcp-server) ⭐⭐⭐⭐

| Поле | Значение |
|---|---|
| Stars | ★ 510 |
| License | NOASSERTION |
| Rating | ⭐⭐⭐⭐ (full YouTube API) |

**Что делает**: full YouTube API MCP — за пределами transcripts: video-management, Shorts, аналитика.
**Аудитория**: YouTube-творцы, автоматизирующие channel management.
**Заметки**: требует YouTube Data API key + OAuth.

---

## 11. Chinese-language Ecosystem

### [leemysw/feishu-docx](https://github.com/leemysw/feishu-docx) ⭐⭐⭐

| Поле | Значение |
|---|---|
| Stars | ★ 193 |
| License | MIT |
| Rating | ⭐⭐⭐ |

**Что делает**: двунаправленные Feishu (Lark) docs / sheet / bitable ↔ Markdown, с OAuth 2.0, CLI, TUI, Claude Skills.
**Аудитория**: китайскоязычные пользователи Feishu / Lark, желающие связать Lark-контент с Claude Code.
**Заметки**: сейчас один из немногих MCP / Skill-вариантов в китайской экосистеме; у WeChat / DingTalk пока нет standalone-MCP (живут внутри chatbot-фреймворков).

### [netease-youdao/LobsterAI](https://github.com/netease-youdao/LobsterAI) ⭐⭐⭐⭐

| Поле | Значение |
|---|---|
| Stars | ★ 5k+ |
| License | MIT |
| Rating | ⭐⭐⭐⭐ |

**Что делает**: «24/7 all-scenario AI agent» от NetEase Youdao — workflow-автоматизация, cross-app координация, обработка файлов. Chinese-native.
**Аудитория**: китайскоязычные пользователи, желающие альтернативу Claude Code / OpenAI Operator-классу all-in-one agents; сценарии с тесной интеграцией с китайскими сервисами (NetEase, DingTalk и т. д.).
**Заметки**: product-style agent (не Skill / MCP); заменяет Claude Code / Codex, а не дополняет.

### [QwenLM/Qwen-Agent](https://github.com/QwenLM/Qwen-Agent) ⭐⭐⭐⭐⭐

| Поле | Значение |
|---|---|
| Stars | ★ 16k+ |
| License | Apache-2.0 |
| Rating | ⭐⭐⭐⭐⭐ |

**Что делает**: официальный Qwen agent framework от Alibaba — RAG, tool use, code interpreter, multi-agent, MCP-совместимый. По дефолту Qwen-модели, но переключаемо на другие LLM.
**Аудитория**: разработчики, использующие Qwen / Tongyi как основной LLM; команды, желающие Chinese-native agent framework (примеры + доки билингвальны, но Chinese-first).
**Заметки**: MCP-совместимость — highlight; подключается к Claude Code-style хостам напрямую; активная поддержка (последний коммит 2026-03).

### [coze-dev/coze-studio](https://github.com/coze-dev/coze-studio) ⭐⭐⭐⭐⭐

| Поле | Значение |
|---|---|
| Stars | ★ 20k+ |
| License | Apache-2.0 |
| Rating | ⭐⭐⭐⭐⭐ |

**Что делает**: open-source выпуск ByteDance Coze — no-code agent builder (workflow / plugin / knowledge / memory), self-hosted или cloud.
**Аудитория**: команды, строящие agents без кода; инженеры, желающие reference implementation enterprise agent-платформы (RAG, workflow, memory, plugin system).
**Заметки**: построен на in-house Eino framework Coze; подключается к OpenAI / Claude / Qwen / domestic китайским LLM. Питает и международный (coze.com), и mainland (coze.cn) продукты.

### [coze-dev/coze-loop](https://github.com/coze-dev/coze-loop) ⭐⭐⭐⭐

| Поле | Значение |
|---|---|
| Stars | ★ 5k+ |
| License | Apache-2.0 |
| Rating | ⭐⭐⭐⭐ |

**Что делает**: agent observability + evaluation платформа Coze — trace, debug, eval, prompt management. Задняя половина agent dev-lifecycle.
**Аудитория**: команды, чьи agents работают в production и нуждаются в мониторинге; разработчики, желающие увидеть, как может быть спроектирован «agent eval / observability».
**Заметки**: peer LangSmith / Arize Phoenix; OSS-выпуск self-hostable.

### [liaokongVFX/LangChain-Chinese-Getting-Started-Guide](https://github.com/liaokongVFX/LangChain-Chinese-Getting-Started-Guide) ⭐⭐⭐⭐

| Поле | Значение |
|---|---|
| Stars | ★ 8.9k+ |
| License | не указано |
| Rating | ⭐⭐⭐⭐ |

**Что делает**: китайскоязычный LangChain getting-started гид — покрывает основы, prompts, memory, agents, chains и применимые примеры. Самый ранний и полный китайский ресурс по LangChain.
**Аудитория**: китайскоязычные, которые хотят LangChain, но находят английские доки тяжёлыми; читатели, желающие понять дизайн LangChain до коммита в фреймворк.
**Заметки**: нет формальной лицензии (контент открыто читается); сам LangChain движется быстро — некоторые API в гайде могут расходиться с последней версией.

### [chatchat-space/Langchain-Chatchat](https://github.com/chatchat-space/Langchain-Chatchat) ⭐⭐⭐⭐

| Поле | Значение |
|---|---|
| Stars | ★ 37k+ |
| License | Apache-2.0 |
| Rating | ⭐⭐⭐⭐ |

**Что делает**: LangChain-based open-source knowledge-base QA система — local deployment, поддерживает множество vector store'ов, end-to-end RAG-пример.
**Аудитория**: китайские команды, желающие RAG без сборки с нуля; сценарии, требующие local-only deployment (без cloud LLM).
**Заметки**: ★ 37k делает её самой популярной RAG-имплементацией в китайской экосистеме; поддержка замедлилась (последний коммит 2025-11). Для новых проектов — fork и оценивай как референс, а не как готовую основу.

> Ищешь WeChat / DingTalk интеграции? Сегодня мейнстрим — chatbot-фреймворки (например, zhayujie/CowAgent), не чистые MCP-серверы. Добавим, когда появятся настоящие MCP.

---

## 12. Other Common (Cloudflare / Stripe…)

### [cloudflare/mcp-server-cloudflare](https://github.com/cloudflare/mcp-server-cloudflare) ⭐⭐⭐⭐⭐

| Поле | Значение |
|---|---|
| Stars | ★ 3.7k+ |
| License | Apache-2.0 |
| Rating | ⭐⭐⭐⭐⭐ (**Cloudflare официально**) |

**Что делает**: официальный MCP Cloudflare — Workers, Pages, R2, KV, D1, DNS, Zero Trust.
**Аудитория**: всем, гоняющим edge / serverless на Cloudflare.
**Заметки**: официально поддерживается; лучший edge platform MCP.

### [stripe/ai](https://github.com/stripe/ai) ⭐⭐⭐⭐

| Поле | Значение |
|---|---|
| Stars | ★ 1.5k+ |
| License | MIT |
| Rating | ⭐⭐⭐⭐ (**Stripe официально**) |

**Что делает**: официальный AI agent toolkit Stripe, включает MCP-сервер — обработка платежей, подписок, refunds, customers.
**Аудитория**: разработчики, подвязывающие payment / billing в agent-потоки.
**Заметки**: ⚠️ это реальные деньги. Тщательно тестируй в sandbox перед production.

---

## 13. Research Workflow Skills (academic / paper / lit)

> ⚠️ **Собственные проекты мейнтейнера**: ниже — skills, которые мейнтейнер репо [@WenyuChiou](https://github.com/WenyuChiou) (Lehigh CEE PhD candidate) использует ежедневно в research и open-source'нул для других исследователей. **Star-count'ы ниже, чем у general-purpose инструментов**, потому что они niche / research-specific. Планка включения ★ 100+ ослаблена в этой секции — единственный критерий тут «реально полезно в research workflow мейнтейнера». Оценивай fit сам.

### [WenyuChiou/ai-research-skills](https://github.com/WenyuChiou/ai-research-skills) ⭐⭐⭐⭐⭐

| Поле | Значение |
|---|---|
| Stars | ★ 60 |
| License | MIT |
| Rating | ⭐⭐⭐⭐⭐ (full research workflow) |

**Что делает**: 14 Claude Code skills, покрывающих частые research-задачи — literature triage, research design, project context, manuscript writing, multi-AI delegation. Упаковано как 5-plugin marketplace, ставится одной командой.
**Аудитория**: аспиранты / postdoc'и, желающие полный «research workflow» skill-set одним drop'ом.
**Заметки**: marketplace-формат, выравнивается с plugin/marketplace-концепцией, преподаваемой в этапе 5.4.

### [WenyuChiou/academic-writing-skills](https://github.com/WenyuChiou/academic-writing-skills) ⭐⭐⭐

| Поле | Значение |
|---|---|
| Stars | ★ 2 |
| License | MIT |
| Rating | ⭐⭐⭐ (узкий, но глубокий) |

**Что делает**: строгий skill для написания / ревизии / submission академической статьи под Claude Code. Field-agnostic, кастомизируется per-paper через journal_format.md и style_overrides.md.
**Аудитория**: исследователи, активно пишущие / ревизирующие статьи, желающие автоматизировать banned-word audit, figure-text coupling, submission checklists.
**Заметки**: один из 5 плагинов внутри ai-research-skills; можно ставить и standalone.

### [WenyuChiou/zotero-skills](https://github.com/WenyuChiou/zotero-skills) ⭐⭐⭐⭐

| Поле | Значение |
|---|---|
| Stars | ★ 16 |
| License | NOASSERTION |
| Rating | ⭐⭐⭐⭐ |

**Что делает**: Zotero CLI skill — программный search, add, classify, annotate ссылок.
**Аудитория**: пользователи Zotero, желающие, чтобы Claude Code напрямую организовывал их библиотеку.
**Заметки**: дополняет [`MuiseDestiny/zotero-gpt`](https://github.com/MuiseDestiny/zotero-gpt) — тот — Zotero-плагин (чат внутри Zotero), этот — CLI / Skill (оперирует Zotero из Claude Code).

### [WenyuChiou/research-hub](https://github.com/WenyuChiou/research-hub) ⭐⭐⭐⭐

| Поле | Значение |
|---|---|
| Stars | ★ 14 |
| License | MIT |
| Rating | ⭐⭐⭐⭐ |

**Что делает**: AI-operable research workspace, мостящий Zotero + Obsidian + NotebookLM, с CLI / MCP / REST / dashboard интерфейсами.
**Аудитория**: исследователи, использующие Zotero / Obsidian / NotebookLM вместе, желающие связать их в один workspace для LLM-оперирования.
**Заметки**: дополняет single-tool MCP (mcp-obsidian, notion-mcp и т. д.) — это hub, интегрирующий несколько инструментов.

---

## 14. Multi-LLM Delegation Skills

> ⚠️ **Собственные проекты мейнтейнера** (то же, что §13): delegation-skills, которые мейнтейнер извлёк из ежедневного workflow. Star-планка ослаблена; критерий — «связка Claude-planner + Codex/Gemini-executor работает надёжно». Multi-LLM-пространство быстро эволюционирует — оценивай вместе с multi-agent фреймворками этапа 7 перед внедрением.

### Как 3 skill'а композируются

3 skill'а ниже **спроектированы для использования вместе**, не как standalone-инструменты:

```
                       ┌─ codex-delegate     →  code-heavy работа
Claude (planner +      ├─ gemini-delegate    →  длинный текст / CJK / 1M контекст
        reviewer)      └─ agent-collab-skills →  splitter + reconciler + acceptance gate
                                                 (когда 2+ delegate'а параллельно)
```

Claude плох в token-heavy mechanical работе (cost, blowout контекста); Codex плох в conversational координации; 1M-контекст Gemini хорош, но reasoning среднего уровня. **Разделение труда: Claude — дизайн / ревью, Codex — реализация, Gemini — длинные черновики / synthesis.**

### [WenyuChiou/codex-delegate](https://github.com/WenyuChiou/codex-delegate) ⭐⭐⭐⭐⭐

| Поле | Значение |
|---|---|
| Stars | ★ 57 |
| License | MIT |
| Rating | ⭐⭐⭐⭐⭐ |

**Что делает**: Claude Code skill, использующий Codex CLI как execution-специалиста — multi-file рефакторинги, batch-правки, boilerplate-генерация, wrapper-based реализации. Claude пишет план + ревьюит; Codex исполняет.
**Аудитория**: разработчики, желающие экономить токены / ускорять large-scale механические правки; ученики, желающие убедиться, что «multi-agent — не просто buzzword».
**Используй для**: рефакторинга 30+ файлов, генерации тестовых scaffold'ов, портирования того же паттерна через N файлов, написания migration-скриптов.
**Не используй для**: архитектурных решений, диагностики багов, security-ревью, задач, требующих conversation-памяти — Claude делает их лучше напрямую.
**Заметки**: работает в паре с `gemini-delegate-skill`. Практическая реализация концепции multi-agent этапа 7.

### [WenyuChiou/gemini-delegate-skill](https://github.com/WenyuChiou/gemini-delegate-skill) ⭐⭐⭐⭐

| Поле | Значение |
|---|---|
| Stars | ★ 34 |
| License | MIT |
| Rating | ⭐⭐⭐⭐ |

**Что делает**: Claude Code skill, использующий Gemini CLI как исполнитель для длинного текста / большого контекста / CJK — 1M-token context window, китайский длинный текст, second-opinion ревью. Claude даёт outline и критику; Gemini пишет длинный черновик.
**Аудитория**: исследователи, пишущие статьи, knowledge worker'ы, пишущие китайские отчёты / Threads-посты, люди, желающие perspective второго LLM для cross-check.
**Используй для**: длинных черновиков (>3000 слов), cross-document synthesis (загрузка многих длинных документов в 1M-context), Chinese / CJK-контента, LLM-vs-LLM сравнительных view.
**Не используй для**: коротких запросов, генерации кода (используй codex), production-critical решений (финальный human-review).
**Заметки**: работает в паре с `codex-delegate` для разделения «Codex пишет код, Gemini пишет прозу».

### [WenyuChiou/agent-collab-skills](https://github.com/WenyuChiou/agent-collab-skills) ⭐⭐

| Поле | Значение |
|---|---|
| Stars | недавно опубликован, ещё нет stars |
| License | MIT |
| Rating | ⭐⭐ (экспериментально — relate как референс) |

**Что делает**: Claude Code marketplace для multi-agent collaboration — task splitter, output reconciler, adversarial debate, shared memory, acceptance gate. Композируется с codex-delegate / gemini-delegate.
**Аудитория**: люди, гоняющие 2+ delegate-агентов за раунд, желающие увидеть один способ паковки multi-agent координации в marketplace.
**Заметки**: **экспериментально** — не относись как к production-grade фреймворку. Это собственная настройка мейнтейнера, выложенная публично как референс. Для production-grade multi-agent см. LangGraph / AutoGen / CrewAI в этапе 7.

---

## Чего здесь нет?

Если твоей интеграции выше нет — сначала проверь эти каталоги:

- [`wong2/awesome-mcp-servers`](https://github.com/wong2/awesome-mcp-servers) — самый полный community MCP server-каталог, 150+ записей по категориям
- [`punkpeye/awesome-mcp-servers`](https://github.com/punkpeye/awesome-mcp-servers) — ещё один каталог MCP-серверов, дополнительный
- [`modelcontextprotocol/servers`](https://github.com/modelcontextprotocol/servers) — официальные reference-серверы Anthropic (filesystem, git, time, memory, fetch, sequential-thinking, …)
- [`travisvn/awesome-claude-skills`](https://github.com/travisvn/awesome-claude-skills) — каталог Claude Skills

### Хочешь добавить что-то?

1. Открой issue с ссылкой на репо, объяснением, почему надо добавить, и в какую категорию подходит.
2. Или PR напрямую: добавь запись под соответствующей категорией в формате (Stars / License / Rating + What it does / Audience / Notes).
3. **Stars < 100 + не-официальный** обычно отклоняется, если только не сможешь аргументировать сильный niche use case.

Прочти [`resources/style-guide.ru.md`](style-guide.ru.md) и [`CONTRIBUTING.md`](../CONTRIBUTING.md) перед submission'ом.

---

## Заметки для тех, кто помогает позже

Не SLA — просто «делай, что можешь» guidance:

- Подтягивай stars / license через `gh api repos/<owner>/<repo>`. **Refresh когда есть время** — без фиксированной cadence.
- Заметил битую ссылку / archived репо? Просто удали.
- Новая категория (AR/VR, IoT и т. д.) — открывай, как только наберётся 1–2 записи стоящих включения.
- «Chinese-language ecosystem» остаётся loose; китайские репо набирают stars медленнее.
- Неконсистентные формулировки или форматирование между записями — не парься. Читаемость PR важнее.
