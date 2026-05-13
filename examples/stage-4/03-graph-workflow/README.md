> **繁體中文** | [简体中文](./README.zh-Hans.md) | [English](./README.en.md)

# 練習 3：圖式 workflow（LangGraph 條件分支 + HITL）

對應 [Stage 4 — Agent Frameworks](../../../stages/04-agent-frameworks.md) 練習 3。
> 🎓 **學習模式**：這份 `starter.py` 是**完整解答**、不是 TODO skeleton。建議用**主動模式**——`mv starter.py starter_reference.py`、看 signature 不看 body、自己重寫一份 `starter.py`、跑 `python test.py` 驗證；卡 20 分鐘再回去對照 reference。完整方法論看 [`docs/HOW_TO_USE.md`](../../../docs/HOW_TO_USE.md)。

> 📚 **想要 chapter-length 深入版？** 本 folder 的 starter 是 illustrative 版、聚焦核心 pattern + 兩條 SDK path，不是 production-grade tutorial。深度教材推薦：
> - [`datawhalechina/hello-agents`](https://github.com/datawhalechina/hello-agents) ⭐ 中文圈最完整、章節式 + 16 種 production 能力。**本練習對應 hello-agents 的 graph workflow + HITL 章節**
> - [LangGraph HITL tutorial](https://langchain-ai.github.io/langgraph/tutorials/human-in-the-loop/) + [LangGraph time-travel docs](https://langchain-ai.github.io/langgraph/concepts/time-travel/)
> - 完整 references 見 [Stage 4 § 精選 Projects](../../../stages/04-agent-frameworks.md#-精選-projects)


## 任務

`classify → [search?] → respond → [HITL] → final`

- **`classify_node`**：看 query 決定 `needs_search`
- **條件分支**：`needs_search=True` 走 `search` node、否則直接 `respond`
- **HITL checkpoint**：`respond_node` 後 interrupt、等人類在 state 改 `approved`
- **`final_node`**：`approved=True` → PUBLISHED、否則 REJECTED

這題 **LangGraph 最拿手**：graph state + checkpointing + interrupt_before 是 LangGraph 招牌組合。CrewAI 對 HITL 支援較弱。

## 怎麼跑

```bash
pip install -r requirements.txt
python starter.py
```

預算：**$0**。這份 demo 的節點都是 deterministic 邏輯、不打 LLM；要實接 Claude / Ollama 在 `respond_node` 改成 `llm.invoke(...)` 即可。

```bash
python test.py             # 6 個 test，驗 routing + HITL 邏輯
python test_anthropic.py   # Path B concept demo
```

## LangGraph 圖結構（精簡）

```python
g = StateGraph(State)
g.add_node("classify", classify_node)
g.add_node("search", search_node)
g.add_node("respond", respond_node)
g.add_node("final", final_node)

g.add_edge(START, "classify")
g.add_conditional_edges("classify", should_search, {"search": "search", "respond": "respond"})
g.add_edge("search", "respond")
g.add_edge("respond", "final")
g.add_edge("final", END)

graph = g.compile(checkpointer=InMemorySaver(), interrupt_before=["final"])
```

## HITL 怎麼運作

```python
# 第一段：跑到 final 之前自動停（因為 interrupt_before=["final"]）
state_before = graph.invoke({"query": ...}, config={"configurable": {"thread_id": "demo"}})
# 此時可以印 state_before["draft"]、問人類「要 publish 嗎？」

# 人類決定：把 approved 寫進 state
graph.update_state(config, {"approved": True})

# 第二段：繼續從 final 跑（None 表示「不給新 input、用 checkpoint」）
state_after = graph.invoke(None, config=config)
```

**關鍵**：`interrupt_before=["final"]` 告訴 graph「跑到 final 之前停」。Production 把它接到 webhook / Slack / 前端 button、等使用者按 approve 才繼續。

## 為什麼這個 pattern 重要

| 情境 | 不用 HITL | 用 HITL |
|---|---|---|
| Agent 發 email | 直接送出（風險） | 顯示草稿、人類按 approve |
| Agent 改 production 設定 | 直接套用 | dry-run 後等核准 |
| Agent 做退款 | 自動退 | 超過 $X 等審核 |

**Production agent 凡是有 side effect 的、都該加 HITL**。LangGraph `interrupt_before` 就是為這個設計。

## 兩個 path 觀察重點

本練習節點都是 deterministic 邏輯、不打 LLM、所以 Path A / Path B 跑出來一致。**重點是學圖結構本身**。要實接 LLM：

```python
# 在 respond_node 改：
from langchain_openai import ChatOpenAI  # Path A
# from langchain_anthropic import ChatAnthropic  # Path B
llm = ChatOpenAI(base_url="http://localhost:11434/v1", api_key="ollama", model="qwen2.5:3b")
draft = llm.invoke(state["query"]).content
return {"draft": draft}
```

## 常見坑

- **`checkpointer` 沒設**：`graph.compile(interrupt_before=[...])` 沒帶 checkpointer 會 raise。必須有 checkpointer 才能 pause/resume
- **`thread_id` 不一致**：第一段 invoke + update_state + 第二段 invoke 必須用同一個 `config={"configurable": {"thread_id": "..."}}`、否則 checkpoint 找不到
- **`interrupt_before` vs `interrupt_after`**：before = 進這個 node 前停、after = 跑完這個 node 停。**HITL 通常用 before**（讓人類看完整 state 再決定）
- **conditional_edges 函數要回 string**：`should_search` return value 必須是 `add_conditional_edges` 第三個參數 dict 的 key、不能 return literal value 直接當 node name

## 想看更聰明的答案？

把 `respond_node` 接 LLM、用真的 model 寫 draft（不再用 template）。Production setup 還會把 checkpointer 換成 SQLite / Redis（`SqliteSaver` / `RedisSaver`）做持久化。

## 延伸

- **加 retry**：在 `search_node` 失敗時 retry、用 LangGraph 的 `error` edge
- **加多個 HITL**：`interrupt_before=["draft", "publish"]` 兩個地方都暫停
- **time-travel debug**：`graph.get_state_history(config)` 拿到所有 checkpoint、可以回到任一步 fork 新 thread
- **加 streaming**：`for state in graph.stream(...)` 邊跑邊看 state
