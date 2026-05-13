# Stage 4 — Agent Frameworks

> **繁體中文** | [简体中文](./04-agent-frameworks.zh-Hans.md) | [English](./04-agent-frameworks.en.md) | [Русский](./04-agent-frameworks.ru.md)

⏱ **時間估算**：2-3 週（約 10-15 小時）

> 💡 用語不熟（framework / supervisor / worker / handoff⋯）→ 翻 [`resources/glossary.md`](../resources/glossary.md)。

你已經從零打造過一個 ReAct agent（Stage 3）。現在來看 framework 到底幫你做了什麼。**挑一個深入學**，其他的瀏覽過去就好，知道什麼時候該換。

## 📌 學習目標

完成這個 stage 後你會：
- 比較 5 個主流 agent framework（LangGraph、AutoGen、CrewAI、Smolagents、OpenAI Agents SDK）
- 替任務挑出對的 framework
- 用兩個 framework 各做一次同樣的 agent，親身感受差異
- 看出什麼時候該丟掉 framework、自己寫

## 🚪 進入條件

你應該已經：
- 跑完 Stage 3 的全部 5 個 hello-X projects
- 從零寫過 ReAct（練習 3）
- 對 async Python 上手（framework 大量依賴 async）

⚠️ **Memory 預備（需要時偷看一下）**：有些 framework 功能會用到 memory 的概念 — LangGraph 用 checkpointing（狀態持久化），CrewAI 在 agent 之間傳遞任務結果（輕量 memory）。這些東西在 [Stage 6 — Memory & RAG](06-memory-rag.md) 會講清楚。你不必先讀完那篇，只是當某個 framework 功能讓你看不懂的時候，去那邊找答案就對了。

## 🤔 什麼是 multi-agent framework？

**單一 agent**（你 Stage 3 寫過了）= 一個 LLM + 一個 ReAct loop + 若干工具，從頭跑到尾。

**多 agent system** = 兩個以上 LLM、各有角色（researcher / writer / critic / 等等）、用 messages 或 shared state 互傳、有 orchestrator 決定誰先誰後、誰看誰的結果。

**Framework 的工作**：把上面那個 orchestration boilerplate（roles、handoff、state、retry、checkpoint、HITL pause）抽出來、讓你只寫角色定義跟任務描述。一句話：**framework 是 multi-agent 的腳手架，不是必需品**——簡單情境你自己寫個 dict 跟 for loop 也行（Stage 7 練習 1 就是這樣）。

> 📚 **想要 chapter-length 深入版**：[`datawhalechina/hello-agents`](https://github.com/datawhalechina/hello-agents)（**16 production 能力含 multi-agent collaboration / role-based / sub-agents**）+ [Anthropic — Building Effective Agents](https://www.anthropic.com/engineering/building-effective-agents)（什麼任務該 multi-agent、什麼任務一個 agent 就夠）。
>
> 🌳 **Claude 生態有另一條路**：[Claude Code 原生 subagent 機制](05-claude-code-ecosystem.md#55--subagentsclaude-code-原生-multi-agent-機制)（`.claude/agents/` + Task tool）**不需要 framework**——直接寫一個 `.md` 檔就是一個 subagent。本 Stage 講 framework path、Stage 5.5 講 Claude path。兩條路徑用途不同：framework 適合**跨 LLM provider** 的 production system；Claude subagent 適合**已經 commit Claude Code** 的工程團隊。

## 📚 必修閱讀

1. [**Anthropic — Building Effective Agents**](https://www.anthropic.com/engineering/building-effective-agents) — 什麼時候用 framework、什麼時候直接用 raw API
2. [**LangChain — Conceptual Guide: Agents**](https://python.langchain.com/docs/concepts/agents/) — agent 的抽象概念
3. [**Best Multi-Agent Frameworks 2026 comparison**](https://gurusup.com/blog/best-multi-agent-frameworks-2026) — 當前市場定位
4. **挑一個 framework 的 Quickstart** — 選 LangGraph 或 CrewAI，把官方教學從頭跑到尾

## 🛠 動手練習

### 練習 1：同一個 agent、兩個 framework
用以下兩個 framework 各做一次同樣的簡單 agent（搜尋 + 摘要）：
- LangGraph
- CrewAI
比較程式碼行數、debug 體驗、以及它們各自把哪些複雜度藏在哪裡。

### 練習 2：多 agent 角色分配
用 CrewAI 做一個 2-3 個 agent、各自有不同角色一起完成同一個任務的 demo。（這種情境 CrewAI 最拿手。）

### 練習 3：圖式 workflow
用 LangGraph 做一個有分支邏輯跟 human-in-the-loop checkpoint 的 workflow。（這種情境 LangGraph 最拿手。）

### 練習 4：CodeAct vs JSON tool
用 Smolagents 做一個會寫 Python 程式碼當作 action 的 agent（CodeAct pattern），跟 練習 1 用的 JSON tool call 路線比較。問同一個問題，看兩種路線怎麼解。

### 練習 5：型別安全 agent
用 Pydantic AI 做一個會回傳結構化輸出的 agent（例如：問問題回 `{ "answer": str, "confidence": float, "sources": [str] }`）。看 Pydantic 的 schema validation 怎麼防止 agent 偷懶或 hallucinate 結構。

## 🎯 精選 Projects

按用途分 5 類。**先看分類表挑入口、再點下面 detail block 看適合誰 / 教什麼**：

| 分類 | Project | 推薦 | 為什麼推薦 |
|---|---|---|---|
| **Production 級**（複雜 multi-agent / 需要 audit）| [LangGraph](https://github.com/langchain-ai/langgraph) ⭐ | ⭐⭐⭐⭐⭐ | 圖式 orchestration + checkpointing + time-travel debug、企業採用率最高 |
| | [microsoft/semantic-kernel](https://github.com/microsoft/semantic-kernel) | ⭐⭐⭐⭐ | C# / Python / Java 三語官方 SDK、企業環境 / .NET / Java 場景 |
| | [agno-agi/agno](https://github.com/agno-agi/agno) | ⭐⭐⭐⭐ | multi-modal agent runtime + control plane（build + serve + monitor 一條龍）|
| **快速雛形 / 多 agent**（role-based / handoff）| [CrewAI](https://github.com/crewAIInc/crewAI) ⭐ | ⭐⭐⭐⭐ | 學習曲線最低、~20 行寫完 crew、適合 researcher → writer → critic pipeline |
| | [Microsoft AutoGen / AG2](https://github.com/microsoft/autogen) | ⭐⭐⭐⭐ | 對話式多 agent、group-chat / debate / peer review pattern 強 |
| | [OpenAI Agents SDK](https://github.com/openai/openai-agents-python) | ⭐⭐⭐⭐ | OpenAI 官方、agent hand-off + 結構化輸出 |
| | [OpenAI Swarm](https://github.com/openai/swarm) | ⭐⭐⭐⭐ | OpenAI 自家最簡 handoff（~200 LOC）、教育用 canonical |
| | [Strands Agents (AWS)](https://github.com/strands-agents/sdk-python) | ⭐⭐⭐⭐ | AWS / Bedrock-native、model-driven 設計、2025 新成員 |
| **特殊路線**（CodeAct / typed / memory-first）| [Hugging Face Smolagents](https://github.com/huggingface/smolagents) | ⭐⭐⭐⭐ | CodeAct pattern 代表（agent 寫 Python code 當 action）、≤1000 LOC |
| | [Pydantic AI](https://github.com/pydantic/pydantic-ai) | ⭐⭐⭐ | type-safe agent、structured output validation、Pydantic 團隊出 |
| | [Letta (formerly MemGPT)](https://github.com/letta-ai/letta) | ⭐⭐⭐⭐ | memory-first multi-agent、OS-paging 概念、long session 場景 |
| **特化** | [LlamaIndex Agents](https://github.com/run-llama/llama_index) | ⭐⭐⭐ | 跟 RAG 緊整合、文件密集型 agent |
| | [agentscope-ai/agentscope](https://github.com/agentscope-ai/agentscope) | ⭐⭐⭐ | 多 agent 平台、視覺化 debug 工具 |
| | [LangChain](https://github.com/langchain-ai/langchain) | ⭐⭐⭐ | 純 orchestration 改用 LangGraph、LangChain 適合 retrieval + chaining 黏合 |
| **基礎設施**（不是 framework、跨 stage 用）| [BerriAI/litellm](https://github.com/BerriAI/litellm) | ⭐⭐⭐⭐ | provider-agnostic SDK + AI gateway、用 OpenAI 形狀 call 100+ LLM |

---

### [LangGraph](https://github.com/langchain-ai/langgraph) ⭐ production 等級

| 欄位 | 內容 |
|---|---|
| 語言 | Python / TypeScript |
| Stars | ★ 31k+ |
| License | MIT |
| 推薦度 | ⭐⭐⭐⭐⭐ |

**教什麼**：基於圖的 agent orchestration。狀態管理、checkpointing、human-in-the-loop、time-travel debugging。

**適合誰**：production 級的多 agent 系統，需要稽核軌跡與 rollback 的場景。企業級。

**備註**：2025 年起企業採用率明顯上升（稽核軌跡、replay-friendly 圖模型）。學習曲線比 CrewAI 陡，但 production 場景值得。建議搭配 LangSmith 做 observability。

**怎麼跑**：
```bash
pip install langgraph langchain-anthropic
# Tutorial: https://langchain-ai.github.io/langgraph/tutorials/introduction/
```

---

### [CrewAI](https://github.com/crewAIInc/crewAI) ⭐ 最容易上手

| 欄位 | 內容 |
|---|---|
| 語言 | Python |
| Stars | ★ 50k+ |
| License | MIT |
| 推薦度 | ⭐⭐⭐⭐ |

**教什麼**：以角色為核心的多 agent 設計。一群（Crew）有不同角色的 agent 朝同一個目標合作。

**適合誰**：快速雛形多 agent 系統。約 20 行就能跑出一個 crew。「研究員 → 寫手 → 審稿」這類管線特別合用。

**備註**：學習曲線最低。但是：長時間 workflow 沒有內建 checkpointing、agent 之間的溝通可控性有限、錯誤處理偏粗糙。雛形用 CrewAI、production 用 LangGraph。

---

### [Microsoft AutoGen / AG2](https://github.com/microsoft/autogen)

| 欄位 | 內容 |
|---|---|
| 語言 | Python |
| Stars | ★ 57k+ |
| License | CC-BY-4.0（注意：這是文件 license，程式碼另外釋出） |
| 推薦度 | ⭐⭐⭐⭐ |

**教什麼**：對話式多 agent 團隊。agent 透過多輪對話互動。group-chat 協調 pattern 是它的強項。

**適合誰**：多 agent 辯論、腦力激盪、peer review 類的 pattern。Microsoft 研究院血統。

**備註**：AG2（v0.4 重寫版）改成 async-first 執行、event-driven 核心。多數既有教學仍在用原本的 AutoGen（v0.2），請留意版本分支。**group-chat 模式怎麼跑 chapter-length 範例 → 看 [Anthropic Cookbook `customer_service_agent`](https://github.com/anthropics/anthropic-cookbook/tree/main/multimodal)（另一個 framework 但 multi-agent orchestration 思路相同）+ Stage 7 練習 1 multi-agent debate**。

---

### [Hugging Face Smolagents](https://github.com/huggingface/smolagents)

| 欄位 | 內容 |
|---|---|
| 語言 | Python |
| Stars | ★ 27k+ |
| License | Apache 2.0 |
| 推薦度 | ⭐⭐⭐⭐ |

**教什麼**：寫程式碼的 agent（CodeAct pattern）— agent 產生 Python 程式碼，而不是 JSON tool call。≤1000 LOC 的設計哲學。

**適合誰**：本地 LLM 生態、HuggingFace 整合場景。設計理念跟主流不同，值得理解。

**備註**：HF 的賭注：agent 應該要小。他們的 CodeAct 路線在思路上很不一樣，跟 JSON-tool 路線對照看，可以看出彼此的取捨。

---

### [OpenAI Agents SDK](https://github.com/openai/openai-agents-python)

| 欄位 | 內容 |
|---|---|
| 語言 | Python |
| License | MIT |
| 推薦度 | ⭐⭐⭐⭐ |

**教什麼**：OpenAI 官方的 agent SDK。agent 之間 hand-off、結構化輸出、OpenAI 原生的開發體驗。

**適合誰**：你已經押注 OpenAI 生態。輕量、跟 GPT-4 系列整合很緊。

**備註**：較新的選手（2025 年下半年才推出）。實戰歷練不如 LangGraph，但 API 很乾淨，值得持續關注它的後續發展。

---

### [OpenAI Swarm](https://github.com/openai/swarm) — 最簡 handoff pattern

| 欄位 | 內容 |
|---|---|
| 語言 | Python |
| License | MIT |
| 推薦度 | ⭐⭐⭐⭐（教育用）/ ⭐⭐⭐（production） |

**教什麼**：OpenAI 自己出的「最小可能 multi-agent」——核心 ~200 行 Python、只有 2 個觀念：**Agent + handoff**。比 CrewAI / LangGraph 都小。

**適合誰**：想理解 multi-agent orchestration 的**核心 mental model** 但不想學整個 framework 的人。把 Swarm source code 讀完是 chapter-length 教材的好替代品。

**備註**：OpenAI 自己定位 Swarm 為「experimental / educational」、官方推 OpenAI Agents SDK 是 production 路線。把 Swarm 當 reading material（不是 production tool）。

---

### [Strands Agents (AWS)](https://github.com/strands-agents/sdk-python)

| 欄位 | 內容 |
|---|---|
| 語言 | Python |
| License | Apache 2.0 |
| 推薦度 | ⭐⭐⭐⭐ |

**教什麼**：AWS 出的新 agent SDK，**model-driven** 設計（讓 LLM 自己 plan、不用 explicit graph definition）。Bedrock-native、跟 AWS 生態（Lambda / Step Functions / Bedrock Agents）整合緊。

**適合誰**：已經 commit AWS 雲端、不想自己 vendor lock-in 卻又能跑 production multi-agent 的團隊。

**備註**：2025 後段推出、定位類似 OpenAI Agents SDK 跟 Anthropic SDK 在自家生態的角色。如果你在 AWS 上、值得跟 LangGraph 對照一次。

---

### [Letta (formerly MemGPT)](https://github.com/letta-ai/letta)

| 欄位 | 內容 |
|---|---|
| 語言 | Python |
| Stars | ★ 18k+ |
| License | Apache 2.0 |
| 推薦度 | ⭐⭐⭐⭐ |

**教什麼**：**memory-first** multi-agent framework。把 OS 的 paging 概念搬到 LLM——分 working memory（in-context）跟 archival storage（vector store），自動換頁。multi-agent collab 也是賣點。

**適合誰**：要做**長 session / 跨 day 對話 / persona-stable** 的 agent（譬如 long-term assistant、therapist bot、tutor）。一般 agent 用不到、但這類場景沒對手。

**備註**：原 MemGPT 是 paper / Berkeley 出身、2024 改名 Letta + 公司化。Stage 6 練習 5 long-term memory 會再提到。

---

### [LlamaIndex Agents](https://github.com/run-llama/llama_index)

| 欄位 | 內容 |
|---|---|
| 語言 | Python |
| Stars | ★ 49k+ |
| License | MIT |
| 推薦度 | ⭐⭐⭐ |

**教什麼**：跟 RAG 緊密整合的 agent。如果你的 agent 需要大量文件/資料 retrieval，LlamaIndex 是自然選擇。

**適合誰**：文件密集型的 agent 應用。研究助理、知識工作者類 agent。

**備註**：retrieval 強、orchestration 弱。純 orchestration 場景不該選它；retrieval 為主的工作很適合。

---

### [Pydantic AI](https://github.com/pydantic/pydantic-ai)

| 欄位 | 內容 |
|---|---|
| 語言 | Python |
| License | MIT |
| 推薦度 | ⭐⭐⭐ |

**教什麼**：型別安全的 agent framework，用 Pydantic 處理結構化輸出。驗證保證很強。

**適合誰**：production 團隊，預設就要 runtime 型別安全 + 結構化輸出。

**備註**：比競品新。Pydantic 團隊的血統讓人對 API 設計有信心。

---

### [agentscope-ai/agentscope](https://github.com/agentscope-ai/agentscope)

| 欄位 | 內容 |
|---|---|
| 語言 | Python |
| Stars | ★ 24k+ |
| License | Apache 2.0 |
| 推薦度 | ⭐⭐⭐ |

**教什麼**：多 agent 平台，視覺化工具是強項。「打造你看得到、看得懂、信得過的 agent」。

**適合誰**：想要視覺化 debug 多 agent 流程的研究者。

**備註**：在西方社群採用度較低，但技術紮實。observability 工具很不錯。

---

### [LangChain](https://github.com/langchain-ai/langchain)

| 欄位 | 內容 |
|---|---|
| 語言 | Python / TypeScript |
| Stars | ★ 135k+ |
| License | MIT |
| 推薦度 | ⭐⭐⭐ |

**教什麼**：最早的「萬用工具袋」framework。chains、agents、memory、retrievers 全部一鍋。

**適合誰**：需要把很多零件黏在一起的快速雛形。

**備註**：很多人 LangChain 用過頭了。專做 agent orchestration 的話，請改用它的繼任者 LangGraph。LangChain 比較適合 retrieval + chaining 的黏合，不適合 agent orchestration。

---

### [microsoft/semantic-kernel](https://github.com/microsoft/semantic-kernel)

| 欄位 | 內容 |
|---|---|
| 語言 | C# / Python / Java |
| Stars | ★ 27k+ |
| License | MIT |
| 推薦度 | ⭐⭐⭐⭐ |

**教什麼**：Microsoft 出品的企業級 SDK——kernel + plugin + planner pattern，**同時支援 C# / Python / Java**，是少數三語言都有官方 SDK 的 agent framework。

**適合誰**：在 Microsoft 技術棧上工作的開發者，或要在 .NET / Java 環境做 agent 的人。

**備註**：抽象層比 smolagents 厚，不適合第一週的初學者。要在企業環境跑、需要 .NET / Java 的場景值得考慮。

---

### [agno-agi/agno](https://github.com/agno-agi/agno)

| 欄位 | 內容 |
|---|---|
| 語言 | Python |
| Stars | ★ 39k+ |
| License | Apache-2.0 |
| 推薦度 | ⭐⭐⭐⭐ |

**教什麼**：multi-modal agent runtime + control plane——除了 build agent，還涵蓋 serving、monitoring、governance。2025 年新一代的 agent platform。

**適合誰**：要把 agent 推到「能 serve、能監控」的階段，但又不想全套 LangGraph + LangSmith 的人。也適合 prototype 階段的快速設計。

**備註**：Stage 4 學它的 agent API，Stage 7 再用它的 runtime / 監控功能。

---

### [BerriAI/litellm](https://github.com/BerriAI/litellm)（不是 framework，是跨 stage 基礎設施）

| 欄位 | 內容 |
|---|---|
| 語言 | Python |
| Stars | ★ 45k+ |
| License | MIT（含 `enterprise/` 子目錄的另外授權） |
| 推薦度 | ⭐⭐⭐⭐ |

**教什麼**：provider-agnostic SDK + AI gateway——**用 OpenAI 形狀的 API 呼叫 100+ 個 LLM**，附 cost tracking、fallback、guardrail。

**適合誰**：要做能切換 Claude / GPT / Gemini / 開源模型的 agent，不想為了切換 provider 改一堆程式碼的人。

**備註**：嚴格來說 LiteLLM 不是 agent framework，而是 framework 底下的「provider 抽象層」——放在 Stage 4 是因為寫 multi-provider agent 時很常會用到。Stage 7 deploy 時也會再用到。Repo 內 `enterprise/` 目錄是另外的授權條款。

---

## ✅ 進 Stage 5 前的自我檢查

你能不能：
- [ ] 用 LangGraph 跟 CrewAI 各做一次同一個 agent
- [ ] 替任務挑出對的 framework（production vs 雛形）
- [ ] 解釋 LangGraph 的 checkpoint 跟 CrewAI 的 task delegation 差在哪
- [ ] 看出什麼時候 CodeAct（Smolagents）比 JSON-tool 更好
- [ ] 判斷什麼時候該丟掉 framework、直接用 raw API

如果可以 → 進 [Stage 5 — Claude Code Ecosystem](05-claude-code-ecosystem.md)。

## 💡 策略提示

不要想把這些全部學完。挑**一個 production 等級的（LangGraph）**跟**一個快速雛形用的（CrewAI）**深入學。其他的 README 瀏覽過去就好，知道有這些選項存在即可。
