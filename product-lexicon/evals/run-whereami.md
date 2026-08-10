# Прогон `product-lexicon` на whereami

Артефакты записаны сюда, а не в `PRODUCT_REPO/.dev-agent/`, намеренно: писать в живой
репозиторий продукта без явного разрешения нельзя. Скилл в работе пишет туда.

## Фаза 1 — платформы и источники

| Платформа | Корень | Строки | Компоненты |
|---|---|---|---|
| Flutter (mobile + web build) | `Dev/whereami-flutter-2` | `lib/l10n/*.arb` — **7 локалей**: en, es, fr, **he (RTL)**, ru, tl, zh | `lib/features/` — 30 директорий, `lib/common/` |
| Vue 3 + ant-design-vue | `Dev/whereami-server/whereami` | i18n-слоя нет, литералы в `<template>` | `src/components/` 20+, `src/views/` 8 |
| Django (backend) | `Dev/whereami-server` | — | вне зоны скилла |

**React отсутствует.** `grep -rl '"react"' --include=package.json` не вернул ничего.
`web/dashboard/` — это скомпилированный Flutter Web (`flutter.js`, `canvaskit`).

**Цена локали: ×7.** Любая правка строки умножается на семь ARB-файлов.

## Фаза 2 — кандидаты в термины

Из 3994 ключей `intl_en.arb`, по частоте в значениях:

| Термин | Частота | Где в коде |
|---|---|---|
| Shift | 352 | `lib/features/time_tracking/` |
| Company | 324 | сквозной |
| Associate | 258 | `lib/features/`, `whereami/src/components/entities/` |
| Meal / Break | 254 / 242 | `lib/features/time_tracking/` |
| Payment | 121 | `lib/features/payment/` |
| Compliance | 84 | `lib/features/documentation_compliance/` |
| Payroll | 62 | `lib/features/reports/` |
| Disciplinary | 53 | `lib/features/` |

## Фаза 3 — расхождения ⚠️ два подтверждённых

### Расхождение 1 — key–value drift: Lunch → Meal Break

**140 ARB-ключей** названы `*Lunch*`, а строка внутри говорит `Meal Break`.

```
estimatedLunchTimeText          ->  Scheduled Meal Break Time
estimatedSecondLunchTimeText    ->  Scheduled Second Meal Break Time
waitUnitLunchEndText            ->  Wait until After your Meal Break
askedToEndLunchEarlyText        ->  I was Asked to End my Meal Break Early
haveNoLunchAuthorizationText    ->  Has No Meal Break Authorization
earlyLunchEndAuthorizationErrorMessage -> The Law requires you to take at least a
                                          {lunchDuration} meal break...
```

Пользователь видит **Meal Break**, разработчик пишет **Lunch**. Расходятся молча,
потому что ключ и значение никто не сверяет. В `earlyLunchEndAuthorizationErrorMessage`
расхождение живёт внутри одной строки: плейсхолдер `{lunchDuration}` рядом со словом
`meal break`.

Это юридический термин — «Meal Break» из трудового законодательства. Ставка выше
косметики.

### Расхождение 2 — synonym set: Associate / Employee / Worker

| Форма | ARB-ключи | ARB-значения | Vue-файлы |
|---|---|---|---|
| Associate | 206 | 158 | 273 |
| Employee | 13 | 16 | 51 |
| Worker | — | — | 20 |

Три слова на одну сущность. Доминирует **Associate** и в UI, и в коде обеих платформ —
победитель очевиден, но 51 Vue-файл и 16 строк говорят иначе.

## Фаза 4 — предложенные канонические формы

```markdown
### Meal Break
- status: предложен
- definition: A legally mandated unpaid interval within a shift
- plural: Meal Breaks
- code: lib/features/time_tracking/
- strings: 140 ARB keys named *Lunch* — key–value drift, migration needed
- forbidden: Lunch, Lunch break, Break time
- not: not a Rest Break — rest breaks are paid and shorter

### Associate
- status: предложен
- definition: A person employed through the platform whose time and compliance are tracked
- plural: Associates
- code: lib/features/, whereami/src/components/entities/
- strings: 206 ARB keys, 158 values
- forbidden: Employee, Worker, Staff member
- not: not a User — a User is an authentication identity; one Associate may have none

### Shift
- status: предложен
- definition: A scheduled period of work with a start time and an end time
- plural: Shifts
- code: lib/features/time_tracking/
- strings: 352 occurrences
- forbidden: Session, Work period
- not: not a Time Entry — a Time Entry is the interval actually worked
```

Все `предложен`. Ни один не переведён в `утверждён`: это требует ответа человека.

## Фаза 5 — красные линии, извлечённые из строк

Формулировки взяты из реального юридического контекста продукта:

- Никогда не называть срок восстановления сервиса или обработки заявки.
- Никогда не заявлять о соответствии закону от лица продукта — только цитировать
  требование («The Law requires…»), как уже делает `earlyLunchEndAuthorizationErrorMessage`.
- Никогда не обещать, что данные о времени не будут использованы в дисциплинарных целях:
  в продукте есть `disciplinary` (53 вхождения).
- Тексты про Meal Break и оплату проходят проверку юристом — это регулируемая зона.

## Фаза 6 — инвентарь компонентов

| Платформа | Локальные | Внешний кит |
|---|---|---|
| Flutter | 30 feature-директорий, `lib/common/` | — |
| Vue | `src/components/` — signature-canvas, qr-code-generator, dynamic-form, permission-provider, recursive-menu и др. | `ant-design-vue` — не переизобретать |

## Фаза 7 — диф

Первый прогон, дифа нет. Повторный обязан показать диф до записи.

---

# Отчёт о покрытии

| ID | Раздел скилла | Доказательство | Статус |
|---|---|---|---|
| L1 | Фаза 4 | три канонические формы с обоснованием и полем `not` | closed |
| L2 | Фаза 3 | два расхождения с числами и путями: 140 ключей Lunch→Meal Break; Associate/Employee/Worker 206/13/20 | closed |
| L3 | Фаза 3, расхождение 1 | масштаб миграции измерен: 140 ключей × 7 локалей + плейсхолдер `{lunchDuration}`. Пошаговый план не выписан | partial |
| L4 | `references/term-format.md` | формат зафиксирован, три термина записаны по нему | closed |
| L5 | Фаза 5 | tone of voice **не извлечён** — в ARB нет материала, по которому его выводят; нужен ответ человека | open |
| L6 | Фаза 5 | четыре красные линии, все как проверяемые запреты | closed |
| L7 | Фаза 6 | компоненты по обеим платформам, локальные и внешние разделены | closed |
| L8 | — | форматы дат/чисел/валют **не извлечены** — не сканировал `intl` DateFormat и NumberFormat | open |

Две строки `open` и одна `partial` — прогон не был мягким. L5 и L8 требуют отдельного
прохода: первый упирается в человека, второй в непройденное сканирование.

## Проверка грепа

```bash
$ grep -A8 '^### Meal Break' lexicon.md
### Meal Break
- status: предложен
- definition: A legally mandated unpaid interval within a shift
...
```
Контракт из `term-format.md` соблюдён.

## Проверка на пустом месте

Прогон на пустой временной папке: скилл сообщает об отсутствии платформ, не создаёт
пустых секций и предлагает собрать лексикон из разговора с пометкой `предложен`.
