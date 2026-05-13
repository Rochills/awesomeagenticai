> **繁體中文** | [简体中文](./README.zh-Hans.md) | [English](./README.en.md)

# 練習 5：Long-term Memory（跨輪對話記得事情）

對應 [Stage 6 — Memory & RAG](../../../stages/06-memory-rag.md) 練習 5。
> 🎓 **學習模式**：這份 `starter.py` 是**完整解答**、不是 TODO skeleton。建議用**主動模式**——`mv starter.py starter_reference.py`、看 signature 不看 body、自己重寫一份 `starter.py`、跑 `python test.py` 驗證；卡 20 分鐘再回去對照 reference。完整方法論看 [`docs/HOW_TO_USE.md`](../../../docs/HOW_TO_USE.md)。

> 📚 **想要 chapter-length 深入版？** 本 folder 的 starter 是 illustrative 版、聚焦核心 pattern + 兩條 SDK path，不是 production-grade tutorial。深度教材推薦：
> - [`datawhalechina/hello-agents`](https://github.com/datawhalechina/hello-agents) ⭐ 中文圈最完整、章節式 + 16 種 production 能力。**本練習對應 hello-agents 的 long-term memory 章節**
> - [mem0](https://github.com/mem0ai/mem0)（auto fact extraction + forgetting）+ [Letta / MemGPT](https://github.com/letta-ai/letta)（兩級 memory pattern）
> - 完整 references 見 [Stage 6 § 精選 Projects](../../../stages/06-memory-rag.md#-精選-projects)


## 任務

Agent 跨多輪對話記得 user 說過的事情。實作方式：

```
Turn 1: user: "I live in Taipei and prefer Python."
        → maybe_remember_fact() 抓到「I + ...」格式、存進 vector store
Turn 2: user: "What's 2+2?"        → recall 拿不到 relevant memory、純算術
Turn 3: user: "Recommend a language for me."
        → recall 拿到「prefer Python」、塞進 system prompt → LLM 知道推薦 Python
```

這是 **RAG 的另一面**——retrieve 對象從外部文件變成「對話歷史」。

## 怎麼跑 — 兩條路徑

### Path A（默認、本機免費）

```bash
pip install -r requirements.txt
ollama pull qwen2.5:3b
ollama serve
python starter.py
```

預算：**$0**。

### Path B（Anthropic）

```bash
pip install -r requirements.txt
export ANTHROPIC_API_KEY=sk-ant-...
python starter_anthropic.py
```

預算：每次 ≈ **$0.001**。

## 不花錢驗證程式邏輯

```bash
python test.py             # 5 個 test、mock LLM
python test_anthropic.py   # Anthropic mock
```

## MemoryStore + chat 流程

```python
class MemoryStore:
    def remember(self, fact: str) -> str:   # add to vector store
    def recall(self, query: str) -> list:    # top-k semantic search

def chat(user_msg, memory):
    memories = memory.recall(user_msg, top_k=3)   # 1. 撈相關 memory
    system = f"Relevant memories: {memories}"      # 2. 塞進 system prompt
    return llm.invoke(system + user_msg)           # 3. LLM 看 memory 回答
```

**核心**：memory 不是當「context window history」存（會爆），而是當「semantic search index」存——LLM 只看到相關的幾條。

## 跟普通 chat history 的差別

| 維度 | Chat history (in-context) | Vector memory store |
|---|---|---|
| 存放位置 | messages array | ChromaDB |
| 容量 | context window 限制（200k-2M token） | 不限（millions of facts） |
| 跨 session | ❌ session 結束就沒 | ✅ persistent |
| 撈出方式 | 所有 history 都進 prompt（吃 token） | top-k semantic search（精準） |
| 適合 | 短對話、單 session | 長 user 關係、多 session、persona |

**Production 用法**：兩個都用——recent N 輪當 in-context、超過 N 輪 + 跨 session 用 vector memory。

## 什麼是「memory-worthy fact」

這份用 heuristic：user 說「I + verb...」就存。Production 通常更複雜：

1. **Explicit trigger**：user 說「remember that...」
2. **Profile facts**：location / language / role / preferences
3. **Past decisions**：上次 agent 怎麼處理某情境
4. **Negative feedback**：「don't suggest X」要存
5. **LLM-extracted**：每輪結束、用 LLM 自己抓 facts（mem0 / Letta / MemGPT 都這麼做）

## 兩個 path 觀察重點

| 觀察項 | Anthropic Claude haiku | Ollama qwen2.5:3b |
|---|---|---|
| 把 memory 融進回答 | 自然（cite memory） | 偶爾 ignore memory、用通用答案 |
| 「無相關 memory」時不強用 | 守規則 | 較鬆 |
| 多 memory 整合 | 好 | 中 |

## 常見坑

- **每輪都 add to memory**：vector store 會爆。要有「fact extraction」過濾、只存值得記的
- **沒 dedup**：使用者多輪重複講「I live in Taipei」、會存 5 條一樣的。要加 dedup 邏輯（similarity > 0.95 視為重複）
- **Forget / update 機制缺失**：使用者搬家了「I now live in Tokyo」、舊 memory「Taipei」要怎麼處理？production 要支援「supersede」概念
- **沒 context size 控制**：recall top-k 太大、context 爆，LLM 也分心
- **隱私 / GDPR**：使用者要求刪除個人資訊、要有 `forget(user_id)` API

## Production-grade 工具

- **[mem0](https://github.com/mem0ai/mem0)**：full memory pipeline、auto-fact-extraction、forgetting、user-scoped namespace
- **[Letta (formerly MemGPT)](https://github.com/letta-ai/letta)**：兩級 memory（working memory + archival storage）、把 OS 的 paging 觀念搬到 LLM
- **CrewAI memory**：framework 內建 short / long term memory
- **LangGraph checkpointer + persistent storage**：自帶 thread-level memory

## 延伸

- **加 dedup**：`if similarity(new, existing) > 0.95: skip`
- **加 LLM-based fact extraction**：每輪結束用小 LLM 抓 facts、不靠 heuristic
- **加 user_id scoping**：MemoryStore 加 `user_id` filter、不同 user 互不污染
- **接 [mem0](https://github.com/mem0ai/mem0)**：production 不要自己寫 memory pipeline、用成熟 lib
