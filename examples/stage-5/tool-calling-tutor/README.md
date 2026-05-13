> **繁體中文** | [简体中文](./README.zh-Hans.md) | [English](./README.en.md)

# tool-calling-tutor — Claude Code skill

> Skill 用途：當你卡在 tool calling（LLM 不呼叫、args 錯、ReAct loop 跑不停、schema 不知道怎麼寫），自動跳出來幫你 4-symptom 診斷 + 5-step 修法走查。

對應 [Stage 3 — Tool Use & Agent 入門](../../../stages/03-tool-use-and-hello-agent.md)，同時是 [Stage 5 — Claude Code Ecosystem](../../../stages/05-claude-code-ecosystem.md) §5.3 的**自帶 skill 範例**。

## 為什麼這個 skill 存在

Tool calling 是整個 curriculum 最陡的學習曲線——schema 設計、SDK response shape、ReAct loop 三個 mental model 疊在一起。Stage 3 doc 已經把概念講清楚，但**遇到「我這份就是不會跑」的時候、需要互動式 debug**。

這個 skill 補的就是這塊缺：

| 已有資源 | 不足 | 這個 skill 補的 |
|---|---|---|
| `stages/03-tool-use-and-hello-agent.md` | 講 6 個練習、不互動 | 互動式 triage：你卡哪個 symptom？ |
| `resources/schema-design-cheatsheet.md` | 5 條規則 + 5 anti-pattern、prescriptive | 走步驟版：bad → good schema 怎麼 4 步改 |
| `resources/glossary.md` §2 | 1 行定義 | 不重複定義、引用為主 |
| `examples/stage-3/02-06/` | 完整可跑 starter | Skill 指過去當 fork template |

## 雙重用途

1. **學習者用**：安裝後當 personal debug 助手。當你 prompt Claude Code「為什麼 LLM 不呼叫我的 tool」、skill 自動載入、走 4-symptom 診斷。
2. **Stage 5 §5.3 meta-example**：學 SKILL.md 怎麼寫的時候，直接看這份。包含完整 frontmatter（含 trigger phrases + Do NOT use for）、`references/` 設計、`evals/evals.json` 範例。

## 怎麼安裝（30 秒）

### Option A：user 級（所有 project 共用）

```bash
mkdir -p ~/.claude/skills/tool-calling-tutor
cp SKILL.md ~/.claude/skills/tool-calling-tutor/
cp -r references evals ~/.claude/skills/tool-calling-tutor/
```

繁體中文使用者：直接用 `SKILL.md`（canonical 是 zh-TW）。
簡體中文：`cp translations/SKILL.zh-Hans.md ~/.claude/skills/tool-calling-tutor/SKILL.md`
English：`cp translations/SKILL.en.md ~/.claude/skills/tool-calling-tutor/SKILL.md`

### Option B：project 級（只在這個 repo 觸發）

```bash
mkdir -p .claude/skills/tool-calling-tutor
cp SKILL.md references/ evals/ .claude/skills/tool-calling-tutor/
```

### 驗證安裝

重啟 Claude Code、然後 prompt：

```
為什麼 LLM 不呼叫我的 tool？
```

預期：Claude 自動載入 skill、先問你「是 (a)/(b)/(c)/(d) 哪個 symptom」、然後 branch 到對應 reference。

## 包含什麼

```
tool-calling-tutor/
├── SKILL.md                          # 主 skill 檔（zh-TW canonical）
├── README.md / .en.md / .zh-Hans.md  # 你正在看的這份
├── references/
│   ├── debug-flowchart.md            # 4-symptom 診斷流程
│   ├── schema-evolution.md           # bad → good schema 4-step worked example
│   └── sdk-diff.md                   # Anthropic vs OpenAI-compat 並排對照
│   （以上每份都有 .en.md / .zh-Hans.md 翻譯）
├── translations/
│   ├── SKILL.en.md                   # SKILL.md 英文版（給英語使用者裝）
│   └── SKILL.zh-Hans.md              # SKILL.md 簡體版
└── evals/
    └── evals.json                    # 5 個 test cases（promptfoo / 手動皆可）
```

## 跑 evals（選擇性）

```bash
# 不裝 promptfoo 也可以、直接眼看 evals/evals.json 的 input 拿去問 Claude、對照 expected_behavior
cat evals/evals.json
```

如果要 batch 跑、裝 [promptfoo](https://github.com/promptfoo/promptfoo)：

```bash
npm install -g promptfoo
promptfoo eval -c evals/evals.json
```

## 跟其他資源的關係

```
        ┌─────────────────────────────────┐
        │  Stage 3 doc + 練習 1-6 inline   │
        │     (學 tool calling 概念)       │
        └────────────────┬─────────────────┘
                         │
                         ▼
        ┌─────────────────────────────────┐
        │  examples/stage-3/02-06/         │
        │     (完整可跑 starter + test)     │
        └────────────────┬─────────────────┘
                         │ fork template
                         ▼
        ┌─────────────────────────────────┐
        │   你的 tool-calling agent        │
        │   ❓ 卡住了                       │
        └────────────────┬─────────────────┘
                         │ 載入
                         ▼
        ┌─────────────────────────────────┐
        │  tool-calling-tutor skill (這個) │
        │  → 4-symptom triage              │
        │  → references/ deep dive          │
        │  → 路由到 cookbook / Stage 4/7   │
        └─────────────────────────────────┘
```

## 不處理什麼

| 情境 | 路 |
|---|---|
| LangChain / LangGraph / CrewAI / Pydantic AI | Stage 4 |
| 寫 MCP server / client | `resources/cookbook.md` §2 |
| Production observability / cost tracking | Stage 7 |
| 一般 prompt engineering | Stage 2 |

## 延伸

- **改 trigger phrases**：在 SKILL.md frontmatter `description` 加你自己常用的觸發句
- **加你的 case 到 references/**：debug-flowchart 裡開新 Section、把你碰到的 weird case 記下來
- **fork 成你的版本**：這個 skill 設計就是 Stage 5 §5.3 的 meta-example、歡迎 fork

## License

跟 repo 一致（MIT）。Skill body 改寫、fork、商用都 OK。
