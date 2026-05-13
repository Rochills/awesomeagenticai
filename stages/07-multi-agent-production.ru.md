# Этап 7 — Multi-Agent · Production

> [繁體中文](./07-multi-agent-production.md) | [简体中文](./07-multi-agent-production.zh-Hans.md) | [English](./07-multi-agent-production.en.md) | **Русский**


⏱ **Оценка времени**: 2–4 недели (~15–30 часов)

> 💡 Этап насыщен терминами (multi-agent / handoff / eval / observability / guardrails / …) → см. [`resources/glossary.ru.md` §4 + §6](../resources/glossary.ru.md#4-multi-agent).

Финальный этап. Ты переходишь от «умею строить agents» к «умею гонять их в production с несколькими координирующимися агентами, eval'ом, observability и деплоем».

## 📌 Цели обучения

- Спроектировать multi-agent orchestration паттерны (debate, planner-executor, peer review)
- Настроить evaluation harness для agents
- Добавить observability (tracing, logging, cost tracking)
- Использовать Anthropic SDK / OpenAI SDK для production-деплоя (продвинутые фичи: streaming, prompt caching, batching)
- Задеплоить agents в production (Docker, serverless, monitoring)

## 📚 Обязательное чтение

1. [**Anthropic — Building Effective Agents**](https://www.anthropic.com/engineering/building-effective-agents) — перечитай с production-линзой
2. [**Anthropic — Prompt Caching**](https://www.anthropic.com/news/prompt-caching) — техника снижения стоимости на 90%
3. [**Anthropic — Message Batches API**](https://docs.anthropic.com/en/docs/build-with-claude/batch-processing) — async batch jobs
4. **Документация одного eval-фреймворка** — promptfoo ИЛИ LangSmith ИЛИ weave
5. [**ai-boost/awesome-harness-engineering**](https://github.com/ai-boost/awesome-harness-engineering) (★ 780+) — agent harness toolkit / паттерны / eval / memory / MCP / observability в одном. **Фреймворки заворачивают LLM в agents; harnesses заворачивают agents в production-системы** — именно про это этот этап.
6. [**ZhangHanDong/harness-engineering-from-cc-to-ai-coding**](https://github.com/ZhangHanDong/harness-engineering-from-cc-to-ai-coding) (★ 1.3k+) — уроки harness-дизайна из чтения source Claude Code (китайский)

## 🛠 Практические упражнения (делать, не просто читать)

### Упражнение 1: Multi-Agent debate
Два агента спорят на тему (например, «Python vs Rust для backend»), третий судит. Понаблюдай за паттернами convergence vs divergence.

### Упражнение 2: Eval
Напиши eval для одного из своих ранних агентов, прогоняй N раз, замерь success rate. Замени «я просто на глаз».

### Упражнение 3: Observability
Подключи LangSmith / Helicone / weave к агенту, посмотри полный trace. Пойми: «дебаг agent'а без observability = чёрный ящик».

### Упражнение 4: SDK advanced
Используй streaming + prompt caching + tool use в одном вызове. Понаблюдай, как падает cost.

### Упражнение 5: Deploy
Упакуй агента в Docker, задеплой в облако (любой провайдер). Научись поставлять прототип как нечто, что другие могут запустить.

## 🎯 Подборка проектов

### Multi-Agent Orchestration

#### [microsoft/autogen](https://github.com/microsoft/autogen)

Уже упомянут в этапе 4. В production-контексте паттерн GroupChat-координации AutoGen — сильный референс для multi-agent debate / brainstorming.

---

#### [crewAIInc/crewAI](https://github.com/crewAIInc/crewAI)

Уже упомянут в этапе 4. Для role-based multi-agent (например, пайплайны research → writer → reviewer) CrewAI — простейший production-паттерн.

---

#### [langchain-ai/langgraph](https://github.com/langchain-ai/langgraph)

Уже упомянут в этапе 4. Для production с audit trails, checkpointing и human-in-the-loop LangGraph лидирует.

---

### Evaluation фреймворки

#### [promptfoo/promptfoo](https://github.com/promptfoo/promptfoo)

| Поле | Значение |
|---|---|
| Stars | ★ 20k+ |
| License | MIT |
| Recommendation | ⭐⭐⭐⭐⭐ |

**Чему учит**: YAML-based eval harness для промптов и агентов. Сравнивай между моделями, гоняй regression-тесты в CI.

**Лучше всего для**: стандартизованный eval-пайплайн. Заменяет «я просто на глаз».

**Запуск**:
```bash
npx promptfoo init
# Редактируй promptfooconfig.yaml
npx promptfoo eval
```

---

#### [EleutherAI/lm-evaluation-harness](https://github.com/EleutherAI/lm-evaluation-harness)

| Поле | Значение |
|---|---|
| Stars | ★ 12k+ |
| License | MIT |
| Recommendation | ⭐⭐⭐⭐ |

**Чему учит**: academic-grade eval framework с сотнями стандартизованных бенчмарков (MMLU, HellaSwag, GSM8K).

**Лучше всего для**: когда нужно сказать «мы получили X% на бенчмарке Y». Research-flavored.

---

#### [openai/evals](https://github.com/openai/evals)

| Поле | Значение |
|---|---|
| Stars | ★ 18k+ |
| Recommendation | ⭐⭐⭐⭐ |

**Чему учит**: eval-фреймворк OpenAI. Кастомные eval'ы под конкретные сценарии.

**Лучше всего для**: когда нужны OpenAI-специфичные eval'ы или контрибьют обратно.

---

### Observability

#### [langfuse/langfuse](https://github.com/langfuse/langfuse)

| Поле | Значение |
|---|---|
| Stars | ★ 26k+ |
| License | MIT (open source) + платный cloud |
| Recommendation | ⭐⭐⭐⭐⭐ |

**Чему учит**: open-source LLM observability — traces, sessions, evals, prompt management.

**Лучше всего для**: self-hosted production observability. Сильная open-source альтернатива LangSmith.

---

#### [LangSmith](https://www.langchain.com/langsmith) (proprietary)

**Чему учит**: observability-платформа LangChain. Traces, evals, итерация промптов.

**Лучше всего для**: если глубоко в LangChain/LangGraph стеке. Только hosted.

---

#### [Helicone](https://github.com/Helicone/helicone)

| Поле | Значение |
|---|---|
| Stars | ★ 5k+ |
| License | Apache 2.0 (open source) + платный cloud |
| Recommendation | ⭐⭐⭐⭐ |

**Чему учит**: LLM observability через прокси — drop-in замена OpenAI/Anthropic клиентов, получаешь logging + caching.

**Лучше всего для**: быстрая инструментовка без переписывания кода.

---

#### [weave (от Weights & Biases)](https://github.com/wandb/weave)

| Поле | Значение |
|---|---|
| Recommendation | ⭐⭐⭐⭐ |

**Чему учит**: tracing + eval framework от W&B. Интегрирован с их ML-платформой.

**Лучше всего для**: команд, уже на W&B для ML experiment tracking.

---

### Anthropic SDK Advanced

#### [anthropics/anthropic-sdk-python](https://github.com/anthropics/anthropic-sdk-python)

| Поле | Значение |
|---|---|
| Recommendation | ⭐⭐⭐⭐⭐ |

**Чему учит**: официальный Python SDK (base API layer). Streaming, async, tool use, prompt caching, batches, files API.

**Лучше всего для**: построение приложений прямо на Claude API, когда нужен raw API control, а не higher-level agent runtime.

---

#### [anthropics/anthropic-sdk-typescript](https://github.com/anthropics/anthropic-sdk-typescript)

**Чему учит**: TS-эквивалент low-level Python SDK.

**Лучше всего для**: TypeScript / Node / web-приложений, желающих base API layer.

---

#### [anthropics/claude-agent-sdk-python](https://github.com/anthropics/claude-agent-sdk-python) ⭐ agent-specific

| Поле | Значение |
|---|---|
| Stars | ★ 6k+ |
| License | MIT |
| Recommendation | ⭐⭐⭐⭐⭐ |

**Чему учит**: **agent-specific SDK** Anthropic (выпущен в середине 2025) — отличается от low-level `anthropic-sdk-python`. Встроенный tool use loop, file access, sandboxed execution, subagent orchestration. Выставляет agent-возможности Claude Code для прямого использования из Python-приложений.

**Лучше всего для**: разработчиков, строящих Claude-based agents, а не просто зовущих API. Избавляет от написания ReAct loop руками, управления tool execution и т. д.

**Заметки**: использует тот же agent runtime, что Claude Code; чтение source этого SDK — самый быстрый путь к пониманию, как Claude Code работает изнутри.

---

#### [anthropics/claude-agent-sdk-typescript](https://github.com/anthropics/claude-agent-sdk-typescript)

| Поле | Значение |
|---|---|
| Stars | ★ 1.4k+ |
| License | NOASSERTION |
| Recommendation | ⭐⭐⭐⭐ |

**Чему учит**: TypeScript-версия Claude Agent SDK.

**Лучше всего для**: разработчиков, строящих Claude agents в Node / web app окружениях.

---

#### [Anthropic Cookbook — Advanced patterns](https://github.com/anthropics/anthropic-cookbook)

Уже упомянут. Конкретно `prompt_caching.ipynb`, `tool_use/` и `multimodal/` notebooks учат продвинутому SDK-использованию.

---

### Deployment

#### [BentoML/BentoML](https://github.com/bentoml/BentoML)

| Поле | Значение |
|---|---|
| Stars | ★ 8k+ |
| License | Apache 2.0 |
| Recommendation | ⭐⭐⭐⭐ |

**Чему учит**: serve любой ML/LLM модели как production API. Docker + serving framework.

**Лучше всего для**: оборачивания agent'а в deployable сервис.

---

#### [LangServe](https://github.com/langchain-ai/langserve)

**Чему учит**: деплой LangChain-приложений как REST API. FastAPI под капотом.

**Лучше всего для**: быстрого деплоя LangChain-based агентов.

---

#### [datawhalechina/self-llm](https://github.com/datawhalechina/self-llm)

| Поле | Значение |
|---|---|
| Language | 中文 (zh-Hans) |
| Stars | ★ 30k+ |
| License | Apache-2.0 |
| Recommendation | ⭐⭐⭐⭐ |

**Чему учит**: comprehensive китайский гайд по fine-tuning и деплою open-source LLM в Linux-окружениях. Покрывает Qwen / Llama / GLM / multimodal модели, full-parameter + LoRA + deployment.

**Лучше всего для**: китайскоязычных команд, разворачивающих open-source LLM у себя. Comprehensive китайский туториал, покрывающий обучение, fine-tuning и деплой.

---

#### [hiyouga/LLaMA-Factory](https://github.com/hiyouga/LLaMA-Factory)

| Поле | Значение |
|---|---|
| Language | Python |
| Stars | ★ 70k+ |
| License | Apache-2.0 |
| Recommendation | ⭐⭐⭐⭐⭐ |

**Чему учит**: самый широко используемый в китайском community LLM fine-tuning framework — унифицирует SFT / DPO / PPO / GRPO обучение между 100+ open-source моделей (Llama / Qwen / DeepSeek / Yi / Mistral и т. д.). Web UI позволяет fine-tune без кода.

**Лучше всего для**: всех, кто fine-tune'ит open-source LLM (не только prompt engineering). Сфокусирован на самом training, в отличие от более широкого scope'а self-llm.

**Заметки**: в комбинации с Ollama / llama.cpp этапа 1 получаешь полную петлю «fine-tune → quantize → local deploy».

---

### [vLLM](https://github.com/vllm-project/vllm)

| Поле | Значение |
|---|---|
| Stars | ★ 79k+ |
| License | Apache 2.0 |
| Recommendation | ⭐⭐⭐⭐ |

**Чему учит**: high-throughput LLM serving. Гоняй open-source модели в production.

**Лучше всего для**: локального развёртывания open-source LLM (Llama, Qwen и т. д.) вместо оплаты API.

---

### Multi-Agent кейс-стади

#### [geekan/MetaGPT](https://github.com/geekan/MetaGPT)

| Поле | Значение |
|---|---|
| Stars | ★ 67k+ |
| License | MIT |
| Recommendation | ⭐⭐⭐⭐⭐ |

**Чему учит**: SOP-driven multi-agent software development team — роли PM / Architect / Engineer, каждая производит артефакты (PRD → design → code) и передаёт следующей роли.

**Лучше всего для**: увидеть, как реализован паттерн **role-specialization + artifact handoff**. Другой дизайн-путь, чем state-machine подход LangGraph.

**Заметки**: поддерживается китайской командой; docs site имеет zh-контент. Стоит сравнить с free-form group chat AutoGen.

---

#### [OpenBMB/ChatDev](https://github.com/OpenBMB/ChatDev)

| Поле | Значение |
|---|---|
| Language | Python |
| Stars | ★ 33k+ |
| License | Apache-2.0 |
| Recommendation | ⭐⭐⭐⭐ |

**Чему учит**: «communicative» software development паттерн — агенты дебатируют на каждой фазе (design / code / test) перед продвижением. Стандартный open-source кейс-стади для **agent debate / peer-review паттерна** с академической статьёй за плечами.

**Лучше всего для**: построения workflow'ов, где «два агента должны бросить вызов друг другу, прежде чем выдать вывод». Сфокусирован на debate-механизме больше, чем AutoGen.

**Заметки**: есть `README-zh.md`, дружелюбен к китайским читателям.

---

#### [princeton-nlp/SWE-agent](https://github.com/princeton-nlp/SWE-agent)

| Поле | Значение |
|---|---|
| Language | Python |
| Stars | ★ 19k+ |
| License | MIT |
| Recommendation | ⭐⭐⭐⭐ |

**Чему учит**: дизайн **Agent-Computer Interface (ACI)** — *форма* tool surface (не промпт) определяет производительность агента на SWE-Bench. Исследовательский вывод Princeton NLP.

**Лучше всего для**: после изучения tool use в этапах 3–4 понять «**почему дизайн tool важнее, чем тюнинг промпта**».

**Заметки**: статья + open-source код — отличный референс для академического multi-agent research'а.

---

## ✅ Самопроверка после этапа 7

Можешь:
- [ ] Спроектировать multi-agent систему с явным coordination протоколом
- [ ] Настроить автоматизированный eval-пайплайн, бегущий в CI
- [ ] Подключить observability (tracing) к production agent'у
- [ ] Замерить и сравнить cost до/после prompt caching на реальной нагрузке
- [ ] Задеплоить агента в облачный сервис (любой провайдер)

Если да → ты прошёл основной путь. Выбери [специализированную ветку](../README.ru.md#️-карта-обучения-две-дорожки) или контрибьють в этот репо.

## 💡 Что дальше

У тебя теперь фундаментальная компетенция. Следующие 6–12 месяцев должны быть про:
1. **Выбери одну production-систему** и доведи от прототипа до production
2. **Контрибьють в upstream** (LangGraph, AutoGen, MCP servers, Anthropic cookbook)
3. **Читай статьи** — agent-research двигается быстро
4. **Построй видимое** — open-source реальный инструмент, не очередной туториал
