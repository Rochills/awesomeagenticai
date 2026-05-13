> **繁體中文** | [简体中文](./README.zh-Hans.md) | [English](./README.en.md)

# 練習 3：Chunking 對照（fixed / paragraph / heading-aware）

對應 [Stage 6 — Memory & RAG](../../../stages/06-memory-rag.md) 練習 3。
> 🎓 **學習模式**：這份 `starter.py` 是**完整解答**、不是 TODO skeleton。建議用**主動模式**——`mv starter.py starter_reference.py`、看 signature 不看 body、自己重寫一份 `starter.py`、跑 `python test.py` 驗證；卡 20 分鐘再回去對照 reference。完整方法論看 [`docs/HOW_TO_USE.md`](../../../docs/HOW_TO_USE.md)。

> 📚 **想要 chapter-length 深入版？** 本 folder 的 starter 是 illustrative 版、聚焦核心 pattern + 兩條 SDK path，不是 production-grade tutorial。深度教材推薦：
> - [`datawhalechina/hello-agents`](https://github.com/datawhalechina/hello-agents) ⭐ 中文圈最完整、章節式 + 16 種 production 能力。**本練習對應 hello-agents 的 RAG chunking 章節**
> - [LangChain RecursiveCharacterTextSplitter docs](https://python.langchain.com/docs/how_to/recursive_text_splitter/) + [LlamaIndex SemanticSplitter](https://docs.llamaindex.ai/en/stable/api_reference/node_parsers/semantic_splitter/)
> - 完整 references 見 [Stage 6 § 精選 Projects](../../../stages/06-memory-rag.md#-精選-projects)


## 任務

同一份文件 → 3 種切法、跑 5 個 query、看哪種切法 retrieval 最準。

| 策略 | 怎麼切 | 適合 |
|---|---|---|
| **fixed-length** | 每 N 字一段、有 overlap | 純文字（log / chat history） |
| **paragraph** | 雙 newline 為界 | 散文 / 文章 |
| **heading-aware** | 看 `# / ##` 切 | structured doc（README / wiki / spec） |

## 怎麼跑

```bash
pip install -r requirements.txt
python starter.py   # 第一次自動下載 embedding model
```

預算：**$0**（純本機）。

```bash
python test.py             # 4 個 test、驗 chunking 邏輯
python test_anthropic.py   # Path B concept demo
```

## 3 種策略對照

### Fixed-length

```python
def chunk_fixed(text, chunk_size=200, overlap=40):
    # 每 200 字一塊、40 字重疊
    # 簡單但會切壞句子
```

**優點**：實作 1 行、適用所有文字
**缺點**：切到一半句子、語意被打斷

### Paragraph-based

```python
def chunk_paragraphs(text):
    return text.split("\n\n")
```

**優點**：保語意完整
**缺點**：段落長度不一（10 字 vs 500 字混在一起、embedding 不準）

### Heading-aware

```python
def chunk_headings(text):
    return re.split(r"\n(?=#{1,3} )", text)
```

**優點**：每個 chunk 含 heading（給 retrieval 額外 signal）、structure 清楚
**缺點**：要 markdown / structured doc。PDF / 純文字無 heading 就不行

## 觀察重點

對 query「How much does the MRT cost?」：

- **fixed-length**：可能切到「...EasyCard is the universal payment. A single ride...」（MRT cost 跟前後 chunk 切開了）
- **paragraph**：抓到完整 Transit 段、含 NT$20-65
- **heading-aware**：抓到完整 ## Transit section、含 heading「Transit」（embedding 對「MRT cost」的相似度更高）

對 query「What food can I try?」：

- **fixed-length**：抓到含 Food section 的 chunk、但可能 boundary 不對
- **paragraph**：抓到 Food 內某個段落
- **heading-aware**：抓到 `## Food` 整段、含 Shilin / dan bing / coffee 資訊一次到位

**punchline**：**chunking 策略決定 RAG 上限**——retrieval 抓不到的內容、再強的 LLM 也答不出。

## Production 額外考量

- **Chunk size**：經驗 200-1000 字（取決於 embedding model 的 token limit、MiniLM 是 512 token）
- **Overlap**：fixed-length 用 10-20% overlap、避免句子被切壞
- **Reranker**：撈 top-20、丟 cross-encoder rerank 留 top-5、精度大躍進
- **Metadata**：每個 chunk 加 `{"section": "Transit"}` 等 metadata、query 時可 filter
- **混合策略**：先 heading 切大塊、每塊內再 fixed-length 切小塊（兩層 hierarchy）

## 常見坑

- **Chunk 太大**：embedding 平均掉細節、retrieval 抓不到精準段落
- **Chunk 太小**：context 不足、LLM 看不到 holistic 答案。需要更多 top-k 補
- **沒測過真實 query**：開發時用 toy query 驗、production query 完全不同。**永遠用真實 query 校 chunking**
- **PDF chunking 直接套 markdown 邏輯**：PDF 有 column / footnote / table、要用 `pdfplumber` 或 `unstructured` 庫處理
- **CJK 文本切到一半字元**：UTF-8 byte slice 會切壞 multi-byte char。用 character-level slice

## 想看更聰明的 chunking？

- **`LangChain RecursiveCharacterTextSplitter`**：自動 fallback、先 try `\n\n`、再 `\n`、再 `.`、再 char
- **`LlamaIndex SemanticSplitter`**：用 embedding 找語意斷點切（最準、慢）
- **`unstructured`**：對 PDF / DOCX / HTML 全套處理

## 延伸

- **改變 chunk_size 跑 grid search**：對 5 個 query、看哪個 size 平均 sim 最高
- **加 metadata filter**：每個 chunk 標 section、query 時可指定「只在 Food section 搜」
- **接練習 4 完整 RAG**：選好 chunking 策略後、丟給 LLM 生答案
