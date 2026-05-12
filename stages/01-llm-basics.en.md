# Stage 1 — LLM Fundamentals

> [繁體中文](./01-llm-basics.md) | [简体中文](./01-llm-basics.zh-Hans.md) | **English** | [Русский](./01-llm-basics.ru.md)


⏱ **Time estimate**: 1 week (~5-8 hours)

> 👋 **Coming from [Stage 0](00-foundations.en.md)?** Nice — your toolchain is set. The next 5-8 hours: your first working call to Claude / GPT / Gemini, how token / context window / temperature shape the output, and per-token cost estimation. **Jumped straight here?** Make sure you can run a Python script and have an API key from one provider — if not, head back to [Stage 0](00-foundations.en.md).

> 💡 **Don't recognize a term?** (LLM / token / context window / temperature / RAG / agent / …) → check [`resources/glossary.en.md`](../resources/glossary.en.md) for 30-second definitions.

## 📌 Learning Goals

After this stage you will be able to:
- Explain what an LLM is, what tokens are, and what context window means
- Make your first API call to Claude / GPT / Gemini and parse the response
- Compare the four major LLM families (Claude / GPT / Gemini / Llama) on strengths
- Estimate cost per task using per-token pricing

## 🚪 Entry Conditions

You should already:
- Be able to run a Python script
- Know what HTTP / REST is conceptually
- Have an API key from at least one provider (Anthropic / OpenAI / Google)

If not — go back to Stage 0 first.

## 📚 Required Reading

1. [**Anthropic — What is Claude?**](https://www.anthropic.com/news/claude-3-family) — official model overview
2. [**OpenAI Quickstart**](https://platform.openai.com/docs/quickstart) — first API call walkthrough
3. [**A Visual Guide to LLM Tokenizers**](https://huggingface.co/learn/llm-course/chapter6/1) — Hugging Face's intro
4. [**Anthropic API Pricing**](https://www.anthropic.com/pricing#anthropic-api) — read the pricing table, calculate cost for 1k input + 1k output

## 🛠 Hands-on Exercises (do them, not just read)

### Exercise: LLM API
Five-line Python script that calls Claude API and prints the response.

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

### Exercise: Tokens
Run the same prompt 100 times and watch token counts vary.
- Notice: temperature ≠ 0 produces variation
- Notice: token count for the SAME English vs Chinese sentence

### Exercise: Pricing
Calculate the actual dollar cost of running 1000 inferences for your hello-world prompt. Use Anthropic's pricing page + count tokens via the SDK's `usage` field.

### Exercise: Cross-Provider Comparison
Send the same prompt to Claude, GPT, and Gemini simultaneously, compare their responses. Notice "why does the same input produce different answers" — answer style, length, and judgment all differ. Use the OpenAI, Anthropic, and Google SDKs side-by-side.

### Exercise: Error Handling
Trigger error conditions deliberately and write retry logic:
- Wrong API key → see how it raises
- Over-long prompt → what happens when the context window is full
- Network drop → write a retry wrapper with exponential backoff
This is foundational for Stage 3-7's production agent code.

### Exercise: Local LLM
**No API fees, runs on your machine**: use Ollama to pull a small model (recommend `llama3.2:3b` or `qwen2.5:3b`), call it via OpenAI-compatible API.
```bash
# Install Ollama: https://ollama.com
ollama pull qwen2.5:3b
ollama serve  # default port 11434
```
Then from Python:
```python
from openai import OpenAI
client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")
r = client.chat.completions.create(
    model="qwen2.5:3b",
    messages=[{"role":"user","content":"Explain ReAct in 3 sentences"}]
)
print(r.choices[0].message.content)
```
**Why do this**: once you can run local LLMs, Stage 3-6 experiments aren't bottlenecked on API costs; privacy-sensitive work also stays offline.

## 🎯 Curated Projects

### [Anthropic Cookbook](https://github.com/anthropics/anthropic-cookbook)

| Field | Value |
|---|---|
| Language | Python |
| Stars | ★ 42k+ |
| License | MIT |
| Recommendation | ⭐⭐⭐⭐⭐ |

**What it teaches**: How to call Claude API for every common pattern — chat, tools, citations, multi-modal, prompt caching.

**Best for**: Anyone starting with Claude. The notebooks walk you through every API feature with runnable examples.

**Notes**: Treat this as your reference manual. Don't try to read it cover-to-cover; use as needed when you hit a specific question.

**Run it**:
```bash
git clone https://github.com/anthropics/anthropic-cookbook
cd anthropic-cookbook/skills/classification
pip install -r requirements.txt
jupyter notebook guide.ipynb
```

---

### [Anthropic Courses](https://github.com/anthropics/courses)

| Field | Value |
|---|---|
| Language | Python / Jupyter |
| Stars | ★ 21k+ |
| License | NOASSERTION (no SPDX upstream; check LICENSE before use) |
| Recommendation | ⭐⭐⭐⭐⭐ |

**What it teaches**: Anthropic's official educational course series — API fundamentals, prompt evaluation, real-world prompting, tool use, Claude with Excel. Each course is a Jupyter notebook you can read and run.

**Best for**: Anyone starting with the Claude API. Complements the Cookbook: Cookbook is a "how do I do X?" lookup, Courses is a "learn it from zero, end-to-end" tutorial.

**Notes**: Start with `anthropic_api_fundamentals` and `prompt_engineering_interactive_tutorial`.

---

### [OpenAI Cookbook](https://github.com/openai/openai-cookbook)

| Field | Value |
|---|---|
| Language | Python / Jupyter |
| Stars | ★ 73k+ |
| License | MIT |
| Recommendation | ⭐⭐⭐⭐⭐ |

**What it teaches**: Same as Anthropic Cookbook but for GPT family. Massive collection of recipes, structured outputs, tool use, embeddings.

**Best for**: Anyone using OpenAI API. The structured outputs and function calling examples are particularly strong.

**Notes**: Larger than Anthropic's cookbook. Use the search heavily — don't browse linearly.

---

### [LangChain Academy](https://academy.langchain.com/)

| Field | Value |
|---|---|
| Format | Free online courses |
| Recommendation | ⭐⭐⭐⭐ |

**What it teaches**: LLM fundamentals, embeddings, RAG, agents — taught through LangChain. Good even if you don't end up using LangChain.

**Best for**: Visual learners who want video walkthroughs.

**Notes**: Some lessons are LangChain-marketing-heavy. Skip those, take the conceptual lessons.

---

### [datawhalechina/happy-llm](https://github.com/datawhalechina/happy-llm)

| Field | Value |
|---|---|
| Language | 中文 (zh-Hans) |
| Stars | ★ 29k+ |
| License | Custom |
| Recommendation | ⭐⭐⭐⭐⭐ |

**What it teaches**: Build LLM from scratch — Chinese-language equivalent of Karpathy's "Zero to Hero" course. Chapters 1-4 cover LLM principles bottom-up, then practical applications.

**Best for**: Chinese-speaking learners who want to truly understand how LLMs work, not just call APIs. Direct counterpart to Hugging Face's LLM Course but in Chinese.

---

### [datawhalechina/llm-universe](https://github.com/datawhalechina/llm-universe)

| Field | Value |
|---|---|
| Language | 中文 (zh-Hans) |
| Stars | ★ 12k+ |
| License | NOASSERTION |
| Recommendation | ⭐⭐⭐⭐ |

**What it teaches**: A beginner-friendly LLM application development tutorial in Chinese. Covers API basics, knowledge bases, RAG, advanced techniques.

**Best for**: Chinese-speaking beginners who want to *build something* with LLM (vs. just understand them).

---

### [jingyaogong/minimind](https://github.com/jingyaogong/minimind)

| Field | Value |
|---|---|
| Language | 中文 + Python |
| Stars | ★ 48k+ |
| License | Apache-2.0 |
| Recommendation | ⭐⭐⭐⭐⭐ |

**What it teaches**: Train a 64M-parameter LLM from scratch in 2 hours — the most popular Chinese hands-on "build LLM from scratch" project. Pretrain + SFT + LoRA + DPO + RLHF all in one repo.

**Best for**: After watching Karpathy's video, run this to actually feel each training stage on real data. The pedagogical value is exceptional.

---

### [datawhalechina/llm-cookbook](https://github.com/datawhalechina/llm-cookbook)

| Field | Value |
|---|---|
| Language | 中文 (zh-Hans) |
| Stars | ★ 23k+ |
| Last update | ⚠️ Stale (Jun 2025; ~1 year inactive) |
| License | Custom (CC BY-NC-SA) |
| Recommendation | ⭐⭐⭐⭐ |

**What it teaches**: Andrew Ng's prompt engineering / building systems / fine-tuning courses translated and adapted for Chinese learners. Hands-on notebooks.

**Best for**: Chinese-speaking beginners who want a guided LLM curriculum.

**Notes**: zh-Hans content (Datawhale uses simplified Chinese) — but technical content transfers fine. Excellent free Chinese-language entry point.

---

### [Hugging Face — Large Language Model Course](https://huggingface.co/learn/llm-course)

| Field | Value |
|---|---|
| Format | Free online course + notebooks |
| License | Apache 2.0 |
| Recommendation | ⭐⭐⭐⭐ |

**What it teaches**: How LLMs actually work (tokenization, transformers, fine-tuning) with Hugging Face ecosystem.

**Best for**: Readers who want to understand what's happening inside, not just the API surface.

---

### 🖥️ Running LLMs Locally (no API fees)

The four entries below are tools to **run LLMs on your own machine** — useful after Exercise: Local LLM, and the answer for privacy-sensitive work, cost-sensitive experiments, or offline scenarios.

---

### [ollama/ollama](https://github.com/ollama/ollama)

| Field | Value |
|---|---|
| Language | Go |
| Stars | ★ 170k+ |
| License | MIT |
| Recommendation | ⭐⭐⭐⭐⭐ |

**What it teaches**: The easiest local LLM runner — one `ollama pull qwen2.5:3b` and you have a working model with built-in OpenAI-compatible API (`http://localhost:11434/v1`); existing OpenAI SDK code barely needs to change.

**Best for**: First-time local LLM users. Also useful as fallback in agent dev — main path on Claude, cost-sensitive parts on Ollama.

**Run it**:
```bash
# Download from https://ollama.com
ollama pull qwen2.5:3b   # ~2GB, decent Chinese support
ollama run qwen2.5:3b    # interactive chat
ollama serve             # start API server
```

---

### [ggml-org/llama.cpp](https://github.com/ggml-org/llama.cpp)

| Field | Value |
|---|---|
| Language | C++ |
| Stars | ★ 108k+ |
| License | MIT |
| Recommendation | ⭐⭐⭐⭐ |

**What it teaches**: The inference engine that Ollama and many local LLM tools use under the hood. Understand quantization (GGUF format, what Q4_K_M / Q5_K_S mean), KV cache, CPU/GPU offloading.

**Best for**: People who want to know "why can a 7B model fit in 8GB RAM?" If Ollama is enough for you, skip; come back when you need fine-grained control.

---

### [mudler/LocalAI](https://github.com/mudler/LocalAI)

| Field | Value |
|---|---|
| Language | Go |
| Stars | ★ 46k+ |
| License | MIT |
| Recommendation | ⭐⭐⭐⭐ |

**What it teaches**: Drop-in OpenAI API replacement — same OpenAI SDK code, point `base_url` at LocalAI, and run LLM, embedding, image generation, TTS, STT all locally.

**Best for**: Teams with compliance / data-privacy requirements that need to replace the entire OpenAI stack with local alternatives. Broader scope than Ollama (not just chat).

---

### [ml-explore/mlx](https://github.com/ml-explore/mlx)

| Field | Value |
|---|---|
| Language | C++ / Python |
| Stars | ★ 25k+ |
| License | MIT |
| Recommendation | ⭐⭐⭐ |

**What it teaches**: Apple's ML framework purpose-built for Apple Silicon (M1/M2/M3/M4 chips). On Macs, often faster than llama.cpp with better memory efficiency.

**Best for**: Mac developers wanting to squeeze maximum performance from Apple Silicon. Linux / Windows users can skip.

**Notes**: Pair it with the `mlx-lm` package for the easiest path.

**Notes**: More academic than cookbooks. Covers training, not just inference.

---

### [karpathy/LLM101n](https://github.com/karpathy/LLM101n)

| Field | Value |
|---|---|
| Status | ⚠️ Archived (last update Aug 2024); outline only — never built out |
| Recommendation | ⭐⭐ |

**What it teaches**: Originally pitched as a build-from-scratch "Storyteller AI LLM" course in Karpathy's signature pedagogical style.

**Best for**: Watch Karpathy's "Let's build GPT from scratch" YouTube video instead — that one is complete and excellent.

**Notes**: The repo is just an outline; the course was never built out. Listed for historical reference only.

---

### [Anthropic — Claude API Quickstart](https://docs.anthropic.com/en/docs/get-started)

| Field | Value |
|---|---|
| Format | Documentation |
| Recommendation | ⭐⭐⭐⭐⭐ |

**What it teaches**: The Claude API official documentation.

**Best for**: Direct reference. Bookmark this.

---

### [karpathy — Let's build GPT from scratch](https://www.youtube.com/watch?v=kCc8FmEb1nY)

| Field | Value |
|---|---|
| Format | YouTube video (2 hours) |
| Recommendation | ⭐⭐⭐⭐⭐ |

**What it teaches**: Build a transformer-based GPT from scratch in PyTorch. Foundational understanding of how LLMs work internally.

**Best for**: Anyone who wants to understand WHY LLMs behave the way they do, not just HOW to call them.

**Notes**: 2 hours of dense content. Pause and code along — don't passively watch.

---

### [rasbt/LLMs-from-scratch](https://github.com/rasbt/LLMs-from-scratch)

| Field | Value |
|---|---|
| Language | Python / Jupyter |
| Stars | ★ 91k+ |
| License | Apache-2.0 |
| Recommendation | ⭐⭐⭐⭐⭐ |

**What it teaches**: Build a GPT-style LLM end-to-end in PyTorch — tokenizer → attention → pretraining → finetuning, paired with Sebastian Raschka's book. Complete notebooks + code, chapter-aligned with the book.

**Best for**: Anyone who wants to truly understand what tokens, attention, and weights are. Complementary to Karpathy's video — that's a 2-hour fly-by, this is the slow read-the-book version.

**Notes**: Companion code to the book (Apache-2.0); free to fork and modify.

---

## ✅ Self-Check Before Stage 2

Can you:
- [ ] Make a Claude API call from Python in 5 lines
- [ ] Explain why "你好" might use 2 tokens but "Hello" uses 1
- [ ] Quote roughly the per-token price for Claude Sonnet vs Opus
- [ ] Name one strength of Claude vs GPT vs Gemini vs Llama

If yes → proceed to [Stage 2 — Prompt Engineering](02-prompt-engineering.en.md).

If no → re-read the Anthropic Quickstart + run all 3 hello-X projects above.

---

> ✅ **Done with Stage 1?** Next, [**Stage 2 — Prompt Engineering**](02-prompt-engineering.en.md) takes 5-12 hours to walk you through writing reusable structured prompts, using few-shot and chain-of-thought for reasoning tasks, and learning to quantify prompt improvement with evals. **Keep going →**
