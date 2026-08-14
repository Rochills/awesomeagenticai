> [繁體中文](./courses.md) | **简体中文** | [English](./courses.en.md)

# 线上 AI Agent 课程（带证书对照）

> [← 回主路线 README](../README.zh-Hans.md)

> 📌 **这份是 reference catalog，不是排名。** 本 repo 是动手做的学习路线，**不取代**结构化线上课程——下面这些课程可当作平行的视频／互动式入门对照。想动手做 → 回 [stages](../README.zh-Hans.md)；想先查用语 → [`resources/glossary.zh-Hans.md`](glossary.zh-Hans.md)。本页只收**会发证书**的课程。

> ⚠️ **先读这段，再往下看。** 完成证书（Certificate of Completion）证明的是**你参与并完成了课程**，不是 mastery，也**不等于** accredited 学历或学分。雇主看的顺序通常是“内容跟职务相不相关 > 评量严不严 > 你做出什么作品 > 机构背书”，证书本身排在后面。把它当成**自主学习的证据 + 维持动机的结构**，不是“拿了证书就能找到工作”。下面“证书”栏只陈述事实，不做价值判断。

---

## ⚡ 快速选（30 秒挑一门）

- **完全没方向** → 先做 [Hugging Face — AI Agents Course](https://huggingface.co/learn/agents-course)：🆓 免费、框架中立、证书要过 quiz + 作业才拿得到。本页最推荐的起点。
- **想免费就拿证书** → Hugging Face、[Weights & Biases — AI Engineering: Agents](https://wandb.ai/site/courses/agents/)、[Anthropic Academy](https://anthropic.skilljar.com/)（Claude / MCP 方向）。
- **想要履历用的大学／大厂背书（付费）** → [IBM — RAG and Agentic AI（Professional Certificate）](https://www.coursera.org/professional-certificates/ibm-rag-and-agentic-ai)、[Vanderbilt — AI Agent Developer](https://www.coursera.org/specializations/ai-agents)。
- **想沿一个框架（LangChain / LangGraph）做到底** → [Coursera — Agentic AI Engineering（Edureka）](https://www.coursera.org/specializations/agentic-ai-engineering)。
- **想用中文** → [NVIDIA DLI 中文](https://www.nvidia.cn/training/instructor-led-workshops/building-agentic-ai-applications-with-llms/)（最贴题）、阿里云 ACA、华为 HCIA-AI。
  > ⚠️ **中文、带证书、又 agent 专门的课，目前基本都要付费**（NVIDIA DLI / 阿里 / 华为）。想**免费**拿证书，现阶段得走上面的英文课（部分有社群字幕）。

**图例**：🆓 免费（含证书）· 💰 付费 · 🆓→💰 旁听免费、证书付费。

---

## 怎么读这份清单

- **学习价值**（讲师可信 + 动手做 + 内容够新）和**证书价值**是两条不同的轴。本清单主要照学习价值排，证书当成大量加注的次要信号。
- ⭐ 星等照 [style-guide §2](style-guide.zh-Hans.md#2-推荐星等定义)：⭐⭐⭐⭐⭐ 必做 … ⭐ 利基。
- **付费 Professional Certificate / Specialization（IBM、大学）认可度，通常高于免费完成证书**；但两者都不是学位，Coursera 那种“X% career outcomes”是行销数字。
- **Agent 领域变化快**：超过 12–18 个月的课，对框架版本（smolagents / LangGraph / MCP）要打 recency 折扣。

---

## 🌍 英文课程

### tier-1（高度可信 + 动手做 + 够新）

| 课程（连结） | 成本 | 适合谁 | 教什么 | 证书 |
|---|---|---|---|---|
| [Hugging Face — AI Agents Course](https://huggingface.co/learn/agents-course) ⭐⭐⭐⭐⭐ | 🆓 | 想用免费、框架中立教材动手做的人 | smolagents / LangGraph / LlamaIndex 三家动手 + observability / eval；建并 benchmark 一个 agent | 免费，两级：Fundamentals（Unit 1 + quiz ≥80%）；Certificate of Completion（再加作业 + 最终挑战）。HF 直接签发 |
| [DeepLearning.AI — Agentic AI](https://www.deeplearning.ai/courses/agentic-ai/) ⭐⭐⭐⭐⭐ | 🆓→💰 | 有中阶 Python + 基本 LLM/API 概念的开发者 | 四个核心设计模式：reflection、tool use、planning、multi-agent（31 视频 + 8 评量作业） | 旁听免费（无证书）；证书需付费 Pro（约 $25–30/月）并完成评量。讲师 Andrew Ng。中文对照：[`datawhalechina/agentic-ai`](https://github.com/datawhalechina/agentic-ai) |
| [Weights & Biases — AI Engineering: Agents](https://wandb.ai/site/courses/agents/) ⭐⭐⭐⭐ | 🆓 | 想学“会评估、可上线”agent 的开发者 | 与 OpenAI 团队合作；reasoning model 建 agent、tool/memory/planning、orchestrator-worker 多 agent、用 accuracy/latency/cost 做可复现 eval（约 2 小时） | 免费完成证书（W&B AI Academy 签发） |
| [IBM — RAG and Agentic AI（Professional Certificate）](https://www.coursera.org/professional-certificates/ibm-rag-and-agentic-ai) ⭐⭐⭐⭐ | 💰 | 想要大厂 Professional Certificate 的人 | RAG + agentic AI 实作，多课程组成的 Professional Certificate | 付费（Coursera Plus；可申请助学金）。IBM 签发，认可度高于一般完成证书 |
| [Vanderbilt 大学 — AI Agent Developer](https://www.coursera.org/specializations/ai-agents) ⭐⭐⭐⭐ | 💰 | 想要大学背书、系统性学 agent 开发的人 | 设计、打造、调校 agent 软件；Python agentic 应用 | 付费（Coursera Plus；可申请助学金）。Vanderbilt 大学 Specialization Certificate |

### tier-2（扎实，但有特定 caveat）

| 课程（连结） | 成本 | 适合谁 | 教什么 | 证书 |
|---|---|---|---|---|
| [Coursera — Agentic AI Engineering（Edureka）](https://www.coursera.org/specializations/agentic-ai-engineering) ⭐⭐⭐ | 💰 | 想沿 LangChain / LangGraph / MCP 一路做完的人 | 4 课：LangChain 生态、LCEL、ReAct/memory、LangGraph 多 agent、MCP 部署、eval | 付费 Specialization Certificate。caveat：Edureka 是商业培训机构（非大学/lab），可信度中等；想要更高背书选上面 IBM / Vanderbilt |
| [Anthropic Academy](https://anthropic.skilljar.com/) ⭐⭐⭐⭐ | 🆓 | 在 Claude / MCP stack 上做 agent 的人 | Claude Code、Claude API、MCP、Agent Skills；17 门自学课、5 条学习轨 | 免费官方证书（Skilljar 签发，含 quiz，email 注册即可，可加 LinkedIn）。caveat：vendor-specific（Claude/MCP），补充而非取代框架中立的基础课 |

> 也想了解但未列为主 entry：[LangChain Academy — Intro to LangGraph](https://academy.langchain.com/courses/intro-to-langgraph)（🆓 免费 LangGraph 完成证书，single-vendor）。云厂商（Google Cloud / AWS）的 agentic 路线多半给 skill badge，跟它们各自的付费**专业认证考试**不是同一回事，别混为一谈。

---

## 🀄 中文课程

> **gap-first 事实**：会发证书、又 agent 专门的中文课**目前都要付费**，且多是**大厂 vendor 认证**（绑自家 stack）；**zh-TW 原生 + 带证书 + agent 专门的几乎不存在**。想免费拿证书，繁中／简中学习者现阶段通常还是走上面的英文课（Hugging Face / W&B / Anthropic 皆免费）。下面三门以 NVIDIA DLI 中文版最贴题。

### tier-1（高度可信）

| 课程（连结） | 成本 | 适合谁 | 教什么 | 证书 |
|---|---|---|---|---|
| [NVIDIA DLI — 使用大语言模型建构代理式 AI（中文）](https://www.nvidia.cn/training/instructor-led-workshops/building-agentic-ai-applications-with-llms/) ⭐⭐⭐⭐ | 💰 | 想用中文、跟着动手做 agent 系统的人 | 用 LLM 建 agentic 系统：deep reasoning、检索、tool 调用、多 agent、LangGraph、上线部署考量（8 小时） | 付费（约 ¥3500／人，讲师带领、排程制），含 6 个月云端 lab。完成测验后拿 NVIDIA DLI 证书。caveat：价格较高、需排课 |

### tier-2（扎实，但有特定 caveat）

| 课程（连结） | 成本 | 适合谁 | 教什么 | 证书 |
|---|---|---|---|---|
| [阿里云 — 大模型 ACA 认证 + 百炼智能体 Clouder](https://edu.aliyun.com/certification) ⭐⭐⭐ | 💰 | 在阿里云（百炼/通义）stack 上做 agent、想要圈内认可的人 | 大模型工程；Clouder 系列含“基于百炼平台构建智能体应用”模组 | 付费官方认证（需实名）。caveat：认可是 vendor-scoped（绑百炼/通义）、非学术可转移；zh-Hans 限定 |
| [华为 — HCIA-AI（大模型应用方向）](https://e.huawei.com/cn/talent/cert/) ⭐⭐⭐ | 💰 | 想要华为生态认可、系统性入门的人 | 2026 V1.0 大纲含人工智慧基础、大模型知识、大模型应用、智算中心方案 | 付费官方认证（考试制）。caveat：认可偏华为生态与大陆就业市场；zh-Hans。HCIP/HCIE 为更深延伸 |

> 其他中文选项以备注处理，不列为主 entry：慕课网“AI Agent 全栈开发工程师”（商业 bootcamp，judge by syllabus、外部认可有限）、教育部“人工智慧课程修读证书”（官方电子证书、偏综合素养非 agent 工程）。**不收** cert-mill（无评量、无可信签发方的泛 AIGC 认证）。

---

## ⚠️ 关于“拿证书”这件事——完整 caveat（请务必照实转述给读者）

1. **完成证书不是 accredited 学历。** 它代表参与和投入，不代表 mastery；跟学分课、学位是两回事。本清单**绝不**把这些证书讲成资格认证。
2. **付费 ≠ 一定被认可，免费 ≠ 一定没份量。** 大厂／大学的付费 Professional Certificate（IBM、Vanderbilt）认可度通常高些；但免费课也可能评量严格（Hugging Face 的证书 gate 在 quiz + 作业 + 挑战）。看的是签发方和评量，不是价格。
3. **这些证书实际证明 exposure 与 effort，不是 competence。** 诚实说法是“自主学习的证据”，不是“能打造可上线 agent 的证明”。
4. **证书最有用的场景是 screening，且很少单独起作用。** 来自可信来源的证书能帮你过初筛，但几乎不保证 offer，要搭作品集才有效。
5. **你做出的作品，比你拿到的证书更重要。** 雇主要的是你能做事的证据（GitHub repo、deploy 的 agent、开源贡献）。一门课真正的 payoff 是它逼你做出的 artifact，不是那张 PDF。
6. **别搜集零散 badge，要往一条连贯的 skill set 走。** 五张不相关的入门证书，远不如一条展示同一 skill set 的连贯路径可信——这也是把课程当“roadmap 的步骤”而非“奖杯墙”的理由。
7. **Recency caveat。** Agent 框架与最佳实务汰换很快，旧 cohort 的证书可能代表过时的知识。看课程的 vintage。

---

## 维护备注

- **最后核对：2026-05。** 课程资讯（尤其证书条件、免费／付费）漂移很快——以各课官网为准，stale 的可见地标注而非默默错误。
- 加新课的门槛：讲师／机构可辨识 + 真的有评量或第一方签发的证书 + 内容够新。**不收** cert-mill（marketplace 型完成证书外部认可近乎零）。
- 三语同步：每次增删／改星等／改证书条件，都要套到 `courses.md` + `courses.en.md` + `courses.zh-Hans.md`。
