# Related Resources

> [繁體中文](./RESOURCES.md) | [简体中文](./RESOURCES.zh-Hans.md) | **English**

> [← Back to main README](README.en.md)

This file collects: term definitions, daily-tool MCP/Skill highlights, topic-based awesome lists, Chinese-community resources. Pulled out of the main README to keep that page focused.

> 💡 **Don't know a term?** (LLM, agent, RAG, token, vector DB, …) → [`resources/glossary.en.md`](resources/glossary.en.md) — 30+ common terms with 30–80-word definitions

---

## Three core terms: MCP / Skills / Plugins

The README and stages reference these three Claude Code ecosystem terms a lot. Quick definitions:

- **MCP (Model Context Protocol)** — Anthropic's open protocol that lets any LLM host (Claude Code, other IDEs, your own agent) talk to any external tool server (filesystem, DB, API, your service) through one interface. Think "USB for LLMs". See [Stage 5.2](stages/05-claude-code-ecosystem.en.md#52--mcp-model-context-protocol--foundation).
- **Skills** — Claude Code's "behavior bundles". A Skill is a `SKILL.md` describing "in what context, do what, can call which MCP tools". Claude Code auto-discovers them. See [Stage 5.3](stages/05-claude-code-ecosystem.en.md#53--skills-claude-codes-behavior-layer--the-most-critical-layer-of-the-claude-code-ecosystem).
- **Plugins / Marketplaces** — package Skills, slash commands, hooks, and MCP configs into a distribution unit installable by your team or community. A marketplace is a catalog of plugins. See [Stage 5.4](stages/05-claude-code-ecosystem.en.md#54--plugins--marketplaces).

Hands-on exercises live in [Stage 5](stages/05-claude-code-ecosystem.en.md), with Track A's [A3](tracks/cli/A3-cli-production.en.md) covering production integration.

---

## Daily-tool integrations: MCP servers + Skills

Connect Claude Code (or any other CLI agent) to the apps you already use, without window-hopping. Mature picks below:

### Notes / Knowledge Base

- [**MarkusPfundstein/mcp-obsidian**](https://github.com/MarkusPfundstein/mcp-obsidian) ★ 3.5k+ — Obsidian REST API plugin lets the LLM read/write your vault
- [**makenotion/notion-mcp-server**](https://github.com/makenotion/notion-mcp-server) ★ 4k+ — Notion **official** MCP, query/create pages, manipulate databases
- [**PleasePrompto/notebooklm-skill**](https://github.com/PleasePrompto/notebooklm-skill) ★ 6.6k+ — NotebookLM Skill, citation-backed answers from your uploaded docs
- [**teng-lin/notebooklm-py**](https://github.com/teng-lin/notebooklm-py) ★ 15k+ — unofficial NotebookLM Python API + CLI, plays well with Claude Code / Codex

### Office Documents (Word / Excel / PowerPoint / PDF)

- [**anthropics/skills**](https://github.com/anthropics/skills) ★ 129k+ — Anthropic **official** Skills with built-in docx / xlsx / pptx / pdf processing
- [**tfriedel/claude-office-skills**](https://github.com/tfriedel/claude-office-skills) ★ 646 — Office skills with automation workflows on top of the official ones

### Google Workspace (Gmail / Docs / Drive / Calendar)

- [**taylorwilsdon/google_workspace_mcp**](https://github.com/taylorwilsdon/google_workspace_mcp) ★ 2.3k+ — full Workspace stack (Gmail, Calendar, Docs, Sheets, Slides, Drive) in one server

### Dev Collaboration

- [**github/github-mcp-server**](https://github.com/github/github-mcp-server) ★ 29k+ — GitHub **official** MCP for issues / PRs / repos
- [**atlassian/atlassian-mcp-server**](https://github.com/atlassian/atlassian-mcp-server) ★ 723 — Atlassian **official** Remote MCP (Jira, Confluence)
- [**jerhadf/linear-mcp-server**](https://github.com/jerhadf/linear-mcp-server) ★ 340+ — Linear MCP
- [**korotovsky/slack-mcp-server**](https://github.com/korotovsky/slack-mcp-server) ★ 1.5k+ — Slack MCP, works without admin permissions

### Research Workflow (by the repo maintainer)

- [**WenyuChiou/ai-research-skills**](https://github.com/WenyuChiou/ai-research-skills) ★ 77 — 14 research-workflow skills as a 5-plugin marketplace
- [**WenyuChiou/research-hub**](https://github.com/WenyuChiou/research-hub) ★ 16 — Zotero + Obsidian + NotebookLM integration workspace
- [**WenyuChiou/zotero-skills**](https://github.com/WenyuChiou/zotero-skills) ★ 22 — Zotero CLI skill
- [**WenyuChiou/codex-delegate**](https://github.com/WenyuChiou/codex-delegate) ★ 57 + [**gemini-delegate-skill**](https://github.com/WenyuChiou/gemini-delegate-skill) ★ 34 — multi-LLM delegation pair

### Chinese-language Ecosystem

- [**leemysw/feishu-docx**](https://github.com/leemysw/feishu-docx) ★ 209 — Feishu (Lark) docs / sheet / bitable ↔ Markdown with Claude Skills support

> The above is just the highlights. **Full 62-entry catalog by category** (incl. databases, browser automation, Figma, Excalidraw, Cloudflare, Stripe, academic-writing / multi-LLM delegation, etc.) lives in [`resources/mcp-skills-catalog.en.md`](resources/mcp-skills-catalog.en.md).

> Looking for more MCP server catalogs? See [`wong2/awesome-mcp-servers`](https://github.com/wong2/awesome-mcp-servers) / [`punkpeye/awesome-mcp-servers`](https://github.com/punkpeye/awesome-mcp-servers) (categorized). **Canva**'s official MCP is still early access — community versions are unstable; will add when stable.

---

## Topic-based awesome lists

This repo **doesn't replace** flat awesome lists. When you already know which tool you want, these are more direct:

### MCP-related

- [**modelcontextprotocol/servers**](https://github.com/modelcontextprotocol/servers) — official reference servers (filesystem, github, sqlite, git, fetch, memory, …)
- [**wong2/awesome-mcp-servers**](https://github.com/wong2/awesome-mcp-servers) — community MCP server catalog, by category (150+)
- [**punkpeye/awesome-mcp-servers**](https://github.com/punkpeye/awesome-mcp-servers) — another MCP server catalog

### Claude Code / Skills / Plugins-related

- [**hesreallyhim/awesome-claude-code**](https://github.com/hesreallyhim/awesome-claude-code) — Claude Code resources (currently restructuring)
- [**travisvn/awesome-claude-skills**](https://github.com/travisvn/awesome-claude-skills) — Claude Skills catalog
- [**anthropics/claude-plugins-official**](https://github.com/anthropics/claude-plugins-official) — Anthropic's official plugin marketplace template; start here when packaging your own plugin

### Chinese-speaking community

- [**datawhalechina/hello-agents**](https://github.com/datawhalechina/hello-agents) — Datawhale systematic agent tutorial (zh-Hans)
- [**WangRongsheng/awesome-LLM-resources**](https://github.com/WangRongsheng/awesome-LLM-resources) — comprehensive zh-Hans LLM resources (8k+ stars)
- [**AiHubCN/Awesome-Chinese-LLM**](https://github.com/AiHubCN/Awesome-Chinese-LLM) — open-source Chinese LLM catalog

---

## What else?

- Main README: [README.en.md](README.en.md)
- Full MCP / Skill catalog: [resources/mcp-skills-catalog.en.md](resources/mcp-skills-catalog.en.md)
- CLI agent comparison guide: [resources/cli-agents-guide.en.md](resources/cli-agents-guide.en.md)
- Style guide / contributing: [resources/style-guide.en.md](resources/style-guide.en.md), [CONTRIBUTING.en.md](CONTRIBUTING.en.md)
