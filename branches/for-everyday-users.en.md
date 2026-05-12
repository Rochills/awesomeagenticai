# For Everyday Users — Specialized Branch

> [繁體中文](./for-everyday-users.md) | [简体中文](./for-everyday-users.zh-Hans.md) | **English** | [Русский](./for-everyday-users.ru.md)

> 🚀 **Never written code or installed Python before?** Start with [`resources/setup-guide.en.md` §A-C](../resources/setup-guide.en.md) (about 30 minutes from zero), then come back. If you already know Python and have an API key, skip it.

> [← Back to main path README](../README.en.md) · You **don't have to walk the full main path** to start here — this branch is for people who **just want to USE AI, not build agents**.

## Use Cases

- Writing email, organizing notes, polishing a cover letter
- Learning new skills (reading English articles, picking up a language, reviewing material)
- Research and comparison (travel, products, schools)
- Daily life flow (recipes, schedules, todo lists)
- Privacy-sensitive scenarios: medical records, personal finance (→ local LLM)

## Where to Start: 4 Tiers by "How Hands-On Are You?"

```
Tier 0: Web / Mobile App  (recommended starting point)
   ↓
Tier 1: Desktop App  (upgrade when you need to handle local files)
   ↓
Tier 2: CLI Agent  (willing to learn a bit of command line; automate daily flows)
   ↓
Tier 3: Local LLM  (privacy-sensitive, cost-sensitive, want offline)
```

**Most people stay at Tier 0 / Tier 1** — Tiers 2-3 are for special needs or learners.

---

## 🎯 Curated Projects

### Tier 0 — Web / Mobile App ⭐ Entry-level

#### [Claude.ai](https://claude.ai) ⭐⭐⭐⭐⭐
Anthropic's official interface. Best for long-form writing, in-depth discussion, complex questions — answer style is more restrained, less hallucination-prone.

#### [ChatGPT](https://chatgpt.com) ⭐⭐⭐⭐⭐
OpenAI's official interface. Largest ecosystem (GPTs, Custom Instructions, Voice mode). The standard general-purpose pick.

#### [Gemini](https://gemini.google.com) ⭐⭐⭐⭐
Google's offering. Long context window (millions of tokens) — particularly good for dropping a whole PDF in to ask questions. Integrated with Google services (Gmail, Docs).

#### [Perplexity](https://perplexity.ai) ⭐⭐⭐⭐
Search engine × LLM — every answer cites sources. Better than ChatGPT for "needs current info" scenarios.

---

### Tier 1 — Desktop App

#### [Claude Desktop](https://claude.ai/download) ⭐⭐⭐⭐⭐
Beyond the web version: drag files in, read local files, retain long conversation context. **Also the gateway to the MCP ecosystem** — you can connect Slack / Gmail / Calendar servers.

#### [ChatGPT Desktop](https://openai.com/chatgpt/desktop) ⭐⭐⭐⭐
Desktop version of ChatGPT. Ask questions about screenshots, voice conversation, integrate with other apps.

---

### Tier 2 — CLI Agents (advanced users willing to learn the command line)

> These tools are positioned for developers but **everyday users can use them too** — e.g. batch-rename files, organize the Downloads folder, auto-write weekly reviews, summarize PDFs into Markdown.
>
> Want a detailed comparison? See [`resources/cli-agents-guide.en.md`](../resources/cli-agents-guide.en.md) — six major CLI agents side by side, recommendations by use case, common pitfalls, real-world setups.
>
> Want step-by-step onboarding? See [`tracks/cli/A1-cli-intro.en.md`](../tracks/cli/A1-cli-intro.en.md) — Track A first stop, from install to your first task.
>
> Want to wire your CLI agent to Notion / Obsidian / Excel / Google docs / etc.? See [`resources/mcp-skills-catalog.en.md`](../resources/mcp-skills-catalog.en.md) — 62 MCP servers / Skills grouped by use case.

#### [anthropics/claude-code](https://github.com/anthropics/claude-code) ⭐⭐⭐⭐⭐
★ 120k+ — Anthropic's official CLI agent. Reads/writes files, runs commands, handles multi-step tasks. **The most beginner-friendly CLI tool for everyday users.**

#### [openai/codex](https://github.com/openai/codex) ⭐⭐⭐⭐⭐

| Field | Value |
|---|---|
| Stars | ★ 80k+ |
| License | Apache-2.0 |

**What it teaches**: OpenAI's lightweight terminal coding agent. Same category as Claude Code, but uses OpenAI models.

**Best for**: People who already subscribe to ChatGPT Plus / Pro and want to use the same account in the terminal.

#### [sst/opencode](https://github.com/sst/opencode) ⭐⭐⭐⭐⭐

| Field | Value |
|---|---|
| Stars | ★ 155k+ |
| License | MIT |

**What it teaches**: Open-source coding agent **not tied to any specific LLM provider** — use Claude, GPT, Gemini, or local Ollama, your choice. Community-maintained, fast iteration.

**Best for**: Self-hosters; people who don't want vendor lock-in; anyone switching between multiple LLMs.

#### [google-gemini/gemini-cli](https://github.com/google-gemini/gemini-cli) ⭐⭐⭐⭐

| Field | Value |
|---|---|
| Stars | ★ 103k+ |
| License | Apache-2.0 |

**What it teaches**: Google's official Gemini CLI agent. Brings Gemini's long context and Google ecosystem integration to the terminal.

**Best for**: Heavy users of the Google ecosystem (Gmail, Drive, Docs).

---

### Tier 3 — Local LLM (privacy / offline / cost)

#### [Ollama](https://github.com/ollama/ollama) ⭐⭐⭐⭐⭐
★ 170k+ — One command to run a local LLM. Use this when privacy-sensitive data (medical records, contracts, family conversations) shouldn't leave your machine. See [Stage 1 — Local LLM](../stages/01-llm-basics.en.md).

#### [LM Studio](https://lmstudio.ai/)
Closed-source but the most beginner-friendly option — drag-and-drop UI, no command line. Mac / Windows / Linux.

---

### Prompt Library

#### [f/awesome-chatgpt-prompts](https://github.com/f/awesome-chatgpt-prompts) ⭐⭐⭐⭐
★ 161k+ — Community-maintained prompt megacatalog. "Act as a translator / résumé consultant / chef..." in hundreds of roles. **When stuck on how to start, browse here.**

---

## Required Reading

1. [**Anthropic — How to write effective prompts**](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/overview) — readable without code
2. [**OpenAI — Prompting Guide**](https://platform.openai.com/docs/guides/prompt-engineering) — the parallel official doc

If you want to go deeper, see [Stage 2 — Prompt Engineering](../stages/02-prompt-engineering.en.md), which has a more systematic treatment.

## Workflows You Can Build

These are templates — adapt to your situation:

- **Weekly journal**: tell Claude.ai what you did this week, ask it to organize into a journal + key items for next week
- **Email triage**: paste pending emails into Claude every morning, ask it to categorize as "reply now / today / this week / skip"
- **Language learning**: voice-mode conversation with ChatGPT in your target language; have it flag grammar mistakes
- **Batch file cleanup**: have Claude Code rename and reorganize all files in your Downloads folder by date + topic
- **Local privacy chat**: Ollama running qwen2.5:7b — ask medical / legal / financial questions without sending data to the cloud

## Tier Recommendations for Everyday Users

90% of scenarios: **stay at Tier 0** — Claude.ai or ChatGPT web. No install, no payment needed (free tiers are rate-limited but enough for daily use).

5% upgrade to Tier 1: handling local files, retaining long conversation history, connecting MCP servers.

5% upgrade to Tier 2-3: real automation needs (e.g. doing the same thing 100 times daily) or privacy-sensitive data that can't go to the cloud.

**Don't let anyone push you to upgrade prematurely** — Tier 0 is enough for most people. Tiers 2-3 are tools, not status symbols.

## Community Notes

Contributions especially welcome:

- Domain-specific prompt templates (cooking, fitness, language learning)
- Chinese-friendly chat tools (Chinese LLMs, localized wrappers)
- Privacy / safety best practices (what data is OK to send / what isn't)

See [CONTRIBUTING.md](../CONTRIBUTING.md).
