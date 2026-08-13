# Phase 7 — Report

Before and after, on both axes, verifiable without rerunning the work.

The reader's question is narrow and specific: **did this change anything it should not
have, and did it achieve what it claimed?**

## Structure

```markdown
# Рефакторинг: <что>

## Зачем
<the problem — the measurement, the complaint, or the reason the code was hard to change.
 Not "код был плохой">

## Режим
clean | fast | both — <and what success meant>

## Что было не так
<the audit findings that were acted on, ranked as they were ranked>

## Что изменилось в коде
| Файл | Что |
|---|---|

было:
    <fragment>
стало:
    <fragment>
почему: <one line — the finding it addresses>

<two or three key moves; the rest named, not quoted>

## Поведение не изменилось
| Проверка | До | После |
|---|---|---|
<every baseline item — this is the section the reviewer reads first>

## Идентичность не изменилась
<structural changes only — omit the section entirely for a purely behavioural one>

| Проверка | До | После |
|---|---|---|
| <framework consistency check> | <output> | <output> |
| предложенных миграций | 0 | **0** |
| строковых ссылок на перемещённое | <n> | <n, обновлено> |

## Контракт держится
| Не меняем (фаза 4) | Проверено чем | Держится |
|---|---|---|

## Метрика
до: <numbers, spread>  →  после: <numbers, spread>
цель: <met | not, and by how much>
<and: nothing became slower — or what did>

## Чего не трогали
<what was out of scope, and what was noticed during the work and left>

## Найденные баги
<found during the audit, not fixed here, routed>

## Что осталось
<non-empty by default>
```

## The section that carries the report

**`Поведение не изменилось`.** It is why the reader opened the document. A refactor
report without a behaviour table is a claim; with one, it is evidence — and it is the
table a reviewer will check line by line before approving a diff that says "no functional
changes".

Keep the rows that did not change. They are the difference between checked and assumed.

**For a structural change that table is not enough and can be actively misleading.** Every
behaviour row will read ✔ while a table has been renamed and every migration naming the
old path has stopped importing. `Идентичность не изменилась` is the section that carries a
structural report, and omitting it while keeping the behaviour table produces a document
that says "verified" about the axis that was not the risk.

## Numbers, not adjectives

"Стало чище" and "работает быстрее" are the two sentences this report exists to replace:

| Instead of | Write |
|---|---|
| стало чище | функция была 140 строк и делала три вещи, стало три функции по одной |
| быстрее | 3 запроса вместо 47; 210±20ms вместо 890±60ms |
| понятнее | вложенность 5 → 2, спецслучай виден в сигнатуре |
| масштабируемее | линейно по строкам вместо квадратично — на 10k строк это <…> |

## Delegate the check and the description

Run it through `review` in `change` and `perf` modes before publishing; findings go into
`Что осталось`.

The PR description is `copy`, team channel — and for this kind of change it leads with the
behaviour table, because that is what the reviewer needs to trust before reading anything
else.

## Where it lands

`.dev-agent/refactors/<slug>/report.md`, beside the baseline. The pair is the evidence:
what the behaviour was, and that it still is.

## Ends with

```
Отчёт:        <path>
Вид:          поведенческий | структурный | оба
Поведение:    идентично | <differences and their status>
Идентичность: <clean | не применимо | what moved>
Контракт:     <"Не меняем" держится> / <total>
Код:          <findings addressed> / <total>
Метрика:      <before → after, target met or not>
Осталось:     <non-empty or explained>
Тексты:       <PR description drafted — not sent>
```
