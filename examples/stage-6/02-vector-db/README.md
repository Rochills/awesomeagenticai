> **繁體中文** | [简体中文](./README.zh-Hans.md) | [English](./README.en.md)

# 練習 2：Vector DB（ChromaDB）+ semantic vs keyword

對應 [Stage 6 — Memory & RAG](../../../stages/06-memory-rag.md) 練習 2。
> 🎓 **學習模式**：這份 `starter.py` 是**完整解答**、不是 TODO skeleton。建議用**主動模式**——`mv starter.py starter_reference.py`、看 signature 不看 body、自己重寫一份 `starter.py`、跑 `python test.py` 驗證；卡 20 分鐘再回去對照 reference。完整方法論看 [`docs/HOW_TO_USE.md`](../../../docs/HOW_TO_USE.md)。

> 📚 **想要 chapter-length 深入版？** 本 folder 的 starter 是 illustrative 版、聚焦核心 pattern + 兩條 SDK path，不是 production-grade tutorial。深度教材推薦：
> - [`datawhalechina/hello-agents`](https://github.com/datawhalechina/hello-agents) ⭐ 中文圈最完整、章節式 + 16 種 production 能力。**本練習對應 hello-agents 的 vector store 章節**
> - [ChromaDB official tutorial](https://docs.trychroma.com/) + [Qdrant / Weaviate / Pinecone 對照](https://github.com/zilliztech/VectorDBBench)（production scale benchmark）
> - 完整 references 見 [Stage 6 § 精選 Projects](../../../stages/06-memory-rag.md#-精選-projects)


## 任務

把 8 個 doc 存進 Chroma、用同一個 query 比較 semantic（vector）跟 keyword（substring）兩種 retrieval。

## 怎麼跑

```bash
pip install -r requirements.txt
python starter.py   # 第一次自動下載 embedding model
```

預算：**$0**。Chroma in-memory mode、跑完就 release。

```bash
python test.py             # 5 個 test、驗 index/query/ranking
python test_anthropic.py   # Path B concept demo（同 starter）
```

## Vector DB 為什麼 vs 為什麼不

| 情境 | List comprehension + cosine | ChromaDB |
|---|---|---|
| < 100 doc | ✅ 簡單夠用 | overkill |
| 100-10K doc | 慢（每次 query 都 re-embed all） | ✅ 持久 + index |
| 10K+ doc | 不行 | ✅（或考慮 production-grade Qdrant / Weaviate） |
| Persistence | ❌ 每次重 embed | ✅ SQLite 後端 |
| Filter / metadata | 自己寫 | ✅ where clause |
| Hybrid search | 自己寫 | ✅ 有 BM25 + vector |

**經驗法則**：練習用 in-memory（`EphemeralClient`）、production 用 `PersistentClient(path=...)`。

## Semantic vs Keyword 對照

```
Query: "where to drink good coffee in Asian cities"

📝 Keyword (substring) → 漏 doc 3
    因為 query 沒有「coffee」精確字串
    （只要 query 換字面、就 miss）

🔍 Semantic (vector) → 抓到 doc 3
    "Coffee shops in Taipei often serve pour-over..."
    語意對齊、不靠字面
```

| 維度 | Keyword search | Semantic search (vector) |
|---|---|---|
| 同義詞 | 漏（"car" 跟 "auto" 不同） | 抓得到 |
| 換字面 | 漏 | 抓得到 |
| 拼字錯 | 漏 | 抓得到（小錯） |
| 精確專有名詞 | 強 | 偶爾混淆 |
| 否定（NOT） | 簡單 | 困難（embedding 不擅長） |
| 速度 | 快 | 中（要 embed query） |
| Production 用法 | BM25 + vector **hybrid** | 同左 |

**Production 結論**：兩條路都要、**hybrid search** 是 best practice。Chroma 0.4+ 內建 BM25 + vector hybrid（`query_texts` 加 `where` filter）。

## Chroma 核心 API

```python
client = chromadb.EphemeralClient()    # in-memory；PersistentClient(path=...) 用磁碟
embed_fn = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="...")
collection = client.get_or_create_collection(name="demo", embedding_function=embed_fn)

# Add docs（自動 embed）
collection.add(ids=[...], documents=[...], metadatas=[{"category": "..."}, ...])

# Query
collection.query(query_texts=[query], n_results=3, where={"category": "tech"})

# Update / Delete
collection.upsert(...)
collection.delete(ids=[...])
```

## 常見坑

- **重複 id `.add()`**：Chroma raise；用 `.upsert()` 或先檢查 `.get()["ids"]`
- **每次 query 重 build collection**：別這樣！`PersistentClient` 持久化、只 index 一次
- **`n_results` 太大**：Chroma 沒返回 reranker、k 太大就會吃到 noise。經驗值 3-10
- **Filter 用錯**：`where={"category": "tech"}` 是 metadata filter、`where_document={"$contains": "..."}` 是 doc 內容 filter
- **embedding function 一致性**：index 時用 model A、query 時用 model B、retrieval 會錯。Chroma 把 embedding_function 綁在 collection 上避免

## 想看 production-grade？

```bash
# Persistent mode
# In starter.py:
collection = build_collection(path="./chroma_db")   # 寫到磁碟

# Cloud embedding（更高精度）
# Replace SentenceTransformerEmbeddingFunction with:
embed_fn = embedding_functions.OpenAIEmbeddingFunction(api_key=..., model_name="text-embedding-3-small")
```

## 延伸

- **加 metadata filter**：`collection.query(query_texts=[q], where={"category": "food"})`
- **Hybrid search**：BM25 + vector、可以用 Chroma 0.4+ 或自己接 `rank_bm25` library
- **Swap to Qdrant / Weaviate**：production scale、需要 distributed
- **接練習 4**：完整 RAG pipeline 用同一個 collection
