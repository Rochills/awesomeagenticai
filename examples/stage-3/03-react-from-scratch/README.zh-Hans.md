> [繁體中文](./README.md) | **简体中文** | [English](./README.en.md)

# 练习 3：从零实现 ReAct（不用 framework）

对应 [Stage 3 — Tool Use & Agent 入门](../../../stages/03-tool-use-and-hello-agent.zh-Hans.md) 练习 3。

## 为什么从零写

ReAct（Reasoning + Acting）是现代 agent 的基础 pattern：

```
while not done:
    thought    = LLM 看完目前 context、讲出下一步要做什么
    action     = LLM 调用一个 tool
    observation = tool 执行结果、喂回去给 LLM
```

LangGraph / CrewAI 把这个 loop 藏起来了。你**自己写过一次**才知道：
- 为什么 messages array 一直长
- tool_use_id 跟 tool_result 怎么配对
- stop_reason 为什么是 `tool_use` 或 `end_turn`
- max_iter 为什么是 safety net

70 行 Python 全交代清楚。

## 怎么跑

```bash
pip install -r requirements.txt
export ANTHROPIC_API_KEY=sk-ant-...
python starter.py
```

预期看到：

```
❓ 问题：台北人口除以纽约人口、答案保留 4 位小数。
------------------------------------------------------------
[step 0] thought: 我先查台北人口...
           tool: lookup_fact({'query': '台北人口'}) → 2602000
[step 1] thought: 接着查纽约人口...
           tool: lookup_fact({'query': '纽约人口'}) → 8336000
[step 2] thought: 计算比例...
           tool: calculator({'expression': '2602000 / 8336000'}) → 0.3121...
[step 3] thought: 答案是 0.3122
------------------------------------------------------------
✅ 最终答案：台北人口除以纽约人口约 0.3122
   共 4 轮
✅ 练习 3 通过 — ReAct loop 自己连用了 lookup_fact 跟 calculator
```

## 不花钱验证程式逻辑

```bash
python test.py
```

`test.py` 用 `unittest.mock.MagicMock` 取代 Anthropic client、塞固定 response、验证你的 loop 逻辑。预期：

```
✅ test_calculator_basic
✅ test_calculator_rejects_eval_injection
✅ test_lookup_fact
✅ test_react_loop_single_tool_call
✅ test_react_loop_multi_step
✅ test_react_loop_respects_max_iter

🎉 全部通过 — 你的 ReAct loop 逻辑正确
```

## 程式结构走查

| 段 | 行 | 在做什么 |
|---|---|---|
| `tool_calculator` | ~30-40 | 安全的计算器（whitelist 过滤、避免 `eval` 漏洞） |
| `tool_lookup_fact` | ~42-50 | 假事实库（教学用、避免依赖外部 API） |
| `TOOLS_SPEC` | ~52-75 | tool schema 给 LLM 看 |
| `TOOL_IMPL` | ~77-80 | name → callable 对应表（dispatch） |
| `react_loop` | ~85-130 | 主循环、含 max_iter safety、`messages` 累积、tool result 接回去 |

## 常见坑

1. **忘记把 assistant response 加进 messages**：下一轮 LLM 就看不到自己上一轮讲过什么、会 loop forever
2. **tool_result 没带 `tool_use_id`**：LLM 无法配对哪个 result 对应哪个 call
3. **`while True` 没 max_iter**：tool 结果写得不好、LLM 会无限调用；safety net 一定要设
4. **eval 没过滤**：calculator 直接 `eval(user_input)` = RCE 漏洞；用 whitelist 或 `ast.literal_eval`

## 想看更聪明的答案？

预设用 `claude-haiku-4-5`（最便宜）。改成 sonnet：

```bash
MODEL=claude-sonnet-4-5 python starter.py
```

或在 `starter.py` 改 `MODEL = ...` 那行。

## 延伸

- **加更多 tool**：在 `TOOLS_SPEC` + `TOOL_IMPL` 补一个 entry 即可
- **加 streaming**：把 `client.messages.create(...)` 换成 `with client.messages.stream(...) as s:`、边跑边印
- **加 prompt cache**：在 `system=` 或 `tools=` 带 `cache_control={"type":"ephemeral"}` 重复 call 省 90% token
- **接 [LangGraph](https://langchain-ai.github.io/langgraph/) 或 [Pydantic AI](https://ai.pydantic.dev/) 看 framework 怎么帮你藏掉这 70 行**
