# Stage 3 — Tool Use & Agent 入門 ⭐

> **繁體中文** | [简体中文](./03-tool-use-and-hello-agent.zh-Hans.md) | [English](./03-tool-use-and-hello-agent.en.md) | [Русский](./03-tool-use-and-hello-agent.ru.md)

⏱ **時間估算**：2-3 週（約 10-20 小時）

> 💡 用語密集（agent / tool use / function calling / ReAct / structured output⋯）→ 翻 [`resources/glossary.md` §2](../resources/glossary.md#2-agent--工具使用)。

這是整個學習路線最關鍵的一站。**你建過一個 agent 才算真懂 agent — 動手練習 不能跳。**

## 📌 學習目標

完成這個 stage 後你會：
- 講得出為什麼 LLM 需要 tools（它不是萬能的，而且文字以外的事它都做不了）
- 定義一個 tool schema，並讓 LLM 呼叫它
- 從零（不靠任何 framework）寫出一個單步 ReAct agent
- 寫出多步 ReAct agent，並讓它自己判斷何時該停
- 分得出哪種問題該用 tool use、哪種純 prompt 就夠

## 🚪 進入條件

你應該已經：
- 有可以跑的 Claude / OpenAI / Gemini API 權限（Stage 1）
- 對 prompt engineering 基礎已經上手（Stage 2）
- 能寫一個吃 JSON 進、吐 JSON 出的 Python 函式

## 📚 必修閱讀

1. [**Anthropic — Tool Use**](https://docs.anthropic.com/en/docs/agents-and-tools/tool-use/overview) — 官方指南
2. [**ReAct: Synergizing Reasoning and Acting in Language Models**](https://arxiv.org/abs/2210.03629) — Yao et al. 2022，奠基論文。至少讀 abstract 跟 Section 3。
3. [**OpenAI — Function Calling**](https://platform.openai.com/docs/guides/function-calling) — function calling 格式參考
4. [**Build an agent from scratch**](https://shafiqulai.github.io/blogs/blog_3.html) — 從零打造 agent 的故事式導覽

## 🛠 動手練習（不是看過就好）

### 練習 1：Function Calling（一個工具、一次呼叫）
給 Claude 一個工具（假的天氣 API）跟一個問題（「台北現在有下雨嗎？」）。看 Claude 怎麼呼叫工具、拿到結果、再回答你。

### 練習 2：多工具選擇
給 Claude 三個工具（搜尋、計算機、行事曆）跟一個任務。看 Claude 怎麼挑工具，順便注意它什麼時候會挑錯。

### 練習 3：從零實作 ReAct（不用 framework）
用 50-80 行 Python 把 Thought → Action → Observation 迴圈寫出來。不要 LangChain、不要 LangGraph，就是純 `while not done: thought; action; observation; ...`。

### 練習 4：多步驟推理任務
一個需要連續呼叫 3-5 次 tool 的任務。例如：「找出台北人口，除以紐約人口，再把比例換成百分比。」每一步用不同的工具。

### 練習 5：錯誤處理
讓某個工具失敗（網路錯誤、輸入無效）。看看 agent 會怎麼處理錯誤、能不能恢復，再加上 retry 機制。

### 練習 6：Function schema 設計（壞 schema 修到好）
**先給 LLM 一份故意寫爛的 schema**——`description` 模糊（「處理資料」）、參數全用 `type: string`、沒分 required / optional、enum 該用沒用。觀察 LLM 怎麼選錯 tool、傳錯參數。然後逐項修：
- description 寫到 LLM 一眼就懂這個 tool 適用情境（不是寫給人讀的 docstring）
- parameters 用對 type（number / boolean / enum / array），required 列清楚
- 模糊邊界用 enum 強制收斂（例如 `unit: "celsius" | "fahrenheit"` 而不是 `unit: string`）
- error 回傳要包 `{"error": "...", "retry_hint": "..."}` 讓 LLM 能恢復

> 💡 詳細 cheatsheet 看 [`resources/schema-design-cheatsheet.md`](../resources/schema-design-cheatsheet.md)——5 條黃金規則 + 5 個常見 anti-pattern。

## 🎯 精選 Projects

### [Anthropic — Tool Use Cookbook](https://github.com/anthropics/anthropic-cookbook/tree/main/tool_use)

| 欄位 | 內容 |
|---|---|
| 語言 | Python |
| License | MIT |
| 推薦度 | ⭐⭐⭐⭐⭐ |

**教什麼**：Claude 支援的所有 tool use 模式 — 單工具、多工具、平行呼叫、結構化輸出抽取。

**適合誰**：練習 1 跟 練習 2，從這裡開始。

**怎麼跑**：
```bash
git clone https://github.com/anthropics/anthropic-cookbook
cd anthropic-cookbook/tool_use
jupyter notebook customer_service_agent.ipynb
```

---

### [Anthropic — Quickstarts](https://github.com/anthropics/anthropic-quickstarts)

| 欄位 | 內容 |
|---|---|
| 語言 | Python / TypeScript |
| Stars | ★ 16k+ |
| License | MIT |
| 推薦度 | ⭐⭐⭐⭐⭐ |

**教什麼**：Anthropic 官方的 動手練習 起手包。三個可直接 deploy 的 agent 範本：`financial-data-analyst`（資料分析 agent）、`customer-support-agent`（客服 agent）、`computer-use-demo`（讓 Claude 操作螢幕）。

**適合誰**：跑完 練習 1 / 練習 2 之後，想看「真的應用會長什麼樣子」的官方參考。比社群實作更 canonical，部署設定也比較完整。

**備註**：每個範本都是獨立 sub-folder，挑一個有興趣的跑就好。Computer use demo 特別值得看 — 是少數示範 agent 操作 GUI 的官方範例。

---

### [pguso/ai-agents-from-scratch](https://github.com/pguso/ai-agents-from-scratch)

| 欄位 | 內容 |
|---|---|
| 語言 | Python |
| License | MIT |
| 推薦度 | ⭐⭐⭐⭐⭐ |

**教什麼**：用本地 LLM 從零打造 agent，零 framework。ReAct、function calling、memory，全部自己寫。設計目的就是把 framework 幫你藏起來的東西攤開給你看。

**適合誰**：練習 3（從零寫 ReAct）。這是最乾淨的「不靠 framework」參考實作。

**備註**：用本地 Ollama，不用花 API 錢。README 值得仔細讀，章節結構安排得很好。

---

### [arunpshankar/react-from-scratch](https://github.com/arunpshankar/react-from-scratch)

| 欄位 | 內容 |
|---|---|
| 語言 | Python |
| License | Apache-2.0 |
| 最後更新 | ⚠️ 2025 年 5 月（更新放緩） |
| 推薦度 | ⭐⭐⭐⭐ |

**教什麼**：ReAct pattern 的多種變體與實作，針對 Gemini 最佳化。

**適合誰**：練習 3 的替代方案，如果你偏好 Gemini。涵蓋 ReAct + Reflection + Self-consistency 等變體。

---

### [mattambrogi/agent-implementation](https://github.com/mattambrogi/agent-implementation)

| 欄位 | 內容 |
|---|---|
| 語言 | Python |
| License | MIT |
| 最後更新 | ⚠️ 已停滯（2024 年 1 月）— 留作教學玩具參考 |
| 推薦度 | ⭐⭐⭐ |

**教什麼**：最精簡的 ReAct agent 實作。為了學習而砍到只剩約 150 行程式碼。

**適合誰**：逐行讀程式碼。練習 3 卡住時可以拿來對照。

---

### [lsdefine/GenericAgent](https://github.com/lsdefine/GenericAgent)

| 欄位 | 內容 |
|---|---|
| 語言 | 中文 + Python |
| Stars | ★ 9k+ |
| License | MIT |
| 推薦度 | ⭐⭐⭐⭐ |

**教什麼**：最精簡的自我演化 agent framework — 核心約 3K 行程式碼，agent 從 seed 自己長出技能樹。支援 Claude / Gemini / Kimi / MiniMax。仍在持續開發。

**適合誰**：練習 3 / 練習 4 的替代方案，給想看「精簡但完整」framework 的讀者。介於 mattambrogi 的玩具版跟完整 LangGraph 之間的中間點。

---

### [HelloAgents (jjyaoao)](https://github.com/jjyaoao/HelloAgents) — `learn_version` 分支

| 欄位 | 內容 |
|---|---|
| 語言 | 中文（zh-Hans）+ Python |
| License | CC BY-NC-SA 4.0 |
| 推薦度 | ⭐⭐⭐⭐⭐（中文讀者） |

**教什麼**：教學導向的多 agent 練習框架，章節式教學，搭配 [Datawhale 的 Hello-Agents 教學](https://github.com/datawhalechina/hello-agents)。涵蓋 16 種能力（tool response、context engineering、session 持久化、sub-agents、circuit breaker、observability 等），用來學 production pattern 的教材，不是直接拿來上 production 的成品。

**適合誰**：中文讀者。**請切到 `learn_version` 分支**，那才是對齊教材的版本。

**備註**：License 是 CC BY-NC-SA — 非商用。教材是 zh-Hans，但技術內容對 zh-TW 讀者沒障礙。

**怎麼跑**：
```bash
pip install hello-agents
git clone -b learn_version https://github.com/jjyaoao/HelloAgents
```

---

### [datawhalechina/hello-agents](https://github.com/datawhalechina/hello-agents)

| 欄位 | 內容 |
|---|---|
| 語言 | 中文（zh-Hans） |
| License | CC BY-NC-SA |
| 推薦度 | ⭐⭐⭐⭐⭐（中文讀者） |

**教什麼**：HelloAgents 的搭配教學。多章節導讀，從「什麼是 agent」一路講到 production 的實務 pattern。

**適合誰**：想要結構化教學加程式碼的中文讀者。

**備註**：請搭配上面 HelloAgents repo 的 `learn_version` 分支一起看。

---

### [QuantaLogic/quantalogic](https://github.com/quantalogic/quantalogic)

| 欄位 | 內容 |
|---|---|
| 語言 | Python |
| License | Apache-2.0 |
| 推薦度 | ⭐⭐⭐ |

**教什麼**：產生 Python 程式碼（而不是 JSON tool call）的 ReAct agent。設計選擇不同 — agent 直接寫程式碼當作 action。

**適合誰**：跑完 練習 3 之後。比較 CodeAct（程式碼即 action）與 JSON tool call 的差別。

---

### [HuggingFace Smolagents](https://github.com/huggingface/smolagents)

| 欄位 | 內容 |
|---|---|
| 語言 | Python |
| Stars | ★ 27k+ |
| License | Apache 2.0 |
| 推薦度 | ⭐⭐⭐⭐ |

**教什麼**：Smol agents（≤1000 LOC）。會寫程式碼的 agent — 執行 Python 而不是 JSON tool call。

**適合誰**：練習 5 的替代方案。特別適合本地 LLM 實驗。

**備註**：HF 的立場：agent 應該要小。他們的 code-action 路線跟 JSON-tool 路線在思路上很不一樣，值得對照來看。

---

### [LangChain — ReAct Agent Template](https://github.com/langchain-ai/react-agent)

| 欄位 | 內容 |
|---|---|
| 語言 | Python |
| License | MIT |
| 推薦度 | ⭐⭐⭐ |

**教什麼**：framework 怎麼把 ReAct pattern 抽象化。LangGraph Studio 的範本。

**適合誰**：練習 3 之後（先自己從零寫過再來）。再來比較 framework 幫你做了哪些事。

---

### [Anthropic — Building Effective Agents（部落格文章）](https://www.anthropic.com/engineering/building-effective-agents)

| 欄位 | 內容 |
|---|---|
| 形式 | 文章 |
| 推薦度 | ⭐⭐⭐⭐⭐ |

**教什麼**：Anthropic 自己寫的指南 — 什麼時候該用 agent（vs. workflow）、常見 pattern、容易踩的坑。Stage 4 之前必讀。

**適合誰**：建立觀念框架。練習 3 寫完之後、學 framework 之前讀。

---

## ✅ 進 Stage 4 前的自我檢查

你能不能：
- [ ] 定義一個 tool schema（name + description + JSON schema 輸入/輸出）
- [ ] 用不到 100 行 Python、不靠任何 framework，把 ReAct 迴圈寫出來
- [ ] 解釋為什麼 agent 需要一個「我做完了」的退出條件
- [ ] 比較 CodeAct（程式碼即 action）跟 JSON-tool 兩種路線
- [ ] 看出哪些問題其實不需要 agent

如果可以 → 進 [Stage 4 — Agent Frameworks](04-agent-frameworks.md)。

如果不行 → 把 練習 3 再跑一次，不要跳過。如果你不懂 framework 在幫你抽象什麼，Stage 4 的那些東西看起來會像黑魔法。
