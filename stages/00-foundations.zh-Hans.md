# Stage 0 — 基础准备

> [繁體中文](./00-foundations.md) | **简体中文** | [English](./00-foundations.en.md) | [Русский](./00-foundations.ru.md)

⏱ **时间估算**：1-2 周（约 5-15 小时，已具备可跳过）

> 💡 **看不懂某个词**？翻 [`resources/glossary.zh-Hans.md`](../resources/glossary.zh-Hans.md) 查 30 秒再回来。Stage 0 还不会碰太多 jargon，但接下来几 stage 会。

## 何时可以跳过这个阶段

如果你能：
- 写一个会呼叫公开 API 并解析 JSON 回应的 Python 函数
- 用 git 做 clone、commit、push，并处理基本的 merge 冲突
- 在自己的操作系统上使用命令行（cd、ls、mkdir、执行 script）
- 看懂 YAML / JSON 文件

→ **直接跳到 [Stage 1](01-llm-basics.zh-Hans.md)**。

如果做不到，就把这个阶段走完。不要跳——后面每个阶段都会预设你已经会这些。

## 📌 学习目标

- 写 Python：函数、类、async/await 基本用法
- 用 git：clone、branch、commit、push、基本冲突处理
- 用 REST API：发 GET/POST、解析 JSON、处理 auth header
- 读写 YAML 跟 JSON

## 🛠 动手练习

- **练习：Python** — 写一个 Python script 呼叫 https://api.github.com/users/torvalds 并印出 follower 数量
- **练习：git** — clone 任何一个公开 repo，做一次 commit，push 到自己的 fork
- **练习：CLI** — 用命令行建几个文件夹跟文件（macOS / Linux：`mkdir project && cd project && mkdir src tests docs`；Windows PowerShell：`New-Item -ItemType Directory -Path project,project\src,project	ests,project\docs`）、执行 Python script、把输出存到文件
- **练习：YAML** — 用 Python 读一个 `.yaml` 配置文件，改一个值，再写回去
- **练习：API auth** — 去 [github.com/settings/tokens](https://github.com/settings/tokens) 产生一个 personal access token（给最少权限：`read:user`），呼叫 `https://api.github.com/user` 需 auth 的 endpoint，看 401（无 token）vs 200（带 token）的差别。注意：production agent 一定会用到 API auth，所以这一题要做

## 🎯 精选资源（不是完整 Project，只是学习素材）

### Python
- [**Python Crash Course**](https://github.com/ehmatthes/pcc_3e) — 书 + 练习（书要付费，练习免费）
- [**Real Python tutorials**](https://realpython.com/) — 高品质免费文章
- [**Corey Schafer YouTube**](https://www.youtube.com/c/Coreyms) — 视频教学，从基础到进阶，讲解清楚
- [**Boot.dev**](https://www.boot.dev/) — 互动式 Python 课程（部分免费）
- [**runoob.com Python 教程**](https://www.runoob.com/python3/python3-tutorial.html) — 中文 Python 入门参考

### Git
- [**Pro Git book**](https://git-scm.com/book/en/v2) — 免费完整参考书
- [**Atlassian Git Tutorials**](https://www.atlassian.com/git/tutorials) — 以 workflow 为主
- [**Oh Shit, Git!?!**](https://ohshitgit.com/) — 出包时的救命手册
- [**git-flight-rules**](https://github.com/k88hudson/git-flight-rules) — “我搞砸了 X，怎么救？”高人气 cheat sheet

### CLI / Shell
- [**The Art of Command Line**](https://github.com/jlevy/the-art-of-command-line) — 涵盖从新手到进阶的命令行技巧（180k+ stars，多语言版）
- [**Learn Shell**](https://www.learnshell.org/) — 互动式 Bash 教学
- [**explainshell.com**](https://explainshell.com/) — 把任何 shell 指令拆解讲解（debug 救星）

### REST API
- [**MDN — HTTP**](https://developer.mozilla.org/en-US/docs/Web/HTTP) — 协定基础
- [**Postman Learning Center**](https://learning.postman.com/) — API 探索工具
- [**HTTPie**](https://github.com/httpie/cli) — 比 `curl` 友善的命令行 HTTP client

### YAML / JSON
- [**YAML 官网**](https://yaml.org/) — 规格
- [**JSON crash course**](https://www.json.org/json-en.html) — 官方快速指南
- [**jq**](https://github.com/jqlang/jq) — 命令行 JSON 处理工具（agent 工作中常用）

## 为什么有这个阶段

大多数“AI agent”教学都预设你已经会这些。如果你还没，就会在奇怪的地方卡关（tool 需要 async、配置文件是 YAML、SDK 安装要用 git）。在这里花一周的投资，可以省下后面 10 周以上的挫折。

---

> ✅ **走完 Stage 0 了？** 接下来 [**Stage 1 — LLM 基础**](01-llm-basics.zh-Hans.md) 会用 5-8 小时带你做完第一次 LLM API 调用、认识 token / context window / temperature，以及用 per-token 计价估算实际任务成本。**继续往下走 →**
