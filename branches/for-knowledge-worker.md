# 給知識工作者 — 專業分支

> **繁體中文** | [简体中文](./for-knowledge-worker.zh-Hans.md) | [English](./for-knowledge-worker.en.md) | [Русский](./for-knowledge-worker.ru.md)

> 🚀 **完全沒開發背景？** 先看 [`resources/setup-guide.md` §A-D](../resources/setup-guide.md)（30-45 分鐘從零）。本分支後面提到的「Claude Code」「MCP」「Skills」都會用到 §D 那個 setup。

> [← 回主路線 README](../README.md) · 走完 **Track A 的 A3** 或 **Track B 的 Stage 7** 後從這裡接續。把 agentic AI 應用到辦公室 / 知識工作上。

## 使用情境

- Email 分流與草擬回信
- 會議筆記 → 行動項目
- 多來源報告整合
- 研究 / 市場情報蒐集
- 決策輔助流程

## 精選 Projects

> 💡 **想把 AI agent 接到 Notion / Gmail / Outlook / Slack / Excel / 飛書？** 62 個常用 MCP server / Skill 整合在 [`resources/mcp-skills-catalog.md`](../resources/mcp-skills-catalog.md)（按使用情境分類）。下面這節保留 workflow / 整合平台級的工具。

### 工作流工具

#### [n8n](https://github.com/n8n-io/n8n) ⭐⭐⭐⭐
可自架的工作流自動化平台，內建 AI 整合，採用視覺化節點式編輯器。

**適合誰**：要把多個 SaaS 工具串起來時（Slack + Gmail + Notion + AI）。

---

#### [Make.com](https://www.make.com/)（前身為 Integromat）
雲端代管的工作流自動化平台，AI 整合節點功能完整。

---

### 知識工作者 Skills

#### [obra/superpowers](https://github.com/obra/superpowers) ⭐⭐⭐⭐

腦力激盪、規劃、決策類的 skill。

---

### 知識管理 / 個人 AI

#### [khoj-ai/khoj](https://github.com/khoj-ai/khoj) ⭐⭐⭐⭐

| 欄位 | 內容 |
|---|---|
| Stars | ★ 34k+ |
| License | AGPL-3.0 |

**教什麼**：自架的「第二大腦」——可以跟 web + 本地文件對話、排程自動化、自訂 agent。

**適合誰**：想自架個人知識庫 + AI assistant 的人。

**備註**：AGPL-3.0 license（傳染性開源）。

---

#### [lobehub/lobe-chat](https://github.com/lobehub/lobe-chat) ⭐⭐⭐⭐⭐

| 欄位 | 內容 |
|---|---|
| Stars | ★ 76k+ |
| License | LobeHub Community License（基於 Apache-2.0 + 商用附加條款） |

**教什麼**：可部署的多 agent 聊天平台——含 plugin marketplace、知識庫、團隊協作。可自架的 AI workspace 代表選項之一。

**適合誰**：要找可自架的協作 chat workspace。

**備註**：商用使用需確認 LobeHub Community License 的附加條款。

---

#### [langflow-ai/langflow](https://github.com/langflow-ai/langflow) ⭐⭐⭐⭐

| 欄位 | 內容 |
|---|---|
| Stars | ★ 147k+ |
| License | MIT |

**教什麼**：視覺化 AI agent 開發平台——拖拉節點設計 agent flow，內建 API + MCP server 部署。比 n8n 更專注在 agent 設計（n8n 是泛用工作流）。

**適合誰**：寧可拉節點不寫 Python 的知識工作者，或要設計 agent 跟團隊溝通流程的人。

---

#### [Mintplex-Labs/anything-llm](https://github.com/Mintplex-Labs/anything-llm) ⭐⭐⭐⭐⭐

| 欄位 | 內容 |
|---|---|
| Stars | ★ 60k+ |
| License | MIT |

**教什麼**：all-in-one 的私有 RAG 工作平台——上傳文件、建 agent、相容 MCP、預設 on-device。**NotebookLM 的私有 self-hosted 替代方案**。

**適合誰**：知識工作者要私有部署、類 NotebookLM 的工具，避免把資料送到雲端。

---

### 對知識工作者有用的 MCP Server

#### 通訊類 MCP server ⭐⭐⭐⭐
Slack / Gmail / Discord 等。Anthropic 原本維護的 reference server 已於 2025 年重整；目前由社群維護的 server 集中在 [**punkpeye/awesome-mcp-servers**](https://github.com/punkpeye/awesome-mcp-servers#communication) 跟 [**wong2/awesome-mcp-servers**](https://github.com/wong2/awesome-mcp-servers)，要找最新的 Slack / Gmail / Drive / Calendar MCP server 可以從這兩個清單翻找。

---

## 可以建的流程

- **每日 email 分流**：掃 inbox → 分類 → 草擬回信讓你 review → 標已讀
- **會議 → 行動項目**：逐字稿 → 主要決策 + 行動項目 → 指派 + 公告
- **每週報告整合**：從 N 個工具拉指標 → 整理 → email summary
- **研究 / 市場情報**：問題 → 多來源搜尋 → 交叉驗證 → 備忘錄

## 層級建議

大多數知識工作者應該從 **Tier 0**（Claude.ai 網頁版）開始，當你有需要對本機 / 雲端檔案重複跑的流程時，再升級到 **Tier 1**（Claude Desktop 加 MCP）。

**Tier 3+（CLI / SDK）對大多數知識工作者任務來說太重。** 不要被別人慫恿過去。

## 閱讀

- [How I Turned Claude Code Into My Personal AI Agent OS](https://aimaker.substack.com/p/how-i-turned-claude-code-into-personal-ai-agent-operating-system-for-writing-research-complete-guide) — 知識工作者個案研究
