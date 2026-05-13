# Этап 0 — Foundations

> [繁體中文](./00-foundations.md) | [简体中文](./00-foundations.zh-Hans.md) | [English](./00-foundations.en.md) | **Русский**


⏱ **Оценка времени**: 1–2 недели (~5–15 часов, можно пропустить, если уже знаешь)

> 💡 **Не знаешь термин?** Проверь [`resources/glossary.ru.md`](../resources/glossary.ru.md) — 30-секундное определение. Этап 0 не опирается на много жаргона, но следующие — да.

## Когда пропустить этот этап

Если умеешь:
- Написать Python-функцию, вызывающую публичный API и парсящую JSON-ответ
- Использовать git: clone, commit, push и базовый merge
- Использовать командную строку на своей ОС (cd, ls, mkdir, запуск скрипта)
- Читать YAML / JSON-файл без замешательства

→ **Сразу к [Этапу 1](01-llm-basics.ru.md)**.

Если не умеешь — пройди этот этап. Не пропускай — все следующие этапы это предполагают.

## 📌 Цели обучения

- Писать Python: функции, классы, основы async/await
- Использовать git: clone, branch, commit, push, базовое разрешение конфликтов
- Использовать REST API: отправить GET/POST, распарсить JSON, обработать auth headers
- Читать и писать YAML и JSON

## 🛠 Практические упражнения

- **Упражнение: Python** — напиши Python-скрипт, вызывающий https://api.github.com/users/torvalds и печатающий follower count
- **Упражнение: git** — клонируй любой публичный репо, сделай коммит, запушь в свой fork
- **Упражнение: CLI** — собери маленькое дерево директорий в командной строке (macOS / Linux: `mkdir project && cd project && mkdir src tests docs`; Windows PowerShell: `New-Item -ItemType Directory -Path project,project\src,project\tests,project\docs`), запусти Python-скрипт, перенаправь вывод в файл
- **Упражнение: YAML** — прочитай `.yaml` config в Python, поменяй значение, запиши обратно
- **Упражнение: API auth** — на [github.com/settings/tokens](https://github.com/settings/tokens) сгенерируй personal access token (minimal scope: `read:user`), вызови auth-required endpoint `https://api.github.com/user`, понаблюдай 401 (без токена) vs 200 (с токеном). Заметь: реальные production agents всегда используют API auth — сделай это упражнение

## 🎯 Подборка ресурсов (не полные проекты, а учебный материал)

### Python
- [**Python Crash Course**](https://github.com/ehmatthes/pcc_3e) — книга + упражнения (платная книга, бесплатные упражнения)
- [**Real Python tutorials**](https://realpython.com/) — качественные бесплатные статьи
- [**Corey Schafer YouTube**](https://www.youtube.com/c/Coreyms) — видео-туториалы, от новичка до продвинутого, очень чёткая подача
- [**Boot.dev**](https://www.boot.dev/) — интерактивный Python-курс (частично бесплатный)
- [**runoob.com Python tutorial**](https://www.runoob.com/python3/python3-tutorial.html) — китайский Python-интро-референс

### Git
- [**Pro Git book**](https://git-scm.com/book/en/v2) — бесплатный, полный референс
- [**Atlassian Git Tutorials**](https://www.atlassian.com/git/tutorials) — workflow-сфокусированный
- [**Oh Shit, Git!?!**](https://ohshitgit.com/) — когда всё идёт не так
- [**git-flight-rules**](https://github.com/k88hudson/git-flight-rules) — «я облажался с X, как откатить?» — популярная шпаргалка

### CLI / Shell
- [**The Art of Command Line**](https://github.com/jlevy/the-art-of-command-line) — навыки командной строки от новичка до продвинутого (180k+ stars, multi-language)
- [**Learn Shell**](https://www.learnshell.org/) — интерактивный Bash-туториал
- [**explainshell.com**](https://explainshell.com/) — разбирает любую shell-команду (life-saver при дебаге)

### REST APIs
- [**MDN — HTTP**](https://developer.mozilla.org/en-US/docs/Web/HTTP) — основы протокола
- [**Postman Learning Center**](https://learning.postman.com/) — инструмент исследования API
- [**HTTPie**](https://github.com/httpie/cli) — дружелюбнее `curl` command-line HTTP-клиент

### YAML / JSON
- [**YAML official site**](https://yaml.org/) — spec
- [**JSON crash course**](https://www.json.org/json-en.html) — официальный quick guide
- [**jq**](https://github.com/jqlang/jq) — command-line JSON-процессор (активно используется в agent workflow'ах)

## Зачем этот этап существует

Большинство туториалов «AI agent» предполагают, что это у тебя уже есть. Если нет — застрянешь в случайных местах (tools требуют async; конфиги — YAML; setup SDK нужен git). Одна неделя инвестиции здесь экономит 10+ недель фрустрации потом.

---

> ✅ **Этап 0 пройден?** Дальше — [**Этап 1 — LLM Fundamentals**](01-llm-basics.ru.md) — за 5–8 часов он проведёт тебя через первый LLM API call, значение token / context window / temperature и покажет, как оценивать реальную стоимость задачи через per-token pricing. **Дальше →**
