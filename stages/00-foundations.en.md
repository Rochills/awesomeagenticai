# Stage 0 — Foundations

> [繁體中文](./00-foundations.md) | [简体中文](./00-foundations.zh-Hans.md) | **English** | [Русский](./00-foundations.ru.md)


⏱ **Time estimate**: 1-2 weeks (~5-15 hours, can skip if you have these)

> 💡 **Don't recognize a term?** Check [`resources/glossary.en.md`](../resources/glossary.en.md) for a 30-second definition. Stage 0 doesn't lean on much jargon, but the next stages do.
> 🗺️ **Want the big picture of the agent landscape first** (why some agents live in a terminal, some in Telegram, some on a Jetson board)? → [`resources/agent-paradigms.en.md`](../resources/agent-paradigms.en.md) (5 agent paradigms, ~10 min read)

## When to skip this stage

If you can:
- Write a Python function that calls a public API and parses JSON response
- Use git to clone, commit, push, and resolve a basic merge
- Use the command line on your OS (cd, ls, mkdir, run a script)
- Read a YAML / JSON file without confusion

→ **Skip directly to [Stage 1](01-llm-basics.md)**.

If you can't, work through this stage. Don't skip — every later stage assumes these.

## 📌 Learning Goals

- Write Python: functions, classes, async/await basics
- Use git: clone, branch, commit, push, basic conflict resolution
- Use REST APIs: send GET/POST, parse JSON, handle auth headers
- Read & write YAML and JSON

## 🛠 Hands-on Exercises

- **Exercise: Python** — write a Python script that calls https://api.github.com/users/torvalds and prints follower count
- **Exercise: git** — clone any public repo, make a commit, push to your fork
- **Exercise: CLI** — make a small directory tree with the command line (macOS / Linux: `mkdir project && cd project && mkdir src tests docs`; Windows PowerShell: `New-Item -ItemType Directory -Path project,project\src,project\tests,project\docs`), run a Python script, redirect output to a file
- **Exercise: YAML** — read a `.yaml` config file in Python, modify a value, write it back
- **Exercise: API auth** — at [github.com/settings/tokens](https://github.com/settings/tokens) generate a personal access token (minimal scope: `read:user`), call the auth-required `https://api.github.com/user` endpoint, observe 401 (no token) vs 200 (with token). Note: real production agents always use API auth — do this exercise

## 🎯 Curated Resources (not full projects, just learning material)

### Python
- [**Python Crash Course**](https://github.com/ehmatthes/pcc_3e) — book + exercises (paid book, free exercises)
- [**Real Python tutorials**](https://realpython.com/) — high-quality free articles
- [**Corey Schafer YouTube**](https://www.youtube.com/c/Coreyms) — video tutorials, beginner to advanced, very clear delivery
- [**Boot.dev**](https://www.boot.dev/) — interactive Python course (partially free)
- [**runoob.com Python tutorial**](https://www.runoob.com/python3/python3-tutorial.html) — Chinese-language Python intro reference

### Git
- [**Pro Git book**](https://git-scm.com/book/en/v2) — free, full-length reference
- [**Atlassian Git Tutorials**](https://www.atlassian.com/git/tutorials) — workflow-focused
- [**Oh Shit, Git!?!**](https://ohshitgit.com/) — when things go wrong
- [**git-flight-rules**](https://github.com/k88hudson/git-flight-rules) — "I screwed up X, how do I undo?" — popular cheat sheet

### CLI / Shell
- [**The Art of Command Line**](https://github.com/jlevy/the-art-of-command-line) — beginner-to-advanced command-line skills (180k+ stars, multi-language)
- [**Learn Shell**](https://www.learnshell.org/) — interactive Bash tutorial
- [**explainshell.com**](https://explainshell.com/) — break down any shell command (debug life-saver)

### REST APIs
- [**MDN — HTTP**](https://developer.mozilla.org/en-US/docs/Web/HTTP) — protocol fundamentals
- [**Postman Learning Center**](https://learning.postman.com/) — API exploration tool
- [**HTTPie**](https://github.com/httpie/cli) — friendlier-than-`curl` command-line HTTP client

### YAML / JSON
- [**YAML official site**](https://yaml.org/) — spec
- [**JSON crash course**](https://www.json.org/json-en.html) — official quick guide
- [**jq**](https://github.com/jqlang/jq) — command-line JSON processor (heavy use in agent workflows)

## Why this stage exists

Most "AI agent" tutorials assume you already have these. If you don't, you'll get blocked at random places (tools requires async; configs are YAML; SDK setup needs git). One week investing here saves 10+ weeks of frustration later.

---

> ✅ **Done with Stage 0?** Next, [**Stage 1 — LLM Fundamentals**](01-llm-basics.en.md) takes 5-8 hours to walk you through your first LLM API call, the meaning of token / context window / temperature, and how to estimate real task cost via per-token pricing. **Keep going →**
