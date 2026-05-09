<div align="right">
  <a href="./README.md">繁體中文</a> | <a href="./README.zh-CN.md">简体中文</a> | <strong>English</strong>
</div>

<div align="center">

![AI Agent Learning Roadmap](resources/diagrams/banner.en.png)

# awesome-agentic-ai-zh

</div>

[![License](https://img.shields.io/badge/license-MIT-blue)](LICENSE)
[![繁中](https://img.shields.io/badge/語言-繁體中文-red)](README.md)
[![简中](https://img.shields.io/badge/語言-简体中文-orange)](README.zh-CN.md)
[![EN](https://img.shields.io/badge/lang-English-blue)](README.en.md)
![GitHub stars](https://img.shields.io/github/stars/WenyuChiou/awesome-agentic-ai-zh?logo=github)
![GitHub forks](https://img.shields.io/github/forks/WenyuChiou/awesome-agentic-ai-zh?logo=github)

> **English companion. The zh-TW [README.md](README.md) is canonical** — content is curated in zh-TW first; this page mirrors it for English readers.

A learning roadmap for agentic AI — **from LLM fundamentals to building multi-agent systems**. Structured 7-stage path: from "what is an LLM, how do tokens work" all the way to multi-agent orchestration and local deployment. Each stage has must-run demos, required reading, and curated projects.

---

## 🎯 Why this exists

If you want to learn AI applications or grow from basics into multi-agent systems — **the most common problem isn't lack of resources, it's not knowing where to start**. Awesome lists in English and Chinese have hundreds of repos but no path; people learning Claude Code, LangGraph, or RAG end up scattered across communities, using different terms, recommending different starter projects.

So we curated **134 high-quality projects** into a "from zero to advanced multi-agent" learning roadmap, organized as **7 stages**. Each stage tells you exactly **what to learn, which exercises to run, which projects to study, and what self-check to pass before advancing**.

After the main path, you go from "**LLM user**" to "**agent system builder**" — capable of designing multi-agent collaboration, writing your own MCP server, and shipping real agent systems.

---

## 📋 Table of Contents

- [🎯 Why this exists](#-why-this-exists)
- [📚 Quick Start](#-quick-start)
- [🗺️ Learning Map (Two Tracks)](#️-learning-map-two-tracks)
- [💡 How to Learn](#-how-to-learn)
- [📚 Related Resources](#-related-resources)
- [🤝 Contributing](#-contributing)
- [🙏 Acknowledgments](#-acknowledgments)
- [🎓 Citation](#-citation)
- [License](#license)

---

## 📚 Quick Start

### Read online
- **[Learning Map (Two Tracks)](#️-learning-map-two-tracks)** — read this section to decide Track A or Track B
- **[Stage 0 Foundations](stages/00-foundations.en.md)** — already know Python / git / API? Skip straight to Stage 1

### Local clone
```bash
git clone https://github.com/WenyuChiou/awesome-agentic-ai-zh.git
cd awesome-agentic-ai-zh
# Start with stages/00-foundations.en.md
```

### ✨ What you get

- 📖 **Fully free** — MIT-licensed, all content open
- 🗺️ **Two learning tracks** — Track A (CLI Power User) for "use existing CLIs"; Track B (Agent Builder) for "build your own". Shared Stages 0-2 foundation.
- 🛠️ **Must-do hands-on exercises** — 1-5 mini projects per stage (specs + success criteria, **you write the code**, not turnkey demos); reading-only doesn't count
- 🎯 **145+ curated projects** — each with star rating, audience, what it teaches, how to run (incl. local LLM runners: Ollama, llama.cpp, LocalAI, MLX)
- 🌏 **Bilingual** — zh-TW canonical, English mirror
- 🎓 **Beyond frameworks: Claude Code ecosystem** — MCP / Skills / Plugins / SDK full stack
- 🔬 **5 specialized branches** — researcher / developer / teacher / knowledge worker / **everyday user**
- ⏱️ **Time commitment, stated upfront** — 14-19 weeks minimum, 5-6 months realistic (5-8 hr/week part-time)

---

## 🗺️ Learning Map (Two Tracks)

![AI Agent Learning Map](resources/diagrams/learning-map.en.png)

After **Stages 0-2 (shared foundations)**, pick a track based on your goal:

- **Track A — CLI Power User**: you want to **USE** existing CLI agents (Claude Code, Codex, OpenCode, Gemini CLI, etc.) to get work done — not build agents from scratch. 3 sub-stages (A1-A3).
- **Track B — Agent Builder**: you want to **BUILD** your own agents — learn frameworks, write ReAct, design multi-agent systems. Stages 3-7 main path.

The two tracks are **not mutually exclusive** — most people start with A to get hands-on, then come back to B for internals (or vice versa). Stage 5 (Claude Code Ecosystem) is used by both tracks.

### Shared Foundations (Stages 0-2)

| Stage | Topic | Key Content | Time |
|---|---|---|---|
| **0** | [Foundations](stages/00-foundations.en.md) | Python · CLI · git · API · JSON | 1-2 wks |
| **1** | [LLM Basics](stages/01-llm-basics.en.md) | tokens · API · model comparison · local LLM | 1 wk |
| **2** | [Prompt Engineering](stages/02-prompt-engineering.en.md) | system prompts · few-shot · CoT | 1-2 wks |

### Track A — CLI Power User (use CLIs to get work done)

| Stage | Topic | Key Content | Time |
|---|---|---|---|
| **A1** | [CLI Agent Intro & Selection](tracks/cli/A1-cli-intro.en.md) | 6-CLI comparison · install · first run | 1 wk |
| **A2** | [CLI Workflow Patterns](tracks/cli/A2-cli-workflow.en.md) | CLAUDE.md · slash commands · multi-step decomposition | 1-2 wks |
| **A3** | [Integration & Production](tracks/cli/A3-cli-production.en.md) | MCP-into-CLI · CI automation · cost / observability | 1-2 wks |

> **Track A total time**: 3-5 weeks (with Stages 0-2: 6-8 weeks). Core reference: [`resources/cli-agents-guide.en.md`](resources/cli-agents-guide.en.md).

### Track B — Agent Builder (build agents from scratch)

| Stage | Topic | Key Content | Time |
|---|---|---|---|
| **3** ⭐ | [Tool Use & Agent Intro](stages/03-tool-use-and-hello-agent.en.md) | function calling · ReAct · 5 hands-on exercises | 2-3 wks |
| **4** | [Agent Frameworks](stages/04-agent-frameworks.en.md) | LangGraph · AutoGen · CrewAI · Smolagents | 2-3 wks |
| **5** ⭐⭐ | [Claude Code Ecosystem](stages/05-claude-code-ecosystem.en.md) | MCP · Skills · Plugins · Marketplace (used by both tracks) | 3-4 wks |
| **6** | [Memory · RAG · Advanced](stages/06-memory-rag.en.md) | vector DB · long-term memory · contextual retrieval | 2 wks |
| **7** | [Multi-Agent · Advanced](stages/07-multi-agent-production.en.md) | multi-agent orchestration · eval · observability · advanced SDK | 2-4 wks |

> **Track B total time**: minimum **14-19 weeks**, realistic **5-6 months** (5-8 hr/week part-time)

> 💡 **Want a concrete cross-stage example?** [Build Your First AI Agent in 7 Steps](walkthroughs/build-first-agent-in-7-steps.en.md) — same Paper Summary Bot traced from Stage 1 through Stage 7, ~350 lines of executable code (**Track B**)

After the main path, pick one of 5 specialized branches. **Not sure which?**

![Branch decision tree](resources/diagrams/branch-decision-tree.en.png)

> 💡 **The Everyday User branch can be read directly without walking the main path** — it's for people who want to use AI without writing code.

| Branch | Best for | Topics |
|---|---|---|
| 🔬 [Researcher](branches/for-researcher.en.md) | Grad students, postdocs, PIs | Lit triage · paper writing · multi-agent review |
| 💻 [Developer](branches/for-developer.en.md) | Software engineers | Cursor · Aider · CLI delegation · code review |
| 🎓 [Teacher](branches/for-teacher.en.md) | Teachers, instructors | Lesson planning · slides · student feedback · privacy / ethics · prompt templates |
| 📊 [Knowledge Worker](branches/for-knowledge-worker.en.md) | Consultants, PMs, analysts | Email · meeting notes · report automation |
| 👥 [Everyday User](branches/for-everyday-users.en.md) | ChatGPT / Claude.ai users | Daily writing · learning · privacy · CLI agent intro |

---

## 💡 How to Learn

Welcome — future agent system builder. Some guidance before you start.

This roadmap balances concepts with hands-on work, helping you **transform from an LLM user into an agent system builder**. It assumes **basic Python**. Before starting:

- **Basic Python** — written functions, used APIs, can read JSON
- **Basic git** — clone, commit, push
- **Motivation to learn** — agents are the fastest-changing area in AI 2025+, and require sustained effort

If anything's missing, do Stage 0; if not, **start at Stage 1**.

The main path has 4 parts:

- **Part 1 (Stages 0-2): Foundations & LLM Basics** — Python / git / API, what's an LLM, prompt design
- **Part 2 (Stages 3-4): Build Your Agent** — from tool use to agents, learn the major frameworks
- **Part 3 (Stage 5): Claude Code Ecosystem** — MCP / Skills / Plugins, the heart of the path
- **Part 4 (Stages 6-7): Advanced Integration** — memory / RAG / multi-agent collaboration

After the main path (14-19 weeks), pick a branch.

The most important advice: **don't skip the hands-on exercises**. Each stage's exercises are "you can't learn this without doing it" — skim past them and you'll get stuck later.

Ready? [Start at Stage 0](stages/00-foundations.en.md).

---

## 📚 Related Resources

The full related-resources block (term definitions + daily-tool MCP/Skill highlights + awesome lists + Chinese-community resources) lives in **[RESOURCES.en.md](RESOURCES.en.md)** so this README stays focused.

Common quick links:

- 📖 **Don't know a term?** (LLM, agent, RAG, token, MCP, Skill, vector DB, …) → [`resources/glossary.en.md`](resources/glossary.en.md) — 30+ common terms, 30–80-word definition each + which stage covers it
- 🔑 **What MCP / Skills / Plugins mean** → [RESOURCES.en.md §three core terms](RESOURCES.en.md#three-core-terms-mcp--skills--plugins)
- 🔌 **Connect to Notion / Obsidian / Excel / GitHub / etc.** → [RESOURCES.en.md §daily-tool integrations](RESOURCES.en.md#daily-tool-integrations-mcp-servers--skills) or full 57-entry catalog [`resources/mcp-skills-catalog.en.md`](resources/mcp-skills-catalog.en.md)
- 🔬 **Research workflow + multi-LLM delegation pair** → [RESOURCES.en.md §research workflow](RESOURCES.en.md#research-workflow-by-the-repo-maintainer)
- 📚 **Topic-based awesome lists / Chinese community** → [RESOURCES.en.md §topic-based](RESOURCES.en.md#topic-based-awesome-lists)

---

## 🤝 Contributing

This repo is an AI learning document — if you've also curated great resources, contributions are very welcome:

- 🐛 **Bug reports** — wrong content, broken links, stale info → open Issue
- 💡 **Suggestions** — missing stage / new project to add → open Issue to discuss
- 📝 **Improvements** — refine existing stage content, fix typos → direct PR
- ✍️ **Add a project** — 1-3 new projects per stage with "why this teaches that stage" rationale
- 🌏 **Translations** — improve the English companion or translate to other languages
- 🌱 **Become a Stage / Branch maintainer** — long-term review of a specific area, see [CONTRIBUTORS.md](CONTRIBUTORS.md)

PR process and style rules: [CONTRIBUTING.md](CONTRIBUTING.md) + [resources/style-guide.en.md](resources/style-guide.en.md).

> Internal phase rollout progress and launch checklist: [`.github/launch-checklist.md`](.github/launch-checklist.md) (maintainer-facing internal doc).

---

## 🙏 Acknowledgments

### Inspiration

- [**Datawhale Hello-Agents**](https://github.com/datawhalechina/hello-agents) — model for systematic agent tutorial structure; inspired our chapter + progress design
- [**Datawhale community**](https://github.com/datawhalechina) — landmark Chinese ML learning community; multiple anchor projects come from them
- [**liyupi/ai-guide**](https://github.com/liyupi/ai-guide) — largest Chinese-language "AI mega-guide" + Vibe Coding tutorial (covers Agent Skills / RAG / MCP / A2A / Harness Engineering). This repo is a "structured roadmap"; ai-guide is a "breadth resource hub" — complementary

### Related projects

Other lists in the same space — useful to browse alongside this repo when hunting for specific tools:

- [`wong2/awesome-mcp-servers`](https://github.com/wong2/awesome-mcp-servers) — categorized MCP server catalog
- [`punkpeye/awesome-mcp-servers`](https://github.com/punkpeye/awesome-mcp-servers) — another MCP server catalog
- [`hesreallyhim/awesome-claude-code`](https://github.com/hesreallyhim/awesome-claude-code) — Claude Code tools & plugins list
- [`nowork-studio/awesome-ai-startups`](https://github.com/nowork-studio/awesome-ai-startups) — curated list of bootstrapped, pre-seed, and angel-funded AI products built by independent founders

These are pure catalogs (browse and pick). This repo is different in that it has a **learning order from Stage 0 all the way to production**.

### Contributors

[![Contributors](https://contrib.rocks/image?repo=WenyuChiou/awesome-agentic-ai-zh)](https://github.com/WenyuChiou/awesome-agentic-ai-zh/graphs/contributors)

New contributors appear above automatically. Full list → [GitHub Contributors](https://github.com/WenyuChiou/awesome-agentic-ai-zh/graphs/contributors).

### Personal

- [@WenyuChiou](https://github.com/WenyuChiou) — Maintainer

---

## 🎓 Citation

If this learning roadmap helps your study or work, please cite:

```bibtex
@misc{awesome_agentic_ai_zh_2026,
  title  = {awesome-agentic-ai-zh: A Structured Learning Roadmap for Agentic AI},
  author = {Chiou, Wenyu},
  year   = {2026},
  url    = {https://github.com/WenyuChiou/awesome-agentic-ai-zh},
  note   = {7-stage learning path from prerequisites to advanced multi-agent systems, with curated projects + hello-X demos. Bilingual (zh-TW / English).}
}
```

---

## 📈 Star History

[![Star History Chart](https://api.star-history.com/svg?repos=WenyuChiou/awesome-agentic-ai-zh&type=Date)](https://star-history.com/#WenyuChiou/awesome-agentic-ai-zh&Date)

---

## License

MIT. Maintained by [@WenyuChiou](https://github.com/WenyuChiou).

<div align="center">
  <p>⭐ If this repo helps you, please give it a Star — it matters for ongoing iteration</p>
</div>
