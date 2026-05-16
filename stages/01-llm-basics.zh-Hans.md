# Stage 1 — LLM 基础（LLM Basics）

> [繁體中文](./01-llm-basics.md) | **简体中文** | [English](./01-llm-basics.en.md)

> **预计学习时间**： 5-8 小时

> 👋 **从 [Stage 0](00-foundations.zh-Hans.md) 来的**：好，环境已经够用——这 5-8 小时：第一次成功调用 Claude / GPT / Gemini API、搞懂 token / context window / temperature 怎么影响输出、用 per-token 计算实际成本。**直接从这里开始的**：先确认你能跑 Python 脚本、有任一家供应商的 API key——做不到请先回 [Stage 0](00-foundations.zh-Hans.md)。

> 掌握 **核心概念**：LLM / token / context window / temperature / RAG / agent，请先阅读 [`resources/glossary.zh-Hans.md`](../resources/glossary.zh-Hans.md)（约 30 分钟）。

### 3 个核心词（先记住，后面 stage 都会用到）

| 词 | 中文 | 一句话 |
|---|---|---|
| **token** | 词元 | 模型计算文字长度与费用的基本单位（中文 1 个字 ≈ 1.5-2 token） |
| **context window** | 上下文窗口 | 模型一次能看到多少 token（Claude 200k / GPT-4o 128k / Gemini 2M） |
| **temperature** | 随机程度参数 | 控制回答是更稳定还是更发散（0 = 最稳定、1 = 更有创意；分类任务用 0.0-0.3、创作用 0.7-1.0） |

→ 这 3 个词贯穿后续所有 stage。Stage 1 的目标就是让你亲手调用 API、直接感受它们怎么影响输出。

## 学习目标

完成本阶段后，你将能够：
- 解释 LLM、token、context window 等核心概念。
- 使用 Python 调用 Claude / GPT / Gemini API。
- 比较不同 LLM 提供商（Claude / GPT / Gemini / Llama）的优劣。
- 理解 per-token 定价模型并估算成本。

## 前置要求

你需要具备以下基础：
- 编写 Python 脚本。
- 理解基本的 HTTP / REST 概念。
- 获取并使用 API key（Anthropic / OpenAI / Google）。

如果没有，请先完成 Stage 0。

## 推荐阅读

1. [**Anthropic - Claude 模型概览**](https://docs.claude.com/en/about-claude/models/overview) - 官方模型总览，包含 2026 最新 Opus 4.7 / Sonnet 4.6 / Haiku 4.5。
2. [**anthropics/courses — Anthropic API Fundamentals**](https://github.com/anthropics/courses) ⭐⭐⭐⭐⭐ ★ 21k+ — Anthropic 官方 5 course umbrella、**module 1「Anthropic API Fundamentals」对应本 stage**。Jupyter notebook、用 Claude 3 Haiku（最便宜）跑、跟着做就能拿到 API 基本功。
3. [**OpenAI Quickstart**](https://platform.openai.com/docs/quickstart) - 学习发送你的第一个 API call。
4. [**A Visual Guide to LLM Tokenizers**](https://huggingface.co/learn/llm-course/chapter6/1) - Hugging Face 的图文并茂指南。
5. [**Anthropic API Pricing**](https://www.anthropic.com/pricing#anthropic-api) - 了解并比较模型成本（例如，1k input + 1k output 的价格）。

## “动手”小练习（在本地运行这些代码）

> 🦙 **本 stage 默认用 Ollama**（成本考量、本机 `gemma4:e4b` 跑得动、$0/run）。每个练习都有 Path A（Ollama、默认）+ Path B（Anthropic、选择性、想看 cloud 高质量时用）。完整 3 路 trade-off 见 [`examples/README.zh-Hans.md`](../examples/README.zh-Hans.md#三条路径--默认用-ollama成本考量)。
>
> 💰 **Stage 1 预算估算**（全 6 练习各跑 3-5 次）：**全本机 = $0**、**全 haiku ≈ $0.30**、**全 sonnet ≈ $0.90**。完整 model 清单 + Stage 1-7 全程预算估算见 [`examples/README.zh-Hans.md#推荐-llm-清单`](../examples/README.zh-Hans.md#推荐-llm-清单)。
>
> 💡 **不装 Ollama 也能读** — 每个练习的 Path B 区块就是 Anthropic 版、选一个跑就行。先 [`pip install openai && ollama pull gemma4:e4b`](https://ollama.com) 就装好 Path A 环境。

### 练习 1：LLM API（hello world）
五行 Python 调用 LLM 并打印响应。**默认用 Ollama 本机跑（免费、offline）**；想看 cloud 答案品质改 Path B Anthropic。详见 [`examples/README.zh-Hans.md`](../examples/README.zh-Hans.md#三条路径--默认用-ollama成本考量)。

<details open>
<summary>📋 <b>起手码 — Path A（本机 Ollama gemma4:e4b、默认）</b>（复制到 <code>practice_1.py</code>、<code>python practice_1.py</code> 就跑）</summary>

```python
# 需要：pip install openai      (用 OpenAI 兼容 SDK 跟 Ollama 沟通)
# 前置：ollama pull gemma4:e4b && ollama serve
import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama",  # Ollama 不检查、随便填
)

r = client.chat.completions.create(
    model="gemma4:e4b",   # 换成 qwen2.5:3b / llama3.2:3b 也可
    max_tokens=100,
    messages=[{"role": "user", "content": "用一句话自我介绍。"}],
)

# === 自我验证 ===
text = r.choices[0].message.content
print("响应：", text)
print("usage:", r.usage)

assert r.choices[0].finish_reason in ("stop", "length"), f"非预期 finish_reason: {r.choices[0].finish_reason}"
assert len(text) > 0, "响应不应为空"
assert r.usage.completion_tokens > 0, "output token 应 > 0"
print("✅ 练习 1 通过 — Ollama gemma4:e4b 已能本机响应、$0/次")
```

**慢吗？** Gemma 4B 在 CPU 上约 5-30s/答案、有 GPU（RTX 3060+）<2s。要更快用 `gemma3:1b`、要更聪明改 `qwen2.5:14b` / `llama3.3:8b`（需 8GB+ VRAM）。

</details>

<details>
<summary>📋 <b>起手码 — Path B（Anthropic API、选择性、想看 cloud 高质量时）</b>（复制到 <code>practice_1_anthropic.py</code>）</summary>

```python
# 需要：pip install anthropic
# 环境变量：export ANTHROPIC_API_KEY=sk-ant-...
import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import anthropic

client = anthropic.Anthropic()
msg = client.messages.create(
    model="claude-haiku-4-5",  # haiku 最便宜；换 sonnet 改这行
    max_tokens=100,
    messages=[{"role": "user", "content": "用一句话自我介绍。"}],
)

# === 自我验证 ===
text = msg.content[0].text
print("响应：", text)
print("usage:", msg.usage)

assert msg.stop_reason in ("end_turn", "max_tokens"), f"非预期 stop_reason: {msg.stop_reason}"
assert len(text) > 0, "响应不应为空"
assert msg.usage.input_tokens > 0 and msg.usage.output_tokens > 0, "token 数应 > 0"
print("✅ 练习 1 通过 — 你已成功打通 Anthropic API")
```

**成本**：每次 ~$0.001 (haiku) / $0.004 (sonnet)、跑这个 hello world 比 Ollama 快 5-15 倍。

</details>

### 练习 2：Tokens
同一个 prompt 跑 100 次，观察 token 数的变化。
- 注意：`temperature ≠ 0` 会产生变动
- 注意：同一句话的英文 vs 中文 token 数差异

<details open>
<summary>📋 <b>起手码 — Path A（本机 Ollama gemma4:e4b、默认）</b>（复制到 <code>practice_2.py</code>）</summary>

```python
# 需要：pip install openai
# 前置：ollama pull gemma4:e4b && ollama serve
import sys, statistics
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from openai import OpenAI

client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")

PROMPTS = {
    "中文": "用一句话描述一只猫在做什么。",
    "English": "Describe in one sentence what a cat is doing.",
}

N = 10  # 本机慢、N 小一点
for label, prompt in PROMPTS.items():
    output_tokens = []
    for _ in range(N):
        r = client.chat.completions.create(
            model="gemma4:e4b",
            max_tokens=80,
            temperature=1.0,
            messages=[{"role": "user", "content": prompt}],
        )
        output_tokens.append(r.usage.completion_tokens)
    print(f"\n[{label}] prompt: {prompt}")
    print(f"  input tokens: {r.usage.prompt_tokens}")
    print(f"  output tokens — min={min(output_tokens)} max={max(output_tokens)} mean={statistics.mean(output_tokens):.1f} stdev={statistics.stdev(output_tokens):.1f}")

# === 自我验证 ===
assert max(output_tokens) > min(output_tokens), "temperature=1.0 下、output 长度应该有 variance"
print("\n✅ 练习 2 通过 — 本机跑 $0")
print("💡 中文 prompt 通常 input tokens 比 English 多（中文 token 化通常一字 ≈ 2 tokens）")
```

</details>

<details>
<summary>📋 <b>起手码 — Path B（Anthropic API、选择性）</b>（复制到 <code>practice_2_anthropic.py</code>）</summary>

```python
# 需要：pip install anthropic
import sys, statistics
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import anthropic
client = anthropic.Anthropic()
PROMPTS = {"中文": "用一句话描述一只猫在做什么。", "English": "Describe in one sentence what a cat is doing."}

for label, prompt in PROMPTS.items():
    output_tokens = []
    for _ in range(20):
        msg = client.messages.create(model="claude-haiku-4-5", max_tokens=80, temperature=1.0,
                                     messages=[{"role": "user", "content": prompt}])
        output_tokens.append(msg.usage.output_tokens)
    print(f"[{label}] input={msg.usage.input_tokens} output min/max/mean={min(output_tokens)}/{max(output_tokens)}/{sum(output_tokens)/len(output_tokens):.1f}")
```

**主要差异**：`messages.create` → `chat.completions.create`；`usage.output_tokens` → `usage.completion_tokens`；`usage.input_tokens` → `usage.prompt_tokens`。**成本**：40 次 ≈ $0.01。

</details>

### 练习 3：Pricing / Latency
**Cost-sensitive 工作**必修：算出你的 hello-world prompt 跑 1000 次在不同 model 上的成本。Ollama 本机是 $0 但有 latency 成本；Cloud LLM 有 $ 成本但快。**会算这两个 trade-off 才能挑对 model**。

<details open>
<summary>📋 <b>起手码 — Path A（本机 Ollama gemma4:e4b、量 latency）</b>（复制到 <code>practice_3.py</code>）</summary>

```python
# 需要：pip install openai
# 前置：ollama pull gemma4:e4b && ollama serve
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
        messages=[{"role": "user", "content": "你好！自我介绍一下。"}],
    )
    latencies.append(time.time() - t0)

avg_latency = sum(latencies) / len(latencies)
out_tok_avg = r.usage.completion_tokens
tps = out_tok_avg / avg_latency if avg_latency > 0 else 0

print(f"model: gemma4:e4b (本机)")
print(f"5 次 latency (sec): min={min(latencies):.2f} max={max(latencies):.2f} mean={avg_latency:.2f}")
print(f"avg output: {out_tok_avg} tokens、约 {tps:.1f} tokens/sec")
print(f"\n1000 次成本: $0 (本机)、预计时长: {avg_latency * 1000 / 60:.1f} 分钟")

# === 自我验证 ===
assert avg_latency > 0, "latency 应 > 0"
assert out_tok_avg > 0, "output token 应 > 0"
print(f"\n✅ 练习 3 通过 — 本机 model $0 但要花 {avg_latency * 1000 / 60:.0f} 分钟跑 1000 次")
print("💡 对照 Path B Anthropic：1000 次只要 ~10-20 分钟但要 $0.25（haiku）")
```

</details>

<details>
<summary>📋 <b>起手码 — Path B（Anthropic API、算 $ 成本）</b>（复制到 <code>practice_3_anthropic.py</code>）</summary>

```python
# 需要：pip install anthropic
import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import anthropic

# Anthropic 2026 Q2 公开计价（每 1M token、USD）— 运行前对照 https://www.anthropic.com/pricing
PRICING = {
    "claude-haiku-4-5":   {"input": 1.00, "output":  5.00},
    "claude-sonnet-4-6":  {"input": 3.00, "output": 15.00},
    "claude-opus-4-7":    {"input": 5.00, "output": 25.00},  # Opus 4.7（2026 年 4 月）价格下调至 5/25
}

client = anthropic.Anthropic()
MODEL = "claude-haiku-4-5"
msg = client.messages.create(model=MODEL, max_tokens=200,
                             messages=[{"role": "user", "content": "你好！自我介绍一下。"}])
in_tok, out_tok = msg.usage.input_tokens, msg.usage.output_tokens
rates = PRICING[MODEL]
cost_one = (in_tok * rates["input"] + out_tok * rates["output"]) / 1_000_000

print(f"model: {MODEL}")
print(f"single: input={in_tok} output={out_tok} → ${cost_one:.6f}")
print(f"1000 calls cost across model tiers:")
for name, r in PRICING.items():
    c = (in_tok * r["input"] + out_tok * r["output"]) / 1_000_000 * 1000
    print(f"  {name:<22} ${c:.4f}")

assert cost_one > 0, "Cloud LLM 一定有成本"
print(f"\n✅ 练习 3 通过（Anthropic）— 1000 次 haiku ≈ $0.25、sonnet 4.6 ≈ $0.76、opus 4.7 ≈ $1.27")
```

**预期输出**：
```
model: claude-haiku-4-5
single: input=14 output=48 → $0.000254
1000 calls cost across model tiers:
  claude-haiku-4-5       $0.2540
  claude-sonnet-4-6      $0.7620
  claude-opus-4-7        $1.2700
```

**Trade-off 对照**：本机 Ollama 跑 1000 次免费但要 ~2 hr；Anthropic haiku ~10 min $0.25；sonnet ~10 min $0.76。**production 场景才考虑 cloud；学习 / 实验 / debug 全用本机**。

</details>

### 练习 4：Cross-Provider 比较
同一个 prompt 同时送给 Claude、GPT、Gemini，比较三家的响应差异。观察「同一句话为什么产生不同答案」——回答风格、长度、判断取舍都不一样。建议用 OpenAI、Anthropic、Google 三家 SDK 各一段程序调用。

→ **基础 starter 范本** → [`examples/stage-1/04-cross-provider/`](../examples/stage-1/04-cross-provider/)（含三家 SDK 并行调用 + table 对照、缺哪家 key 就 skip 哪家；illustrative，**不是 chapter-length 完整教程**）

### 练习 5：Error Handling
故意触发错误情境并写 retry：
- API key 错误 → 看怎么 raise
- prompt 超长 → context window 满了会发生什么
- 网络断掉 → 写一个有 exponential backoff 的 retry wrapper

这是后面 Stage 3-7 写 production agent 一定会用到的基础。

→ **基础 starter 范本** → [`examples/stage-1/05-error-handling/`](../examples/stage-1/05-error-handling/)（含 mock-based test、不用真的断网就能验证 retry 逻辑；illustrative，**不是 chapter-length 完整教程**）

### 练习 6：Local LLM
**不付 API 费用、跑在自己电脑上**：用 Ollama 下载一个小模型（建议 `llama3.2:3b` 或 `qwen2.5:3b`），用 OpenAI 兼容 API 调用它。

```bash
# 1. 装 Ollama: https://ollama.com
ollama pull qwen2.5:3b
ollama serve  # 默认 port 11434
```

<details>
<summary>📋 <b>起手码</b>（复制到 <code>practice_6.py</code>）</summary>

```python
# 需要：pip install openai
# 前置：Ollama 已 serve、qwen2.5:3b 已 pull
import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama",  # Ollama 不检查、随便填
)

r = client.chat.completions.create(
    model="qwen2.5:3b",
    messages=[{"role": "user", "content": "用 3 句话介绍什么是 ReAct。"}],
)

text = r.choices[0].message.content
print("响应：", text)

# === 自我验证 ===
assert len(text) > 10, "响应太短、Ollama 可能没跑起来"
print(f"✅ 练习 6 通过 — 你的本机 Ollama 已能透过 OpenAI 兼容 API 调用")
print(f"💡 跑这次完全没花钱（除了你的电力）")
```

**为什么要做**：学会跑本地 LLM 后，后面 Stage 3-6 的实验都不会被 API 费用卡住；隐私敏感场景也能 offline。

</details>

## 开源项目学习

### [Anthropic Cookbook](https://github.com/anthropics/anthropic-cookbook)      

| 属性 | 值 |
|---|---|
| 语言 | Python |
| Stars | 42k+ |
| License | MIT |
| 推荐指数 | ★★★★★ |

**一句话总结**：官方 Claude API 示例，覆盖了从 chat、tools、citations、multi-modal 到 prompt caching 的所有核心功能。

**适合谁**：所有希望使用 Claude 的开发者。这是最权威的 Notebook 示例，可以帮你快速上手任何一个 API 功能（如果你不喜欢阅读官方文档）。

**怎么用**：把它当成一个可以随时翻阅和复制粘贴的代码片段库。★★★☆☆，内容组织比较零散，查找特定功能需要一些时间。

**快速开始**：
```bash
git clone https://github.com/anthropics/anthropic-cookbook
cd anthropic-cookbook/skills/classification
pip install -r requirements.txt
jupyter notebook guide.ipynb
```

---

### [Anthropic Courses](https://github.com/anthropics/courses)

| 属性 | 值 |
|---|---|
| 语言 | Python / Jupyter |
| Stars | 21k+ |
| License | NOASSERTION（非标准 SPDX 标识符，但包含 LICENSE 文件）|
| 推荐指数 | ★★★★★ |

**一句话总结**：Anthropic 官方出品的免费课程，系统性地介绍了从 API 基础、prompt evaluation、real-world prompting、tool use 到 Claude with Excel 的核心主题，全部以 Jupyter notebook 形式提供，交互性极强。

**适合谁**：希望系统学习 Claude API 的开发者。比 Cookbook 更系统，Cookbook 提供了“how”，而 Courses 解释了“why”，更适合初学者，提供了从零到一的清晰路径。

**怎么用**：强烈建议完成 `anthropic_api_fundamentals` 和 `prompt_engineering_interactive_tutorial`。

---

### [OpenAI Cookbook](https://github.com/openai/openai-cookbook)

| 属性 | 值 |
|---|---|
| 语言 | Python / Jupyter |
| Stars | 73k+ |
| License | MIT |
| 推荐指数 | ★★★★★ |

**一句话总结**：与 Anthropic Cookbook 类似，但专注于 GPT 模型，包含了大量关于 structured output、tool use、embedding 的 recipe。

**适合谁**：需要使用 OpenAI API 的开发者，特别是对 structured output 和 function calling 功能感兴趣的。

**怎么用**：如果你在 Anthropic 的 cookbook 中找不到答案，可以来这里看看。两个项目的组织方式和风格都很相似。

---

### [LangChain Academy](https://academy.langchain.com/)

| 属性 | 值 |
|---|---|
| 形式 | 在线视频课程 |
| 推荐指数 | ★★★★☆ |

**一句话总结**：从 LLM 基础、embedding、RAG 到 agent，系统介绍 LangChain 生态的核心概念。LangChain 的作者亲自讲解。

**适合谁**：未来打算以 LangChain 为主要框架的开发者。

**怎么用**：作为入门，选择性观看。如果你没有 LangChain 背景，直接进入后面阶段可能会感到困惑。

---

### [datawhalechina/happy-llm](https://github.com/datawhalechina/happy-llm)     

| 属性 | 值 |
|---|---|
| 语言 | 中文（zh-Hans）|
| Stars | 29k+ |
| License | Custom |
| 推荐指数 | ★★★★★ |

**一句话总结**：一个面向初学者的中文 LLM 学习项目，以 Karpathy 的 Zero to Hero 系列为蓝本，用中文详细拆解了 1-4 章的内容，让你从零开始构建一个 LLM（如果你对理论和代码实现都感兴趣）。

**适合谁**：希望深入理解 LLM 底层原理的学习者，或者不想啃英文视频，可以把它当作 Hugging Face 的 LLM Course 的替代品。

---

### [datawhalechina/llm-universe](https://github.com/datawhalechina/llm-universe)

| 属性 | 值 |
|---|---|
| 语言 | 中文（zh-Hans）|
| Stars | 12k+ |
| License | NOASSERTION |
| 推荐指数 | ★★★★☆ |

**一句话总结**：另一个系统性的中文教程，覆盖了从“模型”、“微调”、“提示”到“应用”的全链路知识，包括 API 基础、LangChain、RAG、Agent 等。

**适合谁**：想找一个 LLM *中文学习路线图* 的人，可以把它作为一个大纲，按图索骥。

---

### [jingyaogong/minimind](https://github.com/jingyaogong/minimind)

| 属性 | 值 |
|---|---|
| 语言 | 中文 + Python |
| Stars | 48k+ |
| License | Apache-2.0 |
| 推荐指数 | ★★★★★ |

**一句话总结**：一个小时内，从头构建一个 64M 参数的 LLM。这个项目不仅带你阅读和理解代码，还把构建 LLM 的整个 project（pretrain + SFT + LoRA + DPO + RLHF）都放到了这个 repo 里。

**适合谁**：看完了 Karpathy 的视频，想快速将理论付诸实践，并体验完整 LLM 训练流程的人。这是一个很好的“动手”项目。

---

### [datawhalechina/llm-cookbook](https://github.com/datawhalechina/llm-cookbook)

| 属性 | 值 |
|---|---|
| 语言 | 中文（zh-Hans）|
| Stars | 23k+ |
| 最后更新 | 注意，项目已归档，最后更新于 2025 年 6 月 1 日 |
| License | Custom (CC BY-NC-SA) |
| 推荐指数 | ★★★★☆ |

**一句话总结**：吴恩达（Andrew Ng）的 prompt engineering / building systems / fine-tuning 三门课程的中文笔记，可以作为快速回顾和查漏补缺的材料，所有内容都以 notebook 形式提供。

**适合谁**：如果你没时间看视频，想快速了解 LLM 应用开发的基础。

**怎么用**：浏览一遍 zh-Hans（Datawhale 的系列）项目，你会发现大部分内容是重复的，选一个你喜欢的风格，然后深入进去，不要贪多。

---

### [Hugging Face - Large Language Model Course](https://huggingface.co/learn/llm-course)

| 属性 | 值 |
|---|---|
| 形式 | 在线视频课程 + notebook |
| License | Apache 2.0 |
| 推荐指数 | ★★★★☆ |

**一句话总结**：系统学习 LLM 核心理论（Tokenization、Transformer、Fine-tuning），全部基于 Hugging Face 生态。

**适合谁**：希望深入了解理论、从零开始构建模型的学习者，而不是停留在 API 调用层面。

---

### 关于在众多项目中如何选择 LLM（以及是否需要 API）

到目前为止，我们已经接触了 4 个“在本地从头构建 LLM”的项目。*对于初学者，我们强烈建议你先忽略它们*，专注于 API 调用，完成练习 1-5，并阅读后面的 Stages 2-7。当你对 agentic AI 应用开发有了全局认知后，再回过头来看这些项目，你会更有方向感。

---

### [ollama/ollama](https://github.com/ollama/ollama)

| 属性 | 值 |
|---|---|
| 语言 | Go |
| Stars | 170k+ |
| License | MIT |
| 推荐指数 | ★★★★★ |

**一句话总结**：在本地运行开源 LLM 的最佳工具。`ollama pull qwen2.5:3b` 一行命令即可下载并运行一个本地模型，并提供 OpenAI 兼容的 API（`http://localhost:11434/v1`），让你可以直接用 OpenAI SDK 进行交互。

**适合谁**：任何需要在本地运行 LLM 的开发者，或者希望在 agent 应用中加入 fallback 机制（例如，当 Claude 成本太高时，降级到 Ollama）。

**快速开始**：
```bash
# 从 https://ollama.com 安装
ollama pull qwen2.5:3b   # 中文支持最好的小模型（约 2GB）
ollama run qwen2.5:3b    # 直接 chat
ollama serve             # 暴露 API server
```

---

### [ggml-org/llama.cpp](https://github.com/ggml-org/llama.cpp)

| 属性 | 值 |
|---|---|
| 语言 | C++ |
| Stars | 108k+ |
| License | MIT |
| 推荐指数 | ★★★★☆ |

**一句话总结**：Llama 系列模型的 C++ 推理引擎，专注于性能和量化（quantization），如 GGUF 格式、Q4_K_M / Q5_K_S 等不同的量化水平，以及 KV cache、CPU/GPU offloading 等高级功能。

**适合谁**：希望在低资源设备（例如，树莓派或 8GB RAM 的旧电脑）上运行 7B 模型的学习者，或者对 Llama 的内部实现感兴趣，需要进行 fine-grained 控制和优化的开发者。

---

### [mudler/LocalAI](https://github.com/mudler/LocalAI)

| 属性 | 值 |
|---|---|
| 语言 | Go |
| Stars | 46k+ |
| License | MIT |
| 推荐指数 | ★★★★☆ |

**一句话总结**：OpenAI API 的 drop-in 替代品，让你可以在本地使用 OpenAI SDK，只需将 `base_url` 指向 LocalAI，即可在本地运行 LLM、embedding、image generation、TTS、STT。

**适合谁**：应用/项目已经深度绑定了 OpenAI 生态，但希望在本地进行测试，或者完全 offline 运行。比 Ollama 更强大，但配置也更复杂。

---

### [ml-explore/mlx](https://github.com/ml-explore/mlx)

| 属性 | 值 |
|---|---|
| 语言 | C++ / Python |
| Stars | 25k+ |
| License | MIT |
| 推荐指数 | ★★★☆☆ |

**一句话总结**：Apple 为 Apple Silicon（M1/M2/M3/M4）芯片设计的机器学习 framework，可以让你在 Mac 上高效运行本地 LLM。可以看作是苹果版的 llama.cpp。

**适合谁**：在 MacBook 上工作的开发者，希望充分利用 Apple Silicon 的性能。不支持 Linux / Windows。

**怎么用**：安装 `mlx-lm` package，开箱即用。

**怎么用**：它的 cookbook 项目有很多不错的本地 inference 示例。

---

### [karpathy/LLM101n](https://github.com/karpathy/LLM101n)

| 属性 | 值 |
|---|---|
| 状态 | 注意，项目已归档，最后更新于 2024 年 8 月 |
| 推荐指数 | ★★★☆☆ |

**一句话总结**：另一个 Karpathy 的项目，目标是训练一个“Storyteller AI LLM”。

**适合谁**：如果你已经看完了 Karpathy 的 "Let's build GPT from scratch" YouTube 视频，并想继续深入，这是一个很好的后续。

**怎么用**：这个 repo 的价值在于它的 `storyteller` 目录，代码非常精简，值得学习。

---

### [Anthropic - Claude API Quickstart](https://docs.anthropic.com/en/docs/get-started)

| 属性 | 值 |
|---|---|
| 形式 | 文档 |
| 推荐指数 | ★★★★★ |

**一句话总结**：Claude API 的官方快速入门文档。

**适合谁**：任何不想看视频，只想快速复制代码片段的人。

---

### [karpathy - Let's build GPT from scratch](https://www.youtube.com/watch?v=kCc8FmEb1nY)

| 属性 | 值 |
|---|---|
| 形式 | YouTube 视频，约 2 小时 |
| 推荐指数 | ★★★★★ |

**一句话总结**：使用 PyTorch 从零开始构建一个 transformer-based GPT。这是理解 LLM 内部工作原理的最佳入门视频。

**适合谁**：希望深入理解 LLM 基础概念的开发者，或者对底层代码实现感兴趣的人。

**怎么用**：2 小时视频，可以开 1.5 倍速观看，配合字幕，很容易跟上。

---

### [rasbt/LLMs-from-scratch](https://github.com/rasbt/LLMs-from-scratch)       

| 属性 | 值 |
|---|---|
| 语言 | Python / Jupyter |
| Stars | 91k+ |
| License | Apache-2.0 |
| 推荐指数 | ★★★★★ |

**一句话总结**：使用 PyTorch 从头构建一个 GPT-style LLM，覆盖了 tokenizer、attention、pretraining、finetuning，作者是 Sebastian Raschka，提供了详细的 notebook + code，以及一本配套的实体书。

**适合谁**：希望系统学习如何从零构建 token、attention、weights 等概念的人。如果 Karpathy 的视频对你来说太像“fly-by”（一飞而过），这本书提供了更深入、更结构化的内容。

**怎么用**：书是 Apache-2.0 协议，可以免费 fork 阅读。

---

## 进入 Stage 2 前的检查点

你需要完成以下任务：
- [ ] 写一个 5 行的 Python 脚本调用 Claude API。
- [ ] 理解“基础概念”中的至少 2 个 token（例如，“Hello” 是 1 个）。
- [ ] 比较 Claude Sonnet vs Opus 的 per-token 价格。
- [ ] 体验至少 2 个不同的 LLM（Claude / GPT / Gemini / Llama）。

如果都完成了，恭喜，进入 [Stage 2 - Prompt Engineering](./02-prompt-engineering.zh-Hans.md)。

如果卡住了，回到 Anthropic Quickstart + 完成至少 3 个 hello-X 脚本。

---

> ✅ **Stage 1 完成？** 接下来 [**Stage 2 — Prompt Engineering**](02-prompt-engineering.zh-Hans.md) 会用 5-12 小时带你写出可重用的结构化 prompt、用 few-shot 跟 chain-of-thought 解推理题、并学会用 eval 量化 prompt 改善幅度。**继续向前 →**
