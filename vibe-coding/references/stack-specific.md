# Стек-специфичные правила — читать только по совпадению стека

Эти правила из [di-sukharev/vibe](https://github.com/di-sukharev/vibe) привязаны
к конкретному шаблону: TypeScript + Bun + Hono + Prisma + Expo + DigitalOcean,
с их структурой монорепо.

**Применяй только если проект реально на этом стеке.** Для Flutter, Python, Go, Swift
и любого другого — игнорируй этот файл целиком, работай по универсальному ядру
из `SKILL.md`.

---

## ⛔ Что намеренно НЕ перенесено — и почему

Три блока исходного документа опасны вне их шаблона. Они исключены сознательно.

### 1. Git And Remote Policy — риск потери remote

Оригинал предписывает:

> «If `origin` points to the template repository and the user has not explicitly said they
> are contributing to the template, remove it with `git remote remove origin`»

Правило написано для свежего клона шаблона. В обычном рабочем репозитории оно
приведёт к сносу настоящего origin.

### 2. «Работай на master»

Оригинал: *«Work on `master` unless explicitly told otherwise»*.

Проверено на реальных проектах: в `Codex/Skills` основная ветка — **`main`**,
в `ePeople/Dev/whereami-server` — **`build`**. Правило про `master` даст неверное
поведение.

**Вместо этого:** определяй текущую ветку фактически (`git branch --show-current`)
и не создавай новых веток без просьбы.

### 3. Bootstrap-Only Instructions

Относится только к первичной установке их шаблона (интервью по `CHECKLIST.md`,
настройка Expo/EAS, удаление блока после setup). К существующим проектам неприменимо.

---

## Структура модулей (их DDD-lite)

- Продуктовые контексты бэкенда: `backend/src/modules/<context>`; наружу — только через
  `index.ts` или явные порты приложения.
- Hono/HTTP живёт в transport, оркестрация юз-кейсов в application, чистые бизнес-правила
  в domain (только когда правила реально есть), Prisma и SDK провайдеров в infrastructure.
- Клиентские контексты: `src/features/<context>`; маршруты и экраны composе публичные API
  фич, а независимые от эндпоинтов возможности — в `src/platform`.
- Не добавляй пустые слои, generic-репозитории, CQRS, event sourcing и библиотеки
  стейт-машин без конкретной продуктовой потребности.
- Предпочитай монолитный бэкенд. Не дроби на микросервисы без операционной необходимости.

## Prisma

- **Не пиши SQL миграций руками.** Выражай изменения схемы декларативно в `schema.prisma`,
  затем генерируй миграции workflow'ом репозитория.
- Не правь `migration.sql` вручную без явной просьбы.
- Дополнительные проверки, бэкфиллы и guard'ы выката — в владеющем слое бэкенда.

## Библиотеки шаблона

Перед добавлением новой библиотеки смотри `package.json`. Предпочитай уже установленные:
**Zod**, **TanStack Query**, **TanStack Form**, **Hono**, **Prisma**, **Expo**.

## Тестирование в их шаблоне

- E2E: **Playwright** для веба, **Maestro** для мобильного. Перед добавлением потоков —
  `docs/TESTING.md`.
- Мобильные селекторы: стабильные React Native `testID` из `mobile/src/constants/testIds.ts`.
  Не использовать координаты и хрупкие текстовые селекторы.
- Expo dev client + Maestro: запускать против установленного development build, не Expo Go.
  `MAESTRO_DEV_SERVER_URL`, преflight доступности backend/Metro, `EXPO_PUBLIC_E2E=1` только
  в E2E-бандлах.
- Тач-цели в мобильных E2E — около `44–48pt` и больше; не использовать `hideKeyboard`.
- `bun run architecture:check` — при изменении границ модулей, фич, контрактов, platform, UI.
- После изменения потоков Maestro: `bun run --cwd mobile e2e:maestro:audit`.

## Локальная база и окружение

- `docs/LOCAL_DATABASE.md` + `docker-compose.yml` — источник истины по локальному PostgreSQL.
  По умолчанию Docker Compose на всех ОС.
- В шелле Codex не считай, что JS-тулинг в `PATH`. Для `node`, `npm`, `bun` предпочитай
  `PATH="/opt/homebrew/bin:$HOME/.bun/bin:$PATH"`.

## Деплой

- Политика деплоя — в `README.md` и `docs/` (`DEPLOYMENT.md`, `STORAGE.md`, `YANDEX_CLOUD.md`).
- Дефолты DigitalOcean — в `scripts/prepare-do-specs.mjs` и `.do/*.yaml.example`.
- Перед деплоем проверь источник релиза: `git remote -v`, `git status --short --branch`,
  сконфигурированную ветку. Грязное дерево или несинхронизированная ветка — **стоп и отчёт**.
  Не запускай `git reset`, `checkout --`, `clean`, `stash` ради возможности задеплоить.
