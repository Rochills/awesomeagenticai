# Stage 6 — 记忆 · RAG · 进阶

> [繁體中文](./06-memory-rag.md) | **简体中文** | [English](./06-memory-rag.en.md) | [Русский](./06-memory-rag.ru.md)

⏱ **时间估算**：2 周（约 10 小时）

> 💡 这 stage 用语密度高（**RAG / 向量数据库 / embedding / chunking / hybrid search / reranking⋯**）→ 不熟先翻 [`resources/glossary.zh-Hans.md` §3](../resources/glossary.zh-Hans.md#3-memory--retrieval--rag)。

不会记住过去互动的 agent 没什么用。RAG（Retrieval-Augmented Generation）是目前的标准做法。这一章两个都会讲到。

## 📌 学习目标

- 区分 short-term、long-term、episodic、semantic memory
- 理解 vector embedding 与相似度搜索
- 建一条基本 RAG 流水线（chunk → embed → store → retrieve → generate）
- 看出 RAG 不该用在哪些地方（以及该用在哪些地方）

## 📚 必修阅读

1. [**LlamaIndex — RAG concepts**](https://docs.llamaindex.ai/en/stable/getting_started/concepts/) — 最清楚的入门
2. [**LangChain — RAG tutorial**](https://python.langchain.com/docs/tutorials/rag/) — 动手做
3. [**Pinecone — Learning Center**](https://www.pinecone.io/learn/) — vector DB 基础
4. [**Anthropic — Contextual Retrieval**](https://www.anthropic.com/news/contextual-retrieval) — Anthropic 搭配 prompt caching 的 RAG 写法
5. [**LangChain — Text splitters**](https://docs.langchain.com/oss/python/integrations/splitters/index) — chunking 策略入门

## 🧭 单元指引

这一章先带你简单理解短期记忆与长期记忆，再聚焦到 RAG。

| 比较维度 | Short-term memory（短期记忆） | Long-term memory（长期记忆） |
|---|---|---|
| 中文可称 | 短期记忆 | 长期记忆 |
| 来源 | 当前对话内容 | 跨 session 或长期保存的信息 |
| 持续时间 | 短，通常限于当前 session | 长，可跨 session |
| 技术基础 | 上下文窗口（context window）/ prompt | 记忆存储层（memory store）/ 用户档案 / 向量数据库 |
| 适合记什么 | 任务细节、刚刚说过的内容 | 稳定偏好、长期目标、背景资料 |
| 是否受 context 长度限制 | 会，因为模型一次能看的内容有限 | 较不会，因为可以先存在外部，需要时再取一小段放回来 |
| 生活例子 | 刚刚收到的手机验证码、正在进行对话的上一句话 | 你深度掌握的知识、图书馆、知识库、读过的书 |

这里的工作阶段（session）可以理解成一次连续互动，例如同一段聊天、同一次任务，或同一次 agent 执行。

RAG 可以想成在帮 agent 盖图书馆。你要先把书放好、分类好，后续要查资料时，才会又快又精准。

最基础的 RAG 可以拆成两条流水线：

- **数据预处理**：ingest → chunk → embed → store（index）。这一步是在建立可检索的知识库。
- **检索生成**：retrieve → generate。这一步是在用户提问时，找出相关内容，再交给 LLM 生成回答。

![RAG 流水线总览](../resources/diagrams/rag-pipeline-overview.jpg)

图中的 RAG Fusion、query rewrite 等属于进阶检索技巧。第一次学 RAG 时，先理解主线流程即可。

上面只是最小骨架。设计与概念细节，会在下面各自区块展开。

读这章时可以顺便思考：RAG 不适合哪些应用场景？哪些场景适合 RAG，但基本 RAG 还不够好？

这会带到更进阶的 RAG 技术，例如 GraphRAG。有兴趣的同学可以思考，为何这种情境要设计这样的 RAG 解决方案，不用实现每种 RAG 技术或细节。

## 🧩 Chunking 怎么想

好的 chunking 可以让 LLM 在有限 context 内，用更精确、完整的信息生成回答。它不是把文字平均切开。

切法取决于应用场景与文档内容。它会决定 retriever 看见的最小语义单位。

一个好 chunk 要同时做到两件事：**够完整**，让模型看得懂上下文；**够聚焦**，让检索不带太多杂讯。chunk 太小会失去前后文，chunk 太大会让相似度搜索变钝。

常见策略：

- **固定长度（Fixed-Length）**：照字符数或 token 数切。优点是简单稳定；缺点是一板一眼，容易切断段落、句子或表格。
- **滑动窗口（Sliding Window）**：每个 chunk 之间保留重叠区块（overlap）。优点是比较不会在边界掉信息；缺点是索引量会变大。
- **递归切割（Recursive）**：先尝试保留段落，如果长度还是不适合，再退到句子、字词等更小单位。通常是入门 RAG 的好基准。
- **语义切割（Semantic Chunking）**：依 embedding 或语义变化切，也就是当前区块与前一个区块的语义相似度出现差异。适合长文件，但成本与复杂度较高。
- **混合策略（Hybrid）**：依照应用场景，思考不同文件结构该怎么混搭切法。例如，一篇论文可能要保留章节、表格、公式与引用脉络。

![Chunking 策略流程](../resources/diagrams/chunking-strategies.jpg)

第一次做 RAG 时，不要一开始就追求复杂切法。LangChain 文件建议多数情境先从 `RecursiveCharacterTextSplitter` 开始。

先跑出基准版本，再用后续 retrieval 结果决定要不要换策略。

```python
from langchain_text_splitters import RecursiveCharacterTextSplitter

text = "这是一个很长的文件内容...（此处省略一千字）..."

splitter = RecursiveCharacterTextSplitter(
    chunk_size=100,
    chunk_overlap=20,
    length_function=len,
)

chunks = splitter.split_text(text)
print(f"共切成 {len(chunks)} 个 chunk")
print(chunks[0])
```

直觉判断 chunking 好不好，可以先看两件事：

- 回答缺漏信息，或有头无尾：通常是 chunk 太小，或 overlap 不够。
- 回答包含正确信息，但混入无关内容：通常是 chunk 太大，或 top-k 捞太多。

Chunking 进阶思考：

- chunking 不是一次设定好就结束，要配合真实 query 与失败案例反复调整。
- chunk size、overlap、top-k、reranker 会互相影响，不要只单看其中一个参数。
- 想想看，如果今天要 RAG 的资料有含图片的 PDF、会议字幕档，要如何切割比较好？

## 🛠 动手练习（不是看过就好）

### 练习 1：Embeddings
把 100 个句子做 embedding，找出某个 query 的最近邻。理解 vector 之间的距离意义。

### 练习 2：Vector DB
把 embedding 存进 Chroma，做语义 query。比对“跟 keyword search 差在哪”。

### 练习 3：Chunking 对照
拿同一份文件做三种切法：固定长度、段落切法、heading-aware 切法。用 5 个真实问题比较 top-k 结果，记录哪种切法比较容易捞到正确上下文。

### 练习 4：完整 RAG 流水线
把一份 PDF 切块 → embed → 取 top-k → 生成回答。这是大多数 RAG 应用的基本骨架。

### 练习 5：Long-term Memory
让 agent 在多轮对话之间记得事情。可以用 `mem0` 或自己用 vector store 接。

## 🎯 精选 Projects

### [LlamaIndex](https://github.com/run-llama/llama_index)

| 栏位 | 内容 |
|---|---|
| Stars | ★ 49k+ |
| 推荐度 | ⭐⭐⭐⭐⭐ |

**教什么**：以 RAG 为核心的 framework。document loader、切块策略、retrieval pattern、query engine。

**适合谁**：以文件为主的应用。RAG 是它的核心。

---

### [Chroma](https://github.com/chroma-core/chroma)

| 栏位 | 内容 |
|---|---|
| Stars | ★ 27k+ |
| License | Apache-2.0 |
| 推荐度 | ⭐⭐⭐⭐⭐ |

**教什么**：开源 embedding 数据库。本机跑，不用搞基础设施。

**适合谁**：上面的练习 2、练习 4。最容易上手的 vector DB。

**怎么跑**：
```python
import chromadb
client = chromadb.Client()
collection = client.create_collection("hello")
collection.add(documents=["doc 1", "doc 2"], ids=["1", "2"])
results = collection.query(query_texts=["query"], n_results=1)
```

---

### [Qdrant](https://github.com/qdrant/qdrant)

| 栏位 | 内容 |
|---|---|
| Stars | ★ 31k+ |
| 推荐度 | ⭐⭐⭐⭐ |

**教什么**：production 等级的 vector DB，用 Rust 写，规模大时比 Chroma 快。

**适合谁**：当 Chroma 跟不上时。有云端版跟自架版。

---

### [Weaviate](https://github.com/weaviate/weaviate)

| 栏位 | 内容 |
|---|---|
| Stars | ★ 16k+ |
| 推荐度 | ⭐⭐⭐⭐ |

**教什么**：有内建模组（text2vec、generative、classification）的 vector DB。schema 驱动。

**适合谁**：production 部署、需要 schema 约束的场景。

---

### [pgvector](https://github.com/pgvector/pgvector)

| 栏位 | 内容 |
|---|---|
| Stars | ★ 21k+ |
| 推荐度 | ⭐⭐⭐⭐ |

**教什么**：在 PostgreSQL 里做向量相似度搜索。SQL 跟向量同一个 DB。

**适合谁**：原本就在用 PostgreSQL、不想多维护一个向量存储的团队。

---

### [LangChain — Memory](https://python.langchain.com/docs/concepts/memory/)

**教什么**：agent memory 模式（buffer、summary、vectorstore-backed）。

**适合谁**：agent 需要跨 session 记得事情时。

---

### [mem0ai/mem0](https://github.com/mem0ai/mem0)

| 栏位 | 内容 |
|---|---|
| Stars | ★ 54k+ |
| 推荐度 | ⭐⭐⭐⭐ |

**教什么**：给 AI agent 用的自我精炼 memory 层。跨 session 存储用户的事实。

**适合谁**：个人助理或 chatbot，需要用户层级 memory 的场景。

---

### [Letta（前身 MemGPT）](https://github.com/letta-ai/letta)

| 栏位 | 内容 |
|---|---|
| Stars | ★ 22k+ |
| 推荐度 | ⭐⭐⭐⭐ |

**教什么**：有阶层式 memory 的长 context agent。灵感来自 OS 的 memory management。

**适合谁**：context 要跑很久的 agent（以月为单位、不是分钟）。

---

### [chatchat-space/Langchain-Chatchat](https://github.com/chatchat-space/Langchain-Chatchat)

| 栏位 | 内容 |
|---|---|
| 语言 | 中文 + Python |
| Stars | ★ 38k+ |
| License | Apache-2.0 |
| 推荐度 | ⭐⭐⭐⭐ |

**教什么**：中文社群最广泛使用的 RAG + Agent 应用 framework，可离线部署、中文友善的默认值，支持 ChatGLM / Qwen / Llama / Ollama 后端。

**适合谁**：要做知识库 / RAG 应用的中文用户。默认值对中文分词 + embedding 处理得不错。

**备注**：最后一次更新是 2025 年 11 月（约 6 个月前——还算活着，但已经到边缘）。

---

### [Anthropic — Contextual Retrieval cookbook](https://platform.claude.com/cookbook/capabilities-contextual-embeddings-guide)

**教什么**：Anthropic 的 contextual retrieval 技巧搭配 prompt caching，附完整端到端范例。

**适合谁**：跑完基本 RAG 之后想升级到 contextual retrieval、在长文件上拿到更好 recall 的人。

**备注**：Anthropic 在 2025 年把 `anthropic-cookbook` 改名为 `claude-cookbooks`。上面的线上 notebook 是现在的标准参考；GitHub 上的原始路径可能会变动。

---

### [infiniflow/ragflow](https://github.com/infiniflow/ragflow)

| 栏位 | 内容 |
|---|---|
| 语言 | Python |
| Stars | ★ 79k+ |
| License | Apache-2.0 |
| 推荐度 | ⭐⭐⭐⭐⭐ |

**教什么**：production 等级的 RAG engine，含深度文件理解（layout、表格、OCR）+ hybrid retrieval + agent loop。“**从零到 deploy RAG service**”的完整参考。

**适合谁**：要把 RAG 真的 ship 给非开发者用的场景。比 LangChain RAG 完整很多，但复杂度也高。

**备注**：是 open-source RAG engine（可自架，附 Docker / 源码部署），不是封闭的 hosted service。云端 demo 只是体验用。

---

### [HKUDS/LightRAG](https://github.com/HKUDS/LightRAG)

| 栏位 | 内容 |
|---|---|
| 语言 | Python |
| Stars | ★ 34k+ |
| License | MIT |
| 推荐度 | ⭐⭐⭐⭐ |

**教什么**：graph + vector hybrid retrieval，加上 summarization-based 的 long-context memory。EMNLP 2025 paper-backed。

**适合谁**：在“**长文件 / 长 context 怎么记忆**”这个问题上想看研究级方法的人。跟 mem0、Letta 互补（它们偏 conversational memory）。

**备注**：研究风格的 codebase，比 ragflow 没那么 polish；学概念好用。

---

### [patchy631/ai-engineering-hub](https://github.com/patchy631/ai-engineering-hub)

| 栏位 | 内容 |
|---|---|
| 语言 | Python / Jupyter |
| Stars | ★ 34k+ |
| License | MIT |
| 推荐度 | ⭐⭐⭐⭐ |

**教什么**：以主题为单位的 LLM / RAG / agent tutorial 集——每个主题一个 notebook，从 basic RAG 到 agent 应用都有。

**适合谁**：想看“同一个概念在不同情境下怎么实作”的对照组学习者。跨多个 stage 都用得上的补充材料，放在 Stage 6 是因为 RAG 主题占多数。

---

## ✅ 进入 Stage 7 前的自我检查

你能不能：
- [ ] 写一条 50 行的 RAG 流水线（load → chunk → embed → store → query → answer）
- [ ] 解释为什么天真的切块在长文件上会失败
- [ ] 针对 API 文件、PDF、表格设计不同的 chunking 策略
- [ ] 在某个规模下，能在 Chroma、Qdrant、pgvector 之间做出选择
- [ ] 区分“给 agent memory”跟“用 RAG”这两件事

如果都可以 → 前往 [Stage 7 — Multi-Agent · Production](./07-multi-agent-production.zh-Hans.md)。
