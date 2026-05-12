# Stage 5 — Claude Code Ecosystem ⭐⭐

> [繁體中文](./05-claude-code-ecosystem.md) | [简体中文](./05-claude-code-ecosystem.zh-Hans.md) | **English** | [Русский](./05-claude-code-ecosystem.ru.md)


⏱ **Time estimate**: 3-4 weeks (~15-25 hours)

> 💡 This stage revolves around four terms (**MCP / Skills / Plugins / Marketplace**) → unfamiliar? See [`resources/glossary.en.md` §5](../resources/glossary.en.md#5-claude-code-ecosystem).

> 📌 **This stage is used by both tracks**:
> - **Track A (CLI Power User)**: A2 uses [5.1 (Claude Code basics)](#51--claude-code-basics); A3 uses [5.2 (MCP)](#52--mcp-model-context-protocol-foundation) + selectively [5.3 (Skills)](#53--skills-claude-code-behavior-layer) and [5.4 (Plugins)](#54--plugins--marketplaces) (A3's Exercise CLI-12 teaches packaging CLAUDE.md / commands into a plugin). Reading angle: "**how to use Claude Code well**"
> - **Track B (Agent Builder)**: works through the full stage 5.1 → 5.4 as "**how Claude Code works internally**" deep dive

> ⚠️ **This stage is not the path for a local LLM.** Claude Code requires Anthropic API / OAuth and cannot directly switch to Ollama or a local endpoint. For offline work, privacy-sensitive files, or avoiding API quota, use [`resources/cookbook.md` Recipe 6](../resources/cookbook.en.md#6-local-llm--cli-agent-quick-walkthrough) with a BYO-LLM CLI agent such as OpenCode / goose / Aider / Hermes.

## Stack at a glance

Top to bottom, each layer is built on the one below:

![Claude Code Ecosystem Stack](../resources/diagrams/stage5-stack.en.png)

Each layer adds one capability:
- **API + SDK**: programmatic access to the LLM
- **Tool Use**: LLM can call functions you define
- **MCP**: standardized protocol so any LLM host can use any tool server
- **Skills**: behavior bundles for Claude Code that can wrap MCP tools
- **Plugins**: package + ship Skills, hooks, commands, MCP configs as one unit

This stage has 4 sub-sections. **Do them in order** — each builds on the previous.

```
5.1  Claude Code Basics       3-5 days   (install, slash commands, CLAUDE.md)
5.2  MCP — Protocol Layer     5-7 days   (write your first MCP server)
5.3  Skills — Behavior Layer  5-7 days   (write your first SKILL.md)
5.4  Plugins & Marketplaces   5-7 days   (package and ship)
```

After this stage you will be able to extend Claude Code, write your own MCP server, and ship a plugin marketplace.

---

## 5.1 — Claude Code Basics

### Learning Goals
- Install Claude Code on your OS
- Use slash commands (`/help`, `/compact`, `/clear`, `/plan`)
- Understand the `~/.claude/` directory structure
- Write a project-level `CLAUDE.md` that customizes behavior

### Required Reading
1. [**Anthropic — Claude Code Quickstart**](https://docs.anthropic.com/en/docs/claude-code/quickstart) — official install guide
2. [**Anthropic — CLAUDE.md best practices**](https://docs.anthropic.com/en/docs/claude-code/memory) — how to write project memory
3. [**KimYx0207/Claude-Code-x-OpenClaw-Guide-Zh**](https://github.com/KimYx0207/Claude-Code-x-OpenClaw-Guide-Zh) — zh-Hans beginner guide

### Hands-on Exercises
- **Exercise: Claude Code** — install, run first session, ask Claude to read a file and summarize
- **Exercise: CLAUDE.md** — write a project CLAUDE.md, observe behavior change

### Curated Projects
- [**anthropics/claude-code**](https://github.com/anthropics/claude-code) — official repo (issues, releases)
- [**KimYx0207/Claude-Code-x-OpenClaw-Guide-Zh**](https://github.com/KimYx0207/Claude-Code-x-OpenClaw-Guide-Zh) — zh-Hans walkthrough
- [**hesreallyhim/awesome-claude-code**](https://github.com/hesreallyhim/awesome-claude-code) — broader resource list (currently restructuring)

---

## 5.2 — MCP (Model Context Protocol) ⭐ Foundation

### Learning Goals
- Explain MCP's three abstractions (Tools, Resources, Prompts)
- Connect an existing MCP server to Claude Desktop or Claude Code
- Write a minimal MCP server in Python that exposes 1-2 tools
- Distinguish MCP server vs Tool Use vs Skills vs Plugins

### Required Reading
1. [**Anthropic — Introducing MCP**](https://www.anthropic.com/news/model-context-protocol) — original announcement, conceptual overview
2. [**MCP Specification**](https://modelcontextprotocol.io/specification) — the actual protocol spec
3. [**Complete Guide to MCP in 2026**](https://dev.to/x4nent/complete-guide-to-mcp-model-context-protocol-in-2026-architecture-implementation-and-4a11) — implementation walkthrough

### Hands-on Exercises
- **Exercise: MCP client** — install `modelcontextprotocol/servers/filesystem` and connect via Claude Desktop. Watch Claude read your files.
- **Exercise: MCP server** — write a Python MCP server that exposes one tool (e.g., "convert temperature"). Connect from Claude Code.
- **Exercise: MCP in production** — connect 2-3 MCP servers in one Claude session and watch them coordinate.

### Curated Projects

> 💡 **Looking for MCP servers for daily tools (Notion / Obsidian / Excel / Postgres / Playwright / Figma…)?**
> See [`resources/mcp-skills-catalog.en.md`](../resources/mcp-skills-catalog.en.md) — 57 commonly-used MCP servers / Skills grouped into 14 categories with stars / license / audience. The section below stays focused on "**reference for writing your own MCP server**" (official servers + SDKs).

#### [modelcontextprotocol/servers](https://github.com/modelcontextprotocol/servers) ⭐ Official

| Field | Value |
|---|---|
| Language | TypeScript / Python |
| Stars | ★ 85k+ |
| License | MIT |
| Recommendation | ⭐⭐⭐⭐⭐ |

**What it teaches**: 20+ reference MCP servers (filesystem, git, github, sqlite, time, fetch, memory, sequential thinking). The canonical examples for writing your own.

**Best for**: Exercise 1 and as reference. Read the source of `everything` server and `filesystem` server to understand the protocol.

**Run it**:
```bash
npx -y @modelcontextprotocol/server-filesystem /path/to/dir
# Or use Python servers:
pip install mcp-server-fetch
```

---

#### [modelcontextprotocol/python-sdk](https://github.com/modelcontextprotocol/python-sdk)

| Field | Value |
|---|---|
| Language | Python |
| License | MIT |
| Recommendation | ⭐⭐⭐⭐⭐ |

**What it teaches**: Official Python SDK for writing MCP servers. Use this for Exercise 2.

**Run it**:
```bash
pip install mcp
# Then follow https://github.com/modelcontextprotocol/python-sdk#quickstart
```

---

#### [modelcontextprotocol/typescript-sdk](https://github.com/modelcontextprotocol/typescript-sdk)

| Field | Value |
|---|---|
| Language | TypeScript |
| License | MIT |
| Recommendation | ⭐⭐⭐⭐ |

**What it teaches**: TypeScript equivalent of the Python SDK. Pick this if you prefer TS.

---

#### [wong2/awesome-mcp-servers](https://github.com/wong2/awesome-mcp-servers) ⭐ Catalog

| Field | Value |
|---|---|
| Format | Curated list |
| Recommendation | ⭐⭐⭐⭐⭐ |

**What it teaches**: Catalog of 150+ community MCP servers organized by category — search, code, cloud, communication, finance.

**Best for**: Discovering existing servers before writing your own. Browse this when you have a specific tool need.

**Notes**: Submission goes through their website (mcpservers.org).

---

#### [punkpeye/awesome-mcp-servers](https://github.com/punkpeye/awesome-mcp-servers)

| Field | Value |
|---|---|
| Recommendation | ⭐⭐⭐⭐ |

**What it teaches**: Alternative MCP server catalog with different organization (often more current).

**Best for**: Cross-reference with wong2's list. Different curators surface different projects.

---

#### [github/github-mcp-server](https://github.com/github/github-mcp-server)

| Field | Value |
|---|---|
| Recommendation | ⭐⭐⭐⭐ |

**What it teaches**: How a real production MCP server is structured. Official GitHub-maintained.

**Best for**: Reading the source as a reference implementation for production-grade MCP server.

---

#### [21st-dev/magic-mcp](https://github.com/21st-dev/magic-mcp)

| Field | Value |
|---|---|
| Stars | ★ 4.8k+ |
| License | NOASSERTION |
| Recommendation | ⭐⭐⭐ |

**What it teaches**: A non-trivial MCP server that creates UI components. Shows how MCP can extend beyond simple data fetching.

**Best for**: Inspiration after Exercise 2 — what creative MCP servers can do.

---

## 5.3 — Skills (Claude Code Behavior Layer)

### Learning Goals
- Anatomy of `SKILL.md` (YAML frontmatter + body)
- When skills auto-load (description matching)
- How to write a SKILL.md that solves your daily task
- Use of `references/`, `scripts/`, `evals/` subdirectories

### Required Reading
1. [**Anthropic — Claude Skills documentation**](https://docs.anthropic.com/en/docs/claude-code/skills)
2. **A few example SKILL.md files** from `anthropics/claude-code` or community marketplaces

### Hands-on Exercises
- **Exercise: SKILL.md** — write a 200-word skill solving one of your daily tasks
- **Exercise: SKILL with references** — add a `references/` markdown the skill can pull from
- **Exercise: SKILL eval** — add `evals/evals.json` with 3-5 self-tests

### Curated Projects

> 💡 **Looking for daily-use Skills (NotebookLM, Excalidraw, Office docs, etc.)?**
> See [`resources/mcp-skills-catalog.en.md`](../resources/mcp-skills-catalog.en.md) — grouped by use case, includes both Anthropic-official and community Skills. The section below stays focused on "**reference material for writing your own Skill**" (specs and showcase).

#### [anthropics/skills](https://github.com/anthropics/skills) ⭐ Official spec

| Field | Value |
|---|---|
| Stars | ★ 128k+ |
| License | NOASSERTION |
| Recommendation | ⭐⭐⭐⭐⭐ |

**What it teaches**: Anthropic's official Skills repo — `spec/` (SKILL.md frontmatter standard), `template/` (starter scaffold), and `skills/` (reference implementations: pdf, docx, xlsx, pptx, skill-creator).

**Best for**: Read this before writing your own SKILL.md — an important reference implementation for SKILL.md structure and frontmatter.

**Notes**: Different from `anthropics/claude-code` — this repo is the dedicated Skills repo; the other is the main Claude Code repo. The broader Agent Skills standard is at [agentskills.io](https://agentskills.io).

---

#### [anthropics/claude-code](https://github.com/anthropics/claude-code)

| Field | Value |
|---|---|
| Recommendation | ⭐⭐⭐⭐ |

**What it teaches**: The Claude Code main repo — issues, releases, and inline skill examples.

**Best for**: Tracking new features, filing bugs, reading release notes.

**Notes**: At this stage (learning Skills), this repo sits below `anthropics/skills` (⭐⭐⭐⭐⭐, the official spec), so it's rated ⭐⭐⭐⭐. In branches (positioned as the end-user entry point), you'll see ⭐⭐⭐⭐⭐ — same repo, audience-specific framing.

---

#### [travisvn/awesome-claude-skills](https://github.com/travisvn/awesome-claude-skills)

| Recommendation | ⭐⭐⭐⭐ |
|---|---|

**What it teaches**: Curated catalog of Claude Skills across the community.

**Best for**: Discovering existing skills before writing your own.

---

#### [obra/superpowers](https://github.com/obra/superpowers)

| Recommendation | ⭐⭐⭐⭐ |
|---|---|

**What it teaches**: 20+ battle-tested skills (TDD, debugging, collaboration patterns) with `/brainstorm`, `/write-plan`, `/execute-plan` commands and skills-search tool.

**Best for**: Power-user setup. Read SKILL.md sources to learn advanced patterns.

---

#### [VoltAgent/awesome-agent-skills](https://github.com/VoltAgent/awesome-agent-skills)

| Field | Value |
|---|---|
| Stars | ★ 20k+ |
| License | MIT |
| Recommendation | ⭐⭐⭐ |

**What it teaches**: 1000+ agent skills compatible with Claude Code, Codex, Gemini CLI, Cursor. Cross-tool perspective.

**Best for**: After you understand SKILL.md, browse for ideas.

---

#### [alirezarezvani/claude-skills](https://github.com/alirezarezvani/claude-skills)

| Recommendation | ⭐⭐⭐ |
|---|---|

**What it teaches**: 232+ Claude Code skills across engineering, marketing, product, compliance.

**Best for**: Domain-specific skill examples.

---

#### [mattpocock/skills](https://github.com/mattpocock/skills)

| Field | Value |
|---|---|
| Stars | ★ 61k+ |
| License | MIT |
| Recommendation | ⭐⭐⭐⭐ |

**What it teaches**: Matt Pocock (well-known TypeScript educator) publishing his actual `.claude/` directory. Each SKILL.md is short (10-50 lines) and not over-engineered.

**Best for**: Seeing what real engineer-daily SKILL.md files look like. A great counter-example to over-engineered 200-line skills.

---

#### [wshobson/agents](https://github.com/wshobson/agents)

| Field | Value |
|---|---|
| Stars | ★ 35k+ |
| License | MIT |
| Recommendation | ⭐⭐⭐⭐ |

**What it teaches**: Combining skills + subagents into multi-agent orchestration. **Goes from single SKILL.md to the agent-as-skill composition pattern.**

**Best for**: Intermediate learners after a few SKILL.md files — when you want to know "how do skills call each other and turn into bigger agent workflows?"

---

## 5.4 — Plugins & Marketplaces

### Learning Goals
- `plugin.json` schema (name, version, skills array, configuration)
- `marketplace.json` schema (plugins array, source, metadata)
- `claude plugin marketplace add` workflow
- Distinguish single-plugin bundle vs multi-plugin marketplace
- Publish your own marketplace

### Required Reading
1. [**Anthropic — Plugins documentation**](https://docs.anthropic.com/en/docs/claude-code/plugins)
2. **Read the `plugin.json` and `marketplace.json` of 2-3 marketplaces below**

### Hands-on Exercises
- **Exercise: plugin install** — install one of the marketplaces below, see it load
- **Exercise: plugin.json** — package the SKILL.md you wrote in 5.3 into a plugin
- **Exercise: marketplace publish** — push to GitHub, install via `claude plugin marketplace add`

### Curated Projects

> 💡 **Want to see how others package plugins?** Several entries in [`resources/mcp-skills-catalog.en.md`](../resources/mcp-skills-catalog.en.md) (dev collab / design / monitoring sections) ship as plugins too (e.g., `timescale/pg-aiguide` is both an MCP server and a plugin). The section below stays focused on "**marketplace structure templates**" as reference.

#### [anthropics/claude-plugins-official](https://github.com/anthropics/claude-plugins-official) ⭐ Official

| Field | Value |
|---|---|
| Stars | ★ 18k+ |
| License | NOASSERTION (each plugin has its own license; check per plugin) |
| Recommendation | ⭐⭐⭐⭐⭐ |

**What it teaches**: Anthropic's official marketplace template — `.claude-plugin/marketplace.json` standard schema, `plugins/` for inline plugins, and `external_plugins/` for plugins referenced from external repos.

**Best for**: Before publishing your own marketplace, this is the official template you'd most want to copy from for the **what should marketplace.json look like?** question.

**Notes**: Beyond schema, this also shows how Anthropic categorizes its official plugins (chrome-devtools, deepwiki, code-research, jam, etc.).

---

#### [obra/superpowers-marketplace](https://github.com/obra/superpowers-marketplace)

| Field | Value |
|---|---|
| Stars | ★ 900+ |
| License | MIT |
| Recommendation | ⭐⭐⭐⭐ |

**What it teaches**: **The minimal marketplace template** — the repo contains only `.claude-plugin/marketplace.json` + README; the plugin source itself lives in external repos. Demonstrates the **curator-only marketplace** form (the curator selects, doesn't bundle source).

**Best for**: Building a "I curate, others write" marketplace. Smaller than `anthropics/claude-plugins-official` — the minimum viable template.

---

#### [trailofbits/skills-curated](https://github.com/trailofbits/skills-curated)

| Field | Value |
|---|---|
| Stars | ★ 388 |
| License | CC-BY-SA-4.0 |
| Recommendation | ⭐⭐⭐ |

**What it teaches**: A curated marketplace from the well-known security firm Trail of Bits, focused on **supply-chain security** — every skill is reviewed, and the README documents the criteria.

**Best for**: Reviewers and teams who care about supply-chain trust and want to study the **curator-vouches-for-safety** model.

**Notes**: Small in scale but significant in framing — shows that a marketplace can be more than a list, it can be a trust mechanism.

---

#### [anthropics/life-sciences](https://github.com/anthropics/life-sciences) (domain-specialized example)

| Field | Value |
|---|---|
| Stars | ★ 331 |
| License | NOASSERTION (marketplace itself has no SPDX; each MCP server is licensed by its own provider) |
| Recommendation | ⭐⭐⭐ |

**What it teaches**: Anthropic's own **domain-specialized marketplace** example (for life sciences / health) — shows how to tailor `marketplace.json` for a single vertical instead of a generic catalog.

**Best for**: Builders making vertical-specific marketplaces (healthcare, finance, legal, edu) who want to see how Anthropic handles it.

**Notes**: Payload is bio-leaning MCP servers, but the marketplace.json shape is the actual lesson.

---

> **"How to publish your own marketplace" tutorial is still missing** — the most reliable resource is currently [Anthropic's official plugin docs](https://docs.claude.com/en/docs/claude-code/plugins). Have you written a high-quality walkthrough? PRs welcome.

---

#### [rohitg00/awesome-claude-code-toolkit](https://github.com/rohitg00/awesome-claude-code-toolkit)

| Recommendation | ⭐⭐⭐ |
|---|---|

**What it teaches**: One of the largest community catalogs of Claude Code agents, skills, hooks, and templates. Wide breadth across many use cases.

**Best for**: After Exercise 3, browse to see what's out there.

---

## ✅ Self-Check Before Stage 6

Can you:
- [ ] Install Claude Code and use 5 different slash commands
- [ ] Connect 2 MCP servers in one Claude session
- [ ] Write your own MCP server in Python that exposes 1 working tool
- [ ] Write a `SKILL.md` that auto-loads on a specific trigger phrase
- [ ] Package skills into a plugin and publish via `marketplace.json`
- [ ] Distinguish MCP / Skills / Plugins / SDK by their roles

If yes → proceed to [Stage 6 — Memory & RAG](06-memory-rag.md).

## 💡 Bonus: After this Stage

- Submit a PR to [`anthropics/claude-cookbooks`](https://github.com/anthropics/claude-cookbooks) (small fix, doc update)
- Submit your own plugin to a community marketplace
- Write a blog post comparing your hello-MCP server with one from the official `modelcontextprotocol/servers` collection
