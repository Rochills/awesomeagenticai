# Stage 3 — Tool Use 与 Agent 入门 ⭐

> [繁体中文](./03-tool-use-and-hello-agent.md) | **简体中文** | [English](./03-tool-use-and-hello-agent.en.md) | [Русский](./03-tool-use-and-hello-agent.ru.md)

⏱ **时间估算**：2-3 周（约 10-20 小时）

> 💡 用语密集（agent / tool use / function calling / ReAct / structured output⋯）→ 翻 [`resources/glossary.zh-Hans.md` §2](../resources/glossary.zh-Hans.md#2-agent--工具使用)。
> 🗺️ **进 Track A（CLI Power User）还是 Track B（Agent Builder）前**，先看 [`resources/agent-paradigms.zh-Hans.md`](../resources/agent-paradigms.zh-Hans.md) — 5 种 agent 型态的全景图，帮你选轨。

这是整个学习路线最关键的一站。**你建过一个 agent 才算真懂 agent**——本 stage 的基础练习建议至少实际手写一次、再依需求往 [hello-agents](https://github.com/datawhalechina/hello-agents) 或本 stage 精选 projects 找深度教材。

## 📌 学习目标

完成这个 stage 后你会：
- 讲得出为什么 LLM 需要 tools（它不是万能的，而且文字以外的事它都做不了）
- 定义一个 tool schema，并让 LLM 调用它
- 从零（不靠任何 framework）写出一个单步 ReAct agent
- 写出多步 ReAct agent，并让它自己判断何时该停
- 分得出哪种问题该用 tool use、哪种纯 prompt 就够

## 🚪 进入条件

你应该已经：
- 有可以跑的 Claude / OpenAI / Gemini API 权限（Stage 1）
- 对 prompt engineering 基础已经上手（Stage 2）
- 能写一个吃 JSON 进、吐 JSON 出的 Python 函数

## 📚 必修阅读

1. [**Anthropic — Tool Use**](https://docs.anthropic.com/en/docs/agents-and-tools/tool-use/overview) — 官方指南
2. [**ReAct: Synergizing Reasoning and Acting in Language Models**](https://arxiv.org/abs/2210.03629) — Yao et al. 2022，奠基论文。至少读 abstract 跟 Section 3。
3. [**OpenAI — Function Calling**](https://platform.openai.com/docs/guides/function-calling) — function calling 格式参考
4. [**Build an agent from scratch**](https://shafiqulai.github.io/blogs/blog_3.html) — 从零打造 agent 的故事式导览

## 🛠 动手练习（基础 illustrative 练习）

> 🦙 **本 stage 默认用 Ollama qwen2.5:3b**（成本考量、tool-use 支持稳定）。Stage 3 进到 tool calling / ReAct loop、`gemma4:e4b` 不够、改用 `qwen2.5:3b`（1.9 GB、`ollama pull qwen2.5:3b` 即装）。每个练习都有 Path A（Ollama、默认）+ Path B（Anthropic、选择性、想看 cloud 高品质 tool-use 时用）。
>
> 💰 **Stage 3 预算估算**（全 6 练习、tool use 较重）：**全本机 = $0**、**全 haiku ≈ $0.50**、**全 sonnet ≈ $1.50**。ReAct loop 练习单次 4-6 tool calls × 5 练习 × 5 reps ≈ $0.80 haiku。完整预算见 [`examples/README.zh-Hans.md#推荐-llm-清单`](../examples/README.zh-Hans.md#推荐-llm-清单本机--clouduser-视角)。
>
> 完整 3 路 trade-off 见 [`examples/README.zh-Hans.md`](../examples/README.zh-Hans.md#三条路径--默认用-ollama成本考量)。
>
> 🆘 **卡住了？** Tool calling 是整个 curriculum 最陡的学习曲线。装 [`examples/stage-5/tool-calling-tutor/`](../examples/stage-5/tool-calling-tutor/) skill——当你 prompt Claude Code「为什么 LLM 不调用我的 tool」、「我这 schema 哪里写坏」会自动载入、走 4-symptom 诊断流程。

### 练习 1：Function Calling（一个工具、一次调用）
给 Claude 一个工具（假的天气 API）跟一个问题（「台北现在有下雨吗？」）。看 Claude 怎么调用工具、拿到结果、再回答你。

<details open>
<summary>📋 <b>起手码 — Path A（本机 Ollama qwen2.5:3b、默认）</b>（复制到 <code>practice_1.py</code>）</summary>

```python
# 需要：pip install openai
# 前置：ollama pull qwen2.5:3b && ollama serve
# Note: Stage 3+ 用 qwen2.5:3b（tool-use 稳定）、不是 gemma4:e4b
import sys, json
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from openai import OpenAI

client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")

# Step 1: 定义 tool schema — OpenAI-compatible 格式包一层 {"type":"function", "function":{...}}
weather_tool = {
    "type": "function",
    "function": {
        "name": "get_weather",
        "description": "查詢城市目前天气（晴/雨/阴），回传一个短字串。",
        "parameters": {
            "type": "object",
            "properties": {
                "city": {"type": "string", "description": "城市名称（如「台北」）"},
            },
            "required": ["city"],
        },
    },
}

# Step 2: 问问题、让 LLM 自己决定要不要调用 tool
resp = client.chat.completions.create(
    model="qwen2.5:3b",
    max_tokens=512,
    tools=[weather_tool],
    messages=[{"role": "user", "content": "台北现在有下雨吗？"}],
)

# === 自我验证 ===
msg = resp.choices[0].message
print("finish_reason:", resp.choices[0].finish_reason)
print("tool_calls:", msg.tool_calls)

assert msg.tool_calls, "预期 LLM 会选择调用 tool（而非直接回答）"
tc = msg.tool_calls[0]
assert tc.function.name == "get_weather", f"预期调用 get_weather、实际 {tc.function.name}"
args = json.loads(tc.function.arguments)
assert args.get("city"), "预期 city 参数有值"
print(f"✅ 练习 1 通过 — qwen2.5:3b 正确选了 get_weather、带 city='{args['city']}' 参数")
```

**预期输出**（樣本）：
```
finish_reason: tool_calls
tool_calls: [ChatCompletionMessageToolCall(id='call_xxx', function=Function(name='get_weather', arguments='{"city": "台北"}'), type='function')]
✅ 练习 1 通过 — qwen2.5:3b 正确选了 get_weather、带 city='台北' 参数
```

**没裝 Ollama 也能验邏輯**：用 `unittest.mock.MagicMock` 取代 client、塞固定 response、assert 一樣 work。完整 mock 范例见 [`examples/stage-3/03-react-from-scratch/test.py`](../examples/stage-3/03-react-from-scratch/test.py)（pattern 跨 backend 通用）。

</details>

<details>
<summary>📋 <b>起手码 — Path B（Anthropic API、选择性）</b>（复制到 <code>practice_1_anthropic.py</code>）</summary>

```python
# 需要：pip install anthropic
# 环境變数：export ANTHROPIC_API_KEY=sk-ant-...
import anthropic

client = anthropic.Anthropic()

# Anthropic native tool schema — 不用包 wrapper
weather_tool = {
    "name": "get_weather",
    "description": "查詢城市目前天气（晴/雨/阴），回传一个短字串。",
    "input_schema": {
        "type": "object",
        "properties": {
            "city": {"type": "string", "description": "城市名称（如「台北」）"},
        },
        "required": ["city"],
    },
}

resp = client.messages.create(
    model="claude-haiku-4-5",
    max_tokens=512,
    tools=[weather_tool],
    messages=[{"role": "user", "content": "台北现在有下雨吗？"}],
)

# === 自我验证 ===
assert resp.stop_reason == "tool_use", f"非预期 stop_reason: {resp.stop_reason}"
tool_calls = [b for b in resp.content if b.type == "tool_use"]
assert tool_calls[0].name == "get_weather"
assert tool_calls[0].input.get("city")
print(f"✅ 练习 1 通过（Anthropic）— Claude 选了 get_weather、city='{tool_calls[0].input['city']}'")
```

**3 个关鍵 SDK 差異**：
- **Schema wrap**：Anthropic 直接 `tools=[{name, description, input_schema}]`；OpenAI/Ollama 要包 `[{"type":"function", "function":{...}}]`
- **Response 路徑**：Anthropic 从 `resp.content[i].type=="tool_use"` 抓；OpenAI/Ollama 从 `resp.choices[0].message.tool_calls[i]`
- **Args 格式**：Anthropic `.input` 是 dict（自動 parse）；OpenAI/Ollama `.function.arguments` 是 JSON string，要 `json.loads(...)`

**成本**：1 次 ≈ $0.001。**Claude 的 tool-use 比 qwen2.5:3b 更稳**——复杂场景（5+ tools、模糊问题）gap 会明显。

</details>

### 练习 2：多工具选择
给 Claude 三个工具（搜索、计算机、行事历）跟一个任务。看 Claude 怎么挑工具，顺便注意它什么时候会挑错。

<details>
<summary>📋 <b>简化版核心观念 — Path A (Ollama)</b></summary>

**NEW vs 练习 1**：tools 从 1 个变 3 个。LLM 看 `description` 边界决定挑哪个——`description` 写得越像「给人读的 docstring」、越容易挑错。

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
# 预期：calculator, {"expression": "(19 * 42) - 8"}
```

**punchline**：3 个 tool 的 `description` 边界要互斥——`calendar` 写「行事历」太笼统、会跟 `web_search` 撞；写「特定日期事件」就清楚。小 model 对 description 质量比 Claude 更敏感。

**Path B (Anthropic) 改 3 行**：schema 拿掉 `{"type": "function", "function": {...}}` 外包、`tool_calls` 变 `[b for b in resp.content if b.type == "tool_use"]`、`tc.input` 已经是 dict 不用 `json.loads`。完整版见 folder。

</details>

→ **完整可跑版** → [`examples/stage-3/02-multi-tool-selection/`](../examples/stage-3/02-multi-tool-selection/)

### 练习 3：从零实现 ReAct（不用 framework）
用 50-80 行 Python 把 Thought → Action → Observation 循环写出来。不要 LangChain、不要 LangGraph，就是纯 `while not done: thought; action; observation; ...`。

<details>
<summary>📋 <b>简化版核心观念 — Path A (Ollama)、ReAct loop 的全部就在这 13 行</b></summary>

**NEW vs 练习 2**：把单次 call 包进循环、`messages` 一直长、看 `tool_calls` 在不在来决定收尾。

```python
# 假设 TOOLS + TOOL_IMPL（dict: name → callable）已经像练习 2 一样定义好
messages = [{"role": "user", "content": "台北人口除以纽约人口？"}]

for step in range(5):  # max_iter safety net
    r = client.chat.completions.create(model="qwen2.5:3b", tools=TOOLS, messages=messages)
    msg = r.choices[0].message
    # 把 assistant response 接回 messages（重要！下轮 LLM 才看得到自己上轮讲什么）
    messages.append({"role": "assistant", "content": msg.content, "tool_calls": msg.tool_calls})
    if not msg.tool_calls:
        print(f"✅ 收尾：{msg.content}"); break
    for tc in msg.tool_calls:
        args = json.loads(tc.function.arguments)
        obs = TOOL_IMPL[tc.function.name](args)  # 本地执行
        # observation 接回 messages（用 role="tool"、配 tool_call_id）
        messages.append({"role": "tool", "tool_call_id": tc.id, "content": obs})
```

**3 个容易踩坑**：
1. **忘记把 assistant response 加回 messages**——下轮 LLM 看不到自己上轮讲什么、会 loop forever
2. **`tool` message 没带 `tool_call_id`**——LLM 无法配对哪个 result 对应哪个 call
3. **没 `max_iter`**——tool 结果写不好时、LLM 会无限调用，safety net 必须设

**Path B (Anthropic) 差几行**：循环架构一模一样、`msg.tool_calls` 变 `[b for b in resp.content if b.type == "tool_use"]`、用 `stop_reason == "end_turn"` 判停、tool result 包成 `{"type": "tool_result", "tool_use_id": ..., "content": obs}` 放进 user message。完整版见 folder。

</details>

→ **完整可跑版** → [`examples/stage-3/03-react-from-scratch/`](../examples/stage-3/03-react-from-scratch/)（含 mock-based test.py、不花 API 钱也能验）

### 练习 4：多步骤推理任务
一个需要连续调用 3-5 次 tool 的任务。例如：「找出台北人口，除以纽约人口，再把比例换成百分比。」每一步用不同的工具。

<details>
<summary>📋 <b>简化版核心观念 — 跟练习 3 同一个 loop、跑久一点而已</b></summary>

**NEW vs 练习 3**：**完全同一个 loop**——只是 `TOOLS` 换成 4 个（`lookup_population` / `divide` / `to_percentage` / `round_int`）、题目自然走完 4 轮 tool call 才收尾。

```python
# 没有新 code、纯粹是 TOOLS / TOOL_IMPL 换内容
TOOL_IMPL = {
    "lookup_population": lambda i: lookup_population(i["city"]),
    "divide":            lambda i: divide(i["a"], i["b"]),
    "to_percentage":     lambda i: to_percentage(i["ratio"]),
    "round_int":         lambda i: round_int(i["x"]),
}
# loop 完全照 练习 3，只是 max_iter 拉大到 8
```

**punchline**：多步推理不是新 pattern、是**让 ReAct loop 跑久一点**。**真正的挑战是「LLM 会不会中间漏一步」**——qwen2.5:3b 可能漏「转百分比」、Claude haiku 较稳。**这恰好是观察「model 规模 vs 多步稳定度」的好实验**。试试 `MODEL=qwen2.5:7b python starter.py` 对照。

</details>

→ **完整可跑版** → [`examples/stage-3/04-multi-step-reasoning/`](../examples/stage-3/04-multi-step-reasoning/)

### 练习 5：错误处理
让某个工具失败（网络错误、输入无效）。看看 agent 会怎么处理错误、能不能恢复，再加上 retry 机制。

<details>
<summary>📋 <b>简化版核心观念 — tool error 是 data、不是 exception</b></summary>

**NEW vs 练习 4**：tool error 回传**结构化 dict**、不要 `raise`。loop 把 dict 接回 LLM、模型自己决定 retry / 改 query / 放弃。

```python
def fetch_weather(city: str) -> dict:
    if network_failed():
        return {"error": "network timeout", "retry_hint": "try again in 1s"}
    return {"city": city, "forecast": "rain", "temperature_c": 24}

# loop 里：
obs = fetch_weather(args["city"])
messages.append({"role": "tool", "tool_call_id": tc.id,
                 "content": json.dumps(obs, ensure_ascii=False)})  # error dict 也是 string 化接回去
# 下一轮 LLM 看到 retry_hint、可能会 retry、可能会放弃、可能会改 query
```

**为什么不 `raise`**：`raise` 直接中断 loop、LLM 没机会 recover。**Production 的 retry 不在 Python 层、而在 LLM 层**——这个 mental flip 是 Stage 3 练习 5 的核心。

**Bad vs Good error 回传**：

| Bad | Good |
|---|---|
| `raise Exception("failed")` | `return {"error": "network timeout", "retry_hint": "try again in 1s"}` |
| `return "failed"` | `return {"error": "...", "category": "transient", "retry_hint": "..."}` |
| 无限 retry | `max_iter` safety + 业务层 retry quota |

**小 model 观察**：qwen2.5:3b 对 `retry_hint` follow-up 较弱、可能直接放弃；Claude haiku 较稳。完整版（含连续失败 graceful end 范例）见 folder。

</details>

→ **完整可跑版** → [`examples/stage-3/05-error-handling/`](../examples/stage-3/05-error-handling/)

### 练习 6：Function schema 设计（坏 schema 修到好）
**先给 LLM 一份故意写烂的 schema**——`description` 模糊（「处理数据」）、参数全用 `type: string`、没分 required / optional、enum 该用没用。观察 LLM 怎么选错 tool、传错参数。然后逐项修：
- description 写到 LLM 一眼就懂这个 tool 适用情境（不是写给人读的 docstring）
- parameters 用对 type（number / boolean / enum / array），required 列清楚
- 模糊边界用 enum 强制收敛（例如 `unit: "celsius" | "fahrenheit"` 而不是 `unit: string`）
- error 回传要包 `{"error": "...", "retry_hint": "..."}` 让 LLM 能恢复

> 💡 详细 cheatsheet 看 [`resources/schema-design-cheatsheet.zh-Hans.md`](../resources/schema-design-cheatsheet.zh-Hans.md)——5 条黄金规则 + 5 个常见 anti-pattern。

<details>
<summary>📋 <b>简化版核心观念 — bad vs good schema 对照</b></summary>

**NEW vs 练习 5**：同一个工具（温度转换）、两种 schema 写法。看 4 个差别。

```python
# ❌ BAD — qwen2.5:3b 几乎必错（Claude haiku 还能猜对、但机率明显下降）
{"name": "convert", "description": "Convert a value.",
 "parameters": {"type": "object", "properties": {
     "value": {"type": "string"}, "unit": {"type": "string"}}}}

# ✅ GOOD — qwen 也能稳定挑对
{"name": "convert_temperature",
 "description": "Use when user asks to convert temperatures between Fahrenheit and Celsius.",
 "parameters": {"type": "object", "properties": {
     "value": {"type": "number", "description": "Temperature value"},
     "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]}},
     "required": ["value", "unit"]}}
```

**4 个改进**：(1) `name` 改具体、(2) `description` 写「**何时**用」而非「**做什么**」、(3) `type` 改 `number`、(4) 加 `required` + `enum`。

**punchline**：**写 schema 的功夫能省下换大 model 的成本**——小 model 对 schema 质量比大 model 敏感，相同 bad schema 在 Claude 上可能还能猜对、在 qwen 上几乎必错。Production 想用便宜 model？schema 必须写到 production-grade。

**搞不定 schema 怎么办**：装 [`examples/stage-5/tool-calling-tutor/`](../examples/stage-5/tool-calling-tutor/) skill，遇到「LLM 不调用我的 tool」、「我这 schema 哪里写坏」会自动跳出来帮你 debug。

</details>

→ **完整可跑版** → [`examples/stage-3/06-schema-design/`](../examples/stage-3/06-schema-design/)（含 bad schema vs good schema 两个版本对照）

## 🎯 精选 Projects

### [Anthropic — Tool Use Cookbook](https://github.com/anthropics/anthropic-cookbook/tree/main/tool_use)

| 字段 | 内容 |
|---|---|
| 语言 | Python |
| License | MIT |
| 推荐度 | ⭐⭐⭐⭐⭐ |

**教什么**：Claude 支持的所有 tool use 模式 — 单工具、多工具、并行调用、结构化输出抽取。

**适合谁**：练习 1 跟 练习 2，从这里开始。

**怎么跑**：
```bash
git clone https://github.com/anthropics/anthropic-cookbook
cd anthropic-cookbook/tool_use
jupyter notebook customer_service_agent.ipynb
```

---

### [Anthropic — Quickstarts](https://github.com/anthropics/anthropic-quickstarts)

| 字段 | 内容 |
|---|---|
| 语言 | Python / TypeScript |
| Stars | ★ 16k+ |
| License | MIT |
| 推荐度 | ⭐⭐⭐⭐⭐ |

**教什么**：Anthropic 官方的 动手练习 起手包。三个可直接 deploy 的 agent 范本：`financial-data-analyst`（数据分析 agent）、`customer-support-agent`（客服 agent）、`computer-use-demo`（让 Claude 操作屏幕）。

**适合谁**：跑完 练习 1 / 练习 2 之后，想看「真的应用会长什么样子」的官方参考。比社群实现更 canonical，部署设置也比较完整。

**备注**：每个范本都是独立 sub-folder，挑一个有兴趣的跑就好。Computer use demo 特别值得看 — 是少数示范 agent 操作 GUI 的官方范例。

---

### [pguso/ai-agents-from-scratch](https://github.com/pguso/ai-agents-from-scratch)

| 字段 | 内容 |
|---|---|
| 语言 | Python |
| License | MIT |
| 推荐度 | ⭐⭐⭐⭐⭐ |

**教什么**：用本地 LLM 从零打造 agent，零 framework。ReAct、function calling、memory，全部自己写。设计目的就是把 framework 帮你藏起来的东西摊开给你看。

**适合谁**：练习 3（从零写 ReAct）。这是最干净的「不靠 framework」参考实现。

**备注**：用本地 Ollama，不用花 API 钱。README 值得仔细读，章节结构安排得很好。

---

### [arunpshankar/react-from-scratch](https://github.com/arunpshankar/react-from-scratch)

| 字段 | 内容 |
|---|---|
| 语言 | Python |
| License | Apache-2.0 |
| 最后更新 | ⚠️ 2025 年 5 月（更新放缓） |
| 推荐度 | ⭐⭐⭐⭐ |

**教什么**：ReAct pattern 的多种变体与实现，针对 Gemini 最佳化。

**适合谁**：练习 3 的替代方案，如果你偏好 Gemini。涵盖 ReAct + Reflection + Self-consistency 等变体。

---

### [mattambrogi/agent-implementation](https://github.com/mattambrogi/agent-implementation)

| 字段 | 内容 |
|---|---|
| 语言 | Python |
| License | MIT |
| 最后更新 | ⚠️ 已停滞（2024 年 1 月）— 留作教学玩具参考 |
| 推荐度 | ⭐⭐⭐ |

**教什么**：最精简的 ReAct agent 实现。为了学习而砍到只剩约 150 行代码。

**适合谁**：逐行读代码。练习 3 卡住时可以拿来对照。

---

### [lsdefine/GenericAgent](https://github.com/lsdefine/GenericAgent)

| 字段 | 内容 |
|---|---|
| 语言 | 中文 + Python |
| Stars | ★ 9k+ |
| License | MIT |
| 推荐度 | ⭐⭐⭐⭐ |

**教什么**：最精简的自我演化 agent framework — 核心约 3K 行代码，agent 从 seed 自己长出技能树。支持 Claude / Gemini / Kimi / MiniMax。仍在持续开发。

**适合谁**：练习 3 / 练习 4 的替代方案，给想看「精简但完整」framework 的读者。介于 mattambrogi 的玩具版跟完整 LangGraph 之间。

---

### [HelloAgents (jjyaoao)](https://github.com/jjyaoao/HelloAgents) — `learn_version` 分支

| 字段 | 内容 |
|---|---|
| 语言 | 中文（zh-Hans）+ Python |
| License | CC BY-NC-SA 4.0 |
| 推荐度 | ⭐⭐⭐⭐⭐（中文读者） |

**教什么**：教学导向的多 agent 练习框架，章节式教学，搭配 [Datawhale 的 Hello-Agents 教学](https://github.com/datawhalechina/hello-agents)。涵盖 16 种能力（tool response、context engineering、session 持久化、sub-agents、circuit breaker、observability 等），用来学 production pattern 的教材，不是直接拿来上 production 的成品。

**适合谁**：中文读者。**请切到 `learn_version` 分支**，那才是对齐教材的版本。

**备注**：License 是 CC BY-NC-SA — 非商用。教材是 zh-Hans，但技术内容对 zh-TW 读者没障碍。

**怎么跑**：
```bash
pip install hello-agents
git clone -b learn_version https://github.com/jjyaoao/HelloAgents
```

---

### [datawhalechina/hello-agents](https://github.com/datawhalechina/hello-agents)

| 字段 | 内容 |
|---|---|
| 语言 | 中文（zh-Hans） |
| License | CC BY-NC-SA |
| 推荐度 | ⭐⭐⭐⭐⭐（中文读者） |

**教什么**：HelloAgents 的搭配教学。多章导读，从「什么是 agent」一路讲到 production 的实务 pattern。

**适合谁**：想要结构化教学加代码的中文读者。

**备注**：请搭配上面 HelloAgents repo 的 `learn_version` 分支一起看。

---

### [QuantaLogic/quantalogic](https://github.com/quantalogic/quantalogic)

| 字段 | 内容 |
|---|---|
| 语言 | Python |
| License | Apache-2.0 |
| 推荐度 | ⭐⭐⭐ |

**教什么**：产生 Python 代码（而不是 JSON tool call）的 ReAct agent。设计选择不同 — agent 直接写代码当作 action。

**适合谁**：跑完 练习 3 之后。比较 CodeAct（代码即 action）与 JSON tool call 的差别。

---

### [HuggingFace Smolagents](https://github.com/huggingface/smolagents)

| 字段 | 内容 |
|---|---|
| 语言 | Python |
| Stars | ★ 27k+ |
| License | Apache 2.0 |
| 推荐度 | ⭐⭐⭐⭐ |

**教什么**：Smol agents（≤1000 LOC）。会写代码的 agent — 执行 Python 而不是 JSON tool call。

**适合谁**：练习 5 的替代方案。特别适合本地 LLM 实验。

**备注**：HF 的立场：agent 应该要小。他们的 code-action 路线跟 JSON-tool 路线在思路上很不一样，值得对照来看。

---

### [LangChain — ReAct Agent Template](https://github.com/langchain-ai/react-agent)

| 字段 | 内容 |
|---|---|
| 语言 | Python |
| License | MIT |
| 推荐度 | ⭐⭐⭐ |

**教什么**：framework 怎么把 ReAct pattern 抽象化。LangGraph Studio 的范本。

**适合谁**：练习 3 之后（先自己从零写过再来）。再来比较 framework 帮你做了哪些事。

---

### [Anthropic — Building Effective Agents（部落格文章）](https://www.anthropic.com/engineering/building-effective-agents)

| 字段 | 内容 |
|---|---|
| 形式 | 文章 |
| 推荐度 | ⭐⭐⭐⭐⭐ |

**教什么**：Anthropic 自己写的指南 — 什么时候该用 agent（vs. workflow）、常见 pattern、容易踩的坑。Stage 4 之前必读。

**适合谁**：建立观念框架。练习 3 写完之后、学 framework 之前读。

---

## ✅ 进 Stage 4 前的自我检查

你能不能：
- [ ] 定义一个 tool schema（name + description + JSON schema 输入/输出）
- [ ] 用不到 100 行 Python、不靠任何 framework，把 ReAct 循环写出来
- [ ] 解释为什么 agent 需要一个「我做完了」的退出条件
- [ ] 比较 CodeAct（代码即 action）跟 JSON-tool 两种路线
- [ ] 看出哪些问题其实不需要 agent

如果可以 → 进 [Stage 4 — Agent Frameworks](04-agent-frameworks.zh-Hans.md)。

如果不行 → 把 练习 3 再跑一次，不要跳过。如果你不懂 framework 在帮你抽象什么，Stage 4 的那些东西看起来会像黑魔法。
