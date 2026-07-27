# 🤖 Агенты

Готовые агенты — наборы скиллов, упакованные в плагины. В отличие от отдельных скиллов
из корня репозитория, агент закрывает **весь рабочий процесс** целиком.

| Агент | Что делает | Скиллы | Статус |
|---|---|---|---|
| **agent-forge** | Превращает любой проект в устанавливаемого агента: анализирует, задаёт форму, генерирует скиллы, упаковывает в плагин, ставит и документирует | `analyze-project`, `verify-agent`, `share-agent` | 🌍 публичный |
| **personal-post** | Одна сырая идея → готовый к публикации личный пост в LinkedIn: спека, копи-текст, карусель и single-page визуал в PDF/PNG | `new-post`, `post-ideas`, `review-post`, `setup-author` | 🌍 публичный |
| **sinister-post** | Контент-пайплайн компании Sinister | `company-post`, `research-topic`, `verify-posts` | 🔒 приватный — [ставится из `sinister-devs/marketing`](#приватные-агенты) |

---

## Установка

### Claude Code

Подключаешь этот репозиторий как маркетплейс — один раз:

```bash
claude plugin marketplace add MichaelTarasov02/Skills
```

Ставишь нужного агента:

```bash
claude plugin install agent-forge@skills
claude plugin install personal-post@skills
```

**Перезапусти Claude Code** (или `/reload-plugins`) — иначе агент не подхватится в текущей сессии.

Проверить:

```bash
claude plugin list
claude plugin details agent-forge@skills
```

### Codex

Codex работает по тому же стандарту [Agent Skills](https://agentskills.io), но ставит
скиллы, а не плагины. Склонируй репо и слинкуй нужные скиллы в общую папку
`~/.agents/skills/` — её читают **и Claude Code, и Codex**:

```bash
git clone https://github.com/MichaelTarasov02/Skills.git ~/team-skills
mkdir -p ~/.agents/skills

# весь агент целиком
ln -s ~/team-skills/agents/agent-forge ~/.agents/skills/agent-forge

# или только нужные скиллы из него
ln -s ~/team-skills/agents/personal-post/skills/new-post ~/.agents/skills/new-post
```

Линкуй, а не копируй — тогда `git pull` в `~/team-skills` обновляет установленное.

Начни новую сессию Codex, чтобы скиллы подхватились.

---

## Как вызывать

Синтаксис зависит от хоста:

| Хост | Вызов |
|---|---|
| Claude Code | `/new-post`, `/agent-forge` |
| Codex | `$new-post`, `$agent-forge` |

Скиллы внутри плагина живут в неймспейсе: `/personal-post:new-post`, `/agent-forge:verify-agent`.

---

## Зависимости

У `personal-post` есть скрипты экспорта визуала на Playwright. После установки:

```bash
cd <путь-к-плагину>/personal-post
npm install
npx playwright install chromium
```

`node_modules/` намеренно не в репозитории — ставится локально.

У `agent-forge` зависимостей нет.

---

## Приватные агенты

Не все агенты публикуются отсюда. `sinister-post` присутствует в этой папке
**симлинком** (чтобы все агенты были в одном месте), но добавлен в `.gitignore`
и распространяется из своего репозитория:

```bash
claude plugin marketplace add sinister-devs/marketing
claude plugin install sinister-post@sinister-marketing
```

Доступ — только у команды Sinister.

**Как сделать своего агента приватным:** положи его источник в нужный репозиторий,
поставь симлинк в `agents/`, добавь строку в `.gitignore` этого репо.

---

## Создать своего агента

Это и есть работа `agent-forge`. Открой агента в папке своего проекта:

```
/agent-forge
```

Он проанализирует проект, покажет предзаполненную форму, соберёт скиллы, упакует
в плагин, установит и напишет документацию. Хочешь сначала посмотреть, что получится,
ничего не создавая — `/agent-forge:analyze-project`.
