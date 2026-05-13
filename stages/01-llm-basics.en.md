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

## 🛠 Hands-on Exercises (foundational, illustrative)

> 🦙 **This stage defaults to Ollama** (cost-driven; `gemma4:e4b` runs locally for $0/run). Every exercise has Path A (Ollama, default) + Path B (Anthropic, optional — use it when you want to see cloud-quality answers). Full three-path trade-off in [`examples/README.en.md`](../examples/README.en.md#three-paths--default-is-ollama-cost-driven).
>
> 💰 **Stage 1 budget estimate** (all 6 exercises, 3-5 runs each): **all local = $0**, **all haiku ≈ $0.30**, **all sonnet ≈ $0.90**. Full model list + Stage 1-7 total budget: [`examples/README.en.md#recommended-llm-list`](../examples/README.en.md#recommended-llm-list-local--cloud-user-perspective).
>
> 💡 **No Ollama yet?** Each exercise also ships a Path B Anthropic version — pick one. To enable Path A in one step: [`pip install openai && ollama pull gemma4:e4b`](https://ollama.com).

### Exercise 1: LLM API (hello world)
Five-line Python script that calls an LLM and prints the response. **Defaults to local Ollama (free, offline)**; switch to Path B Anthropic when you want cloud-quality answers. Details in [`examples/README.en.md`](../examples/README.en.md#three-paths--default-is-ollama-cost-driven).

<details open>
<summary>📋 <b>Starter code — Path A (local Ollama gemma4:e4b, default)</b> (copy to <code>practice_1.py</code> and run <code>python practice_1.py</code>)</summary>

```python
# Requires: pip install openai      (OpenAI-compatible SDK talks to Ollama)
# Pre-req: ollama pull gemma4:e4b && ollama serve
import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama",  # Ollama doesn't check this — anything works
)

r = client.chat.completions.create(
    model="gemma4:e4b",   # swap to qwen2.5:3b / llama3.2:3b if preferred
    max_tokens=100,
    messages=[{"role": "user", "content": "Introduce yourself in one sentence."}],
)

# === Self-check ===
text = r.choices[0].message.content
print("Response:", text)
print("usage:", r.usage)

assert r.choices[0].finish_reason in ("stop", "length"), f"unexpected finish_reason: {r.choices[0].finish_reason}"
assert len(text) > 0, "response should not be empty"
assert r.usage.completion_tokens > 0, "output token count should be > 0"
print("✅ Exercise 1 passed — local Ollama gemma4:e4b answered for $0")
```

**How slow?** Gemma 4B on CPU: ~5-30 s/answer; on GPU (RTX 3060+): <2 s. For speed use `gemma3:1b`; for quality use `qwen2.5:14b` / `llama3.3:8b` (needs 8 GB+ VRAM).

</details>

<details>
<summary>📋 <b>Starter code — Path B (Anthropic API, optional, when you want cloud quality)</b> (copy to <code>practice_1_anthropic.py</code>)</summary>

```python
# Requires: pip install anthropic
# Env: export ANTHROPIC_API_KEY=sk-ant-...
import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import anthropic

client = anthropic.Anthropic()
msg = client.messages.create(
    model="claude-haiku-4-5",  # haiku = cheapest; switch to sonnet by changing this line
    max_tokens=100,
    messages=[{"role": "user", "content": "Introduce yourself in one sentence."}],
)

# === Self-check ===
text = msg.content[0].text
print("Response:", text)
print("usage:", msg.usage)

assert msg.stop_reason in ("end_turn", "max_tokens"), f"unexpected stop_reason: {msg.stop_reason}"
assert len(text) > 0, "response should not be empty"
assert msg.usage.input_tokens > 0 and msg.usage.output_tokens > 0, "token counts should be > 0"
print("✅ Exercise 1 passed — Anthropic API is reachable from your machine")
```

**Cost**: ~$0.001/run (haiku) or ~$0.004/run (sonnet); this hello-world is also 5-15× faster than Ollama.

</details>

### Exercise 2: Tokens
Run the same prompt 100 times and watch token counts vary.
- Notice: `temperature ≠ 0` produces variation
- Notice: token count for the SAME English vs Chinese sentence

<details open>
<summary>📋 <b>Starter code — Path A (local Ollama gemma4:e4b, default)</b> (copy to <code>practice_2.py</code>)</summary>

```python
# Requires: pip install openai
# Pre-req: ollama pull gemma4:e4b && ollama serve
import sys, statistics
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from openai import OpenAI

client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")

PROMPTS = {
    "Chinese": "用一句話描述一隻貓在做什麼。",
    "English": "Describe in one sentence what a cat is doing.",
}

N = 10  # local is slower; start small
for label, prompt in PROMPTS.items():
    output_tokens = []
    for _ in range(N):
        r = client.chat.completions.create(
            model="gemma4:e4b",
            max_tokens=80,
            temperature=1.0,  # high temp to amplify variance
            messages=[{"role": "user", "content": prompt}],
        )
        output_tokens.append(r.usage.completion_tokens)
    print(f"\n[{label}] prompt: {prompt}")
    print(f"  input tokens: {r.usage.prompt_tokens}")
    print(f"  output tokens — min={min(output_tokens)} max={max(output_tokens)} mean={statistics.mean(output_tokens):.1f} stdev={statistics.stdev(output_tokens):.1f}")

# === Self-check ===
assert max(output_tokens) > min(output_tokens), "with temperature=1.0, output length should vary"
print("\n✅ Exercise 2 passed — observed temperature → token variance, $0/run")
print("💡 Chinese prompts typically use MORE input tokens (one Chinese character ≈ 2 tokens)")
```

</details>

<details>
<summary>📋 <b>Starter code — Path B (Anthropic API, optional)</b> (copy to <code>practice_2_anthropic.py</code>)</summary>

```python
# Requires: pip install anthropic
import sys, statistics
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import anthropic
client = anthropic.Anthropic()
PROMPTS = {"Chinese": "用一句話描述一隻貓在做什麼。", "English": "Describe in one sentence what a cat is doing."}

for label, prompt in PROMPTS.items():
    output_tokens = []
    for _ in range(20):
        msg = client.messages.create(model="claude-haiku-4-5", max_tokens=80, temperature=1.0,
                                     messages=[{"role": "user", "content": prompt}])
        output_tokens.append(msg.usage.output_tokens)
    print(f"[{label}] input={msg.usage.input_tokens} output min/max/mean={min(output_tokens)}/{max(output_tokens)}/{sum(output_tokens)/len(output_tokens):.1f}")
```

**Key SDK diffs**: `messages.create` → `chat.completions.create`; `usage.output_tokens` → `usage.completion_tokens`; `usage.input_tokens` → `usage.prompt_tokens`. **Cost**: 40 runs ≈ $0.01.

</details>

### Exercise 3: Pricing / Latency
**Cost-sensitive work required**: compute how long and how much it takes to run 1000 hello-world inferences. Local Ollama is $0 but has latency cost; cloud LLMs cost money but are faster. **Knowing this trade-off is how you pick the right model**.

<details open>
<summary>📋 <b>Starter code — Path A (local Ollama gemma4:e4b, measure latency)</b> (copy to <code>practice_3.py</code>)</summary>

```python
# Requires: pip install openai
# Pre-req: ollama pull gemma4:e4b && ollama serve
import sys, time
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from openai import OpenAI

client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")

latencies = []
for _ in range(5):
    t0 = time.time()
    r = client.chat.completions.create(
        model="gemma4:e4b",
        max_tokens=200,
        messages=[{"role": "user", "content": "Hi! Please introduce yourself."}],
    )
    latencies.append(time.time() - t0)

avg_latency = sum(latencies) / len(latencies)
out_tok_avg = r.usage.completion_tokens
tps = out_tok_avg / avg_latency if avg_latency > 0 else 0

print(f"model: gemma4:e4b (local)")
print(f"5 latencies (sec): min={min(latencies):.2f} max={max(latencies):.2f} mean={avg_latency:.2f}")
print(f"avg output: {out_tok_avg} tokens, ~{tps:.1f} tokens/sec")
print(f"\n1000-run cost: $0 (local); projected duration: {avg_latency * 1000 / 60:.1f} minutes")

# === Self-check ===
assert avg_latency > 0, "latency should be > 0"
assert out_tok_avg > 0, "output token count should be > 0"
print(f"\n✅ Exercise 3 passed — local model is $0 but takes ~{avg_latency * 1000 / 60:.0f} min for 1000 runs")
print("💡 Compare Path B Anthropic: 1000 runs is ~10-20 min at $0.25 (haiku)")
```

</details>

<details>
<summary>📋 <b>Starter code — Path B (Anthropic API, compute $ cost)</b> (copy to <code>practice_3_anthropic.py</code>)</summary>

```python
# Requires: pip install anthropic
import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import anthropic

# Anthropic public pricing 2026 Q1 (per 1M tokens, USD) — verify at https://www.anthropic.com/pricing
PRICING = {
    "claude-haiku-4-5":   {"input": 1.00, "output":  5.00},
    "claude-sonnet-4-5":  {"input": 3.00, "output": 15.00},
    "claude-opus-4-5":    {"input": 15.0, "output": 75.00},
}

client = anthropic.Anthropic()
MODEL = "claude-haiku-4-5"
msg = client.messages.create(model=MODEL, max_tokens=200,
                             messages=[{"role": "user", "content": "Hi! Please introduce yourself."}])
in_tok, out_tok = msg.usage.input_tokens, msg.usage.output_tokens
rates = PRICING[MODEL]
cost_one = (in_tok * rates["input"] + out_tok * rates["output"]) / 1_000_000

print(f"model: {MODEL}")
print(f"single: input={in_tok} output={out_tok} → ${cost_one:.6f}")
print(f"1000 calls cost across model tiers:")
for name, r in PRICING.items():
    c = (in_tok * r["input"] + out_tok * r["output"]) / 1_000_000 * 1000
    print(f"  {name:<22} ${c:.4f}")

assert cost_one > 0, "Cloud LLM always has a cost"
print(f"\n✅ Exercise 3 passed (Anthropic) — 1000 runs: haiku ≈ $0.25, sonnet ≈ $0.76, opus ≈ $3.81")
```

**Trade-off**: local Ollama is $0 for 1000 runs but takes ~2 hr; Anthropic haiku is ~10 min for $0.25; sonnet ~10 min for $0.76. **Use cloud only for production; learning / experiments / debug stay local.**

</details>

### Exercise 4: Cross-Provider Comparison
Send the same prompt to Claude, GPT, and Gemini simultaneously, compare their responses. Notice "why does the same input produce different answers" — answer style, length, and judgment all differ. Use the OpenAI, Anthropic, and Google SDKs side-by-side.

→ **Full runnable version** → [`examples/stage-1/04-cross-provider/`](../examples/stage-1/04-cross-provider/) (parallel calls to all three SDKs + comparison table; missing keys are skipped gracefully)

### Exercise 5: Error Handling
Trigger error conditions deliberately and write retry logic:
- Wrong API key → see how it raises
- Over-long prompt → what happens when the context window is full
- Network drop → write a retry wrapper with exponential backoff

This is foundational for Stage 3-7's production agent code.

→ **Full runnable version** → [`examples/stage-1/05-error-handling/`](../examples/stage-1/05-error-handling/) (mock-based tests so you can verify the retry logic without unplugging your ethernet cable)

### Exercise 6: Local LLM
**No API fees, runs on your machine**: use Ollama to pull a small model (recommend `llama3.2:3b` or `qwen2.5:3b`), call it via OpenAI-compatible API.

```bash
# 1. Install Ollama: https://ollama.com
ollama pull qwen2.5:3b
ollama serve  # default port 11434
```

<details>
<summary>📋 <b>Starter code</b> (copy to <code>practice_6.py</code>)</summary>

```python
# Requires: pip install openai
# Pre-req: Ollama is running, qwen2.5:3b is pulled
import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama",  # Ollama doesn't check this — anything works
)

r = client.chat.completions.create(
    model="qwen2.5:3b",
    messages=[{"role": "user", "content": "Explain ReAct in 3 sentences."}],
)

text = r.choices[0].message.content
print("Response:", text)

# === Self-check ===
assert len(text) > 10, "response is too short — Ollama may not be running"
print(f"✅ Exercise 6 passed — local Ollama reachable through the OpenAI-compatible API")
print(f"💡 This run cost you $0 (except for electricity)")
```

**Why do this**: once you can run local LLMs, Stage 3-6 experiments aren't bottlenecked on API costs; privacy-sensitive work also stays offline.

</details>

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
