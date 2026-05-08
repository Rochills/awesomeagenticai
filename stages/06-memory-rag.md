# Stage 6 — Memory · RAG · 進階

> **繁體中文** | [English](./06-memory-rag.en.md)

⏱ **時間估算**：2 週（約 10 小時）

> 💡 這 stage 用語密度高（**RAG / 向量資料庫 / embedding / chunking / hybrid search / reranking⋯**）→ 不熟先翻 [`resources/glossary.md` §3](../resources/glossary.md#3-memory--retrieval--rag)。

不會記住過去互動的 agent 沒什麼用。RAG（Retrieval-Augmented Generation）是目前的標準做法。這一章兩個都會講到。

## 📌 學習目標

- 區分 short-term、long-term、episodic、semantic memory
- 理解 vector embedding 與相似度搜尋
- 建一條基本 RAG 流水線（chunk → embed → store → retrieve → generate）
- 看出 RAG 不該用在哪些地方（以及該用在哪些地方）

## 📚 必修閱讀

1. [**LlamaIndex — RAG concepts**](https://docs.llamaindex.ai/en/stable/getting_started/concepts/) — 最清楚的入門
2. [**LangChain — RAG tutorial**](https://python.langchain.com/docs/tutorials/rag/) — 動手做
3. [**Pinecone — Learning Center**](https://www.pinecone.io/learn/) — vector DB 基礎
4. [**Anthropic — Contextual Retrieval**](https://www.anthropic.com/news/contextual-retrieval) — Anthropic 搭配 prompt caching 的 RAG 寫法
5. [**LangChain — Text splitters**](https://docs.langchain.com/oss/python/integrations/splitters/index) — chunking 策略入門

## 🧭 單元指引

這一章先帶你簡單理解短期記憶與長期記憶，再聚焦到 RAG。

| 比較面向 | Short-term memory（短期記憶） | Long-term memory（長期記憶） |
|---|---|---|
| 中文可稱 | 短期記憶 | 長期記憶 |
| 來源 | 當前對話內容 | 跨 session 或長期保存的資訊 |
| 持續時間 | 短，通常限於目前 session | 長，可跨 session |
| 技術基礎 | 上下文視窗（context window）/ prompt | 記憶儲存層（memory store）/ 使用者檔案 / 向量資料庫 |
| 適合記什麼 | 任務細節、剛剛說過的內容 | 穩定偏好、長期目標、背景資料 |
| 是否受 context 長度限制 | 會，因為模型一次能看的內容有限 | 較不會，因為可以先存在外部，需要時再取一小段放回來 |
| 生活例子 | 剛剛收到的手機驗證碼、正在進行對話的上一句話 | 你深化學會的知識、圖書館、知識庫、讀過的書 |

這裡的工作階段（session）可以理解成一次連續互動，例如同一段聊天、同一次任務，或同一次 agent 執行。

RAG 可以想成在幫 agent 蓋圖書館。你要先把書放好、分類好，後續要查資料時，才會又快又精準。

最基礎的 RAG 可以拆成兩條流水線：

- **資料預處理**：ingest → chunk → embed → store（index）。這一步是在建立可檢索的知識庫。
- **檢索生成**：retrieve → generate。這一步是在使用者提問時，找出相關內容，再交給 LLM 生成回答。

![RAG 流水線總覽](../resources/diagrams/rag-pipeline-overview.jpg)

圖中的 RAG Fusion、query rewrite 等屬於進階檢索技巧。第一次學 RAG 時，先理解主線流程即可。

上面只是最小骨架。設計與概念細節，會在下面各自區塊展開。

讀這章時可以順便思考：RAG 不適合哪些應用場景？哪些場景適合 RAG，但基本 RAG 還不夠好？

這會帶到更進階的 RAG 技術，例如 GraphRAG。有興趣的同學可以思考，為何這種情境要設計這樣的 RAG 解決方案，不用實作每種 RAG 技術或細節。

## 🧩 Chunking 怎麼想

好的 chunking 可以讓 LLM 在有限 context 內，用更精確、完整的資訊生成回答。它不是把文字平均切開。

切法取決於應用場景與文件內容。它會決定 retriever 看見的最小語意單位。

一個好 chunk 要同時做到兩件事：**夠完整**，讓模型看得懂上下文；**夠聚焦**，讓檢索不帶太多雜訊。chunk 太小會失去前後文，chunk 太大會讓相似度搜尋變鈍。

常見策略：

- **固定長度（Fixed-Length）**：照字元數或 token 數切。優點是簡單穩定；缺點是一板一眼，容易切斷段落、句子或表格。
- **滑動視窗（Sliding Window）**：每個 chunk 之間保留重疊區塊（overlap）。優點是比較不會在邊界掉資訊；缺點是索引量會變大。
- **遞迴切割（Recursive）**：先嘗試保留段落，如果長度還是不適合，再退到句子、字詞等更小單位。通常是入門 RAG 的好基準。
- **語意切割（Semantic Chunking）**：依 embedding 或語意變化切，也就是當前區塊與前一個區塊的語意相似度出現差異。適合長文件，但成本與複雜度較高。
- **混合策略（Hybrid）**：依照應用場景，思考不同文件結構該怎麼混搭切法。例如，一篇論文可能要保留章節、表格、公式與引用脈絡。

![Chunking 策略流程](../resources/diagrams/chunking-strategies.jpg)

第一次做 RAG 時，不要一開始就追求複雜切法。LangChain 文件建議多數情境先從 `RecursiveCharacterTextSplitter` 開始。

先跑出基準版本，再用後續 retrieval 結果決定要不要換策略。

```python
from langchain_text_splitters import RecursiveCharacterTextSplitter

text = "這是一個很長的文件內容...（此處省略一千字）..."

splitter = RecursiveCharacterTextSplitter(
    chunk_size=100,
    chunk_overlap=20,
    length_function=len,
)

chunks = splitter.split_text(text)
print(f"共切成 {len(chunks)} 個 chunk")
print(chunks[0])
```

直覺判斷 chunking 好不好，可以先看兩件事：

- 回答缺漏資訊，或有頭無尾：通常是 chunk 太小，或 overlap 不夠。
- 回答包含正確資訊，但混入無關內容：通常是 chunk 太大，或 top-k 撈太多。

Chunking 進階思考：

- chunking 不是一次設定好就結束，要配合真實 query 與失敗案例反覆調整。
- chunk size、overlap、top-k、reranker 會互相影響，不要只單看其中一個參數。
- 想想看，如果今天要 RAG 的資料有含圖片的 PDF、會議字幕檔，要如何切割比較好？

## 🛠 動手練習（不是看過就好）

### 練習 1：Embeddings
把 100 個句子做 embedding，找出某個 query 的最近鄰。理解 vector 之間的距離意義。

### 練習 2：Vector DB
把 embedding 存進 Chroma，做語意 query。比對「跟 keyword search 差在哪」。

### 練習 3：Chunking 對照
拿同一份文件做三種切法：固定長度、段落切法、heading-aware 切法。用 5 個真實問題比較 top-k 結果，記錄哪種切法比較容易撈到正確上下文。

### 練習 4：完整 RAG 流水線
把一份 PDF 切塊 → embed → 取 top-k → 生成回答。這是大多數 RAG 應用的基本骨架。

### 練習 5：Long-term Memory
讓 agent 在多輪對話之間記得事情。可以用 `mem0` 或自己用 vector store 接。

## 🎯 精選 Projects

### [LlamaIndex](https://github.com/run-llama/llama_index)

| 欄位 | 內容 |
|---|---|
| Stars | ★ 49k+ |
| 推薦度 | ⭐⭐⭐⭐⭐ |

**教什麼**：以 RAG 為核心的 framework。document loader、切塊策略、retrieval pattern、query engine。

**適合誰**：以文件為主的應用。RAG 是它的核心。

---

### [Chroma](https://github.com/chroma-core/chroma)

| 欄位 | 內容 |
|---|---|
| Stars | ★ 27k+ |
| License | Apache-2.0 |
| 推薦度 | ⭐⭐⭐⭐⭐ |

**教什麼**：開源 embedding 資料庫。本機跑，不用搞基礎設施。

**適合誰**：上面的練習 2、練習 4。最容易上手的 vector DB。

**怎麼跑**：
```python
import chromadb
client = chromadb.Client()
collection = client.create_collection("hello")
collection.add(documents=["doc 1", "doc 2"], ids=["1", "2"])
results = collection.query(query_texts=["query"], n_results=1)
```

---

### [Qdrant](https://github.com/qdrant/qdrant)

| 欄位 | 內容 |
|---|---|
| Stars | ★ 31k+ |
| 推薦度 | ⭐⭐⭐⭐ |

**教什麼**：production 等級的 vector DB，用 Rust 寫，規模大時比 Chroma 快。

**適合誰**：當 Chroma 跟不上時。有雲端版跟自架版。

---

### [Weaviate](https://github.com/weaviate/weaviate)

| 欄位 | 內容 |
|---|---|
| Stars | ★ 16k+ |
| 推薦度 | ⭐⭐⭐⭐ |

**教什麼**：有內建模組（text2vec、generative、classification）的 vector DB。schema 驅動。

**適合誰**：production 部署、需要 schema 約束的場景。

---

### [pgvector](https://github.com/pgvector/pgvector)

| 欄位 | 內容 |
|---|---|
| Stars | ★ 21k+ |
| 推薦度 | ⭐⭐⭐⭐ |

**教什麼**：在 PostgreSQL 裡做向量相似度搜尋。SQL 跟向量同一個 DB。

**適合誰**：原本就在用 PostgreSQL、不想多維護一個向量儲存的團隊。

---

### [LangChain — Memory](https://python.langchain.com/docs/concepts/memory/)

**教什麼**：agent memory 模式（buffer、summary、vectorstore-backed）。

**適合誰**：agent 需要跨 session 記得事情時。

---

### [mem0ai/mem0](https://github.com/mem0ai/mem0)

| 欄位 | 內容 |
|---|---|
| Stars | ★ 54k+ |
| 推薦度 | ⭐⭐⭐⭐ |

**教什麼**：給 AI agent 用的自我精煉 memory 層。跨 session 儲存使用者的事實。

**適合誰**：個人助理或 chatbot，需要使用者層級 memory 的場景。

---

### [Letta（前身 MemGPT）](https://github.com/letta-ai/letta)

| 欄位 | 內容 |
|---|---|
| Stars | ★ 22k+ |
| 推薦度 | ⭐⭐⭐⭐ |

**教什麼**：有階層式 memory 的長 context agent。靈感來自 OS 的 memory management。

**適合誰**：context 要跑很久的 agent（以月為單位、不是分鐘）。

---

### [chatchat-space/Langchain-Chatchat](https://github.com/chatchat-space/Langchain-Chatchat)

| 欄位 | 內容 |
|---|---|
| 語言 | 中文 + Python |
| Stars | ★ 38k+ |
| License | Apache-2.0 |
| 推薦度 | ⭐⭐⭐⭐ |

**教什麼**：中文社群最廣泛使用的 RAG + Agent 應用 framework，可離線部署、中文友善的預設值，支援 ChatGLM / Qwen / Llama / Ollama 後端。

**適合誰**：要做知識庫 / RAG 應用的中文使用者。預設值對中文斷詞 + embedding 處理得不錯。

**備註**：最後一次更新是 2025 年 11 月（約 6 個月前——還算活著，但已經到邊緣）。

---

### [Anthropic — Contextual Retrieval cookbook](https://platform.claude.com/cookbook/capabilities-contextual-embeddings-guide)

**教什麼**：Anthropic 的 contextual retrieval 技巧搭配 prompt caching，附完整端到端範例。

**適合誰**：跑完基本 RAG 之後想升級到 contextual retrieval、在長文件上拿到更好 recall 的人。

**備註**：Anthropic 在 2025 年把 `anthropic-cookbook` 改名為 `claude-cookbooks`。上面的線上 notebook 是現在的標準參考；GitHub 上的原始路徑可能會變動。

---

### [infiniflow/ragflow](https://github.com/infiniflow/ragflow)

| 欄位 | 內容 |
|---|---|
| 語言 | Python |
| Stars | ★ 79k+ |
| License | Apache-2.0 |
| 推薦度 | ⭐⭐⭐⭐⭐ |

**教什麼**：production 等級的 RAG engine，含深度文件理解（layout、表格、OCR）+ hybrid retrieval + agent loop。「**從零到 deploy RAG service**」的完整參考。

**適合誰**：要把 RAG 真的 ship 給非開發者用的場景。比 LangChain RAG 完整很多，但複雜度也高。

**備註**：是 open-source RAG engine（可自架，附 Docker / 原始碼部署），不是封閉的 hosted service。雲端 demo 只是體驗用。

---

### [HKUDS/LightRAG](https://github.com/HKUDS/LightRAG)

| 欄位 | 內容 |
|---|---|
| 語言 | Python |
| Stars | ★ 34k+ |
| License | MIT |
| 推薦度 | ⭐⭐⭐⭐ |

**教什麼**：graph + vector hybrid retrieval，加上 summarization-based 的 long-context memory。EMNLP 2025 paper-backed。

**適合誰**：在「**長文件 / 長 context 怎麼記憶**」這個問題上想看研究級方法的人。跟 mem0、Letta 互補（它們偏 conversational memory）。

**備註**：研究風格的 codebase，比 ragflow 沒那麼 polish；學概念好用。

---

### [patchy631/ai-engineering-hub](https://github.com/patchy631/ai-engineering-hub)

| 欄位 | 內容 |
|---|---|
| 語言 | Python / Jupyter |
| Stars | ★ 34k+ |
| License | MIT |
| 推薦度 | ⭐⭐⭐⭐ |

**教什麼**：以主題為單位的 LLM / RAG / agent tutorial 集——每個主題一個 notebook，從 basic RAG 到 agent 應用都有。

**適合誰**：想看「同一個概念在不同情境下怎麼實作」的對照組學習者。跨多個 stage 都用得上的補充材料，放在 Stage 6 是因為 RAG 主題佔多數。

---

## ✅ 進入 Stage 7 前的自我檢查

你能不能：
- [ ] 寫一條 50 行的 RAG 流水線（load → chunk → embed → store → query → answer）
- [ ] 解釋為什麼天真的切塊在長文件上會失敗
- [ ] 針對 API 文件、PDF、表格設計不同的 chunking 策略
- [ ] 在某個規模下，能在 Chroma、Qdrant、pgvector 之間做出選擇
- [ ] 區分「給 agent memory」跟「用 RAG」這兩件事

如果都可以 → 前往 [Stage 7 — Multi-Agent · Production](07-multi-agent-production.md)。
