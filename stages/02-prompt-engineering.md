# Stage 2 — Prompt Engineering

> **繁體中文** | [简体中文](./02-prompt-engineering.zh-Hans.md) | [English](./02-prompt-engineering.en.md) | [Русский](./02-prompt-engineering.ru.md)

⏱ **時間估算**：1-2 週（約 5-12 小時）

> 👋 **從 [Stage 1](01-llm-basics.md) 來的**：好，你會呼叫 API 了——這 5-12 小時：寫出可重用的結構化 prompt、用 few-shot 跟 chain-of-thought 解難題、用 eval 量化 prompt 改善幅度。**直接從這裡開始的**：先確認你會呼叫 LLM API、會用 token 算成本——做不到請先回 [Stage 1](01-llm-basics.md)。

> 💡 用語不熟（prompt / few-shot / CoT / system prompt⋯）→ 翻 [`resources/glossary.md`](../resources/glossary.md)。

## 📌 學習目標

走完這個階段後你會：
- 寫出結構化 prompt（角色 + 任務 + 格式 + 範例）
- 應用 few-shot prompting，並知道什麼時候有用
- 在推理任務上使用 chain-of-thought（CoT）
- 反覆迭代修改一個 prompt 並衡量改善
- 看出什麼時候 prompt 已經到極限了（這時你需要 tool / agent）

## 🚪 進入條件

你應該已經：
- 會呼叫 LLM API（Stage 1）
- 會解析 / 走訪 API 回應

## 📚 必修閱讀

1. [**Anthropic Prompt Engineering Guide**](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/overview) — 官方，整理得不錯
2. [**OpenAI Prompt Engineering**](https://platform.openai.com/docs/guides/prompt-engineering) — OpenAI 觀點
3. [**dair-ai Prompt Engineering Guide**](https://www.promptingguide.ai/) — 學術風，深入
4. [**Anthropic — Prompting Best Practices**](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/be-clear-and-direct) — 直接清楚

## 🛠 動手練習

> 🦙 **本 stage 默認用 Ollama gemma4:e4b**（成本考量、$0/run）。Prompt engineering 對小 model 更有教學價值——小 model 對 prompt 質量敏感、能讓你看清楚 system prompt / few-shot / CoT / refinement 各自帶來多少改善。每個練習都有 Path A（Ollama、默認）+ Path B（Anthropic、選擇性）。
>
> 💰 **Stage 2 預算估算**（全 4 練習各跑 3-5 次）：**全本機 = $0**、**全 haiku ≈ $0.20**、**全 sonnet ≈ $0.60**。Few-shot 分類任務的 12 calls × 5 reps ≈ $0.30 haiku / $0.90 sonnet。完整預算見 [`examples/README.md#推薦-llm-清單`](../examples/README.md#推薦-llm-清單本機--clouduser-視角)。
>
> 完整 3 路 trade-off 見 [`examples/README.md`](../examples/README.md#三條路徑--默認用-ollama成本考量)。

### 練習 1：System Prompt
同樣的 user message，三個不同的 system prompt。觀察人格 / 輸出格式怎麼變。

<details open>
<summary>📋 <b>起手碼 — Path A（本機 Ollama gemma4:e4b、默認）</b>（複製到 <code>practice_1.py</code>）</summary>

```python
# 需要：pip install openai
# 前置：ollama pull gemma4:e4b && ollama serve
import sys, json
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from openai import OpenAI

client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")

# 同一個 user message、3 個不同 system prompt
SYSTEM_PROMPTS = {
    "嚴肅律師": "你是嚴謹的合約律師。回答要精準、引用法條編號、避免任何主觀形容詞。",
    "幼兒園老師": "你是溫柔的幼兒園老師、要對 5 歲小孩說話。用比喻、口語、少於 80 字。",
    "JSON 機器": "你只回 JSON。schema: {\"answer\": string, \"confidence\": float}",
}

USER_MSG = "請幫我解釋什麼是租賃合約。"

outputs = {}
for label, system in SYSTEM_PROMPTS.items():
    # Note: Ollama 把 system 放 messages 第一筆（不像 Anthropic 用 system= 參數）
    r = client.chat.completions.create(
        model="gemma4:e4b",
        max_tokens=200,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": USER_MSG},
        ],
    )
    outputs[label] = r.choices[0].message.content
    print(f"\n--- [{label}] ---")
    print(outputs[label])

# === 自我驗證 ===
json_output = outputs["JSON 機器"]
assert "{" in json_output and "}" in json_output, "JSON 機器版輸出應該含 JSON braces"
try:
    parsed = json.loads(json_output.strip().split("\n")[-1] if "\n" in json_output else json_output)
    assert "answer" in parsed, "JSON schema 應包含 answer 欄位"
except json.JSONDecodeError:
    pass  # 容許 model 回 JSON 含解釋文字、最後一筆才是 JSON
print(f"\n✅ 練習 1 通過 — 同一個問題、3 種人格 / 格式 / 語氣")
print("💡 觀察：律師長、老師短、JSON 機器一定是 {...}")
```

**預期輸出**（樣本、gemma4:e4b 對 system prompt 遵循度 OK 但不如 Claude 嚴謹）：
```
--- [嚴肅律師] ---
依民法第 421 條...

--- [幼兒園老師] ---
租賃合約就像借玩具給朋友、講好什麼時候還、要付多少糖果...

--- [JSON 機器] ---
{"answer": "租賃合約是當事人約定一方以物租與他方使用...", "confidence": 0.85}
```

</details>

<details>
<summary>📋 <b>起手碼 — Path B（Anthropic API、選擇性）</b>（複製到 <code>practice_1_anthropic.py</code>）</summary>

```python
# 需要：pip install anthropic
import sys, json
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import anthropic
client = anthropic.Anthropic()
SYSTEM_PROMPTS = {
    "嚴肅律師": "你是嚴謹的合約律師。回答要精準、引用法條編號、避免任何主觀形容詞。",
    "幼兒園老師": "你是溫柔的幼兒園老師、要對 5 歲小孩說話。用比喻、口語、少於 80 字。",
    "JSON 機器": "你只回 JSON。schema: {\"answer\": string, \"confidence\": float}",
}
USER_MSG = "請幫我解釋什麼是租賃合約。"

outputs = {}
for label, system in SYSTEM_PROMPTS.items():
    # Anthropic 用 system= 參數（不放 messages 內）
    msg = client.messages.create(model="claude-haiku-4-5", max_tokens=200,
                                 system=system, messages=[{"role": "user", "content": USER_MSG}])
    outputs[label] = msg.content[0].text
    print(f"\n--- [{label}] ---")
    print(outputs[label])

# 同樣的 JSON assert（schema 跨 backend 通用）
json_output = outputs["JSON 機器"]
assert "{" in json_output and "}" in json_output
print(f"\n✅ 練習 1 通過（Anthropic）")
```

**主要差異**：
- Anthropic: `system=...` 參數
- Ollama / OpenAI-compatible: `messages=[{"role": "system", ...}, ...]`

**Anthropic 對 system prompt 遵循度通常比 4B 小 model 更嚴謹**——「嚴肅律師」會真的引用法條編號。

</details>

### 練習 2：Few-Shot
挑一個分類任務。先用 0-shot 跑，再用 3-shot 跑。量一下準確率差多少。

<details open>
<summary>📋 <b>起手碼 — Path A（本機 Ollama gemma4:e4b、默認）</b>（複製到 <code>practice_2.py</code>）</summary>

```python
# 需要：pip install openai
# 前置：ollama pull gemma4:e4b && ollama serve
import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from openai import OpenAI

client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")

# 中文情緒分類（正面 / 負面 / 中立）
TEST_SET = [
    ("這部電影超讚、看完想再看一次！", "正面"),
    ("劇情無聊、演員演技尷尬。", "負面"),
    ("這是一部 2019 年的電影。", "中立"),
    ("我不確定喜不喜歡、可能再想想。", "中立"),
    ("第一集很不錯但第二集就崩了。", "負面"),
    ("看完心情很好、推薦！", "正面"),
]

FEW_SHOT_EXAMPLES = """範例：
input: 這家餐廳的牛排好吃到讓我哭出來。
output: 正面

input: 服務生態度很差、我再也不會來了。
output: 負面

input: 這家店位於新北市三重區。
output: 中立
"""


def classify(text: str, *, use_few_shot: bool) -> str:
    prefix = FEW_SHOT_EXAMPLES + "\n" if use_few_shot else ""
    prompt = f"{prefix}input: {text}\noutput:"
    r = client.chat.completions.create(
        model="gemma4:e4b",
        max_tokens=10,
        messages=[{"role": "user", "content": prompt}],
    )
    return r.choices[0].message.content.strip().splitlines()[0]


def evaluate(use_few_shot: bool) -> tuple[int, int]:
    correct = 0
    for text, label in TEST_SET:
        pred = classify(text, use_few_shot=use_few_shot)
        ok = label in pred
        print(f"  {'✓' if ok else '✗'} [{label}] {text[:30]}... → '{pred}'")
        if ok:
            correct += 1
    return correct, len(TEST_SET)


print("=== 0-shot ===")
c0, n = evaluate(use_few_shot=False)
print(f"正確 {c0}/{n} = {c0/n:.0%}")

print("\n=== 3-shot ===")
c3, _ = evaluate(use_few_shot=True)
print(f"正確 {c3}/{n} = {c3/n:.0%}")

# === 自我驗證 ===
assert c3 >= c0, f"預期 3-shot 不比 0-shot 差、實際 {c3} < {c0}（小 model 樣本小、跑幾次比較）"
print(f"\n✅ 練習 2 通過 — 0-shot {c0}/{n}、3-shot {c3}/{n}（本機 $0）")
print("💡 觀察：'中立' 在 0-shot 容易被誤判成正面或負面、3-shot 後改善明顯")
print("💡 小 model（gemma4:e4b）通常 0-shot 表現比 Claude 差更多、所以 few-shot 改善幅度更大")
```

</details>

<details>
<summary>📋 <b>起手碼 — Path B（Anthropic API、選擇性）</b>（複製到 <code>practice_2_anthropic.py</code>）</summary>

```python
# 需要：pip install anthropic
# 把 starter Path A 的 client 跟 classify() 改成：
import anthropic
client = anthropic.Anthropic()

def classify(text: str, *, use_few_shot: bool) -> str:
    prefix = FEW_SHOT_EXAMPLES + "\n" if use_few_shot else ""
    msg = client.messages.create(
        model="claude-haiku-4-5",
        max_tokens=10,
        messages=[{"role": "user", "content": f"{prefix}input: {text}\noutput:"}],
    )
    return msg.content[0].text.strip().splitlines()[0]
# 其餘 TEST_SET / FEW_SHOT_EXAMPLES / evaluate() 跟 Path A 一樣
```

**成本**：6 題 × 2 條件 = 12 次 ≈ $0.005。**Claude 通常 0-shot 已經有不錯準確率**、所以 few-shot 改善幅度比小 model 小。

</details>

### 練習 3：CoT
挑一個數學文字題，比較：
- 純 prompt
- 純 prompt + 「Let's think step by step」
- 純 prompt + 一個展示 CoT 的範例

<details open>
<summary>📋 <b>起手碼 — Path A（本機 Ollama gemma4:e4b、默認）</b>（複製到 <code>practice_3.py</code>）</summary>

```python
# 需要：pip install openai
# 前置：ollama pull gemma4:e4b && ollama serve
import sys, re
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from openai import OpenAI

client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")

QUESTION = "小明有 3 顆蘋果。他給了小華 1 顆、又從媽媽那邊拿到 5 顆、然後吃了 2 顆。請問現在剩幾顆？"
ANSWER = 5  # 3 - 1 + 5 - 2 = 5

COT_EXAMPLE = """範例：
Q: 一隻雞有 2 隻腳。3 隻雞跟 1 個人共有幾隻腳？
A: 讓我一步一步算。3 隻雞 × 2 隻腳 = 6 隻腳。1 個人有 2 隻腳。總共 6 + 2 = 8 隻腳。答案是 8。
"""


def ask(prompt: str) -> str:
    r = client.chat.completions.create(
        model="gemma4:e4b",
        max_tokens=300,
        messages=[{"role": "user", "content": prompt}],
    )
    return r.choices[0].message.content


def extract_number(text: str) -> int | None:
    nums = re.findall(r"-?\d+", text)
    return int(nums[-1]) if nums else None


# A. 純 prompt
out_a = ask(QUESTION); ans_a = extract_number(out_a)

# B. + Let's think step by step
out_b = ask(QUESTION + "\nLet's think step by step."); ans_b = extract_number(out_b)

# C. + CoT example
out_c = ask(COT_EXAMPLE + "\n\nQ: " + QUESTION + "\nA:"); ans_c = extract_number(out_c)

for label, out, ans in [("A 純 prompt", out_a, ans_a), ("B +step-by-step", out_b, ans_b), ("C +CoT example", out_c, ans_c)]:
    print(f"\n--- [{label}] 答案={ans} {'✓' if ans == ANSWER else '✗'} ---")
    print(out[:200])

# === 自我驗證 ===
correct = sum(1 for a in (ans_a, ans_b, ans_c) if a == ANSWER)
assert correct >= 1, f"3 種 prompt 至少要 1 種答對、實際 {correct}/3"
# 小 model 對 CoT 依賴性更高、放寬條件：B 或 C 至少 1 對（vs Anthropic Path B 要求嚴格）
assert ans_b == ANSWER or ans_c == ANSWER, "B (step-by-step) 或 C (CoT example) 至少一種要答對 — CoT 對小 model 是基本功"
print(f"\n✅ 練習 3 通過 — {correct}/3 答對（本機 $0）")
print(f"💡 觀察小 model：A 純 prompt 通常答錯、B/C 加 CoT 後明顯改善——比 Claude 更能凸顯 CoT 重要性")
```

</details>

<details>
<summary>📋 <b>起手碼 — Path B（Anthropic API、選擇性）</b>（複製到 <code>practice_3_anthropic.py</code>）</summary>

把 Path A 的 client + ask() 改成：

```python
import anthropic
client = anthropic.Anthropic()

def ask(prompt: str) -> str:
    msg = client.messages.create(model="claude-haiku-4-5", max_tokens=300,
                                 messages=[{"role": "user", "content": prompt}])
    return msg.content[0].text
```

**Claude 通常 3/3 全對**（包括 A 純 prompt）—— 對照 gemma4:e4b 可能只 1-2/3 對，能看到 CoT 對小 model 的價值。

</details>

### 練習 4：Iterative Refinement
拿一個模糊的 prompt，refine 5 次。把每一輪記下來。觀察哪些改動會提升品質。

<details open>
<summary>📋 <b>起手碼 — Path A（本機 Ollama gemma4:e4b、默認）</b>（複製到 <code>practice_4.py</code>）— 這題沒有「對錯」、重點是觀察過程</summary>

```python
# 需要：pip install openai
# 前置：ollama pull gemma4:e4b && ollama serve
import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from openai import OpenAI

client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")

# 5 個 iteration、每一輪 prompt 都比前一輪更具體
PROMPTS = {
    "v1 模糊": "寫一段介紹 ReAct 的文字。",
    "v2 加目標讀者": "寫一段介紹 ReAct 的文字、給寫過 Python 的軟體工程師看。",
    "v3 加格式": "寫一段介紹 ReAct 的文字、給寫過 Python 的軟體工程師看。100 字以內、用一個段落。",
    "v4 加 example 要求": "寫一段介紹 ReAct 的文字、給寫過 Python 的軟體工程師看。100 字以內、用一個段落、結尾舉一個具體例子（譬如查天氣）。",
    "v5 加禁忌": "寫一段介紹 ReAct 的文字、給寫過 Python 的軟體工程師看。100 字以內、用一個段落、結尾舉一個具體例子（譬如查天氣）。不要用「賦能」「驅動」「智能」這類空泛詞彙。",
}

outputs = {}
for label, prompt in PROMPTS.items():
    r = client.chat.completions.create(
        model="gemma4:e4b",
        max_tokens=200,
        messages=[{"role": "user", "content": prompt}],
    )
    text = r.choices[0].message.content
    outputs[label] = text
    print(f"\n--- [{label}] ({len(text)} chars) ---")
    print(text)

# === 自我驗證 ===
v1_len, v5_len = len(outputs["v1 模糊"]), len(outputs["v5 加禁忌"])
banned_words = ("賦能", "驅動", "智能")
v5_has_banned = any(w in outputs["v5 加禁忌"] for w in banned_words)
assert v5_len > 0, "v5 必須有輸出"
assert not v5_has_banned, f"v5 應該避免禁忌詞、實際含: {[w for w in banned_words if w in outputs['v5 加禁忌']]}"
print(f"\n✅ 練習 4 通過 — v5 長度 {v5_len}、無禁忌詞（本機 $0）")
print(f"💡 觀察：v1 ({v1_len} chars) 通常比 v5 ({v5_len} chars) 「鬆」、加約束會逼 prompt 收斂")
print("💡 用 gemma4:e4b 跑這題特別有感——小 model 對 prompt 質量極敏感、5 輪 refine 的差距會比 Claude 更明顯")
```

</details>

<details>
<summary>📋 <b>起手碼 — Path B（Anthropic API、選擇性）</b>（複製到 <code>practice_4_anthropic.py</code>）</summary>

把 Path A 的 client + 迴圈內 `client.chat.completions.create(...)` 改成：

```python
import anthropic
client = anthropic.Anthropic()

# 迴圈內：
msg = client.messages.create(model="claude-haiku-4-5", max_tokens=200,
                             messages=[{"role": "user", "content": prompt}])
text = msg.content[0].text
```

其餘 PROMPTS / outputs / assert 邏輯完全相同。**成本**：5 次 ≈ $0.002。

**Claude vs gemma4 對 prompt 細緻度的差別**：Claude haiku 通常 v1 已能寫出 OK 段落、v5 加上約束後優化幅度較小；小 model v1 常空泛無用、v5 加禁忌後才開始能讀。

</details>

**進階做法**：把這 5 輪輸出全存進 csv、Stage 7 練習 2 會教怎麼把這變成 eval harness 量化「prompt 改善了多少」。

## 🎯 精選 Projects

### [dair-ai/Prompt-Engineering-Guide](https://github.com/dair-ai/Prompt-Engineering-Guide)

| 欄位 | 內容 |
|---|---|
| Stars | ★ 60k+ |
| License | MIT |
| 推薦度 | ⭐⭐⭐⭐⭐ |

**教什麼**：從基礎到進階（CoT、ToT、ReAct、RAG）的端到端 prompt engineering。學術風但實用。

**適合誰**：當參考用。先大致掃過一次，需要某個技巧時再回來查。

---

### [f/awesome-chatgpt-prompts](https://github.com/f/awesome-chatgpt-prompts)

| 欄位 | 內容 |
|---|---|
| Stars | ★ 130k+ |
| License | CC0 |
| 推薦度 | ⭐⭐⭐ |

**教什麼**：上百個角色型 prompt。「Act as a [角色]...」的模式。

**適合誰**：卡關時找靈感。不要照抄——把模式拿出來改寫。

---

### [PromptingGuide.ai](https://www.promptingguide.ai/)

**教什麼**：跟 dair-ai GitHub 同樣的內容，但做成網站、有可以跑的範例。

**適合誰**：手機閱讀。

---

### [microsoft/prompt-engine](https://github.com/microsoft/prompt-engine)

| 欄位 | 內容 |
|---|---|
| 推薦度 | ⭐⭐⭐ |

**教什麼**：管理大量 prompt 的 TypeScript library（樣板、對話歷史）。

**適合誰**：開始要在 production 管很多 prompt 時。

---

### [microsoft/promptflow](https://github.com/microsoft/promptflow)

| 欄位 | 內容 |
|---|---|
| Stars | ★ 10k+ |
| 推薦度 | ⭐⭐⭐ |

**教什麼**：視覺化 prompt 設計 + 評估工具。

**適合誰**：以 prompt 為主、需要 eval 的團隊型應用。

---

### [GoogleCloudPlatform/generative-ai](https://github.com/GoogleCloudPlatform/generative-ai)

| 欄位 | 內容 |
|---|---|
| 推薦度 | ⭐⭐⭐ |

**教什麼**：Google Cloud 的 prompting cookbook（notebook，PaLM/Gemini 為主）。

**適合誰**：用 Google 技術棧時的跨廠商觀點。

---

### [Anthropic Cookbook — Prompt patterns](https://github.com/anthropics/anthropic-cookbook)

Stage 1 已經提過。這裡特別推 `misc/prompt_caching.ipynb` 跟 `multimodal/` 系列 notebook，會教進階 prompting 模式。

---

### [stanfordnlp/dspy](https://github.com/stanfordnlp/dspy)

| 欄位 | 內容 |
|---|---|
| 語言 | Python |
| Stars | ★ 34k+ |
| License | MIT |
| 推薦度 | ⭐⭐⭐⭐⭐ |

**教什麼**：把 prompt 當 code 寫——定義 signature 跟 module、用 compiler / teleprompter 自動最佳化 prompt，不用手刻 f-string。Stanford NLP 出品，是 Stage 2 → Stage 3 的橋。

**適合誰**：跑完 dair-ai 的指南、開始問「我要怎麼把 prompt 規模化（不是再多 hard-code）」的人。

**備註**：是 framework 不是 tutorial，學習門檻比 prompt-engineering-guide 高。建議搭配官方 tutorial 網站 dspy.ai 一起讀。

---

### [NirDiamant/Prompt_Engineering](https://github.com/NirDiamant/Prompt_Engineering)

| 欄位 | 內容 |
|---|---|
| 語言 | Python / Jupyter |
| Stars | ★ 7k+ |
| License | NOASSERTION（自訂條款，研究 / 非商用為主，使用前讀條款） |
| 推薦度 | ⭐⭐⭐⭐ |

**教什麼**：22 種 prompt engineering 技巧的可執行 Jupyter notebook（zero-shot → CoT → ReAct → constitutional），2025 年的更新內容，比 dair-ai 更動手。

**適合誰**：偏好「邊跑邊學」的人。每個技巧都有獨立 notebook，挑感興趣的看。

---

## 🔭 進階：context engineering（不是 prompt engineering 了）

當你發現「**單一 prompt 已經 cover 不了**」——要動態組 system prompt + 拉 memory + 塞 retrieved chunks + 接多個 tool definitions——這已經不叫 prompt engineering，叫 **context engineering**。是 prompt engineering 的下一層。

**這個 stage 不用學完它**，只是給個方向性提示：

- 在 [Stage 6（Memory · RAG）](06-memory-rag.md) 會碰到（什麼資料塞進 prompt）
- 在 [Stage 7（Multi-Agent · Production）](07-multi-agent-production.md) 完整面對（context window 預算、memory 階層、observability）

延伸閱讀（不必修、未來想深挖時看）：

- [`Meirtz/Awesome-Context-Engineering`](https://github.com/Meirtz/Awesome-Context-Engineering)（★ 3k+）——從 prompt engineering 一路推到 production agent 的 survey
- [`Windy3f3f3f3f/how-claude-code-works`](https://github.com/Windy3f3f3f3f/how-claude-code-works)（★ 2k+）——Claude Code 內部解析，含 context engineering 章節

## ✅ 進 Stage 3 前的自我檢查

你能不能：
- [ ] 寫一個有 system message + user message + 3 個範例 message 的 prompt（few-shot）
- [ ] 示範 CoT 在某個推理任務上提升準確率
- [ ] 反覆 refine 一個 prompt 5 次，每一版都留下記錄
- [ ] 看出 prompt 不是對的工具的時候（這時要用 tool use）

如果可以 → 進 [Stage 3 — Tool Use & Agent 入門](03-tool-use-and-hello-agent.md)。這是最重要的一個階段——prompt 不要急著跳過去，但也不要卡在這裡。
