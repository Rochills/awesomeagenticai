> [繁體中文](./README.md) | [简体中文](./README.zh-Hans.md) | **English**

# Exercise 1: Embeddings + Nearest Neighbors

Pairs with [Stage 6 — Memory & RAG](../../../stages/06-memory-rag.en.md) Exercise 1.

## Task

Embed 100 sentences, then for a query find the top-k most similar. Observe what cosine similarity ranking means.

## How to run — two paths

### Path A (default, free, local)

```bash
pip install -r requirements.txt
python starter.py   # downloads ~80 MB on first run
```

Budget: **$0**. `sentence-transformers/all-MiniLM-L6-v2` runs on CPU, ~100 sentences in < 1 second.

### Path B (cloud embedding, comparison, very cheap)

```bash
pip install -r requirements.txt
export OPENAI_API_KEY=sk-...
python starter_anthropic.py
```

Budget: ~**$0.00002** per run (text-embedding-3-small, 100 sentences).

> 💡 **Anthropic doesn't provide an embedding API** — they officially recommend [Voyage AI](https://www.voyageai.com/). This demo uses OpenAI (most common); swapping to Voyage is a client swap.

## Validate the logic

```bash
python test.py             # mock SentenceTransformer, no download
python test_anthropic.py   # mock OpenAI client, validate normalize
```

## Core concepts

```python
# 1. Encode → vector
sent_vecs = model.encode(sentences, normalize_embeddings=True)  # 100 × 384 vec
q_vec = model.encode([query], normalize_embeddings=True)[0]      # 384 vec

# 2. Cosine similarity = dot product (because normalized)
sims = sent_vecs @ q_vec        # 100 similarity scores

# 3. Top-k
top_idx = np.argsort(-sims)[:top_k]
```

**Why normalize**: normalized vectors' dot product equals cosine similarity directly (range [-1, 1]) — no need to recompute norms. Standard vector DB trick.

## Local vs cloud embedding

| Dimension | sentence-transformers (local) | OpenAI text-embedding-3-small (cloud) |
|---|---|---|
| Dims | 384 | 1536 |
| Speed (100 sents, CPU) | < 1s | 1-2s (incl. network) |
| Cost | $0 | $0.00002 / 100 sentences |
| Multilingual | OK (`paraphrase-multilingual-MiniLM-L12-v2`) | Strong |
| Long context (>512 tokens) | Truncated | Strong |
| Determinism | 100% | 99% (API has minor noise) |

**Bottom line**: personal / small data / local experimentation — sentence-transformers is plenty. Heavy multilingual / long docs / SaaS — go cloud.

## Common pitfalls

- **No normalization**: cosine ≠ dot product; compute `sim = dot(a,b) / (|a||b|)` yourself
- **Mixed precision**: sentence-transformers defaults to fp32; fp16 quantization (memory savings) shifts similarities 1-2%
- **Don't compare vectors across models**: MiniLM and OpenAI are different semantic spaces; cosines aren't comparable
- **Tiny queries**: 1-2 word queries embed poorly; use full sentences

## Want better embeddings?

```bash
# Larger local model (better accuracy, slower)
# In starter.py change MODEL_NAME to:
#   "sentence-transformers/all-mpnet-base-v2"           # 768 dims, ↑ accuracy
#   "sentence-transformers/paraphrase-multilingual-..." # multilingual

# Higher-quality cloud
EMBED_MODEL=text-embedding-3-large python starter_anthropic.py   # 3072 dims, $$
```

## Extensions

- **BM25 + embedding hybrid**: combine keyword and semantic — common in production
- **Add a reranker**: feed top-k to a cross-encoder (`cross-encoder/ms-marco-MiniLM-L-6-v2`) — big precision lift
- **Plug into Exercise 2 vector DB**: store in Chroma so you don't re-embed each run
