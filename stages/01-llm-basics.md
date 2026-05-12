# Stage 1 — LLM 基礎

> **繁體中文** | [简体中文](./01-llm-basics.zh-Hans.md) | [English](./01-llm-basics.en.md) | [Русский](./01-llm-basics.ru.md)

⏱ **時間估算**：1 週（約 5-8 小時）

> 👋 **從 [Stage 0](00-foundations.md) 來的**：好，環境已經夠用——這 5-8 小時：第一次成功呼叫 Claude / GPT / Gemini API、搞懂 token / context window / temperature 怎麼影響輸出、用 per-token 計算實際成本。**直接從這裡開始的**：先確認你能跑 Python script、有任一家供應商的 API key——做不到請先回 [Stage 0](00-foundations.md)。

> 💡 **看不懂某個詞**（LLM / token / context window / temperature / RAG / agent⋯）→ 先翻 [`resources/glossary.md`](../resources/glossary.md) 查 30 秒再回來。

## 📌 學習目標

走完這個階段後你會：
- 解釋 LLM 是什麼、token 是什麼、context window 是什麼意思
- 第一次成功呼叫 Claude / GPT / Gemini API 並解析回應
- 在強項上比較四大 LLM 家族（Claude / GPT / Gemini / Llama）
- 用 per-token 計價來估算單次任務的成本

## 🚪 進入條件

你應該已經：
- 能跑 Python script
- 概念上知道 HTTP / REST 是什麼
- 至少有一家供應商的 API key（Anthropic / OpenAI / Google）

如果還沒——先回 Stage 0。

## 📚 必修閱讀

1. [**Anthropic — What is Claude?**](https://www.anthropic.com/news/claude-3-family) — 官方模型總覽
2. [**OpenAI Quickstart**](https://platform.openai.com/docs/quickstart) — 第一次 API call 的步驟
3. [**A Visual Guide to LLM Tokenizers**](https://huggingface.co/learn/llm-course/chapter6/1) — Hugging Face 的入門
4. [**Anthropic API Pricing**](https://www.anthropic.com/pricing#anthropic-api) — 把計價表看完，算一下 1k input + 1k output 的成本

## 🛠 動手練習（必做練習，不是看過就好）

### 練習：LLM API
五行 Python 呼叫 Claude API 並印出回應。

```python
from anthropic import Anthropic
client = Anthropic()
msg = client.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=100,
    messages=[{"role": "user", "content": "Hello, who are you?"}]
)
print(msg.content[0].text)
```

### 練習：Tokens
同一個 prompt 跑 100 次，觀察 token 數的變化。
- 注意：temperature ≠ 0 會產生變動
- 注意：同一句話的英文 vs 中文 token 數差異

### 練習：Pricing
算出你的 hello-world prompt 跑 1000 次的實際美金成本。用 Anthropic 的 pricing page + SDK 的 `usage` 欄位來算 token。

### 練習：Cross-Provider 比較
同一個 prompt 同時送給 Claude、GPT、Gemini，比較三家的回應差異。觀察「同一句話為什麼產生不同答案」——回答風格、長度、判斷取捨都不一樣。建議用 OpenAI、Anthropic、Google 三家 SDK 各一段程式呼叫。

### 練習：Error Handling
故意觸發錯誤情境並寫 retry：
- API key 錯誤 → 看怎麼 raise
- prompt 超長 → context window 滿了會發生什麼
- 網路斷掉 → 寫一個有 exponential backoff 的 retry wrapper
這是後面 Stage 3-7 寫 production agent 一定會用到的基礎。

### 練習：Local LLM
**不付 API 費用、跑在自己電腦上**：用 Ollama 下載一個小模型（建議 `llama3.2:3b` 或 `qwen2.5:3b`），用 OpenAI-相容 API 呼叫它。
```bash
# 裝 Ollama: https://ollama.com
ollama pull qwen2.5:3b
ollama serve  # 預設 port 11434
```
然後從 Python：
```python
from openai import OpenAI
client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")
r = client.chat.completions.create(
    model="qwen2.5:3b",
    messages=[{"role":"user","content":"用 3 句話介紹什麼是 ReAct"}]
)
print(r.choices[0].message.content)
```
**為什麼要做**：學會跑本地 LLM 後，後面 Stage 3-6 的實驗都不會被 API 費用卡住；隱私敏感場景也能 offline。

## 🎯 精選 Projects

### [Anthropic Cookbook](https://github.com/anthropics/anthropic-cookbook)

| 欄位 | 內容 |
|---|---|
| 語言 | Python |
| Stars | ★ 42k+ |
| License | MIT |
| 推薦度 | ⭐⭐⭐⭐⭐ |

**教什麼**：用 Claude API 處理常見場景的方法——chat、tools、citations、multi-modal、prompt caching。

**適合誰**：所有要開始用 Claude 的人。Notebook 會帶你走過每一個 API 功能，每個都有可以跑的範例。

**備註**：把它當參考書用，不要從頭讀到尾；遇到具體問題再來查。

**怎麼跑**：
```bash
git clone https://github.com/anthropics/anthropic-cookbook
cd anthropic-cookbook/skills/classification
pip install -r requirements.txt
jupyter notebook guide.ipynb
```

---

### [Anthropic Courses](https://github.com/anthropics/courses)

| 欄位 | 內容 |
|---|---|
| 語言 | Python / Jupyter |
| Stars | ★ 21k+ |
| License | NOASSERTION（上游未提供 SPDX；使用前請讀 LICENSE） |
| 推薦度 | ⭐⭐⭐⭐⭐ |

**教什麼**：Anthropic 官方教育課程系列——API 基礎、prompt evaluation、real-world prompting、tool use、Claude with Excel。每門課都是 Jupyter notebook 形式，可以邊讀邊跑。

**適合誰**：剛開始用 Claude API 的人。跟 Cookbook 互補：Cookbook 是「想做 X 怎麼做」的查詢手冊，Courses 是「從零開始系統性學一遍」的完整課程。

**備註**：建議先跑 `anthropic_api_fundamentals` 跟 `prompt_engineering_interactive_tutorial`。

---

### [OpenAI Cookbook](https://github.com/openai/openai-cookbook)

| 欄位 | 內容 |
|---|---|
| 語言 | Python / Jupyter |
| Stars | ★ 73k+ |
| License | MIT |
| 推薦度 | ⭐⭐⭐⭐⭐ |

**教什麼**：跟 Anthropic Cookbook 一樣，但是 GPT 家族版。大量 recipe、structured output、tool use、embedding。

**適合誰**：所有用 OpenAI API 的人。structured output 跟 function calling 的範例特別強。

**備註**：比 Anthropic 的 cookbook 大很多，要多用搜尋——不要一頁一頁瀏覽。

---

### [LangChain Academy](https://academy.langchain.com/)

| 欄位 | 內容 |
|---|---|
| 形式 | 免費線上課程 |
| 推薦度 | ⭐⭐⭐⭐ |

**教什麼**：LLM 基礎、embedding、RAG、agent——透過 LangChain 教。就算你最後不用 LangChain 也值得看。

**適合誰**：喜歡看影片教學的視覺型學習者。

**備註**：有些課程偏 LangChain 行銷，跳過那些，留下觀念課就好。

---

### [datawhalechina/happy-llm](https://github.com/datawhalechina/happy-llm)

| 欄位 | 內容 |
|---|---|
| 語言 | 中文（zh-Hans） |
| Stars | ★ 29k+ |
| License | Custom |
| 推薦度 | ⭐⭐⭐⭐⭐ |

**教什麼**：從零開始建 LLM——對應 Karpathy 的「Zero to Hero」課程的中文版。第 1-4 章從底層講 LLM 原理，後面接實作應用。

**適合誰**：想真正搞懂 LLM 怎麼運作、不只是會呼叫 API 的中文學習者。等同於 Hugging Face 的 LLM Course，但是中文。

---

### [datawhalechina/llm-universe](https://github.com/datawhalechina/llm-universe)

| 欄位 | 內容 |
|---|---|
| 語言 | 中文（zh-Hans） |
| Stars | ★ 12k+ |
| License | NOASSERTION |
| 推薦度 | ⭐⭐⭐⭐ |

**教什麼**：面向新手開發者的大模型應用開發教學。涵蓋 API 基礎、知識庫、RAG、進階技巧。

**適合誰**：想用 LLM *做點東西*（不只是理解）的中文新手。

---

### [jingyaogong/minimind](https://github.com/jingyaogong/minimind)

| 欄位 | 內容 |
|---|---|
| 語言 | 中文 + Python |
| Stars | ★ 48k+ |
| License | Apache-2.0 |
| 推薦度 | ⭐⭐⭐⭐⭐ |

**教什麼**：2 小時從零訓練 64M 參數 LLM——目前最熱門的中文「從零打造 LLM」實作 project。Pretrain + SFT + LoRA + DPO + RLHF 全部在同一個 repo。

**適合誰**：看完 Karpathy 影片之後，跑這個來實際感受每個訓練階段在真資料上的樣子。教學價值非常高。

---

### [datawhalechina/llm-cookbook](https://github.com/datawhalechina/llm-cookbook)

| 欄位 | 內容 |
|---|---|
| 語言 | 中文（zh-Hans） |
| Stars | ★ 23k+ |
| 最後更新 | ⚠️ 已停滯（2025 年 6 月；停約 1 年） |
| License | Custom (CC BY-NC-SA) |
| 推薦度 | ⭐⭐⭐⭐ |

**教什麼**：把 Andrew Ng 的 prompt engineering / building systems / fine-tuning 課程翻譯改編給中文學習者。有可以動手的 notebook。

**適合誰**：想要一條完整 LLM 學習路線的中文新手。

**備註**：內容是 zh-Hans（Datawhale 用簡中），但技術內容看得懂沒問題。免費中文入門資源中相當好的選擇。

---

### [Hugging Face — Large Language Model Course](https://huggingface.co/learn/llm-course)

| 欄位 | 內容 |
|---|---|
| 形式 | 免費線上課程 + notebook |
| License | Apache 2.0 |
| 推薦度 | ⭐⭐⭐⭐ |

**教什麼**：LLM 內部到底怎麼運作（tokenization、transformer、fine-tuning），搭配 Hugging Face 生態系。

**適合誰**：想搞懂內部機制、不只想看 API 表面的讀者。

---

### 🖥️ 本地端執行 LLM（不用付 API 費用）

下面 4 個是「**把 LLM 跑在自己電腦上**」的工具——適合 練習：Local LLM 之後想深入的人，也是隱私敏感、API 費用敏感、或要 offline 工作場景的解法。

---

### [ollama/ollama](https://github.com/ollama/ollama)

| 欄位 | 內容 |
|---|---|
| 語言 | Go |
| Stars | ★ 170k+ |
| License | MIT |
| 推薦度 | ⭐⭐⭐⭐⭐ |

**教什麼**：最容易上手的本地 LLM runner——一行 `ollama pull qwen2.5:3b` 就有一個能跑的模型，內建 OpenAI-相容 API（`http://localhost:11434/v1`），既有的 OpenAI SDK 程式碼幾乎不用改。

**適合誰**：第一次跑本地 LLM 的人。也適合在 agent 開發時當 fallback——主流程接 Claude，砍成本的部分接 Ollama。

**怎麼跑**：
```bash
# https://ollama.com 下載安裝
ollama pull qwen2.5:3b   # 中文友善的小模型，約 2GB
ollama run qwen2.5:3b    # 互動 chat
ollama serve             # 啟動 API server
```

---

### [ggml-org/llama.cpp](https://github.com/ggml-org/llama.cpp)

| 欄位 | 內容 |
|---|---|
| 語言 | C++ |
| Stars | ★ 108k+ |
| License | MIT |
| 推薦度 | ⭐⭐⭐⭐ |

**教什麼**：Ollama 跟一堆本地 LLM 工具底層都在用的 inference engine。理解 quantization（GGUF 格式、Q4_K_M / Q5_K_S 各代表什麼）、KV cache、CPU/GPU offloading 怎麼運作。

**適合誰**：想搞清楚「為什麼 7B 模型可以塞進 8GB RAM」的人。Ollama 用起來夠了的話，可以暫時不碰；要 fine-grained 控制就回來讀這個。

---

### [mudler/LocalAI](https://github.com/mudler/LocalAI)

| 欄位 | 內容 |
|---|---|
| 語言 | Go |
| Stars | ★ 46k+ |
| License | MIT |
| 推薦度 | ⭐⭐⭐⭐ |

**教什麼**：drop-in 的 OpenAI API 替代品——同一份 OpenAI SDK 程式碼，把 base_url 改指到 LocalAI，就能在本地跑 LLM、embedding、image generation、TTS、STT。

**適合誰**：團隊有合規 / 資料隱私要求，要把 OpenAI 全套服務改成本地的場景。比 Ollama 範圍更廣（不只 chat）。

---

### [ml-explore/mlx](https://github.com/ml-explore/mlx)

| 欄位 | 內容 |
|---|---|
| 語言 | C++ / Python |
| Stars | ★ 25k+ |
| License | MIT |
| 推薦度 | ⭐⭐⭐ |

**教什麼**：Apple 為 Apple Silicon（M1/M2/M3/M4 晶片）量身打造的 ML framework。在 Mac 上跑本地 LLM 通常比 llama.cpp 還快，記憶體效率好。

**適合誰**：用 MacBook 開發、想榨乾 Apple Silicon 性能的人。Linux / Windows 使用者可跳。

**備註**：搭配 `mlx-lm` package 用最方便。

**備註**：比 cookbook 學術一點。有講訓練，不只是 inference。

---

### [karpathy/LLM101n](https://github.com/karpathy/LLM101n)

| 欄位 | 內容 |
|---|---|
| 狀態 | ⚠️ 已封存（最後更新 2024 年 8 月）；只有大綱，從未真正寫完 |
| 推薦度 | ⭐⭐ |

**教什麼**：原本要做成 Karpathy 招牌教學風格的「Storyteller AI LLM」從零打造課程。

**適合誰**：直接去看 Karpathy 的「Let's build GPT from scratch」YouTube 影片即可——那部完整又精彩。

**備註**：這個 repo 只有大綱，課程沒做出來，列在這裡只是當歷史紀錄。

---

### [Anthropic — Claude API Quickstart](https://docs.anthropic.com/en/docs/get-started)

| 欄位 | 內容 |
|---|---|
| 形式 | 文件 |
| 推薦度 | ⭐⭐⭐⭐⭐ |

**教什麼**：Claude API 的官方文件。

**適合誰**：直接當參考用，加到書籤。

---

### [karpathy — Let's build GPT from scratch](https://www.youtube.com/watch?v=kCc8FmEb1nY)

| 欄位 | 內容 |
|---|---|
| 形式 | YouTube 影片（2 小時） |
| 推薦度 | ⭐⭐⭐⭐⭐ |

**教什麼**：用 PyTorch 從零開始打造 transformer-based GPT。對 LLM 內部運作有奠基性的理解。

**適合誰**：想搞懂 LLM 為什麼會這樣表現（不只是怎麼呼叫）的人。

**備註**：2 小時的高密度內容。暫停跟著寫程式碼，不要被動看。

---

### [rasbt/LLMs-from-scratch](https://github.com/rasbt/LLMs-from-scratch)

| 欄位 | 內容 |
|---|---|
| 語言 | Python / Jupyter |
| Stars | ★ 91k+ |
| License | Apache-2.0 |
| 推薦度 | ⭐⭐⭐⭐⭐ |

**教什麼**：用 PyTorch 從零打造一個 GPT-style LLM——tokenizer → attention → pretraining → finetuning，配套 Sebastian Raschka 的書。完整的 notebook + code，章節對應書本。

**適合誰**：想真正搞懂 token、attention、weights 是什麼的人。跟 Karpathy 影片互補——影片是 2 小時 fly-by，這個是慢慢讀完整本書的版本。

**備註**：是書籍的配套程式碼（Apache-2.0），可自由 fork 跟改。

---

## ✅ 進 Stage 2 前的自我檢查

你能不能：
- [ ] 用 5 行 Python 呼叫 Claude API
- [ ] 解釋為什麼「你好」可能用 2 個 token，但「Hello」只用 1 個
- [ ] 大致說出 Claude Sonnet vs Opus 的 per-token 價格
- [ ] 各說出 Claude / GPT / Gemini / Llama 的一個強項

如果可以 → 進 [Stage 2 — Prompt Engineering](02-prompt-engineering.md)。

如果不行 → 重看 Anthropic Quickstart + 把上面 3 個 hello-X 都跑一次。

---

> ✅ **Stage 1 完成？** 接下來 [**Stage 2 — Prompt Engineering**](02-prompt-engineering.md) 會用 5-12 小時帶你寫出可重用的結構化 prompt、用 few-shot 跟 chain-of-thought 解推理題、並學會用 eval 量化 prompt 改善幅度。**繼續往下走 →**
