# For Developers — Specialized Branch

> [繁體中文](./for-developer.md) | [简体中文](./for-developer.zh-Hans.md) | **English** | [Русский](./for-developer.ru.md)

> 🚀 **First time installing Claude Code or writing `CLAUDE.md` / `SKILL.md`?** The quick setup guide is [`resources/setup-guide.en.md` §D-E](../resources/setup-guide.en.md). Skip it if you already know this.

> [← Back to main path README](../README.en.md) · Continue here after **Track A's A3** or **Track B's Stage 7**. Apply agentic AI to coding workflows.

## Use Cases

- AI pair programming (Cursor, Aider, Claude Code, Cline, Continue)
- Code review automation
- Test generation
- Multi-agent coding tasks (planning + execution)
- IDE integration and CI governance

## Curated Projects

> Six major CLI agents (Claude Code / Codex / OpenCode / Gemini CLI / goose / Aider / Hermes Agent) compared side-by-side in [`resources/cli-agents-guide.en.md`](../resources/cli-agents-guide.en.md). New to CLI agents and want step-by-step onboarding → [`tracks/cli/A1-cli-intro.en.md`](../tracks/cli/A1-cli-intro.en.md) (Track A first stop). Looking for MCP / Skill integrations to wire CLI into daily tools (GitHub, Linear, Atlassian, Postgres, Playwright, Figma…) → [`resources/mcp-skills-catalog.en.md`](../resources/mcp-skills-catalog.en.md) (62 entries by category). Below lists only the key entries developers should know.

### Coding Agents

#### [Cursor](https://www.cursor.com/) ⭐⭐⭐⭐⭐
Editor-integrated AI pair programmer. Industry standard for AI-assisted coding.

#### [Aider-AI/aider](https://github.com/Aider-AI/aider) ⭐⭐⭐⭐⭐
★ 44k+ · Apache-2.0 — git-aware CLI pair-programmer. Edits files in your repo directly and writes commits for you. **The open-source reference for "git-native AI editing."** Model-agnostic.

#### [anthropics/claude-code](https://github.com/anthropics/claude-code) ⭐⭐⭐⭐⭐
★ 120k+ — Anthropic's official agentic coding assistant. Skills + plugins ecosystem.

#### [cline/cline](https://github.com/cline/cline) ⭐⭐⭐⭐⭐
★ 61k+ · Apache-2.0 — VS Code extension, autonomous in-IDE agent: tool use, browser, step-by-step approval. **The first pick for VS Code users wanting IDE-native agentic dev.**

#### [continuedev/continue](https://github.com/continuedev/continue) ⭐⭐⭐⭐
★ 33k+ · Apache-2.0 — source-controlled AI checks, enforceable in CI. Represents the **team / governance** angle on coding agents.

#### [OpenHands (formerly OpenDevin)](https://github.com/All-Hands-AI/OpenHands) ⭐⭐⭐⭐
★ 72k+ · MIT — open-source autonomous software development agent. More aggressive design than Aider / Claude Code — agent runs in its own sandbox and commits autonomously. Best for "throw a whole issue at it" scenarios.

#### [block/goose](https://github.com/block/goose) ⭐⭐⭐⭐
★ 43k+ · Apache-2.0 — Open-source, extensible AI agent that goes beyond code suggestions — install / execute / edit / test, with any LLM. Supports multiple LLM providers and MCP, ships as desktop app, CLI, and API. (Repo now resolves to `aaif-goose/goose`.)

#### [RooCodeInc/Roo-Code](https://github.com/RooCodeInc/Roo-Code) ⭐⭐⭐⭐
★ 23k+ · Apache-2.0 — VS Code coding agent with a "**team of specialized modes**" model. Different from Cline's single-agent flow.

### Code Review

#### [obra/superpowers](https://github.com/obra/superpowers) ⭐⭐⭐⭐
20+ battle-tested skills including TDD patterns, debugging, collaboration patterns. Good source for code-review skill design.

## Workflows To Master

- **AI pair programming**: pick one of Claude Code / Cursor / Cline for daily work
- **Git-native AI editing**: run Aider for a week, get used to the "AI edits → commit → review" rhythm
- **AI checks in CI**: use Continue to wire AI checks into your PR pipeline
- **Test generation**: write a skill / prompt that generates pytest tests from a function signature
- **Code review automation**: GitHub Action calling Claude API on every PR

### 3 Concrete Workflow Recipes

**1. AI Pair Programming (daily cadence)**
1. Start a feature → `git checkout -b feature/xxx`
2. Hand the task to Claude Code / Cursor — **make it write a plan first** (don't dive into code)
3. Review the plan, course-correct → only then approve coding
4. After it's done: run tests + lint → review the diff yourself (**don't blind-accept**)
5. Write the commit message yourself, or have AI draft and edit before committing

**2. Aider Git-Native Flow (closest "pair with AI" experience)**
```bash
# Inside the repo
aider --model anthropic/claude-sonnet-4-20250514

# Natural-language ask
> Add a timezone parameter to parse_date in utils.py, default UTC

# Aider edits + commits automatically. To roll back:
> /undo  # undoes the last AI commit
```

**3. PR-time Claude code review (GitHub Action)**

`.github/workflows/claude-review.yml`:
```yaml
on:
  pull_request:
jobs:
  review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
      - name: Run Claude review
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
        run: |
          # Use anthropics/claude-code-action or your own script
          # Get git diff, run prompt, post results back to PR
```
Reference: official [`anthropics/claude-code-action`](https://github.com/anthropics/claude-code-action) GitHub Action.

## Common Pitfalls (Anti-patterns)

| ❌ Don't | ✅ Do instead |
|---|---|
| Let AI push directly to main | Always go through PR → review → merge |
| Blind-accept large refactor diffs | Break into < 50 LOC chunks, review each |
| Hand `.env` / API keys to the AI | Use your tool's exclusion mechanism — Cursor `.cursorignore` / Aider `.aiderignore` / Claude Code `permissions.deny` in `.claude/settings.json` |
| Let AI run shell freely against production code | Sandbox + permission whitelist |
| Take AI-generated tests at face value | Run coverage + intentionally break a unit to see if tests catch it |
| Discover wrong direction after many commits | **Plan-first** mode: review the plan before any coding |

## Tier Upgrade Path

- **Tier 0**: Cursor / Claude Desktop — IDE chat, no agents
- **Tier 1**: Claude Code / Cline / OpenCode — CLI with file-system access and CLAUDE.md, still human-in-the-loop
- **Tier 2**: Author your own Skills + MCP servers — package your dev workflow as shared team skills
- **Tier 3**: Auto-running agents in CI + production observability — graduates to [Stage 7](../stages/07-multi-agent-production.en.md) territory

> Tier 0-1 covers ~90% of developers. **Validate ROI before going Tier 2+**: only worth the investment if your team is large, flows are repetitive, and incidents are irreversible.

## Other Branches Also Apply

Branches that overlap heavily with developers:

- **Doing ML research / writing papers** → [Researcher branch](./for-researcher.en.md)
- **Wire Notion / Linear / Atlassian / Postgres / Figma into your CLI** → [`resources/mcp-skills-catalog.en.md`](../resources/mcp-skills-catalog.en.md)
- **Author your own Skill / MCP server** → [Stage 5](../stages/05-claude-code-ecosystem.en.md) + [`resources/cookbook.en.md`](../resources/cookbook.en.md)
- **Schema design details** → [`resources/schema-design-cheatsheet.en.md`](../resources/schema-design-cheatsheet.en.md)
- **CLI from zero** → [Track A](../tracks/cli/A1-cli-intro.en.md) (A1 → A2 → A3)

## Community Note

Contributions especially welcome:

- IDE-specific config templates (Cursor `.cursorrules`, Claude Code `CLAUDE.md` for Python / Go / Rust, etc.)
- Language-specific Skills (Python / TypeScript / Rust / Go best-practice patterns)
- CI / pre-commit hook integration case studies
- **Multi-developer team governance** — sharing Skills across devs, permission design, cost tracking

See [CONTRIBUTING.md](../CONTRIBUTING.md).
