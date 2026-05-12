# A3 — Integration & Production

> [繁體中文](./A3-cli-production.md) | [简体中文](./A3-cli-production.zh-Hans.md) | **English** | [Русский](./A3-cli-production.ru.md)

> [← A2 — CLI Workflow Patterns](A2-cli-workflow.en.md) · **Track A: CLI Power User** — Stop 3 (final)

⏱ **Time estimate**: 1-2 weeks (~8-15 hours)

After your CLI runs smoothly, the next step: **wire it into your real workflow**. MCP server integration, CI automation, cost / observability. After this stop, the CLI is no longer just your personal tool — it's part of your team's workflow.

## 📌 Learning Goals

- Connect 1-3 MCP servers to your CLI (Slack / Gmail / internal API / DB)
- Set up GitHub Actions to auto-run Claude Code (PR review, release notes, etc.)
- Add observability (trace, cost, latency) to CLI workflows
- Plan a cost budget — know roughly what a big task costs in tokens

## 📚 Required Reading

1. [**Stage 5.2 — MCP (Model Context Protocol)**](../../stages/05-claude-code-ecosystem.en.md#52--mcp-model-context-protocol-foundation) — MCP concept and basics
2. [**Anthropic — Prompt Caching**](https://www.anthropic.com/news/prompt-caching) — the key trick for 90% cost reduction
3. [**Stage 7 — Observability section**](../../stages/07-multi-agent-production.en.md#observability) — langfuse / Helicone / weave
4. [**`resources/cli-agents-guide.en.md`** §"Common pitfalls"](../../resources/cli-agents-guide.en.md) — most common production issues with CLIs

## 🛠 Hands-on Exercises

### Exercise CLI-9: MCP server connected to CLI
Following [Stage 5.2 Exercise: MCP client](../../stages/05-claude-code-ecosystem.en.md#hello-x), connect at least one useful MCP server to your CLI:
- `filesystem` server → let the CLI read files outside its default scope
- `github` server → let it read PRs / issues directly
- Custom server → connect your internal API / DB

Success: in a CLI conversation, ask "does my PR have conflicts?" and have the CLI answer via MCP (without you opening a browser).

### Exercise CLI-10: GitHub Actions + CLI
Write `.github/workflows/cli-review.yml`:
- Trigger: PR opened / synchronize
- Run: in the GH Actions runner, execute Claude Code (or Codex), feed it `git diff` + your `.claude/commands/review.md`
- Output: PR comment

Success: open a new PR, see a review comment within 1-2 minutes.

> Starting points: Anthropic's official [`claude-code-action`](https://github.com/anthropics/claude-code-action); Codex has GitHub App and CLI modes.

### Exercise CLI-11: Cost tracking
Run a daily task. **Predict** the token usage first, then actually run it and check the usage. The gap is usually big (you typically underestimate).
- Math: input tokens + output tokens × model price each
- Connect langfuse or Helicone ([Stage 7 Observability](../../stages/07-multi-agent-production.en.md#observability)) for tracing
- Observe: which sub-task consumes the most tokens? Are you sending unnecessary long context?

### Exercise CLI-12: Skill / plugin team sharing
Package your `.claude/commands/` and `CLAUDE.md` into a plugin, publish to internal marketplace or GitHub. Teammates `claude plugin install` and get the same workflow.
- Skill / plugin details in [Stage 5.3 + 5.4](../../stages/05-claude-code-ecosystem.en.md)
- Template: [anthropics/claude-plugins-official](https://github.com/anthropics/claude-plugins-official)

## 🎯 Curated Projects

### MCP server collection (CLI-friendly)

> 💡 **Looking for MCPs that connect to daily tools** (Notion / Obsidian / Excel / Postgres / Playwright / Slack / Linear / Figma…): see [`resources/mcp-skills-catalog.en.md`](../../resources/mcp-skills-catalog.en.md) — 62 entries grouped by category, each with stars / license / audience. The list below is for "writing your own MCP server / finding reference implementations".

#### [modelcontextprotocol/servers](https://github.com/modelcontextprotocol/servers) ⭐⭐⭐⭐⭐
★ 85k+ — Official reference servers. filesystem, github, sqlite, git, time, fetch, memory, sequential-thinking.
> See [Stage 5.2](../../stages/05-claude-code-ecosystem.en.md#52--mcp-model-context-protocol-foundation).

#### [wong2/awesome-mcp-servers](https://github.com/wong2/awesome-mcp-servers)
Community MCP server catalog. 150+ servers categorized.

---

### CI Integration Patterns

#### [anthropics/claude-code-action](https://github.com/anthropics/claude-code-action)
Official GitHub Action template. PR review, issue triage, auto-fix.

#### [continuedev/continue](https://github.com/continuedev/continue) ⭐⭐⭐⭐
★ 33k+ — Wire AI checks into CI; enforce in PR pipeline.
> Full intro in [`branches/for-developer.en.md`](../../branches/for-developer.en.md).

---

### Observability + Cost

#### [langfuse/langfuse](https://github.com/langfuse/langfuse) ⭐⭐⭐⭐⭐
★ 26k+ — Open-source LLM observability. Trace, cost, sessions in one place.
> See [Stage 7 Observability](../../stages/07-multi-agent-production.en.md#observability).

#### [Helicone](https://github.com/Helicone/helicone) ⭐⭐⭐⭐
★ 5k+ — Proxy-based monitoring. Just change `base_url` and you get logging + caching.

#### [promptfoo/promptfoo](https://github.com/promptfoo/promptfoo) ⭐⭐⭐⭐⭐
★ 20k+ — Eval framework. Run regression tests before promoting CLI workflows to production.
> See [Stage 7 Eval](../../stages/07-multi-agent-production.en.md#evaluation-frameworks).

---

### Production CLI Workflow Templates

#### [obra/superpowers](https://github.com/obra/superpowers) ⭐⭐⭐⭐
★ 178k+ — Production-ready skill collection. See how someone else does a complete CLI workflow.

#### [obra/superpowers-marketplace](https://github.com/obra/superpowers-marketplace)
★ 900+ — Minimal marketplace template. Reference when packaging your team's CLI workflow.

## ✅ Track A Full Self-Check

Can you:
- [ ] Have at least 1 MCP server connected to your daily CLI
- [ ] Have at least 1 CI workflow auto-running a CLI agent
- [ ] State the rough token / cost / latency for some specific task you run
- [ ] Packaged your CLAUDE.md / commands at least once (even just for yourself)
- [ ] Know which tasks deserve observability and which don't

If yes → **Track A complete**. Pick a [specialized branch](../../README.en.md#️-learning-map-two-tracks) and continue (researcher / developer / teacher / knowledge-worker / everyday-users).

If you want to go deeper into "**how to write your own CLI agent**" (not use existing) → jump to [Track B Stage 3](../../stages/03-tool-use-and-hello-agent.en.md). Track A and Track B are complementary.

## 💡 What's Next

After Track A you're a CLI power user. Next phase choices:

1. **Deepen CLI workflow** (keep refining your setup)
   - Subscribe to Anthropic / OpenAI changelogs
   - Quarterly review of [`resources/cli-agents-guide.en.md`](../../resources/cli-agents-guide.en.md) for new tools
   - Share CLAUDE.md / skills with your team

2. **Cross to Track B** (learn to write your own agent)
   - Stage 3-4: tool use + frameworks
   - Stage 5: deep dive into Claude Code internals
   - Stage 7: write your own multi-agent system

3. **Walk a specialized branch** (apply CLI to a specific domain)
   - Researcher / developer / knowledge-worker / teacher / everyday-users
   - Each branch uses what you learned in Track A
