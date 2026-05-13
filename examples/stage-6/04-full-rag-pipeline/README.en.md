> [繁體中文](./README.md) | [简体中文](./README.zh-Hans.md) | **English**

# Exercise 4: Full RAG Pipeline

Pairs with [Stage 6 — Memory & RAG](../../../stages/06-memory-rag.en.md) Exercise 4.

## Task

Tie Exercises 1-3 together:

```
doc → chunk_doc → embed → ChromaDB → top_k retrieve → LLM generation
```

Sample KB is a company onboarding doc with 4 sections (vacation / remote / expenses / tech stack).

## How to run — two paths

### Path A (default, free, local)

```bash
pip install -r requirements.txt
ollama pull qwen2.5:3b
ollama serve
python starter.py
```

Budget: **$0**.

### Path B (Anthropic, cloud-quality answers)

```bash
pip install -r requirements.txt
export ANTHROPIC_API_KEY=sk-ant-...
python starter_anthropic.py
```

Budget: ~**$0.001** per run.

## Validate the logic

```bash
python test.py             # 5 tests — mock LLM, exercise full pipeline
python test_anthropic.py   # Anthropic mock
```

`test.py` uses a mock LLM through the full pipeline (chunking → retrieval → generation), confirming the prompt actually includes context and `generate` sees the retrieval output.

## RAG in 4 steps

```python
def rag(query, doc):
    collection = build_kb(doc)           # 1. chunk + embed + index (one-time)
    contexts = retrieve(collection, q)    # 2. top-k semantic search
    answer = generate(q, contexts)        # 3. LLM reads context, answers
    return {"contexts": contexts, "answer": answer}
```

Each step has independent trade-offs:

| Step | Main knob | Affects |
|---|---|---|
| chunk | size / overlap / strategy | retrieval ceiling |
| embed | model size / multilingual | retrieval precision |
| retrieve | top_k / metadata filter / reranker | recall vs precision |
| generate | prompt / model / temperature | answer quality |

## Generation prompt pattern

```python
prompt = f"""Answer the user's question based ONLY on the context below.
If the context doesn't contain the answer, say "I don't have that information".

Context:
{context_text}

Question: {query}

Answer:"""
```

**Three key instructions**:
1. `based ONLY on context` — prevents hallucination
2. `if missing → say so` — gives the LLM an out, no forced answers
3. Context then Question — models prefer this layout

## Path comparison

| Observation | Anthropic Claude haiku | Ollama qwen2.5:3b |
|---|---|---|
| Grounding in context | Stable (sticks to context) | Sometimes drifts, fills with general knowledge |
| "I don't have that info" rate | High (follows rules) | Low (forces an answer) |
| Fluency | High | Medium |
| Multi-context integration | Good | Sometimes only looks at the first |
| Speed | 1-3s | 5-15s on CPU |
| Cost | $0.001 | $0 |

**Production reality**: RAG quality = retrieval quality × generation quality. Retrieval miss → LLM hallucinates; retrieval good but LLM weak → low-quality answer. Stage 7 production often uses local / mid-size for retrieval and Claude / GPT for generation.

## Common pitfalls

- **No "only based on context" instruction**: LLM goes off-script, fills from training data — uncontrolled
- **`top_k` too high**: long context, attention diffuses, wrong answers
- **`top_k` too low**: misses key sections, can't answer
- **Context after the question**: LLMs weight the start of the prompt more; put context first
- **No eval for "say unknown when you can't answer"**: production needs 5-10 eval cases for this

## Production-grade RAG

- **Persistent ChromaDB**: `chromadb.PersistentClient(path=...)` to skip re-indexing
- **Reranker**: retrieve top-20, cross-encoder rerank, keep top-3
- **Citation**: prompt "cite which context section you used", LLM tags [chunk_0]
- **Streaming**: `client.chat.completions.create(stream=True)`
- **LangGraph integration**: turn retrieve → generate into graph nodes with fallback path

## Extensions

- **Query rewriting**: LLM rewrites the user query into something better for retrieval (HyDE pattern)
- **Multi-hop RAG**: first retrieve gives partial answer, use partial answer to retrieve more
- **Plug into Exercise 5 long-term memory**: dialogue history also goes into vector store
