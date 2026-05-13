# Stage 7 — Multi-Agent · Production

> **繁體中文** | [简体中文](./07-multi-agent-production.zh-Hans.md) | [English](./07-multi-agent-production.en.md) | [Русский](./07-multi-agent-production.ru.md)

⏱ **時間估算**：2-4 週（約 15-30 小時）

> 💡 用語密度高（multi-agent / handoff / eval / observability / guardrails⋯）→ 翻 [`resources/glossary.md` §4 + §6](../resources/glossary.md#4-multi-agent)。

最後一個階段。你正從「我會做 agent」走向「我能在 production 跑起來，多個 agent 協作、有 eval、有 observability、會 deploy」。

## 📌 學習目標

- 設計 multi-agent orchestration 模式（debate、planner-executor、peer review）
- 為 agent 架一套 evaluation harness
- 加上 observability（tracing、logging、cost tracking）
- 用 Anthropic SDK / OpenAI SDK 做 production deploy（進階功能：streaming、prompt caching、batching）
- 把 agent deploy 到 production（Docker、serverless、monitoring）

## 📚 必修閱讀

1. [**Anthropic — Building Effective Agents**](https://www.anthropic.com/engineering/building-effective-agents) — 用 production 的角度再讀一次
2. [**Anthropic — Prompt Caching**](https://www.anthropic.com/news/prompt-caching) — 90% 成本下降的技巧
3. [**Anthropic — Message Batches API**](https://docs.anthropic.com/en/docs/build-with-claude/batch-processing) — 非同步 batch job
4. **任一 eval framework 的文件** — promptfoo 或 LangSmith 或 weave
5. [**ai-boost/awesome-harness-engineering**](https://github.com/ai-boost/awesome-harness-engineering)（★ 780+）— agent harness 的工具 / pattern / eval / memory / MCP / observability 全集合。**framework 把 LLM 包成 agent；harness 把 agent 包成 production system**——這個 stage 學的就是 harness。
6. [**ZhangHanDong/harness-engineering-from-cc-to-ai-coding**](https://github.com/ZhangHanDong/harness-engineering-from-cc-to-ai-coding)（★ 1.3k+）— 從 Claude Code 原始碼學 harness 設計（中文）

## 🛠 動手練習（基礎 illustrative 練習）

### 練習 1：Multi-Agent 辯論
兩個 agent 辯論一個題目（例如「該用 Python 還是 Rust 寫 backend」），第三個 agent 當裁判。觀察辯論收斂或分歧的 pattern。

### 練習 2：Eval
替你前面的 agent 寫一份 eval，跑 N 次量成功率。把「我用眼睛看一下」的習慣換掉。

### 練習 3：Observability
把 LangSmith、Helicone、或 weave 接上一個 agent，看完整 trace。理解「沒 observability 的 agent debug = 黑盒」。

### 練習 4：SDK 進階
在同一次呼叫裡用 streaming + prompt caching + tool use。看成本怎麼降下來。

### 練習 5：Deploy
把一個 agent 包進 Docker，deploy 到雲端（任何 provider 都行）。學會把 prototype 變成可以給別人跑的東西。

## 🎯 精選 Projects

本 stage 已按用途分 7 個子分類。**先看這張總覽表挑入口、再下捲看 detail block**：

| 分類 | 代表 projects | 該看什麼 |
|---|---|---|
| **Multi-Agent Orchestration** | AutoGen / CrewAI / LangGraph | Stage 4 已介紹、production 場景再回頭看 GroupChat / hierarchical / state machine 用法 |
| **Evaluation Frameworks** | promptfoo ⭐ / lm-evaluation-harness / openai/evals | 寫 eval set、跑 regression、CI 整合 |
| **Observability** | Langfuse ⭐ / LangSmith / Helicone / W&B Weave | trace + cost + latency、production 必裝 |
| **Anthropic SDK 進階** | anthropic-sdk-python / **claude-agent-sdk-python** ⭐ / cookbook | prompt caching / batch API / files / **Claude Code 內部運作**（agent SDK = 看內部原始碼）|
| **Deployment** | BentoML / LangServe / vLLM / LLaMA-Factory | 上 production server / GPU inference / fine-tune |
| **本地 deploy 中文教材** | datawhalechina/self-llm | 中文圈 self-host LLM 最完整指南 |
| **Multi-Agent 案例研究** | MetaGPT / ChatDev / SWE-agent | 看「真實 multi-agent 工程怎麼設計」、不是 framework 而是 case study |

> 🌳 **Claude 原生 subagent 機制**（不用 framework 也能 multi-agent）見 [Stage 5.5](05-claude-code-ecosystem.md#55--subagentsclaude-code-原生-multi-agent-機制)。本 stage 重 framework / production；Stage 5.5 重 markdown-based subagent 編排。

---

### Multi-Agent Orchestration

#### [microsoft/autogen](https://github.com/microsoft/autogen)

Stage 4 已提過。在 production 場景下，AutoGen 的 GroupChat 協作模式是 multi-agent 辯論 / brainstorming 的好參考。

---

#### [crewAIInc/crewAI](https://github.com/crewAIInc/crewAI)

Stage 4 已提過。要做角色式的 multi-agent（例如 research → writer → reviewer 流水線），CrewAI 是最簡單的 production pattern。

---

#### [langchain-ai/langgraph](https://github.com/langchain-ai/langgraph)

Stage 4 已提過。要 production 加上 audit trail、checkpoint、human-in-the-loop，LangGraph 領先。

---

### Evaluation Frameworks

#### [promptfoo/promptfoo](https://github.com/promptfoo/promptfoo)

| 欄位 | 內容 |
|---|---|
| Stars | ★ 20k+ |
| License | MIT |
| 推薦度 | ⭐⭐⭐⭐⭐ |

**教什麼**：以 YAML 為基礎的 prompt 跟 agent eval harness。可以跨模型比較、在 CI 跑回歸測試。

**適合誰**：把 eval 流程標準化。取代「我用眼睛看一下就好」。

**怎麼跑**：
```bash
npx promptfoo init
# 編輯 promptfooconfig.yaml
npx promptfoo eval
```

---

#### [EleutherAI/lm-evaluation-harness](https://github.com/EleutherAI/lm-evaluation-harness)

| 欄位 | 內容 |
|---|---|
| Stars | ★ 12k+ |
| License | MIT |
| 推薦度 | ⭐⭐⭐⭐ |

**教什麼**：學術等級的 eval framework，內建幾百個標準 benchmark（MMLU、HellaSwag、GSM8K）。

**適合誰**：你需要主張「我們在 benchmark Y 上拿到 X%」的時候。比較研究風格。

---

#### [openai/evals](https://github.com/openai/evals)

| 欄位 | 內容 |
|---|---|
| Stars | ★ 18k+ |
| 推薦度 | ⭐⭐⭐⭐ |

**教什麼**：OpenAI 的 eval framework。可以針對特定 use case 寫客製 eval。

**適合誰**：你需要 OpenAI 專屬 eval、或想回饋上游時。

---

### Observability

#### [langfuse/langfuse](https://github.com/langfuse/langfuse)

| 欄位 | 內容 |
|---|---|
| Stars | ★ 26k+ |
| License | MIT（開源）+ 付費雲端 |
| 推薦度 | ⭐⭐⭐⭐⭐ |

**教什麼**：開源的 LLM observability——traces、sessions、evals、prompt management。

**適合誰**：自架的 production observability。LangSmith 的開源替代方案，實力很強。

---

#### [LangSmith](https://www.langchain.com/langsmith)（商業）

**教什麼**：LangChain 的 observability 平台。Trace、eval、prompt 迭代。

**適合誰**：整套 stack 都在 LangChain / LangGraph 上面。只有 hosted 版。

---

#### [Helicone](https://github.com/Helicone/helicone)

| 欄位 | 內容 |
|---|---|
| Stars | ★ 5k+ |
| License | Apache 2.0（開源）+ 付費雲端 |
| 推薦度 | ⭐⭐⭐⭐ |

**教什麼**：用 proxy 做 LLM observability——當作 OpenAI/Anthropic client 的替身，順便拿到 logging + caching。

**適合誰**：不想改程式、想快速上 instrumentation 時。

---

#### [weave（Weights & Biases 出品）](https://github.com/wandb/weave)

| 欄位 | 內容 |
|---|---|
| 推薦度 | ⭐⭐⭐⭐ |

**教什麼**：W&B 出的 tracing + eval framework。跟他們的 ML 平台整合。

**適合誰**：團隊已經在用 W&B 做 ML 實驗追蹤。

---

### Anthropic SDK 進階

#### [anthropics/anthropic-sdk-python](https://github.com/anthropics/anthropic-sdk-python)

| 欄位 | 內容 |
|---|---|
| 推薦度 | ⭐⭐⭐⭐⭐ |

**教什麼**：官方 Python SDK（基礎 API 層）。streaming、async、tool use、prompt caching、batches、files API。

**適合誰**：直接基於 Claude API 做應用。

---

#### [anthropics/anthropic-sdk-typescript](https://github.com/anthropics/anthropic-sdk-typescript)

**教什麼**：Python SDK 的 TS 版本。

**適合誰**：TypeScript / Node / web app。

---

#### [anthropics/claude-agent-sdk-python](https://github.com/anthropics/claude-agent-sdk-python) ⭐ agent 專用

| 欄位 | 內容 |
|---|---|
| Stars | ★ 6k+ |
| License | MIT |
| 推薦度 | ⭐⭐⭐⭐⭐ |

**教什麼**：Anthropic 在 2025 年中釋出的 **agent 專用 SDK**，跟基礎 `anthropic-sdk-python` 不同——這個內建 tool use loop、file access、sandbox 執行、subagent 編排，把 Claude Code 用的 agent capabilities 開放給 Python 應用直接用。

**適合誰**：要打造 Claude-based agent 而不是只呼叫 API 的開發者。比起手刻 ReAct loop、自己管 tool execution，這個 SDK 把這些抽象都做好了。

**備註**：跟 Claude Code 共用同一套 agent runtime；想理解 Claude Code 內部怎麼運作的，讀這個 SDK 的原始碼是最快的路徑。**Hands-on subagent 編排教學**（`.claude/agents/` + Task tool）見 [Stage 5.5](05-claude-code-ecosystem.md#55--subagentsclaude-code-原生-multi-agent-機制)——本 SDK 是 programmatic 入口、Stage 5.5 是 markdown-based 入口、兩條路徑共用同一個 runtime。

---

#### [anthropics/claude-agent-sdk-typescript](https://github.com/anthropics/claude-agent-sdk-typescript)

| 欄位 | 內容 |
|---|---|
| Stars | ★ 1.4k+ |
| License | NOASSERTION |
| 推薦度 | ⭐⭐⭐⭐ |

**教什麼**：Claude Agent SDK 的 TypeScript 版。

**適合誰**：要在 Node / web app 環境打造 Claude agent 的開發者。

---

#### [Anthropic Cookbook — Advanced patterns](https://github.com/anthropics/anthropic-cookbook)

之前已提過。特別是 `prompt_caching.ipynb`、`tool_use/`、`multimodal/` 三個 notebook，教進階 SDK 用法。

---

### Deployment

#### [BentoML/BentoML](https://github.com/bentoml/BentoML)

| 欄位 | 內容 |
|---|---|
| Stars | ★ 8k+ |
| License | Apache 2.0 |
| 推薦度 | ⭐⭐⭐⭐ |

**教什麼**：把任何 ML/LLM model 包成 production API。Docker + serving framework。

**適合誰**：把 agent 包成可 deploy 的 service。

---

#### [LangServe](https://github.com/langchain-ai/langserve)

**教什麼**：把 LangChain app deploy 成 REST API。底層用 FastAPI。

**適合誰**：以 LangChain 為基礎的 agent 想快速 deploy。

---

#### [datawhalechina/self-llm](https://github.com/datawhalechina/self-llm)

| 欄位 | 內容 |
|---|---|
| 語言 | 中文（zh-Hans） |
| Stars | ★ 30k+ |
| License | Apache-2.0 |
| 推薦度 | ⭐⭐⭐⭐ |

**教什麼**：開源大模型食用指南——一份完整的中文指南，講怎麼在 Linux 上 fine-tune 跟 deploy 開源 LLM。涵蓋 Qwen / Llama / GLM / 多模態模型，全參數 + LoRA + deployment 都有。

**適合誰**：要自架開源 LLM 的中文團隊。training-to-deployment 整個流程的 production 等級中文教學。

---

#### [hiyouga/LLaMA-Factory](https://github.com/hiyouga/LLaMA-Factory)

| 欄位 | 內容 |
|---|---|
| 語言 | Python |
| Stars | ★ 70k+ |
| License | Apache-2.0 |
| 推薦度 | ⭐⭐⭐⭐⭐ |

**教什麼**：中文社群最廣泛使用的 LLM fine-tuning framework——統一 100+ 個開源模型（Llama / Qwen / DeepSeek / Yi / Mistral 等）的 SFT、DPO、PPO、GRPO 訓練流程。Web UI 可以零程式碼跑 fine-tuning。

**適合誰**：要 fine-tune 開源 LLM（不只是 prompt-engineering）的人。比 self-llm 範圍更聚焦在「訓練」本身。

**備註**：搭配前面 Stage 1 的 Ollama / llama.cpp，能完整跑「fine-tune → quantize → 本地 deploy」的閉環。

---

### [vLLM](https://github.com/vllm-project/vllm)

| 欄位 | 內容 |
|---|---|
| Stars | ★ 79k+ |
| License | Apache 2.0 |
| 推薦度 | ⭐⭐⭐⭐ |

**教什麼**：高吞吐量的 LLM serving。可以在 production 跑開源模型。

**適合誰**：自架開源 LLM（Llama、Qwen 等等）取代付費 API 的場景。

---

### Multi-Agent 案例研究

#### [geekan/MetaGPT](https://github.com/geekan/MetaGPT)

| 欄位 | 內容 |
|---|---|
| Stars | ★ 67k+ |
| License | MIT |
| 推薦度 | ⭐⭐⭐⭐⭐ |

**教什麼**：以 SOP（Standard Operating Procedure）為核心的多 agent 軟體開發 team——PM / Architect / Engineer 各自有角色，從 PRD → 設計 → 程式碼一路產出 artifact 交接給下一棒。

**適合誰**：想看「**角色分工 + artifact 交接**」這種 pattern 怎麼實作的人。跟 LangGraph 的 state machine 路線不同，是另一條 multi-agent 設計思路。

**備註**：中文團隊維護，docs site 有 zh 內容。值得拿來跟 AutoGen 的 free-form group chat 對比。

---

#### [OpenBMB/ChatDev](https://github.com/OpenBMB/ChatDev)

| 欄位 | 內容 |
|---|---|
| 語言 | Python |
| Stars | ★ 33k+ |
| License | Apache-2.0 |
| 推薦度 | ⭐⭐⭐⭐ |

**教什麼**：「對話式」軟體開發 pattern——agents 在 design / code / test 各階段互相辯論才推進。這是 **agent debate / peer-review pattern** 最標準的開源案例，背後有論文。

**適合誰**：要打造「兩個 agent 互相挑戰才產出結論」這種 workflow 的人。比 AutoGen 更聚焦在 debate 機制。

**備註**：有 `README-zh.md`，中文讀者友善。

---

#### [princeton-nlp/SWE-agent](https://github.com/princeton-nlp/SWE-agent)

| 欄位 | 內容 |
|---|---|
| 語言 | Python |
| Stars | ★ 19k+ |
| License | MIT |
| 推薦度 | ⭐⭐⭐⭐ |

**教什麼**：**Agent-Computer Interface (ACI)** 的設計思路——tool 介面的形狀（不是 prompt）決定 agent 在 SWE-Bench 上的成績。Princeton NLP 的論文成果。

**適合誰**：在 Stage 3-4 學完 tool use 之後，想理解「**為什麼 tool 設計比 prompt tuning 重要**」的人。

**備註**：論文 + 實作開源，是學術 multi-agent 研究的好參考。

---

## ✅ Stage 7 之後的自我檢查

你能不能：
- [ ] 設計一個 multi-agent 系統，協作協定講得清楚
- [ ] 在 CI 跑自動 eval pipeline
- [ ] 把 observability（tracing）接到 production agent
- [ ] 在真實 workload 上量測 prompt caching 前後的成本差異
- [ ] 把 agent deploy 到雲端（任何 provider）

如果都可以 → 你已經跑完主路線。挑一個[特化分支](../README.md#️-7-階段學習地圖)，或回過頭來貢獻這份 repo。

## 💡 接下來

你已經有基礎能力了。接下來 6-12 個月應該專注在：
1. **挑一個 production 系統** 從 prototype 推到 production
2. **回饋上游**（LangGraph、AutoGen、MCP servers、Anthropic cookbook）
3. **讀論文**——agent 研究進展很快
4. **做出看得到的東西**——開源一個真的工具，不要再寫教學了
