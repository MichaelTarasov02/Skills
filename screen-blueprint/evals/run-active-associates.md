# Прогон `screen-blueprint` на `active-associates.vue`

Экран: `whereami-server/whereami/src/views/active-associates.vue`, 178 строк.
Отчёт об экране, который **уже написан** — проверка №2 из промпта: найти, каких
состояний не хватает в реализации.

## Фаза 1 — существующая конвенция

Флаговая: `data()` возвращает `loading: false`. Ошибка не хранится в состоянии вообще —
она уходит в `notification.error`. Значит на экране состояния ошибки нет, есть только
всплывающее уведомление, после которого остаётся пустая таблица.

```js
async loadData() {
  this.loading = true
  await this.$store.dispatch('report/getActiveAssociatesReport', {...})
    .then(data => { this.tableData = ... })
    .catch(() => {
      notification.error({
        message: 'Error',
        description: 'An error occurred while loading the Active Users Report. Please try to open this page later'
      })
    })
  this.loading = false
}
```

## Фаза 2 — матрица состояний против реализации

| Состояние | В коде | Проверка |
|---|---|---|
| Success | есть — `a-table` с `tableData` | ✅ |
| Loading | есть — `:loading="loading"`, кнопки `:disabled="loading"` | ✅ |
| Partial | нет | ❌ отчёт грузится одним запросом, частичного нет — **допустимо**, но не помечено |
| Empty | **нет** — `grep -cE "a-empty\|emptyText\|no-data"` → `0` | ❌ падает в дефолт `a-table` → `No Data` |
| Error | только тост, экран остаётся пустым, retry нет | ❌ |
| Offline | **нет** — `grep -c "internet-connection"` → `0`, хотя компонент в проекте есть | ❌ |
| No access | **нет** — `grep -ci permission` → `0`, хотя есть `permission-provider.vue` и `no-permissions.vue` | ❌ |

**Пять из семи состояний не отвечены.** Три из них — empty, offline, no access — имеют
в этом же репозитории готовые компоненты, которые экран не использует.

Empty здесь особенно дорогой: экран фильтруется по диапазону дат. Пользователь, выбравший
период без данных, увидит `No Data` — тот же экран, что и пользователь, у которого
вообще нет ассоциатов. Два разных положения, один ответ.

## Фаза 3 — граничные данные

Таблица без пагинации и без виртуализации, `:scroll="{ x: 600 }"` — только горизонтальный.
Тысяча ассоциатов отрендерится целиком. Длинное имя в колонке не имеет правила обрезания.

## Побочная находка — терминология

В файле `Associate`/`Associates` встречается 9 раз, включая `active_associates_data` и
`associate_number`. Единственная строка, которую **читает пользователь**, говорит
`Active Users Report`.

Это расхождение №2 из прогона `product-lexicon` (Associate / Employee / Worker), пойманное
на живом экране: код говорит канонически, UI — нет.

Текст ошибки нарушает и правила стиля из `interface-copy`: `message: 'Error'`, «An error
occurred», «Please», и «try to open this page later» — обещание без срока и без retry.

---

# Blueprint: Active Associates

## Placement
- route: `/active-associates`, guard: не проверен — экран не обращается к правам
- parent: `recursive-menu`, раздел отчётов
- back: возврат в меню отчётов

## States

### Success
- shows: таблица ассоциатов за выбранный период
- component: `a-table`

### Loading
- shows: спиннер поверх таблицы, кнопки disabled
- component: `a-table :loading`

### Partial
- not applicable: отчёт приходит одним запросом, частичной загрузки нет

### Empty — nothing created yet
- shows: объяснение, что ассоциаты появятся после первой смены
- slot: empty.none-created
- component: `a-empty` с переопределённым description

### Empty — filter matched nothing
- shows: сводку выбранного периода и действие сброса
- slot: empty.no-results
- component: `a-empty` с переопределённым description

### Error
- shows: состояние на экране, не тост; сохранённый фильтр; кнопка повтора
- slot: error.load-failed
- component: `a-result` status="error"

### Offline
- shows: баннер отсутствия связи, таблица из последнего успешного ответа если есть
- slot: error.offline
- component: `internet-connection-alert`

### No access
- shows: объяснение, кто выдаёт доступ к отчётам
- slot: empty.access
- component: `no-permissions` view

## Text slots
- SLOT: empty.none-created | type: empty-state/created | context: no associates have ever worked a shift
- SLOT: empty.no-results | type: empty-state/filter | context: date range excludes all associates
- SLOT: empty.access | type: empty-state/access | context: user lacks the reports permission
- SLOT: error.load-failed | type: error | context: report request failed, retry available
- SLOT: error.offline | type: error | context: device has no connection, cached data may be shown
- SLOT: action.export | type: action | context: downloads the filtered list to Excel

## Interactive elements
- ELEM: date-range-picker | role: input | action: filters the list | state: disabled while loading
- ELEM: export-button | role: button | action: downloads Excel | state: disabled while loading or empty
- ELEM: retry-button | role: button | action: repeats the failed request | state: visible in Error only

## Boundary data
- 0 associates → Empty, one of two kinds by cause
- 10 000 associates → таблица без пагинации и виртуализации, рендерится целиком
- очень длинное имя → правила обрезания нет
- период без данных → Empty/filter, не Empty/created

## Components
- reuse: `a-table`, `a-empty`, `a-result`, `internet-connection-alert`, `no-permissions`
- new: ни одного — всё нужное в репозитории есть

## Open questions
- Кто выдаёт доступ к отчётам — решает продукт
- Нужна ли пагинация при 10 000 строк — решает разработчик по реальному объёму
- `Active Users Report` → `Active Associates Report`: правка строки, решает продукт
