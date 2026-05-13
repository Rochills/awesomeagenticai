> [繁體中文](./README.md) | [简体中文](./README.zh-Hans.md) | **English**

# tool-calling-tutor — Claude Code skill

> What this skill does: when you're stuck on tool calling (LLM won't call, args wrong, ReAct loop runs forever, don't know how to write a schema), it auto-loads to walk you through a 4-symptom diagnostic + 5-step fix.

Pairs with [Stage 3 — Tool Use & Agent Intro](../../../stages/03-tool-use-and-hello-agent.en.md). Also serves as the **bundled skill example** for [Stage 5 — Claude Code Ecosystem](../../../stages/05-claude-code-ecosystem.en.md) §5.3.

## Why this skill exists

Tool calling is the steepest learning curve in the curriculum — schema design + SDK response shape + ReAct loop are three mental models stacked at once. The Stage 3 doc covers the concepts, but **when you hit "this just doesn't work", you need interactive debugging**.

This skill fills that gap:

| Existing resource | Limit | What this skill adds |
|---|---|---|
| `stages/03-tool-use-and-hello-agent.en.md` | Covers 6 exercises, not interactive | Interactive triage: which symptom are you stuck on? |
| `resources/schema-design-cheatsheet.en.md` | 5 rules + 5 anti-patterns, prescriptive | Procedural: bad → good schema in 4 step-by-step iterations |
| `resources/glossary.en.md` §2 | 1-line definitions | Doesn't redefine, references |
| `examples/stage-3/02-06/` | Full runnable starters | Skill points at them as fork templates |

## Dual purpose

1. **For learners**: install as a personal debug assistant. When you prompt Claude Code with "why won't the LLM call my tool", the skill auto-loads and walks the 4-symptom diagnostic.
2. **As a Stage 5 §5.3 meta-example**: when learning to write SKILL.md, study this one directly. Includes full frontmatter (with trigger phrases + Do NOT use for), `references/` design, and `evals/evals.json` example.

## Install (30 seconds)

### Option A: user-level (shared across all projects)

```bash
mkdir -p ~/.claude/skills/tool-calling-tutor
cp SKILL.md ~/.claude/skills/tool-calling-tutor/
cp -r references evals ~/.claude/skills/tool-calling-tutor/
```

English speakers: `cp translations/SKILL.en.md ~/.claude/skills/tool-calling-tutor/SKILL.md` (canonical is zh-TW).
Simplified Chinese: `cp translations/SKILL.zh-Hans.md ~/.claude/skills/tool-calling-tutor/SKILL.md`

### Option B: project-level (only triggers in this repo)

```bash
mkdir -p .claude/skills/tool-calling-tutor
cp SKILL.md references/ evals/ .claude/skills/tool-calling-tutor/
```

### Verify the install

Restart Claude Code, then prompt:

```
Why won't the LLM call my tool?
```

Expected: Claude auto-loads the skill, first asks "are you on symptom (a)/(b)/(c)/(d)", then branches to the matching reference.

## What's inside

```
tool-calling-tutor/
├── SKILL.md                          # main skill file (zh-TW canonical)
├── README.md / .en.md / .zh-Hans.md  # this file
├── references/
│   ├── debug-flowchart.md            # 4-symptom diagnostic
│   ├── schema-evolution.md           # bad → good schema worked example
│   └── sdk-diff.md                   # Anthropic vs OpenAI-compat side-by-side
│   (each has .en.md / .zh-Hans.md translations)
├── translations/
│   ├── SKILL.en.md                   # English version of SKILL.md
│   └── SKILL.zh-Hans.md              # Simplified Chinese version
└── evals/
    └── evals.json                    # 5 test cases (promptfoo or manual)
```

## Run evals (optional)

```bash
# Without promptfoo: just read evals/evals.json, paste each input into Claude, compare with expected_behavior
cat evals/evals.json
```

Batch with [promptfoo](https://github.com/promptfoo/promptfoo):

```bash
npm install -g promptfoo
promptfoo eval -c evals/evals.json
```

## Relationship to other resources

```
        ┌─────────────────────────────────┐
        │  Stage 3 doc + inline 練習 1-6   │
        │     (learn tool-calling concepts) │
        └────────────────┬─────────────────┘
                         │
                         ▼
        ┌─────────────────────────────────┐
        │  examples/stage-3/02-06/         │
        │     (full runnable starters)     │
        └────────────────┬─────────────────┘
                         │ fork template
                         ▼
        ┌─────────────────────────────────┐
        │   your tool-calling agent        │
        │   ❓ stuck                        │
        └────────────────┬─────────────────┘
                         │ skill loads
                         ▼
        ┌─────────────────────────────────┐
        │  tool-calling-tutor skill (this) │
        │  → 4-symptom triage              │
        │  → references/ deep dive          │
        │  → route to cookbook / Stage 4/7 │
        └─────────────────────────────────┘
```

## What this skill does NOT handle

| Situation | Route to |
|---|---|
| LangChain / LangGraph / CrewAI / Pydantic AI | Stage 4 |
| Building MCP server / client | `resources/cookbook.en.md` §2 |
| Production observability / cost tracking | Stage 7 |
| General prompt engineering | Stage 2 |

## Extensions

- **Customize trigger phrases**: add your own catch phrases to SKILL.md frontmatter `description`
- **Add your cases to references/**: open new sections in debug-flowchart for weird cases you've hit
- **Fork it**: this skill is designed as a Stage 5 §5.3 meta-example — forking welcome

## License

Same as repo (MIT). Free to rewrite, fork, use commercially.
