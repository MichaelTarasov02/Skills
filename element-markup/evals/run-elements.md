# Прогоны `element-markup`

## Прогон 1 — пять типов элементов × две платформы

Элементы взяты с реального экрана `active-associates.vue` и его мобильного аналога.

### 1. Иконочная кнопка — экспорт списка

**Vue**
```vue
<a-button type="text" aria-label="Export associate list" @click="exportList">
  <template #icon><DownloadOutlined aria-hidden="true" /></template>
</a-button>
```
Аналитика: **не применима** — в Vue-приложении нет продуктового SDK.
Тест-id: не нужен, находится по role + name.

**Flutter**
```dart
IconButton(
  icon: const Icon(Icons.download),
  tooltip: l10n.exportAssociateListText,
  onPressed: _export,
)
```
Аналитика: предложение `report_exported` со свойством `format`.
Тест-id: `Key('export-associates')` — семь локалей делают поиск по label ненадёжным.

### 2. Поле формы с ошибкой

**Vue**
```vue
<a-form-item
  label="Phone number"
  :validate-status="err ? 'error' : ''"
  :help="err"
  extra="10 digits, US numbers only"
>
  <a-input v-model:value="phone" :aria-invalid="!!err" aria-describedby="phone-help" />
</a-form-item>
```

**Flutter**
```dart
TextFormField(
  decoration: InputDecoration(
    labelText: l10n.enterPhoneNumberText,
    helperText: l10n.phoneNumberHintText,
    errorText: _err,
  ),
  validator: _validatePhone,
)
```
`errorText` связывает ошибку с полем в дереве семантики автоматически — руками не связывать.

### 3. Модальное окно

**Vue** — `a-modal` с `aria-labelledby`, `:keyboard="true"`, `@after-close="restoreFocus"`.
**Flutter** — `showDialog` с `barrierDismissible: false`; ловушка и возврат фокуса встроены.

Разница принципиальная: в Vue возврат фокуса нужно писать руками, во Flutter он есть
по умолчанию. Обратное предположение — источник ошибок при переносе паттерна.

### 4. Список с динамическим обновлением

**Vue**
```vue
<div aria-live="polite" aria-atomic="true">{{ count }} associates found</div>
```
Регион должен быть в DOM **до** появления текста.

**Flutter**
```dart
SemanticsService.announce(l10n.associatesFoundText(count), Directionality.of(context));
```
`Directionality.of(context)` вместо `TextDirection.ltr` — иначе объявление ломается в иврите.

### 5. Кастомный контрол — комбобокс фильтра компаний

**Vue** — `a-select show-search` реализует контракт APG целиком.
**Flutter** — `Shortcuts`/`Actions` с `ArrowDown`, `ArrowUp`, `Enter`, `Escape`;
Escape маппится на встроенный `DismissIntent`.

Вывод по обеим платформам одинаковый: **сначала проверь кит**. Самописный комбобокс,
попавший в четыре клавиши из семи, хуже китового.

---

## Прогон 2 — «нативное прежде ARIA»

**Вход:** «размети кликабельный div как кнопку».

**Выход:**

```vue
<!-- не это -->
<div role="button" tabindex="0" @click="..." @keydown.enter="..." @keydown.space="...">

<!-- это -->
<button type="button" @click="...">
```

Скилл не навесил `role="button"`. Обоснование в выводе: `<button>` даёт фокусируемость,
клавиатуру, объявление роли и состояние disabled без единого атрибута; `div` требует
воспроизвести четыре вещи руками, и space-нажатие обычно забывают.

## Прогон 3 — подчинение плану трекинга

**Проверка:**
```bash
$ ls whereami-flutter-2/.telemetry whereami-server/.telemetry
нет ни в одном репозитории
```

**Выход скилла:**

> Плана трекинга нет. В Flutter присутствует `firebase_analytics: ^11.4.2` — событие
> предлагаю, но как предложение, а не по схеме. В Vue продуктового SDK нет вообще,
> только `@sentry/vue` — слой аналитики неприменим.
> Чтобы это перестало быть предложением, запусти `product-tracking-design-tracking-plan`.

Имя события не выдумано в вакууме: `report_exported` собрано по правилам из
`analytics.md` и помечено как предложение.

## Прогон 4 — расширение вместо создания

**Вход:** «нужно событие на экспорт в CSV, экспорт в Excel уже логируется».

**Выход:**

> Не заводи `report_exported_csv`. Добавь свойство к существующему:
> `report_exported { format: xlsx | csv }`.
> Причина: одно событие с измерением остаётся анализируемым при добавлении форматов;
> два события разбивают один вопрос на два запроса и объединение.

## Прогон 5 — бюджет

```
element-markup/SKILL.md — см. вывод wc -w ниже
```
Лимит из промпта — 3000 слов. Все двенадцать примеров разметки вынесены в
`references/vue.md` и `references/flutter.md`, в теле нет ни одного — намеренно.

---

# Отчёт о покрытии

| ID | Где | Доказательство | Статус |
|---|---|---|---|
| M1 | тело, «Native before ARIA» + оба reference | прогон 2, диф div→button с обоснованием | closed |
| M2 | vue.md, flutter.md | прогон 1.1, обе платформы; имя описывает действие | closed |
| M3 | vue.md, flutter.md | пустой alt / `ExcludeSemantics` как явное решение | closed |
| M4 | vue.md, flutter.md | DOM-порядок, запрет положительного tabindex, RTL-оговорка | closed |
| M5 | vue.md, flutter.md | прогон 1.3, включая различие платформ по возврату фокуса | closed |
| M6 | vue.md, flutter.md | `:focus-visible`, тема Flutter; оговорка «проверять с клавиатурой» | closed |
| M7 | vue.md, flutter.md | прогон 1.4, polite vs assertive, `Directionality.of` | closed |
| M8 | analytics.md | прогон 3 — плана нет, сказано прямо | closed |
| M9 | analytics.md | таблица include/exclude, лимиты Firebase | closed |
| M10 | analytics.md | прогон 4 | closed |
| M11 | vue.md, flutter.md | инверсия: сначала доступное имя, id только когда имени нет | closed |
| M12 | vue.md, flutter.md | прогон 1.5, полный контракт клавиш комбобокса | closed |

Все двенадцать закрыты. **Не проверено на живом продукте:** прогоны 1–5 показывают
разметку, но ни один элемент не размечен в реальном коде `whereami` и не проверен
скринридером. Это ограничение прогона, а не покрытия — реальная проверка VoiceOver и
TalkBack требует устройства.
