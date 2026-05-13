# Stage 3 — Tool Use & Agent 入門 ⭐

> **繁體中文** | [简体中文](./03-tool-use-and-hello-agent.zh-Hans.md) | [English](./03-tool-use-and-hello-agent.en.md) | [Русский](./03-tool-use-and-hello-agent.ru.md)

⏱ **時間估算**：2-3 週（約 10-20 小時）

> 💡 用語密集（agent / tool use / function calling / ReAct / structured output⋯）→ 翻 [`resources/glossary.md` §2](../resources/glossary.md#2-agent--工具使用)。
> 🗺️ **進 Track A（CLI Power User）還是 Track B（Agent Builder）前**，先看 [`resources/agent-paradigms.md`](../resources/agent-paradigms.md) — 5 種 agent 型態的全景圖，幫你選軌。

這是整個學習路線最關鍵的一站。**你建過一個 agent 才算真懂 agent**——本 stage 的基礎練習建議至少實際手寫一次、再依需求往 [hello-agents](https://github.com/datawhalechina/hello-agents) 或本 stage 精選 projects 找深度教材。

## 📌 學習目標

完成這個 stage 後你會：
- 講得出為什麼 LLM 需要 tools（它不是萬能的，而且文字以外的事它都做不了）
- 定義一個 tool schema，並讓 LLM 呼叫它
- 從零（不靠任何 framework）寫出一個單步 ReAct agent
- 寫出多步 ReAct agent，並讓它自己判斷何時該停
- 分得出哪種問題該用 tool use、哪種純 prompt 就夠

## 🚪 進入條件

你應該已經：
- 有可以跑的 Claude / OpenAI / Gemini API 權限（Stage 1）
- 對 prompt engineering 基礎已經上手（Stage 2）
- 能寫一個吃 JSON 進、吐 JSON 出的 Python 函式

## 📚 必修閱讀

1. [**Anthropic — Tool Use**](https://docs.anthropic.com/en/docs/agents-and-tools/tool-use/overview) — 官方指南
2. [**ReAct: Synergizing Reasoning and Acting in Language Models**](https://arxiv.org/abs/2210.03629) — Yao et al. 2022，奠基論文。至少讀 abstract 跟 Section 3。
3. [**OpenAI — Function Calling**](https://platform.openai.com/docs/guides/function-calling) — function calling 格式參考
4. [**Build an agent from scratch**](https://shafiqulai.github.io/blogs/blog_3.html) — 從零打造 agent 的故事式導覽

## 🛠 動手練習（基礎 illustrative 練習）

> 🦙 **本 stage 默認用 Ollama qwen2.5:3b**（成本考量、tool-use 支援穩定）。Stage 3 進到 tool calling / ReAct loop、`gemma4:e4b` 不夠、改用 `qwen2.5:3b`（1.9 GB、`ollama pull qwen2.5:3b` 即裝）。每個練習都有 Path A（Ollama、默認）+ Path B（Anthropic、選擇性、想看 cloud 高品質 tool-use 時用）。
>
> 💰 **Stage 3 預算估算**（全 6 練習、tool use 較重）：**全本機 = $0**、**全 haiku ≈ $0.50**、**全 sonnet ≈ $1.50**。ReAct loop 練習單次 4-6 tool calls × 5 練習 × 5 reps ≈ $0.80 haiku。完整預算見 [`examples/README.md#推薦-llm-清單`](../examples/README.md#推薦-llm-清單本機--clouduser-視角)。
>
> 完整 3 路 trade-off 見 [`examples/README.md`](../examples/README.md#三條路徑--默認用-ollama成本考量)。
>
> 🆘 **卡住了？** Tool calling 是整個 curriculum 最陡的學習曲線。裝 [`examples/stage-5/tool-calling-tutor/`](../examples/stage-5/tool-calling-tutor/) skill——當你 prompt Claude Code「為什麼 LLM 不呼叫我的 tool」、「我這 schema 哪裡寫壞」會自動載入、走 4-symptom 診斷流程。
>
> 🪜 **本 stage 是 single-agent 起點**：一個 LLM + ReAct loop。**Multi-agent 概念**（多個 agent 協作）入門看 [Stage 4 § 什麼是 multi-agent framework](04-agent-frameworks.md#-什麼是-multi-agent-framework)、**Claude 原生 subagent 機制**（`.claude/agents/` + Task tool、不需 framework）看 [Stage 5.5](05-claude-code-ecosystem.md#55--subagentsclaude-code-原生-multi-agent-機制)。

### 練習 1：Function Calling（一個工具、一次呼叫）
給 Claude 一個工具（假的天氣 API）跟一個問題（「台北現在有下雨嗎？」）。看 Claude 怎麼呼叫工具、拿到結果、再回答你。

<details open>
<summary>📋 <b>起手碼 — Path A（本機 Ollama qwen2.5:3b、默認）</b>（複製到 <code>practice_1.py</code>）</summary>

```python
# 需要：pip install openai
# 前置：ollama pull qwen2.5:3b && ollama serve
# Note: Stage 3+ 用 qwen2.5:3b（tool-use 穩定）、不是 gemma4:e4b
import sys, json
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from openai import OpenAI

client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")

# Step 1: 定義 tool schema — OpenAI-compatible 格式包一層 {"type":"function", "function":{...}}
weather_tool = {
    "type": "function",
    "function": {
        "name": "get_weather",
        "description": "查詢城市目前天氣（晴/雨/陰），回傳一個短字串。",
        "parameters": {
            "type": "object",
            "properties": {
                "city": {"type": "string", "description": "城市名稱（如「台北」）"},
            },
            "required": ["city"],
        },
    },
}

# Step 2: 問問題、讓 LLM 自己決定要不要呼叫 tool
resp = client.chat.completions.create(
    model="qwen2.5:3b",
    max_tokens=512,
    tools=[weather_tool],
    messages=[{"role": "user", "content": "台北現在有下雨嗎？"}],
)

# === 自我驗證 ===
msg = resp.choices[0].message
print("finish_reason:", resp.choices[0].finish_reason)
print("tool_calls:", msg.tool_calls)

assert msg.tool_calls, "預期 LLM 會選擇呼叫 tool（而非直接回答）"
tc = msg.tool_calls[0]
assert tc.function.name == "get_weather", f"預期呼叫 get_weather、實際 {tc.function.name}"
args = json.loads(tc.function.arguments)
assert args.get("city"), "預期 city 參數有值"
print(f"✅ 練習 1 通過 — qwen2.5:3b 正確選了 get_weather、帶 city='{args['city']}' 參數")
```

**預期輸出**（樣本）：
```
finish_reason: tool_calls
tool_calls: [ChatCompletionMessageToolCall(id='call_xxx', function=Function(name='get_weather', arguments='{"city": "台北"}'), type='function')]
✅ 練習 1 通過 — qwen2.5:3b 正確選了 get_weather、帶 city='台北' 參數
```

**沒裝 Ollama 也能驗邏輯**：用 `unittest.mock.MagicMock` 取代 client、塞固定 response、assert 一樣 work。完整 mock 範例見 [`examples/stage-3/03-react-from-scratch/test.py`](../examples/stage-3/03-react-from-scratch/test.py)（pattern 跨 backend 通用）。

</details>

<details>
<summary>📋 <b>起手碼 — Path B（Anthropic API、選擇性）</b>（複製到 <code>practice_1_anthropic.py</code>）</summary>

```python
# 需要：pip install anthropic
# 環境變數：export ANTHROPIC_API_KEY=sk-ant-...
import anthropic

client = anthropic.Anthropic()

# Anthropic native tool schema — 不用包 wrapper
weather_tool = {
    "name": "get_weather",
    "description": "查詢城市目前天氣（晴/雨/陰），回傳一個短字串。",
    "input_schema": {
        "type": "object",
        "properties": {
            "city": {"type": "string", "description": "城市名稱（如「台北」）"},
        },
        "required": ["city"],
    },
}

resp = client.messages.create(
    model="claude-haiku-4-5",
    max_tokens=512,
    tools=[weather_tool],
    messages=[{"role": "user", "content": "台北現在有下雨嗎？"}],
)

# === 自我驗證 ===
assert resp.stop_reason == "tool_use", f"非預期 stop_reason: {resp.stop_reason}"
tool_calls = [b for b in resp.content if b.type == "tool_use"]
assert tool_calls[0].name == "get_weather"
assert tool_calls[0].input.get("city")
print(f"✅ 練習 1 通過（Anthropic）— Claude 選了 get_weather、city='{tool_calls[0].input['city']}'")
```

**3 個關鍵 SDK 差異**：
- **Schema wrap**：Anthropic 直接 `tools=[{name, description, input_schema}]`；OpenAI/Ollama 要包 `[{"type":"function", "function":{...}}]`
- **Response 路徑**：Anthropic 從 `resp.content[i].type=="tool_use"` 抓；OpenAI/Ollama 從 `resp.choices[0].message.tool_calls[i]`
- **Args 格式**：Anthropic `.input` 是 dict（自動 parse）；OpenAI/Ollama `.function.arguments` 是 JSON string，要 `json.loads(...)`

**成本**：1 次 ≈ $0.001。**Claude 的 tool-use 比 qwen2.5:3b 更穩**——複雜場景（5+ tools、模糊問題）gap 會明顯。

</details>

### 練習 2：多工具選擇
給 Claude 三個工具（搜尋、計算機、行事曆）跟一個任務。看 Claude 怎麼挑工具，順便注意它什麼時候會挑錯。

<details>
<summary>📋 <b>簡化版核心觀念 — Path A (Ollama)</b></summary>

**NEW vs 練習 1**：tools 從 1 個變 3 個。LLM 看 `description` 邊界決定挑哪個——`description` 寫得越像「給人讀的 docstring」、越容易挑錯。

```python
from openai import OpenAI
import json

client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")

TOOLS = [
    {"type": "function", "function": {"name": "web_search",
        "description": "Search current or external info not in the prompt.",
        "parameters": {"type": "object", "properties": {"query": {"type": "string"}}, "required": ["query"]}}},
    {"type": "function", "function": {"name": "calculator",
        "description": "Evaluate basic arithmetic with +, -, *, /, parentheses.",
        "parameters": {"type": "object", "properties": {"expression": {"type": "string"}}, "required": ["expression"]}}},
    {"type": "function", "function": {"name": "calendar_lookup",
        "description": "Look up events for a specific date.",
        "parameters": {"type": "object", "properties": {"date": {"type": "string"}}, "required": ["date"]}}},
]

resp = client.chat.completions.create(model="qwen2.5:3b", tools=TOOLS,
    messages=[{"role": "user", "content": "What is (19 * 42) - 8?"}])

tc = resp.choices[0].message.tool_calls[0]
print(f"LLM 挑了: {tc.function.name}, args: {json.loads(tc.function.arguments)}")
# 預期：calculator, {"expression": "(19 * 42) - 8"}
```

**punchline**：3 個 tool 的 `description` 邊界要互斥——`calendar` 寫「行事曆」太籠統、會跟 `web_search` 撞；寫「特定日期事件」就清楚。小 model 對 description 質量比 Claude 更敏感。

**Path B (Anthropic) 改 3 行**：schema 拿掉 `{"type": "function", "function": {...}}` 外包、`tool_calls` 變 `[b for b in resp.content if b.type == "tool_use"]`、`tc.input` 已經是 dict 不用 `json.loads`。完整版見 folder。

</details>

→ **完整可跑版** → [`examples/stage-3/02-multi-tool-selection/`](../examples/stage-3/02-multi-tool-selection/)

### 練習 3：從零實作 ReAct（不用 framework）
用 50-80 行 Python 把 Thought → Action → Observation 迴圈寫出來。不要 LangChain、不要 LangGraph，就是純 `while not done: thought; action; observation; ...`。

<details>
<summary>📋 <b>簡化版核心觀念 — Path A (Ollama)、ReAct loop 的全部就在這 13 行</b></summary>

**NEW vs 練習 2**：把單次 call 包進迴圈、`messages` 一直長、看 `tool_calls` 在不在來決定收尾。

```python
# 假設 TOOLS + TOOL_IMPL（dict: name → callable）已經像練習 2 一樣定義好
messages = [{"role": "user", "content": "台北人口除以紐約人口？"}]

for step in range(5):  # max_iter safety net
    r = client.chat.completions.create(model="qwen2.5:3b", tools=TOOLS, messages=messages)
    msg = r.choices[0].message
    # 把 assistant response 接回 messages（重要！下輪 LLM 才看得到自己上輪講什麼）
    messages.append({"role": "assistant", "content": msg.content, "tool_calls": msg.tool_calls})
    if not msg.tool_calls:
        print(f"✅ 收尾：{msg.content}"); break
    for tc in msg.tool_calls:
        args = json.loads(tc.function.arguments)
        obs = TOOL_IMPL[tc.function.name](args)  # 本地執行
        # observation 接回 messages（用 role="tool"、配 tool_call_id）
        messages.append({"role": "tool", "tool_call_id": tc.id, "content": obs})
```

**3 個容易踩坑**：
1. **忘記把 assistant response 加回 messages**——下輪 LLM 看不到自己上輪講什麼、會 loop forever
2. **`tool` message 沒帶 `tool_call_id`**——LLM 無法配對哪個 result 對應哪個 call
3. **沒 `max_iter`**——tool 結果寫不好時、LLM 會無限呼叫，safety net 必須設

**Path B (Anthropic) 差幾行**：迴圈架構一模一樣、`msg.tool_calls` 變 `[b for b in resp.content if b.type == "tool_use"]`、用 `stop_reason == "end_turn"` 判停、tool result 包成 `{"type": "tool_result", "tool_use_id": ..., "content": obs}` 放進 user message。完整版見 folder。

</details>

→ **完整可跑版** → [`examples/stage-3/03-react-from-scratch/`](../examples/stage-3/03-react-from-scratch/)（含 mock-based test.py、不花 API 錢也能驗）

### 練習 4：多步驟推理任務
一個需要連續呼叫 3-5 次 tool 的任務。例如：「找出台北人口，除以紐約人口，再把比例換成百分比。」每一步用不同的工具。

<details>
<summary>📋 <b>簡化版核心觀念 — 跟練習 3 同一個 loop、跑久一點而已</b></summary>

**NEW vs 練習 3**：**完全同一個 loop**——只是 `TOOLS` 換成 4 個（`lookup_population` / `divide` / `to_percentage` / `round_int`）、題目自然走完 4 輪 tool call 才收尾。

```python
# 沒有新 code、純粹是 TOOLS / TOOL_IMPL 換內容
TOOL_IMPL = {
    "lookup_population": lambda i: lookup_population(i["city"]),
    "divide":            lambda i: divide(i["a"], i["b"]),
    "to_percentage":     lambda i: to_percentage(i["ratio"]),
    "round_int":         lambda i: round_int(i["x"]),
}
# loop 完全照 練習 3，只是 max_iter 拉大到 8
```

**punchline**：多步推理不是新 pattern、是**讓 ReAct loop 跑久一點**。**真正的挑戰是「LLM 會不會中間漏一步」**——qwen2.5:3b 可能漏「轉百分比」、Claude haiku 較穩。**這恰好是觀察「model 規模 vs 多步穩定度」的好實驗**。試試 `MODEL=qwen2.5:7b python starter.py` 對照。

</details>

→ **完整可跑版** → [`examples/stage-3/04-multi-step-reasoning/`](../examples/stage-3/04-multi-step-reasoning/)

### 練習 5：錯誤處理
讓某個工具失敗（網路錯誤、輸入無效）。看看 agent 會怎麼處理錯誤、能不能恢復，再加上 retry 機制。

<details>
<summary>📋 <b>簡化版核心觀念 — tool error 是 data、不是 exception</b></summary>

**NEW vs 練習 4**：tool error 回傳**結構化 dict**、不要 `raise`。loop 把 dict 接回 LLM、模型自己決定 retry / 改 query / 放棄。

```python
def fetch_weather(city: str) -> dict:
    if network_failed():
        return {"error": "network timeout", "retry_hint": "try again in 1s"}
    return {"city": city, "forecast": "rain", "temperature_c": 24}

# loop 裡：
obs = fetch_weather(args["city"])
messages.append({"role": "tool", "tool_call_id": tc.id,
                 "content": json.dumps(obs, ensure_ascii=False)})  # error dict 也是 string 化接回去
# 下一輪 LLM 看到 retry_hint、可能會 retry、可能會放棄、可能會改 query
```

**為什麼不 `raise`**：`raise` 直接中斷 loop、LLM 沒機會 recover。**Production 的 retry 不在 Python 層、而在 LLM 層**——這個 mental flip 是 Stage 3 練習 5 的核心。

**Bad vs Good error 回傳**：

| Bad | Good |
|---|---|
| `raise Exception("failed")` | `return {"error": "network timeout", "retry_hint": "try again in 1s"}` |
| `return "failed"` | `return {"error": "...", "category": "transient", "retry_hint": "..."}` |
| 無限 retry | `max_iter` safety + 業務層 retry quota |

**小 model 觀察**：qwen2.5:3b 對 `retry_hint` follow-up 較弱、可能直接放棄；Claude haiku 較穩。完整版（含連續失敗 graceful end 範例）見 folder。

</details>

→ **完整可跑版** → [`examples/stage-3/05-error-handling/`](../examples/stage-3/05-error-handling/)

### 練習 6：Function schema 設計（壞 schema 修到好）
**先給 LLM 一份故意寫爛的 schema**——`description` 模糊（「處理資料」）、參數全用 `type: string`、沒分 required / optional、enum 該用沒用。觀察 LLM 怎麼選錯 tool、傳錯參數。然後逐項修：
- description 寫到 LLM 一眼就懂這個 tool 適用情境（不是寫給人讀的 docstring）
- parameters 用對 type（number / boolean / enum / array），required 列清楚
- 模糊邊界用 enum 強制收斂（例如 `unit: "celsius" | "fahrenheit"` 而不是 `unit: string`）
- error 回傳要包 `{"error": "...", "retry_hint": "..."}` 讓 LLM 能恢復

> 💡 詳細 cheatsheet 看 [`resources/schema-design-cheatsheet.md`](../resources/schema-design-cheatsheet.md)——5 條黃金規則 + 5 個常見 anti-pattern。

<details>
<summary>📋 <b>簡化版核心觀念 — bad vs good schema 對照</b></summary>

**NEW vs 練習 5**：同一個工具（溫度轉換）、兩種 schema 寫法。看 4 個差別。

```python
# ❌ BAD — qwen2.5:3b 幾乎必錯（Claude haiku 還能猜對、但機率明顯下降）
{"name": "convert", "description": "Convert a value.",
 "parameters": {"type": "object", "properties": {
     "value": {"type": "string"}, "unit": {"type": "string"}}}}

# ✅ GOOD — qwen 也能穩定挑對
{"name": "convert_temperature",
 "description": "Use when user asks to convert temperatures between Fahrenheit and Celsius.",
 "parameters": {"type": "object", "properties": {
     "value": {"type": "number", "description": "Temperature value"},
     "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]}},
     "required": ["value", "unit"]}}
```

**4 個改進**：(1) `name` 改具體、(2) `description` 寫「**何時**用」而非「**做什麼**」、(3) `type` 改 `number`、(4) 加 `required` + `enum`。

**punchline**：**寫 schema 的功夫能省下換大 model 的成本**——小 model 對 schema 質量比大 model 敏感，相同 bad schema 在 Claude 上可能還能猜對、在 qwen 上幾乎必錯。Production 想用便宜 model？schema 必須寫到 production-grade。

**搞不定 schema 怎麼辦**：裝 [`examples/stage-5/tool-calling-tutor/`](../examples/stage-5/tool-calling-tutor/) skill，遇到「LLM 不呼叫我的 tool」、「我這 schema 哪裡寫壞」會自動跳出來幫你 debug。

</details>

→ **完整可跑版** → [`examples/stage-3/06-schema-design/`](../examples/stage-3/06-schema-design/)（含 bad schema vs good schema 兩個版本對照）

## 🎯 精選 Projects

按用途分 4 類。**先看分類表挑入口、再點下面 detail block 看適合誰 / 教什麼**：

| 分類 | Project | 推薦 | 為什麼推薦 |
|---|---|---|---|
| **官方 cookbook**（先看這個）| [Anthropic — Tool Use Cookbook](https://github.com/anthropics/anthropic-cookbook/tree/main/tool_use) | ⭐⭐⭐⭐⭐ | 單工具 → 多工具 → parallel → structured output 全部 notebook |
| | [Anthropic — Quickstarts](https://github.com/anthropics/anthropic-quickstarts) | ⭐⭐⭐⭐⭐ | 3 個 deploy-ready agent 範本（financial / customer-support / computer-use） |
| | [Anthropic — Building Effective Agents（部落格）](https://www.anthropic.com/engineering/building-effective-agents) | ⭐⭐⭐⭐⭐ | 什麼時候該用 agent / 常見 pattern / 容易踩的坑、Stage 4 前必讀 |
| **從零實作 ReAct**（理解原理）| [pguso/ai-agents-from-scratch](https://github.com/pguso/ai-agents-from-scratch) | ⭐⭐⭐⭐⭐ | 用本機 LLM 從零打造 agent、zero framework |
| | [arunpshankar/react-from-scratch](https://github.com/arunpshankar/react-from-scratch) | ⭐⭐⭐⭐ | ReAct 變體 + Reflection + Self-consistency、Gemini 最佳化 |
| | [mattambrogi/agent-implementation](https://github.com/mattambrogi/agent-implementation) | ⭐⭐⭐ | ~150 行最精簡 ReAct、⚠️ 已停滯（2024-01）但可逐行讀 |
| | [lsdefine/GenericAgent](https://github.com/lsdefine/GenericAgent) | ⭐⭐⭐⭐ | 自我演化 agent framework、~3K 行精簡完整、支援 Claude / Gemini / Kimi |
| **CodeAct 路線**（agent 寫程式碼當 action）| [HuggingFace Smolagents](https://github.com/huggingface/smolagents) | ⭐⭐⭐⭐ | ≤1000 LOC、CodeAct pattern 代表 |
| | [QuantaLogic/quantalogic](https://github.com/quantalogic/quantalogic) | ⭐⭐⭐ | 另一條 CodeAct 路線、跟 JSON tool 路線對照 |
| **中文章節式深度教材**（chapter-length）| [datawhalechina/hello-agents](https://github.com/datawhalechina/hello-agents) ⭐ 本 stage 推薦 | ⭐⭐⭐⭐⭐ | **16 種能力**含 tool use / ReAct / context engineering / sub-agents / circuit breaker / observability。中文圈最完整、章節式 |
| | [HelloAgents (jjyaoao)](https://github.com/jjyaoao/HelloAgents) `learn_version` | ⭐⭐⭐⭐⭐ | 上面教材的 code repo、`learn_version` 分支對齊章節 |
| **Framework 對照**（看 framework 怎麼藏掉 ReAct loop）| [LangChain — ReAct Agent Template](https://github.com/langchain-ai/react-agent) | ⭐⭐⭐ | 練習 3 自己寫完後、再來看 framework 抽象做了什麼 |

---

### [Anthropic — Tool Use Cookbook](https://github.com/anthropics/anthropic-cookbook/tree/main/tool_use)

| 欄位 | 內容 |
|---|---|
| 語言 | Python |
| License | MIT |
| 推薦度 | ⭐⭐⭐⭐⭐ |

**教什麼**：Claude 支援的所有 tool use 模式 — 單工具、多工具、平行呼叫、結構化輸出抽取。

**適合誰**：練習 1 跟 練習 2，從這裡開始。

**怎麼跑**：
```bash
git clone https://github.com/anthropics/anthropic-cookbook
cd anthropic-cookbook/tool_use
jupyter notebook customer_service_agent.ipynb
```

---

### [Anthropic — Quickstarts](https://github.com/anthropics/anthropic-quickstarts)

| 欄位 | 內容 |
|---|---|
| 語言 | Python / TypeScript |
| Stars | ★ 16k+ |
| License | MIT |
| 推薦度 | ⭐⭐⭐⭐⭐ |

**教什麼**：Anthropic 官方的 動手練習 起手包。三個可直接 deploy 的 agent 範本：`financial-data-analyst`（資料分析 agent）、`customer-support-agent`（客服 agent）、`computer-use-demo`（讓 Claude 操作螢幕）。

**適合誰**：跑完 練習 1 / 練習 2 之後，想看「真的應用會長什麼樣子」的官方參考。比社群實作更 canonical，部署設定也比較完整。

**備註**：每個範本都是獨立 sub-folder，挑一個有興趣的跑就好。Computer use demo 特別值得看 — 是少數示範 agent 操作 GUI 的官方範例。

---

### [pguso/ai-agents-from-scratch](https://github.com/pguso/ai-agents-from-scratch)

| 欄位 | 內容 |
|---|---|
| 語言 | Python |
| License | MIT |
| 推薦度 | ⭐⭐⭐⭐⭐ |

**教什麼**：用本地 LLM 從零打造 agent，零 framework。ReAct、function calling、memory，全部自己寫。設計目的就是把 framework 幫你藏起來的東西攤開給你看。

**適合誰**：練習 3（從零寫 ReAct）。這是最乾淨的「不靠 framework」參考實作。

**備註**：用本地 Ollama，不用花 API 錢。README 值得仔細讀，章節結構安排得很好。

---

### [arunpshankar/react-from-scratch](https://github.com/arunpshankar/react-from-scratch)

| 欄位 | 內容 |
|---|---|
| 語言 | Python |
| License | Apache-2.0 |
| 最後更新 | ⚠️ 2025 年 5 月（更新放緩） |
| 推薦度 | ⭐⭐⭐⭐ |

**教什麼**：ReAct pattern 的多種變體與實作，針對 Gemini 最佳化。

**適合誰**：練習 3 的替代方案，如果你偏好 Gemini。涵蓋 ReAct + Reflection + Self-consistency 等變體。

---

### [mattambrogi/agent-implementation](https://github.com/mattambrogi/agent-implementation)

| 欄位 | 內容 |
|---|---|
| 語言 | Python |
| License | MIT |
| 最後更新 | ⚠️ 已停滯（2024 年 1 月）— 留作教學玩具參考 |
| 推薦度 | ⭐⭐⭐ |

**教什麼**：最精簡的 ReAct agent 實作。為了學習而砍到只剩約 150 行程式碼。

**適合誰**：逐行讀程式碼。練習 3 卡住時可以拿來對照。

---

### [lsdefine/GenericAgent](https://github.com/lsdefine/GenericAgent)

| 欄位 | 內容 |
|---|---|
| 語言 | 中文 + Python |
| Stars | ★ 9k+ |
| License | MIT |
| 推薦度 | ⭐⭐⭐⭐ |

**教什麼**：最精簡的自我演化 agent framework — 核心約 3K 行程式碼，agent 從 seed 自己長出技能樹。支援 Claude / Gemini / Kimi / MiniMax。仍在持續開發。

**適合誰**：練習 3 / 練習 4 的替代方案，給想看「精簡但完整」framework 的讀者。介於 mattambrogi 的玩具版跟完整 LangGraph 之間的中間點。

---

### [HelloAgents (jjyaoao)](https://github.com/jjyaoao/HelloAgents) — `learn_version` 分支

| 欄位 | 內容 |
|---|---|
| 語言 | 中文（zh-Hans）+ Python |
| License | CC BY-NC-SA 4.0 |
| 推薦度 | ⭐⭐⭐⭐⭐（中文讀者） |

**教什麼**：教學導向的多 agent 練習框架，章節式教學，搭配 [Datawhale 的 Hello-Agents 教學](https://github.com/datawhalechina/hello-agents)。涵蓋 16 種能力（tool response、context engineering、session 持久化、sub-agents、circuit breaker、observability 等），用來學 production pattern 的教材，不是直接拿來上 production 的成品。

**適合誰**：中文讀者。**請切到 `learn_version` 分支**，那才是對齊教材的版本。

**備註**：License 是 CC BY-NC-SA — 非商用。教材是 zh-Hans，但技術內容對 zh-TW 讀者沒障礙。

**怎麼跑**：
```bash
pip install hello-agents
git clone -b learn_version https://github.com/jjyaoao/HelloAgents
```

---

### [datawhalechina/hello-agents](https://github.com/datawhalechina/hello-agents)

| 欄位 | 內容 |
|---|---|
| 語言 | 中文（zh-Hans） |
| License | CC BY-NC-SA |
| 推薦度 | ⭐⭐⭐⭐⭐（中文讀者） |

**教什麼**：HelloAgents 的搭配教學。多章節導讀，從「什麼是 agent」一路講到 production 的實務 pattern。

**適合誰**：想要結構化教學加程式碼的中文讀者。

**備註**：請搭配上面 HelloAgents repo 的 `learn_version` 分支一起看。

---

### [QuantaLogic/quantalogic](https://github.com/quantalogic/quantalogic)

| 欄位 | 內容 |
|---|---|
| 語言 | Python |
| License | Apache-2.0 |
| 推薦度 | ⭐⭐⭐ |

**教什麼**：產生 Python 程式碼（而不是 JSON tool call）的 ReAct agent。設計選擇不同 — agent 直接寫程式碼當作 action。

**適合誰**：跑完 練習 3 之後。比較 CodeAct（程式碼即 action）與 JSON tool call 的差別。

---

### [HuggingFace Smolagents](https://github.com/huggingface/smolagents)

| 欄位 | 內容 |
|---|---|
| 語言 | Python |
| Stars | ★ 27k+ |
| License | Apache 2.0 |
| 推薦度 | ⭐⭐⭐⭐ |

**教什麼**：Smol agents（≤1000 LOC）。會寫程式碼的 agent — 執行 Python 而不是 JSON tool call。

**適合誰**：練習 5 的替代方案。特別適合本地 LLM 實驗。

**備註**：HF 的立場：agent 應該要小。他們的 code-action 路線跟 JSON-tool 路線在思路上很不一樣，值得對照來看。

---

### [LangChain — ReAct Agent Template](https://github.com/langchain-ai/react-agent)

| 欄位 | 內容 |
|---|---|
| 語言 | Python |
| License | MIT |
| 推薦度 | ⭐⭐⭐ |

**教什麼**：framework 怎麼把 ReAct pattern 抽象化。LangGraph Studio 的範本。

**適合誰**：練習 3 之後（先自己從零寫過再來）。再來比較 framework 幫你做了哪些事。

---

### [Anthropic — Building Effective Agents（部落格文章）](https://www.anthropic.com/engineering/building-effective-agents)

| 欄位 | 內容 |
|---|---|
| 形式 | 文章 |
| 推薦度 | ⭐⭐⭐⭐⭐ |

**教什麼**：Anthropic 自己寫的指南 — 什麼時候該用 agent（vs. workflow）、常見 pattern、容易踩的坑。Stage 4 之前必讀。

**適合誰**：建立觀念框架。練習 3 寫完之後、學 framework 之前讀。

---

## ✅ 進 Stage 4 前的自我檢查

你能不能：
- [ ] 定義一個 tool schema（name + description + JSON schema 輸入/輸出）
- [ ] 用不到 100 行 Python、不靠任何 framework，把 ReAct 迴圈寫出來
- [ ] 解釋為什麼 agent 需要一個「我做完了」的退出條件
- [ ] 比較 CodeAct（程式碼即 action）跟 JSON-tool 兩種路線
- [ ] 看出哪些問題其實不需要 agent

如果可以 → 進 [Stage 4 — Agent Frameworks](04-agent-frameworks.md)。

如果不行 → 把 練習 3 再跑一次，不要跳過。如果你不懂 framework 在幫你抽象什麼，Stage 4 的那些東西看起來會像黑魔法。
