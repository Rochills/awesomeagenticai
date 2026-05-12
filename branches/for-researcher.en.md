# For Researchers — Specialized Branch

> [繁體中文](./for-researcher.md) | [简体中文](./for-researcher.zh-Hans.md) | **English** | [Русский](./for-researcher.ru.md)

> 🚀 **First time installing Python or creating an API key?** Start with [`resources/setup-guide.en.md` §A-C](../resources/setup-guide.en.md). This branch assumes you can run Python scripts, have an API key, and can use git.

> [← Back to main path README](../README.en.md) · Continue here after **Track A's A3** or **Track B's Stage 7**. Apply agentic AI to research workflows.

## Use Cases

- Literature triage and matrix building
- Paper memory extraction (claims, figures, citations)
- Multi-agent paper review (peer review patterns)
- NotebookLM brief verification
- Reference management automation

## Curated Projects

> 💡 **Want to wire Claude Code into NotebookLM, Obsidian, Notion, Excel, PDF, Excalidraw, and other research tools?** 62 integrations in [`resources/mcp-skills-catalog.en.md`](../resources/mcp-skills-catalog.en.md) (grouped by use case). The section below keeps research-specific tools and marketplaces.

### Research Workflow Marketplaces

#### [flonat/claude-research](https://github.com/flonat/claude-research) ⭐⭐⭐

Claude Code infrastructure for PhD researchers — skills, agents, hooks, rules for academic workflows. Strong LaTeX/bibliography focus.

---

### Literature RAG / Q&A

#### [Future-House/paper-qa](https://github.com/Future-House/paper-qa) ⭐⭐⭐⭐⭐

| Field | Value |
|---|---|
| Stars | ★ 8k+ |
| License | Apache-2.0 |

**What it teaches**: High-accuracy RAG over PDF documents, with grounded sentence-level citations on every answer.

**Best for**: Researchers writing literature reviews who need "every answer must be traceable to its source." More rigorous than generic RAG.

---

#### [assafelovic/gpt-researcher](https://github.com/assafelovic/gpt-researcher) ⭐⭐⭐⭐

| Field | Value |
|---|---|
| Stars | ★ 27k+ |
| License | Apache-2.0 |

**What it teaches**: Autonomous deep-research agent — planner + multi-source crawl + report synthesis. Give it a research topic, get a markdown / PDF brief out.

**Best for**: Researchers who need to quickly scope new topics and produce research briefs.

---

### Outline & Writing

#### [stanford-oval/storm](https://github.com/stanford-oval/storm) ⭐⭐⭐⭐

| Field | Value |
|---|---|
| Stars | ★ 28k+ |
| License | MIT |

**What it teaches**: Multi-perspective outline-then-write pipeline — agent first generates an outline from multiple angles, then expands into Wikipedia-style articles. From Stanford OVAL.

**Best for**: Learning **outline-driven writing**. Great for producing topic briefs from scratch; the closest open-source analog to NotebookLM's structured report flow.

**Notes**: Last push was over 6 months ago — verify the latest commit date before relying on it.

---

#### [kaixindelele/ChatPaper](https://github.com/kaixindelele/ChatPaper) ⭐⭐⭐⭐⭐ (Chinese readers)

| Field | Value |
|---|---|
| Language | Chinese + Python |
| Stars | ★ 19k+ |
| License | NOASSERTION (custom non-commercial) |

**What it teaches**: Full arXiv workflow for Chinese researchers — paper summary + translation + polishing + review-response generation. Maintained by a Chinese team; defaults are friendly to Chinese-language workflows.

**Best for**: Chinese graduate students looking for a Chinese-friendly entry-level paper workflow tool.

**Notes**: License is custom non-commercial — read the original terms before any use; common practice is research / personal use, but you should verify the terms yourself.

---

### Citation Manager Integrations

#### [MuiseDestiny/zotero-gpt](https://github.com/MuiseDestiny/zotero-gpt) ⭐⭐⭐⭐

| Field | Value |
|---|---|
| Stars | ★ 7k+ |
| License | AGPL-3.0 |

**What it teaches**: A Zotero LLM plugin — chat with your library, summarize selections, generate inline notes.

**Best for**: Heavy Zotero users who want AI inside their reading workflow without switching tools.

**Notes**: AGPL-3.0 license (copyleft) — derivative products that ship modifications must follow the terms.

---

### Research Workflow Skills (by the repo maintainer)

> Skills / workspaces the repo maintainer [@WenyuChiou](https://github.com/WenyuChiou) (Lehigh CEE PhD candidate) uses daily for research. Listed here so other researchers can pick them up directly. Full entries in [`resources/mcp-skills-catalog.en.md` §13-§14](../resources/mcp-skills-catalog.en.md#13-research-workflow-skills-academic--paper--lit).

#### [WenyuChiou/ai-research-skills](https://github.com/WenyuChiou/ai-research-skills) ⭐⭐⭐⭐⭐

★ 60 · MIT — 14 Claude Code skills covering the full research pipeline (lit triage, research design, project context, manuscript writing, multi-AI delegation), packaged as a 5-plugin marketplace. One command installs everything.

#### [WenyuChiou/research-hub](https://github.com/WenyuChiou/research-hub) ⭐⭐⭐⭐

★ 14 · MIT — Zotero + Obsidian + NotebookLM triple-workspace integration with CLI / MCP / REST / dashboard interfaces. A must-see for researchers using all three.

#### [WenyuChiou/zotero-skills](https://github.com/WenyuChiou/zotero-skills) ⭐⭐⭐⭐

★ 16 — Zotero CLI skill: search / add / classify / annotate. Complementary to zotero-gpt (chat inside Zotero); this one lets Claude Code operate Zotero from outside.

#### [WenyuChiou/academic-writing-skills](https://github.com/WenyuChiou/academic-writing-skills) ⭐⭐⭐

★ 2 · MIT — rigorous academic paper writing / revision / submission skill. Automates banned-word audit, figure-text coupling, submission checklist. Per-paper journal_format / style_overrides for customization.

#### [WenyuChiou/codex-delegate](https://github.com/WenyuChiou/codex-delegate) ⭐⭐⭐⭐⭐ + [WenyuChiou/gemini-delegate-skill](https://github.com/WenyuChiou/gemini-delegate-skill) ⭐⭐⭐⭐

★ 57 + ★ 34 · MIT — Multi-LLM delegation skill pair. Research scenario: Claude as planner + Codex executes implementation (code / figures / tables) + Gemini drafts long form (Chinese reports, English paper sections). Practical implementation of the Stage 7 multi-agent concept.

---

### Multi-Agent for Research

#### [langchain-ai/open_deep_research](https://github.com/langchain-ai/open_deep_research) ⭐⭐⭐⭐⭐

| Field | Value |
|---|---|
| Stars | ★ 11k+ |
| License | MIT |

**What it teaches**: Open-source Deep Research — supports both single-agent and supervisor + multi-researcher architectures (the multi-agent path currently lives in `src/legacy/`), parallel search, citation-grounded report synthesis. A solid reference for "LLM agent that auto-produces a cited brief."

**Best for**: Researchers building "agent auto-generates a cited brief" workflows. A solid open-source pick when you want a maintained reference implementation.

**Notes**: Depends on LangGraph + search tools (API key required).

---

#### [SakanaAI/AI-Scientist-v2](https://github.com/SakanaAI/AI-Scientist-v2) ⭐⭐⭐⭐

| Field | Value |
|---|---|
| Stars | ★ 6k+ |
| License | The AI Scientist Source Code License (source-available, non-commercial + manuscript-disclosure clause) |

**What it teaches**: End-to-end multi-agent science loop: ideate → code → experiment → write → peer-review. Sakana AI's research implementation of "AI writes a full ML paper."

**Best for**: Researchers who want to see "what does a swarm of agents running a full research lifecycle look like." Architecture reference, not a production tool.

**Notes**: Outputs are demo-level (not field-ready), ML/CS-domain bias. License is a custom source-available term (with a manuscript-disclosure clause) — read the LICENSE file before use.

---

> Still missing: actively-maintained peer-review automation, conference-review pipelines. If you've built or know of one, please open a PR.

## Required Reading

1. [The Effortless Academic — Claude Code beginner guides](https://effortlessacademic.com/claude-code-and-cowork-for-academics-beginner-guide-part-1/)
2. [Pedro Sant'Anna — Researcher setup guide](https://paulgp.substack.com/p/getting-started-with-claude-code)

## Workflows To Master

- **Literature triage**: use `paper-qa` for grounded Q&A over your PDF library, then `gpt-researcher` to auto-generate briefs, output to Obsidian / Notion
- **Outline-driven writing**: use `storm` to auto-generate multi-perspective outlines from a topic, then expand to formal sections by hand
- **Chinese paper workflow**: use `ChatPaper` for summary / translation / polishing, then human review
- **Zotero in-app AI**: install `zotero-gpt` and ask questions or summarize selections directly in your reading flow
