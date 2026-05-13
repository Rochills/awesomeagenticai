# Changelog

Last 14 days of substantive changes. Older history lives in `git log`.

Format: `YYYY-MM-DD · category · 1-line summary (commit-sha)`.

---

## 2026-05-13

- **i18n** · **Russian (ru) translation added as 4th language**. `sync-language-switchers.py` extended to recognize `<file>.ru.md` mirrors with graceful degradation; existing zh-TW / en / zh-Hans switchers stay intact unless a Russian sibling exists, in which case `Русский` is appended (`deb7863`).
- **i18n** · Russian content shipped in 6 waves: W1 README + setup-guide + glossary (`a5d0d3d`); W2 5 audience branches (`3732fd0`); W3 8 stages 00-07 (`dd29d82`); W4 RESOURCES + 7 reference docs incl. 62-entry mcp-skills-catalog (`526e647`); W5 CLI tracks A1-A3 + paper-summary-bot walkthrough (`ccff4f9`); W6 CONTRIBUTING + this entry. Total ~7300 lines of Russian docs across 28 new `.ru.md` files. Translation conventions: keep EN tech terms (agent, tool use, prompt engineering) with optional Russian gloss on first mention; preserve code blocks / URLs / anchor IDs verbatim; reuse `.en.png` diagrams.

## 2026-05-11

- **accessibility** · `resources/setup-guide.md` (3 langs) — addresses the dev-fluency assumption gap that subagent audit flagged across 5 non-dev branches. 5 sections covering API key registration, Python install, hello-world, Claude Code first auth, SKILL.md primer (`3c88b2b`). Plus 15 branch-top callouts on all 5 audience branches. `resources/README.{en,zh-Hans}.md` created for trilingual parity.
- **accessibility** · README — promoted setup-guide pointer to top of Quick Start across all 3 langs (`ad47706`). Was buried in §Related Resources where non-dev visitors hit technical walls before discovering it.
- **accessibility** · setup-guide opens with a 4-tier on-ramp (Web / Desktop / CLI / API) + official download URLs for Claude.ai, ChatGPT, Gemini, Le Chat, Claude Desktop, ChatGPT Desktop, LM Studio (`3c89952`). Replaces the abstract "decide two things" intro so non-dev readers see "just use claude.ai for free" as the first option, not "register API key → install Python".
- **accessibility** · setup-guide adds a 3rd tier between Desktop and CLI: **IDE with built-in AI** (Cursor, Windsurf, Cline, Continue, Roo Code, Zed, GitHub Copilot) with download URLs (`7e14093`). Distinguishes "AI sidekick while you write code" from "agent runs autonomous task in terminal".

## 2026-05-10

- **funnel** · Stage 1 → Stage 2 callouts added across 3 langs to address visible drop in `traffic/popular/paths` (`0ee2a3a`)
- **outreach** · 3 awesome-list targets backfilled into channel-partners matrix from launch-checklist: `travisvn/awesome-claude-skills`, `WangRongsheng/awesome-LLM-resources`, `AiHubCN/Awesome-Chinese-LLM` (`90a6ad1`)
- **outreach** · PR #6135 to `punkpeye/awesome-mcp-servers` — addressed bot `name-check`, replied to non-applicable `glama-check` + `emoji-check` (`81a7313`)
- **content** · Cookbook Recipe 6 — **Local-LLM × CLI Agent walkthrough** (`5855852`). Bridges Stage 1 (local LLM) + Stage 5 (CLI agent) end-to-end. Explicitly notes Claude Code does **not** support local LLM as backend; routes readers to OpenCode / goose / Aider / Hermes instead. Stage 5 + cli-agents-guide also gain matching pointers.
- **catalog** · Hermes Agent (`NousResearch/hermes-agent` ★142k) added as 7th major CLI agent across `cli-agents-guide`, `tracks/cli/A1`, and 5 dependent files (`698f13a`). Differentiator: cloud-VM-native, model-neutral (200+ LLMs via OpenRouter / NIM / GLM / Kimi / etc.), self-improving skill loop.
- **i18n** · `*.zh-CN.md` → `*.zh-Hans.md` migration per BCP 47 / W3C compliance (`21b653d`). 25 files renamed, ~270 markdown lines updated, tooling (`sync-language-switchers.py`, `lint.yml`, `generate-stage5-stack.py`) migrated. Thanks [@xfq](https://github.com/xfq) (W3C i18n lead) for flagging in [#9](https://github.com/WenyuChiou/awesome-agentic-ai-zh/issues/9). Added to CONTRIBUTORS (`868691d`).
- **visuals** · English README hero (`banner.en.png`), Learning Map (`learning-map.en.png`), and Branch Decision Tree (`branch-decision-tree.en.png`) refreshed to ChatGPT-rendered versions (`c7edff8`, `4be6b88`, `6c03c58`).

## 2026-05-09

- **outreach** · Day 1 PR sent: `punkpeye/awesome-mcp-servers#6135`, adding awesome-agentic-ai-zh to `## Tutorials` (`a0dc4d5`). Plan revised after upstream audit caught `hesreallyhim/awesome-claude-code` mid-reorg (Day 2 = issue not PR) (`708259c`).
- **outreach** · 8 channel-partner pitch templates created in `.github/outreach/` plus tracking matrix `.github/channel-partners.md` (`2f63745`). Targets: Datawhale, liyupi, HuggingFace, LangChain (kyrolabs), awesome-claude-code, awesome-mcp-servers, Zhipu, Moonshot.
- **catalog** · §11 中文圈專用 expanded from 2 → 7 entries: `QwenLM/Qwen-Agent`, `coze-dev/coze-studio`, `coze-dev/coze-loop`, `liaokongVFX/LangChain-Chinese-Getting-Started-Guide`, `chatchat-space/Langchain-Chatchat` (`4809039`).
- **funnel** · Stage 0 → Stage 1 callouts added (`3dfe761`).
- **ci** · zh-Hans companion files excluded from zh-TW banned-word audit (closes #7) (`3acc3f2`).

## 2026-05-08

- **content** · `for-teacher` branch expanded with 3-tier teacher AI use-case framework (Chen 2020, Mittal 2024) via @scott0127 PR #6 (`cd1cad4`).
- **content** · Stage 6 unit guide: memory + RAG overview via @scott0127 PR #5.
- **content** · Branch decision tree (zh-Hans) added, English banner added, `for-developer` branch thickened 56 → 138 lines × 3 langs.

## 2026-05-07

- **catalog** · 3 user-flagged gaps filled: `safishamsi/graphify`, `pbakaus/impeccable`, `netease-youdao/LobsterAI` + context-engineering and harness-engineering coverage.
- **content** · `resources/cookbook.md` added with 5 (now 6) step-by-step recipes covering Skill / MCP / Office / NotebookLM / Zotero / Local-LLM workflows.

## 2026-05-06

- **launch** · Repo announced to bilingual community. Star count: 0 → 519 in week one.
- **content** · `learning-map.png` polished, README hero banner placement finalized.

---

## Conventions

- Each commit SHA is clickable: `https://github.com/WenyuChiou/awesome-agentic-ai-zh/commit/<sha>`
- Categories: `content` (stages/branches/tracks) · `catalog` (mcp-skills-catalog entries) · `funnel` (cross-stage navigation) · `visuals` (diagrams/banners) · `i18n` (translation/locale) · `outreach` (channel partners) · `ci` (workflows/lint) · `launch` (one-time events)
- Maintained manually; not auto-generated. Updated alongside substantive commits.
