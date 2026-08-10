# Доступы к прод-окружению

Читай этот файл, когда база, логи или ветка не отвечают, либо когда нужно поднять доступ с нуля. При штатном разборе он не нужен: если туннель уже поднят и MCP отвечает, иди дальше.

Три независимых канала: логи, база, код. Проверяются по отдельности, ломаются тоже по отдельности.

## Быстрая проверка всех трёх

```bash
# 1. Логи — MCP-сервер epeople_logs
claude mcp get epeople_logs

# 2. База — туннель
bash "${CLAUDE_PLUGIN_ROOT}/skills/analyze-case/scripts/db-tunnel.sh" up
export PATH="/opt/homebrew/opt/libpq/bin:$PATH"
psql -h localhost -p 15433 -U sp -d whereami_bb -tAc "SELECT 1;"

# 3. Код — ветка, развёрнутая в проде
git -C /Users/mihail_tarasov/Codex/ePeople/Dev/whereami-server rev-parse --abbrev-ref HEAD
```

Ожидаемо: `✔ Connected`, `1`, `build`.

## Логи

MCP-сервер `epeople_logs`, инструменты `list_logs`, `tail_log`, `grep_log`. Ходит по SSH на хост `prod` (34.209.2.122) и читает `/app/logs` внутри контейнера `whereami-production-bb-task`.

Не отвечает — проверь SSH напрямую, это отсекает половину причин:

```bash
printf '{"action":"list"}' | ssh prod /usr/local/bin/prod-log-reader
```

Ключ `~/.ssh/rolotex_keys.pem`, права строго `600`. Алиас `prod` в `~/.ssh/config`.

**Известное ограничение:** `grep_log` по ротированным `request.log` падает с `exited with code -9` — ридер убивает процесс по 30-секундному таймауту, файлы слишком велики. Обход: сузить паттерн до самой редкой строки, взять `tail_log` для свежих событий, или искать в `errors.log` / `general.log` за ту же дату.

## Базы

**Обе системы на одном сервере.** Отличается только имя базы:

| Система | База | Где данные |
|---|---|---|
| ePeople | `whereami_bb` | схема `public` |
| Schedule | `portal` | схемы по тенантам: `sfhcr` (306 таблиц), `sfhcr2` (287) |

RDS внутри VPC, снаружи не резолвится. Только через SSH-туннель на локальный порт 15433.

```bash
bash "${CLAUDE_PLUGIN_ROOT}/skills/analyze-case/scripts/db-tunnel.sh" up
bash "${CLAUDE_PLUGIN_ROOT}/skills/analyze-case/scripts/db-tunnel.sh" psql            # ePeople
bash "${CLAUDE_PLUGIN_ROOT}/skills/analyze-case/scripts/db-tunnel.sh" psql portal     # Schedule
bash "${CLAUDE_PLUGIN_ROOT}/skills/analyze-case/scripts/db-tunnel.sh" q "SELECT 1"
bash "${CLAUDE_PLUGIN_ROOT}/skills/analyze-case/scripts/db-tunnel.sh" q portal "SELECT 1"
bash "${CLAUDE_PLUGIN_ROOT}/skills/analyze-case/scripts/db-tunnel.sh" down
```

Учётка `kl_ro_user`, пароль в `~/.pgpass`. `psql` в `/opt/homebrew/opt/libpq/bin`.

**Read-only обеспечен сервером, а не дисциплиной.** У роли выставлен `default_transaction_read_only`, любая запись отбивается: `ERROR: cannot execute DELETE in a read-only transaction`. Флаги `rolsuper`, `rolcreatedb`, `rolcreaterole` — все false. Проверено на обеих базах.

Это снимает прежнее ограничение про ручную осторожность: сломать данные технически невозможно.

**Не перепутай кластер.** Рабочий — `production-knowledgeloop-portal.cluster-ciygynwc56k0.us-west-2.rds.amazonaws.com`. Есть похожий `staging-knowledgeloop-portal...` — он отстаёт на десятки миграций.

**Запросы к Schedule всегда с указанием схемы:** `SELECT ... FROM sfhcr.schedule_assignments`. Без префикса таблица не найдётся.

## Код

В проде развёрнута ветка **`build`**, не `master`. Разница достигала 90 коммитов.

```bash
cd /Users/mihail_tarasov/Codex/ePeople/Dev/whereami-server
git fetch origin build && git checkout build && git pull --ff-only
```

Разбор бага по `master` — это чтение кода, который в проде не исполняется.

Репозитории: сервер `Dev/whereami-server` (кроме подпапки `whereami/`), веб `Dev/whereami-server/whereami`, мобильное `Dev/whereami-flutter-2`.

## Если что-то не работает

| Симптом | Причина | Что делать |
|---|---|---|
| MCP `Failed to connect` | сервер не зарегистрирован или упал | `claude mcp get epeople_logs`, при отсутствии зарегистрировать заново |
| SSH `Permission denied` | права на ключе | `chmod 600 ~/.ssh/rolotex_keys.pem` |
| `psql: connection refused` | туннель не поднят | скрипт `up`, проверить `lsof -nP -iTCP:15433 -sTCP:LISTEN` |
| `column does not exist` | не тот кластер | проверить, что туннель смотрит на `production-`, а не на `staging-` |
| `grep_log` код `-9` | таймаут ридера на большом файле | сузить паттерн или взять другой лог |
