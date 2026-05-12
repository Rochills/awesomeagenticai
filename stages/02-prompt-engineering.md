# Stage 2 — Prompt Engineering

> **繁體中文** | [简体中文](./02-prompt-engineering.zh-Hans.md) | [English](./02-prompt-engineering.en.md) | [Русский](./02-prompt-engineering.ru.md)

⏱ **時間估算**：1-2 週（約 5-12 小時）

> 👋 **從 [Stage 1](01-llm-basics.md) 來的**：好，你會呼叫 API 了——這 5-12 小時：寫出可重用的結構化 prompt、用 few-shot 跟 chain-of-thought 解難題、用 eval 量化 prompt 改善幅度。**直接從這裡開始的**：先確認你會呼叫 LLM API、會用 token 算成本——做不到請先回 [Stage 1](01-llm-basics.md)。

> 💡 用語不熟（prompt / few-shot / CoT / system prompt⋯）→ 翻 [`resources/glossary.md`](../resources/glossary.md)。

## 📌 學習目標

走完這個階段後你會：
- 寫出結構化 prompt（角色 + 任務 + 格式 + 範例）
- 應用 few-shot prompting，並知道什麼時候有用
- 在推理任務上使用 chain-of-thought（CoT）
- 反覆迭代修改一個 prompt 並衡量改善
- 看出什麼時候 prompt 已經到極限了（這時你需要 tool / agent）

## 🚪 進入條件

你應該已經：
- 會呼叫 LLM API（Stage 1）
- 會解析 / 走訪 API 回應

## 📚 必修閱讀

1. [**Anthropic Prompt Engineering Guide**](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/overview) — 官方，整理得不錯
2. [**OpenAI Prompt Engineering**](https://platform.openai.com/docs/guides/prompt-engineering) — OpenAI 觀點
3. [**dair-ai Prompt Engineering Guide**](https://www.promptingguide.ai/) — 學術風，深入
4. [**Anthropic — Prompting Best Practices**](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/be-clear-and-direct) — 直接清楚

## 🛠 動手練習

### 練習：System Prompt
同樣的 user message，三個不同的 system prompt。觀察人格 / 輸出格式怎麼變。

### 練習：Few-Shot
挑一個分類任務。先用 0-shot 跑，再用 3-shot 跑。量一下準確率差多少。

### 練習：CoT
挑一個數學文字題，比較：
- 純 prompt
- 純 prompt + 「Let's think step by step」
- 純 prompt + 一個展示 CoT 的範例

### 練習：Iterative Refinement
拿一個模糊的 prompt，refine 5 次。把每一輪記下來。觀察哪些改動會提升品質。

## 🎯 精選 Projects

### [dair-ai/Prompt-Engineering-Guide](https://github.com/dair-ai/Prompt-Engineering-Guide)

| 欄位 | 內容 |
|---|---|
| Stars | ★ 60k+ |
| License | MIT |
| 推薦度 | ⭐⭐⭐⭐⭐ |

**教什麼**：從基礎到進階（CoT、ToT、ReAct、RAG）的端到端 prompt engineering。學術風但實用。

**適合誰**：當參考用。先大致掃過一次，需要某個技巧時再回來查。

---

### [f/awesome-chatgpt-prompts](https://github.com/f/awesome-chatgpt-prompts)

| 欄位 | 內容 |
|---|---|
| Stars | ★ 130k+ |
| License | CC0 |
| 推薦度 | ⭐⭐⭐ |

**教什麼**：上百個角色型 prompt。「Act as a [角色]...」的模式。

**適合誰**：卡關時找靈感。不要照抄——把模式拿出來改寫。

---

### [PromptingGuide.ai](https://www.promptingguide.ai/)

**教什麼**：跟 dair-ai GitHub 同樣的內容，但做成網站、有可以跑的範例。

**適合誰**：手機閱讀。

---

### [microsoft/prompt-engine](https://github.com/microsoft/prompt-engine)

| 欄位 | 內容 |
|---|---|
| 推薦度 | ⭐⭐⭐ |

**教什麼**：管理大量 prompt 的 TypeScript library（樣板、對話歷史）。

**適合誰**：開始要在 production 管很多 prompt 時。

---

### [microsoft/promptflow](https://github.com/microsoft/promptflow)

| 欄位 | 內容 |
|---|---|
| Stars | ★ 10k+ |
| 推薦度 | ⭐⭐⭐ |

**教什麼**：視覺化 prompt 設計 + 評估工具。

**適合誰**：以 prompt 為主、需要 eval 的團隊型應用。

---

### [GoogleCloudPlatform/generative-ai](https://github.com/GoogleCloudPlatform/generative-ai)

| 欄位 | 內容 |
|---|---|
| 推薦度 | ⭐⭐⭐ |

**教什麼**：Google Cloud 的 prompting cookbook（notebook，PaLM/Gemini 為主）。

**適合誰**：用 Google 技術棧時的跨廠商觀點。

---

### [Anthropic Cookbook — Prompt patterns](https://github.com/anthropics/anthropic-cookbook)

Stage 1 已經提過。這裡特別推 `misc/prompt_caching.ipynb` 跟 `multimodal/` 系列 notebook，會教進階 prompting 模式。

---

### [stanfordnlp/dspy](https://github.com/stanfordnlp/dspy)

| 欄位 | 內容 |
|---|---|
| 語言 | Python |
| Stars | ★ 34k+ |
| License | MIT |
| 推薦度 | ⭐⭐⭐⭐⭐ |

**教什麼**：把 prompt 當 code 寫——定義 signature 跟 module、用 compiler / teleprompter 自動最佳化 prompt，不用手刻 f-string。Stanford NLP 出品，是 Stage 2 → Stage 3 的橋。

**適合誰**：跑完 dair-ai 的指南、開始問「我要怎麼把 prompt 規模化（不是再多 hard-code）」的人。

**備註**：是 framework 不是 tutorial，學習門檻比 prompt-engineering-guide 高。建議搭配官方 tutorial 網站 dspy.ai 一起讀。

---

### [NirDiamant/Prompt_Engineering](https://github.com/NirDiamant/Prompt_Engineering)

| 欄位 | 內容 |
|---|---|
| 語言 | Python / Jupyter |
| Stars | ★ 7k+ |
| License | NOASSERTION（自訂條款，研究 / 非商用為主，使用前讀條款） |
| 推薦度 | ⭐⭐⭐⭐ |

**教什麼**：22 種 prompt engineering 技巧的可執行 Jupyter notebook（zero-shot → CoT → ReAct → constitutional），2025 年的更新內容，比 dair-ai 更動手。

**適合誰**：偏好「邊跑邊學」的人。每個技巧都有獨立 notebook，挑感興趣的看。

---

## 🔭 進階：context engineering（不是 prompt engineering 了）

當你發現「**單一 prompt 已經 cover 不了**」——要動態組 system prompt + 拉 memory + 塞 retrieved chunks + 接多個 tool definitions——這已經不叫 prompt engineering，叫 **context engineering**。是 prompt engineering 的下一層。

**這個 stage 不用學完它**，只是給個方向性提示：

- 在 [Stage 6（Memory · RAG）](06-memory-rag.md) 會碰到（什麼資料塞進 prompt）
- 在 [Stage 7（Multi-Agent · Production）](07-multi-agent-production.md) 完整面對（context window 預算、memory 階層、observability）

延伸閱讀（不必修、未來想深挖時看）：

- [`Meirtz/Awesome-Context-Engineering`](https://github.com/Meirtz/Awesome-Context-Engineering)（★ 3k+）——從 prompt engineering 一路推到 production agent 的 survey
- [`Windy3f3f3f3f/how-claude-code-works`](https://github.com/Windy3f3f3f3f/how-claude-code-works)（★ 2k+）——Claude Code 內部解析，含 context engineering 章節

## ✅ 進 Stage 3 前的自我檢查

你能不能：
- [ ] 寫一個有 system message + user message + 3 個範例 message 的 prompt（few-shot）
- [ ] 示範 CoT 在某個推理任務上提升準確率
- [ ] 反覆 refine 一個 prompt 5 次，每一版都留下記錄
- [ ] 看出 prompt 不是對的工具的時候（這時要用 tool use）

如果可以 → 進 [Stage 3 — Tool Use & Agent 入門](03-tool-use-and-hello-agent.md)。這是最重要的一個階段——prompt 不要急著跳過去，但也不要卡在這裡。
