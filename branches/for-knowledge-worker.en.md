# For Knowledge Workers — Specialized Branch

> [繁體中文](./for-knowledge-worker.md) | [简体中文](./for-knowledge-worker.zh-Hans.md) | **English** | [Русский](./for-knowledge-worker.ru.md)

> 🚀 **No development background at all?** Start with [`resources/setup-guide.en.md` §A-D](../resources/setup-guide.en.md) (30-45 minutes from zero). Later mentions of "Claude Code", "MCP", and "Skills" in this branch all rely on the §D setup.

> [← Back to main path README](../README.en.md) · Continue here after **Track A's A3** or **Track B's Stage 7**. Apply agentic AI to office / knowledge work.

## Use Cases

- Email triage and drafting
- Meeting notes → action items
- Report aggregation from multiple sources
- Research / market intelligence gathering
- Decision-support workflows

## Curated Projects

> 💡 **Want to wire your AI agent to Notion / Gmail / Outlook / Slack / Excel / Lark?** 57 commonly-used MCP server / Skill integrations in [`resources/mcp-skills-catalog.en.md`](../resources/mcp-skills-catalog.en.md) (grouped by use case). The section below stays focused on workflow / integration-platform-level tools.

### Workflow Tools

#### [n8n](https://github.com/n8n-io/n8n) ⭐⭐⭐⭐
Self-hostable workflow automation platform with built-in AI integration; visual node-based editor.

**Best for**: When you need glue between many SaaS tools (Slack + Gmail + Notion + AI).

---

#### [Make.com](https://www.make.com/) (formerly Integromat)
Hosted workflow automation. Strong AI integration nodes.

---

### Knowledge Worker Skills

#### [obra/superpowers](https://github.com/obra/superpowers) ⭐⭐⭐⭐

Brainstorming, planning, and decision-making skills.

---

### Knowledge Management / Personal AI

#### [khoj-ai/khoj](https://github.com/khoj-ai/khoj) ⭐⭐⭐⭐

| Field | Value |
|---|---|
| Stars | ★ 34k+ |
| License | AGPL-3.0 |

**What it teaches**: Self-hosted "second brain" — chat with web + local docs, schedule automations, build custom agents.

**Best for**: People wanting a self-hosted personal knowledge base + AI assistant.

**Notes**: AGPL-3.0 license (copyleft).

---

#### [lobehub/lobe-chat](https://github.com/lobehub/lobe-chat) ⭐⭐⭐⭐⭐

| Field | Value |
|---|---|
| Stars | ★ 76k+ |
| License | LobeHub Community License (Apache-2.0 base + commercial conditions) |

**What it teaches**: Deployable multi-agent chat platform — plugin marketplace, knowledge bases, team collaboration. One representative option for self-hosted AI workspaces.

**Best for**: Self-hosting a collaborative chat workspace.

**Notes**: Commercial use needs to verify the LobeHub Community License's added conditions.

---

#### [langflow-ai/langflow](https://github.com/langflow-ai/langflow) ⭐⭐⭐⭐

| Field | Value |
|---|---|
| Stars | ★ 147k+ |
| License | MIT |

**What it teaches**: Visual AI-agent development platform — drag-and-drop node design for agent flows, with built-in API + MCP server deployment. More agent-focused than n8n (n8n is generic workflow).

**Best for**: Knowledge workers who'd rather wire nodes than write Python; or anyone designing agent flows for team handoff.

---

#### [Mintplex-Labs/anything-llm](https://github.com/Mintplex-Labs/anything-llm) ⭐⭐⭐⭐⭐

| Field | Value |
|---|---|
| Stars | ★ 60k+ |
| License | MIT |

**What it teaches**: All-in-one private RAG workspace — upload documents, build agents, MCP-compatible, on-device by default. **A self-hosted alternative to NotebookLM**.

**Best for**: Knowledge workers wanting a NotebookLM-style tool, self-hosted, without sending data to the cloud.

---

### MCP Servers Useful for Knowledge Workers

#### Communication MCP servers ⭐⭐⭐⭐
Slack / Gmail / Discord etc. The original Anthropic-hosted reference servers were reorganized in 2025; community-maintained servers now live in [**punkpeye/awesome-mcp-servers**](https://github.com/punkpeye/awesome-mcp-servers#communication) and [**wong2/awesome-mcp-servers**](https://github.com/wong2/awesome-mcp-servers). Browse those lists for current Slack / Gmail / Drive / Calendar MCP servers.

---

## Workflows To Build

- **Daily email triage**: scan inbox → categorize → draft replies for review → mark read
- **Meeting → action items**: transcript → key decisions + action items → assign + post
- **Weekly report aggregation**: pull metrics from N tools → synthesize → email summary
- **Research / market intel**: question → search multiple sources → cross-validate → memo

## Tier Recommendations

Most knowledge workers should start at **Tier 0** (Claude.ai web), upgrade to **Tier 1** (Claude Desktop with MCP) when you need repeat workflows over local/cloud files.

**Tier 3+ (CLI / SDK) is overkill for most knowledge worker tasks.** Don't be talked into it.

## Reading

- [How I Turned Claude Code Into My Personal AI Agent OS](https://aimaker.substack.com/p/how-i-turned-claude-code-into-personal-ai-agent-operating-system-for-writing-research-complete-guide) — knowledge worker case study
