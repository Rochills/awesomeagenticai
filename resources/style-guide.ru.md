# Style Guide для `awesome-agentic-ai-zh`

> [繁體中文](./style-guide.md) | [简体中文](./style-guide.zh-Hans.md) | [English](./style-guide.en.md) | **Русский**

Это **единственный источник правды** для каталога: терминология, схема записи, нотация лицензий, стиль письма, запрещённые слова.

Прочти это перед открытием PR. Мейнтейнеры будут использовать этот гайд для ревью.

---

## 📋 Содержание

- [1. Схема project entry](#1-схема-project-entry)
- [2. Определения recommendation star](#2-определения-recommendation-star)
- [3. Запрещённые слова и альтернативы](#3-запрещённые-слова-и-альтернативы)
- [4. Английские существительные оставлять](#4-английские-существительные-оставлять)
- [5. Конвенции нотации лицензий](#5-конвенции-нотации-лицензий)
- [6. Шаблон stage page](#6-шаблон-stage-page)
- [7. Шаблон branch page](#7-шаблон-branch-page)
- [8. Стиль письма](#8-стиль-письма)
- [9. Ссылки и цитирование](#9-ссылки-и-цитирование)

---

## 1. Схема project entry

Каждая project entry использует структуру:

```markdown
### [Repo Name](https://github.com/owner/repo) ⭐⭐⭐⭐

| Field | Value |
|---|---|
| Language | Python |
| Stars | ★ 12k+ |
| License | MIT |
| Recommendation | ⭐⭐⭐⭐ |

**What it teaches**: 1–2 предложения о том, чему этот проект учит на этом этапе.

**Best for**: 1 предложение о том, кому стоит изучать и почему.

**Notes**: 1–3 предложения личной оценки. Что сильно, что слабо, что пропустить. (Опционально.)

**Run it**:
\`\`\`bash
# минимальная команда install / first-run
\`\`\`
```

### Required fields (GitHub-репо entry)
Для записей, являющихся реальными GitHub-репо:
- `Stars` (формат `★ Xk+`, без разделителя тысяч)
- `License` (SPDX ID или аннотированное исключение, см. §5)
- `Recommendation` (⭐ × N, см. §2)
- `What it teaches`, `Best for`

### Required fields (не-репо entry: статья / курс / видео / протокол / документация)
Некоторые записи — блоги, видео, официальные доки или каталог-хабы — не GitHub-репо. Для них:
- `Recommendation` (обязательно)
- `What it teaches`, `Best for` (обязательно)
- `Format` (обязательно, например `Article` / `Video` / `Course` / `Curated list` / `Specification`)
- `Stars` / `License` могут быть опущены (нет GitHub-репо для привязки)

Пример: запись блога `Anthropic — Building Effective Agents` использует `Format = Article` + `Recommendation` без `Stars` или `License`.

### Optional fields
- `Language` — основной язык программирования (Python / TypeScript / Chinese)
- `Last update` / `Status` — флаг, если stale или поддержка замедлилась
- `Notes`, `Run it`

### Конвенции заголовков
- Этапы 1–4 / 6 используют `### [Repo](url)`
- Этап 5 / 7 / branches используют `#### [Repo](url)` (когда есть родительская H3-категория)
- Суффикс со звёздами допустим: `### [Repo](url) ⭐⭐⭐⭐⭐` или sub-label: `### [Repo](url) ⭐ Official`

---

## 2. Определения recommendation star

| Stars | Значение | Когда использовать |
|---|---|---|
| ⭐⭐⭐⭐⭐ | Must-read / must-run | Пропуск приведёт к застреванию на этом этапе |
| ⭐⭐⭐⭐ | Highly recommended | Сильный материал, чтобы углубиться в тему |
| ⭐⭐⭐ | Solid example | Стоит запустить для cross-reference'а |
| ⭐⭐ | Useful reference | Листай, если интересно |
| ⭐ | Niche / advanced / для полноты | Большинство читателей могут пропустить |

**Правила:**
- Репо, упомянутый в разных этапах / ветках, **должен иметь тот же рейтинг** (если нет audience-специфичной причины — тогда явно отметь)
- Не накручивай звёзды, чтобы «выглядело подбадривающе». Честность > вежливость
- Коммерческие продукты (Cursor, LangSmith и т. д.) следуют той же шкале

---

## 3. Запрещённые слова и альтернативы

Этот документ — **Traditional Chinese (zh-TW, Taiwan)**. Китайский гид перечисляет zh-Hans-описки, которых надо избегать. Для английских companion-файлов правила проще:

> 📌 **Конвенция language tag (BCP 47 / W3C i18n)**: репо использует `.zh-Hans.md` (не `.zh-CN.md`) для упрощённого китайского зеркала. `Hans` / `Hant` — [BCP 47 script subtags](https://www.w3.org/International/articles/language-tags/), отвязанные от региона — упрощённый китайский также используется в Сингапуре и Малайзии, не только в материковом Китае, поэтому `Hans` точнее, чем `CN`. Канонический контент `README.md` — **zh-Hant-TW** (традиционный китайский, тайваньские конвенции), оставлен без суффикса как дефолтная landing-страница GitHub. Региональные различия могут быть добавлены потом как `zh-Hans-CN` / `zh-Hant-HK` и т. д. Спасибо [@xfq](https://github.com/xfq) (W3C i18n lead) за поднятие этого в [#9](https://github.com/WenyuChiou/awesome-agentic-ai-zh/issues/9).

### Избегай overclaim-фраз

| Избегай | Используй вместо |
|---|---|
| «лучший в мире» / «сильнейший в индустрии» | «comprehensive» / «well-known» / «widely-used» |
| «production-grade» (когда описываешь учебный материал) | «teaching-oriented» / «material to learn production patterns from» |
| «единственный выбор» / «definitive» | «хороший вариант» / «entry-level pick» |
| «самый срочный» / «самый важный» | (просто отбрось модификатор) |
| «authoritative reference» (если не действительно официальная spec) | «important reference implementation» / «official template» |
| «no problem» (про legal/license) | «check the terms before use» / «verify the terms yourself» |

---

## 4. Английские существительные оставлять

В техническом тексте есть термины, которые **читаются естественнее на английском**, чем в переводе:

- `LLM`, `API`, `SDK`, `MCP`
- `agent`, `tool use`, `function calling`, `prompt`, `prompt caching`
- `framework`, `library`, `repo`, `commit`, `PR`, `branch`
- `RAG`, `embedding`, `vector DB`, `retrieval`, `chunk`, `token`
- `streaming`, `async`, `batch`, `webhook`
- `marketplace`, `plugin`, `skill`, `hook`
- `production` (в значении «production environment») — но каталог намеренно избегает его во многих местах (см. китайский §3)
- `hello-world`, `hands-on exercise` — оставлять (zh-TW canonical использует `動手練習`; en mirror переводит как `hands-on exercise(s)`)

**Тест**: технический читатель остановится на переведённой форме? Если да — оставь английский.

---

## 5. Конвенции нотации лицензий

### Прямой SPDX
- `MIT`
- `Apache-2.0`
- `BSD-3-Clause`
- `GPL-3.0`
- `LGPL-3.0`

### Аннотированные исключения

| Ситуация | Нотация |
|---|---|
| Нет SPDX upstream | `NOASSERTION (no SPDX upstream; check LICENSE before use)` |
| AGPL (copyleft) | `AGPL-3.0` + Notes: `AGPL-3.0 license (copyleft) — derivative products that ship modifications must follow the terms.` |
| Custom non-commercial | `NOASSERTION (custom non-commercial)` + Notes: `License is a custom non-commercial term — read the original terms before use.` |
| Множественный per-plugin | `NOASSERTION (each plugin has its own license; check per plugin)` |
| Creative Commons | `CC-BY-4.0`, `CC-BY-NC-SA-4.0` и т. д. |

**Правило**: **никогда** не читай лицензию как юридический совет. Не говори «ok для personal use». Говори «read the original terms before use».

---

## 6. Шаблон stage page

> Тот же шаблон применяется к двум локациям:
> - `stages/0X-*.md` — общий фундамент (0–2) + Track B (Этапы 3–7)
> - `tracks/cli/AX-*.md` — под-этапы Track A (A1–A3) тоже следуют этому шаблону, с большей долей cross-links (большинство записей ссылаются на существующий контент Stage 5 / 7 / cli-agents-guide)

Каждый этап (кроме этапа 0) должен иметь:

```markdown
# Stage N — Topic

> **English** | [繁體中文](./0N-slug.md)

⏱ **Time estimate**: N-M weeks (~X-Y hours)

[1-2 предложения описания core-вопроса этапа]

## 📌 Learning Goals
- bullet 1
- bullet 2

## 🚪 Entry Conditions (только Stage 1+)
You should have:
- ...

## 📚 Required Reading
1. [Link](url) — описание
2. ...

## 🛠 Hands-on Exercises (do them, not just read)

### Exercise N: Title
Description.

[3-5 hands-on упражнений]

## 🎯 Curated Projects

### [Project Name](url) ⭐⭐⭐⭐
[схема записи по §1]

[N записей]

## ✅ Self-Check Before Stage N+1
Can you:
- [ ] ...
- [ ] ...

If yes → proceed to Stage N+1.
If no → ...

## 💡 What's Next (optional, обычно используется в последнем этапе)
```

**Исключение этапа 0**: можно опустить `Curated Projects` и `Entry Conditions` — это prerequisite gateway.

---

## 7. Шаблон branch page

```markdown
# For [audience] — Specialized Branch

> **English** | [繁體中文](./for-X.md)

> [← Back to main path README](../README.en.md) · Branching from end of Stage 7

## Use Cases
- bullet 1
- bullet 2

## Curated Projects

### Sub-category 1
#### [Project](url) ⭐⭐⭐⭐
[entry]

### Sub-category 2
...

## Required Reading
1. ...

## Workflows To Master
- bullet 1
- bullet 2
```

Записи branch могут быть лаконичнее, чем stage-записи (полная schema-таблица опциональна), но ссылка + звёзды + 1–2 предложения описания — минимум.

---

## 8. Стиль письма

### Длина предложения
- **Одно предложение ≤ 25–30 слов** для английского
- Разбивай длинные на два
- Не вгоняй английский ритм в переведённый китайский (и наоборот)

### Голос
- Предпочитай активный: «Claude calls the tool» ✓
- Избегай пассивного: «The tool is called by Claude» ✗

### «You» vs «we»
- **«You» первым** — это learner-facing материал
- «I» для авторского мнения: «I recommend ...»
- Избегай «we» (если нет реальных соавторов)

### Связки
- Предпочитай простые: «but, so, because»
- Избегай: «however, therefore, hence»

---

## 9. Ссылки и цитирование

### Внутренние ссылки
- Между этапами: relative path `[Stage 4](04-agent-frameworks.en.md)`
- Branch ↔ README: `[← Back to main path](../README.en.md)`
- Cross-stage репо-ссылки: полное имя + link, не просто «as cited earlier»

### Внешние ссылки
- GitHub-репо: `https://github.com/owner/repo` (без trailing slash)
- Статья / блог: полный URL, жирный заголовок
- Коммерческий продукт (Cursor, Make.com и т. д.): официальный URL, не affiliate

### Конвенции link text
- Заголовок repo entry: `[owner/repo](url)` или `[Project Name](url)`
- In-prose цитирование: `[Repo Name](url)` или `\`owner/repo\`` (inline code для коротких ссылок)
- **Избегай**: «click here», «press this»

---

## Связанные внутренние design-доки

Этот style-guide покрывает «как писать запись». Для **дизайн-rationale** — почему эти 5 branches, почему 7 stages — см.:

- [`branches/DESIGN.md`](../branches/DESIGN.md) — заметки по дизайну branches (почему эти аудитории, куда что относится) (zh)
- [`stages/DESIGN.md`](../stages/DESIGN.md) — заметки по дизайну stages (почему эта структура, как выбраны упражнения) (zh)
- [`cli-agents-guide.ru.md`](cli-agents-guide.ru.md) — cross-cutting CLI agent comparison

## Модификация этого гайда

PR'ы к этому гайду приветствуются. Сначала открой Issue для обсуждения — terminology-решения затрагивают 100+ записей.

Текущий мейнтейнер: [@WenyuChiou](https://github.com/WenyuChiou).
