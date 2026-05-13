# Этап 1 — LLM Fundamentals

> [繁體中文](./01-llm-basics.md) | [简体中文](./01-llm-basics.zh-Hans.md) | [English](./01-llm-basics.en.md) | **Русский**


⏱ **Оценка времени**: 1 неделя (~5–8 часов)

> 👋 **Пришёл с [этапа 0](00-foundations.ru.md)?** Хорошо — toolchain готов. Следующие 5–8 часов: первый рабочий вызов к Claude / GPT / Gemini, как token / context window / temperature влияют на вывод и оценка стоимости per-token. **Прыгнул прямо сюда?** Убедись, что можешь запустить Python-скрипт и есть API-ключ от одного провайдера — если нет, вернись на [Этап 0](00-foundations.ru.md).

> 💡 **Не знаешь термин?** (LLM / token / context window / temperature / RAG / agent / …) → проверь [`resources/glossary.ru.md`](../resources/glossary.ru.md) — 30-секундные определения.

## 📌 Цели обучения

После этого этапа сможешь:
- Объяснить, что такое LLM, что такое tokens и что значит context window
- Сделать первый API-вызов к Claude / GPT / Gemini и распарсить ответ
- Сравнить четыре основных LLM-семейства (Claude / GPT / Gemini / Llama) по сильным сторонам
- Оценить стоимость задачи по per-token pricing

## 🚪 Условия входа

Уже должен:
- Запускать Python-скрипт
- Знать концептуально, что такое HTTP / REST
- Иметь API-ключ хотя бы от одного провайдера (Anthropic / OpenAI / Google)

Если нет — сначала вернись на этап 0.

## 📚 Обязательное чтение

1. [**Anthropic — What is Claude?**](https://www.anthropic.com/news/claude-3-family) — официальный обзор моделей
2. [**OpenAI Quickstart**](https://platform.openai.com/docs/quickstart) — прохождение первого API-вызова
3. [**A Visual Guide to LLM Tokenizers**](https://huggingface.co/learn/llm-course/chapter6/1) — введение от Hugging Face
4. [**Anthropic API Pricing**](https://www.anthropic.com/pricing#anthropic-api) — прочитай pricing таблицу, посчитай стоимость 1k input + 1k output

## 🛠 Практические упражнения (делать, не только читать)

### Упражнение: LLM API
Пять строк Python, вызывающие Claude API и печатающие ответ.

```python
from anthropic import Anthropic
client = Anthropic()
msg = client.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=100,
    messages=[{"role": "user", "content": "Hello, who are you?"}]
)
print(msg.content[0].text)
```

### Упражнение: Tokens
Запусти один и тот же промпт 100 раз и понаблюдай, как меняются token counts.
- Заметь: temperature ≠ 0 порождает вариацию
- Заметь: token count для ОДНОГО английского vs китайского предложения

### Упражнение: Pricing
Посчитай реальную dollar-стоимость 1000 inference'ов для своего hello-world промпта. Используй Anthropic pricing page + считай токены через SDK `usage` field.

### Упражнение: Cross-Provider Comparison
Отправь один и тот же промпт в Claude, GPT и Gemini одновременно, сравни ответы. Заметь «почему один и тот же input даёт разные ответы» — стиль, длина и judgment отличаются. Используй OpenAI, Anthropic и Google SDK бок-о-бок.

### Упражнение: Error Handling
Намеренно вызови условия ошибок и напиши retry-логику:
- Неверный API-ключ → посмотри, как поднимается ошибка
- Слишком длинный промпт → что происходит, когда context window полон
- Network drop → напиши retry-обёртку с exponential backoff
Это фундаментально для production agent-кода этапов 3–7.

### Упражнение: Local LLM
**Без платы провайдеру за API, работает на твоей машине**: используй Ollama, чтобы скачать небольшую модель (рекомендую `llama3.2:3b` или `qwen2.5:3b`), обращайся через OpenAI-совместимый API.
```bash
# Установка Ollama: https://ollama.com
ollama pull qwen2.5:3b
ollama serve  # порт по умолчанию 11434
```
Затем из Python:
```python
from openai import OpenAI
client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")
r = client.chat.completions.create(
    model="qwen2.5:3b",
    messages=[{"role":"user","content":"Explain ReAct in 3 sentences"}]
)
print(r.choices[0].message.content)
```
**Зачем**: как только умеешь гонять локальные LLM, эксперименты этапов 3–6 не упираются в стоимость API; privacy-чувствительная работа тоже остаётся offline.

## 🎯 Подборка проектов

### [Anthropic Cookbook](https://github.com/anthropics/anthropic-cookbook)

| Поле | Значение |
|---|---|
| Language | Python |
| Stars | ★ 42k+ |
| License | MIT |
| Recommendation | ⭐⭐⭐⭐⭐ |

**Чему учит**: как вызывать Claude API для каждого распространённого паттерна — chat, tools, citations, multi-modal, prompt caching.

**Лучше всего для**: всех, кто стартует с Claude. Notebooks ведут через каждую API-фичу с запускаемыми примерами.

**Заметки**: относись к этому как к reference manual. Не читай от корки до корки; обращайся по необходимости.

**Запуск**:
```bash
git clone https://github.com/anthropics/anthropic-cookbook
cd anthropic-cookbook/skills/classification
pip install -r requirements.txt
jupyter notebook guide.ipynb
```

---

### [Anthropic Courses](https://github.com/anthropics/courses)

| Поле | Значение |
|---|---|
| Language | Python / Jupyter |
| Stars | ★ 21k+ |
| License | NOASSERTION (нет SPDX upstream; проверь LICENSE перед использованием) |
| Recommendation | ⭐⭐⭐⭐⭐ |

**Чему учит**: официальная серия образовательных курсов Anthropic — API fundamentals, prompt evaluation, real-world prompting, tool use, Claude с Excel. Каждый курс — Jupyter notebook, который можно читать и запускать.

**Лучше всего для**: всех, кто стартует с Claude API. Дополняет Cookbook: Cookbook — это «как мне сделать X?» lookup, Courses — «учим с нуля, end-to-end» туториал.

**Заметки**: начни с `anthropic_api_fundamentals` и `prompt_engineering_interactive_tutorial`.

---

### [OpenAI Cookbook](https://github.com/openai/openai-cookbook)

| Поле | Значение |
|---|---|
| Language | Python / Jupyter |
| Stars | ★ 73k+ |
| License | MIT |
| Recommendation | ⭐⭐⭐⭐⭐ |

**Чему учит**: то же, что Anthropic Cookbook, но для GPT-семейства. Огромная коллекция рецептов, structured outputs, tool use, embeddings.

**Лучше всего для**: всех, кто использует OpenAI API. Особенно сильны примеры structured outputs и function calling.

**Заметки**: больше Anthropic cookbook'а. Активно используй поиск — не листай линейно.

---

### [LangChain Academy](https://academy.langchain.com/)

| Поле | Значение |
|---|---|
| Format | Бесплатные онлайн-курсы |
| Recommendation | ⭐⭐⭐⭐ |

**Чему учит**: LLM fundamentals, embeddings, RAG, agents — через LangChain. Хорошо, даже если в итоге не будешь использовать LangChain.

**Лучше всего для**: visual learners, которым нужен video walkthrough.

**Заметки**: некоторые уроки тяжело перегружены маркетингом LangChain. Их пропускай, бери концептуальные.

---

### [datawhalechina/happy-llm](https://github.com/datawhalechina/happy-llm)

| Поле | Значение |
|---|---|
| Language | 中文 (zh-Hans) |
| Stars | ★ 29k+ |
| License | Custom |
| Recommendation | ⭐⭐⭐⭐⭐ |

**Чему учит**: построй LLM с нуля — китайскоязычный аналог «Zero to Hero» курса Karpathy. Главы 1–4 покрывают принципы LLM bottom-up, потом практическое применение.

**Лучше всего для**: китайскоязычных учеников, желающих по-настоящему понять, как работают LLM, не только звать API. Прямой аналог Hugging Face LLM Course на китайском.

---

### [datawhalechina/llm-universe](https://github.com/datawhalechina/llm-universe)

| Поле | Значение |
|---|---|
| Language | 中文 (zh-Hans) |
| Stars | ★ 12k+ |
| License | NOASSERTION |
| Recommendation | ⭐⭐⭐⭐ |

**Чему учит**: дружелюбный к новичкам туториал по разработке LLM-приложений на китайском. Покрывает основы API, базы знаний, RAG, продвинутые техники.

**Лучше всего для**: китайскоязычных новичков, желающих *что-то построить* с LLM (vs. просто понимать их).

---

### [jingyaogong/minimind](https://github.com/jingyaogong/minimind)

| Поле | Значение |
|---|---|
| Language | 中文 + Python |
| Stars | ★ 48k+ |
| License | Apache-2.0 |
| Recommendation | ⭐⭐⭐⭐⭐ |

**Чему учит**: обучи 64M-параметровый LLM с нуля за 2 часа — самый популярный китайский hands-on «build LLM from scratch» проект. Pretrain + SFT + LoRA + DPO + RLHF — всё в одном репо.

**Лучше всего для**: после просмотра видео Karpathy запусти этот, чтобы реально прочувствовать каждый этап обучения на реальных данных. Педагогическая ценность исключительная.

---

### [datawhalechina/llm-cookbook](https://github.com/datawhalechina/llm-cookbook)

| Поле | Значение |
|---|---|
| Language | 中文 (zh-Hans) |
| Stars | ★ 23k+ |
| Last update | ⚠️ Stale (июнь 2025; ~1 год без активности) |
| License | Custom (CC BY-NC-SA) |
| Recommendation | ⭐⭐⭐⭐ |

**Чему учит**: курсы Эндрю Нга по prompt engineering / building systems / fine-tuning, переведённые и адаптированные для китайских учеников. Hands-on notebooks.

**Лучше всего для**: китайскоязычных новичков, желающих guided LLM-программу.

**Заметки**: zh-Hans контент (Datawhale использует упрощённый китайский) — но технический контент переносится нормально. Отличная бесплатная китайскоязычная точка входа.

---

### [Hugging Face — Large Language Model Course](https://huggingface.co/learn/llm-course)

| Поле | Значение |
|---|---|
| Format | Бесплатный онлайн-курс + notebooks |
| License | Apache 2.0 |
| Recommendation | ⭐⭐⭐⭐ |

**Чему учит**: как LLM на самом деле работают (tokenization, transformers, fine-tuning) с экосистемой Hugging Face.

**Лучше всего для**: читателей, желающих понять, что происходит внутри, а не только API surface.

---

### 🖥️ Запуск LLM локально (без API-комиссий)

Четыре записи ниже — инструменты для **запуска LLM на твоей машине** — полезно после Упражнения: Local LLM, и ответ для privacy-чувствительной работы, cost-чувствительных экспериментов или offline-сценариев.

---

### [ollama/ollama](https://github.com/ollama/ollama)

| Поле | Значение |
|---|---|
| Language | Go |
| Stars | ★ 170k+ |
| License | MIT |
| Recommendation | ⭐⭐⭐⭐⭐ |

**Чему учит**: самый простой local LLM runner — одна `ollama pull qwen2.5:3b` — и у тебя рабочая модель со встроенным OpenAI-совместимым API (`http://localhost:11434/v1`); существующий OpenAI SDK код почти не нужно менять.

**Лучше всего для**: пользователей local LLM впервые. Также полезно как fallback в agent-разработке — основной путь на Claude, cost-чувствительные части на Ollama.

**Запуск**:
```bash
# Скачать с https://ollama.com
ollama pull qwen2.5:3b   # ~2GB, приличная поддержка китайского
ollama run qwen2.5:3b    # интерактивный чат
ollama serve             # старт API-сервера
```

---

### [ggml-org/llama.cpp](https://github.com/ggml-org/llama.cpp)

| Поле | Значение |
|---|---|
| Language | C++ |
| Stars | ★ 108k+ |
| License | MIT |
| Recommendation | ⭐⭐⭐⭐ |

**Чему учит**: inference engine, который Ollama и многие local LLM инструменты используют под капотом. Пойми quantization (формат GGUF, что значит Q4_K_M / Q5_K_S), KV cache, CPU/GPU offloading.

**Лучше всего для**: тех, кто хочет знать «почему 7B-модель помещается в 8GB RAM?». Если Ollama хватает — пропусти; возвращайся, когда нужен fine-grained control.

---

### [mudler/LocalAI](https://github.com/mudler/LocalAI)

| Поле | Значение |
|---|---|
| Language | Go |
| Stars | ★ 46k+ |
| License | MIT |
| Recommendation | ⭐⭐⭐⭐ |

**Чему учит**: drop-in замена OpenAI API — тот же OpenAI SDK код, направь `base_url` на LocalAI и гоняй LLM, embedding, image generation, TTS, STT — всё локально.

**Лучше всего для**: команд с compliance / data-privacy требованиями, которым нужно заменить весь OpenAI-стек локальными альтернативами. Шире, чем Ollama (не только chat).

---

### [ml-explore/mlx](https://github.com/ml-explore/mlx)

| Поле | Значение |
|---|---|
| Language | C++ / Python |
| Stars | ★ 25k+ |
| License | MIT |
| Recommendation | ⭐⭐⭐ |

**Чему учит**: ML-фреймворк Apple, специально построенный под Apple Silicon (M1/M2/M3/M4). На Mac'ах часто быстрее llama.cpp с лучшей memory efficiency.

**Лучше всего для**: Mac-разработчиков, желающих выжать максимум из Apple Silicon. Linux / Windows пользователи могут пропускать.

**Заметки**: парь с пакетом `mlx-lm` для простейшего пути.

**Заметки**: более академический, чем cookbook'и. Покрывает обучение, не только inference.

---

### [karpathy/LLM101n](https://github.com/karpathy/LLM101n)

| Поле | Значение |
|---|---|
| Status | ⚠️ Archived (последний апдейт август 2024); только outline — никогда не достроен |
| Recommendation | ⭐⭐ |

**Чему учит**: изначально позиционировался как build-from-scratch «Storyteller AI LLM» курс в фирменном педагогическом стиле Karpathy.

**Лучше всего для**: смотри лучше видео Karpathy «Let's build GPT from scratch» на YouTube — оно полное и отличное.

**Заметки**: репо — только outline; курс не был построен. В списке только для исторической отсылки.

---

### [Anthropic — Claude API Quickstart](https://docs.anthropic.com/en/docs/get-started)

| Поле | Значение |
|---|---|
| Format | Документация |
| Recommendation | ⭐⭐⭐⭐⭐ |

**Чему учит**: официальная документация Claude API.

**Лучше всего для**: прямой референс. Закладку.

---

### [karpathy — Let's build GPT from scratch](https://www.youtube.com/watch?v=kCc8FmEb1nY)

| Поле | Значение |
|---|---|
| Format | YouTube видео (2 часа) |
| Recommendation | ⭐⭐⭐⭐⭐ |

**Чему учит**: построй transformer-based GPT с нуля на PyTorch. Фундаментальное понимание, как LLM работают изнутри.

**Лучше всего для**: всех, кто хочет понять ПОЧЕМУ LLM ведут себя так, как ведут, а не только КАК их вызывать.

**Заметки**: 2 часа плотного контента. Паузь и кодь параллельно — не смотри пассивно.

---

### [rasbt/LLMs-from-scratch](https://github.com/rasbt/LLMs-from-scratch)

| Поле | Значение |
|---|---|
| Language | Python / Jupyter |
| Stars | ★ 91k+ |
| License | Apache-2.0 |
| Recommendation | ⭐⭐⭐⭐⭐ |

**Чему учит**: построй GPT-style LLM end-to-end на PyTorch — tokenizer → attention → pretraining → finetuning, в паре с книгой Sebastian Raschka. Полные notebooks + код, выровнены по главам книги.

**Лучше всего для**: всех, кто хочет по-настоящему понять, что такое tokens, attention и weights. Дополняет видео Karpathy — то 2-часовой fly-by, это медленный read-the-book вариант.

**Заметки**: companion code к книге (Apache-2.0); свободно форкай и модифицируй.

---

## ✅ Самопроверка перед этапом 2

Можешь:
- [ ] Сделать Claude API вызов из Python в 5 строк
- [ ] Объяснить, почему «你好» может занимать 2 токена, а «Hello» — 1
- [ ] Назвать примерно per-token цену Claude Sonnet vs Opus
- [ ] Назвать одну сильную сторону Claude vs GPT vs Gemini vs Llama

Если да → переходи к [Этапу 2 — Prompt Engineering](02-prompt-engineering.ru.md).

Если нет → перечитай Anthropic Quickstart + запусти все 3 hello-X проекта выше.

---

> ✅ **Этап 1 пройден?** Дальше — [**Этап 2 — Prompt Engineering**](02-prompt-engineering.ru.md) — 5–12 часов проводят через написание переиспользуемых структурированных промптов, использование few-shot и chain-of-thought для reasoning-задач и обучение количественно оценивать улучшение промпта через eval'ы. **Дальше →**
