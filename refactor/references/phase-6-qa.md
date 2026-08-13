# Phase 6 — QA

Three questions, in this order. The first is the one that matters.

## 1. Is the behaviour identical?

Compare against `.dev-agent/refactors/<slug>/baseline.md`, item by item:

| Baseline item | Before | After | Same |
|---|---|---|---|
| ordinary input | <…> | <…> | ✔ |
| empty | <…> | <…> | ✔ |
| error type and message | <…> | <…> | **✘ — <what differs>** |
| result ordering | <…> | <…> | ✔ |
| side effects, and how many | <…> | <…> | ✔ |
| query or call count | <…> | <…> | ✔ |

**Every baseline item gets a row, including the ones that obviously did not change.** A
missing row is indistinguishable from an unchecked one, and the whole pipeline rests on
this table.

A difference here is not a small finding. Either it is intended and was agreed — and then
the change is not purely a refactor and the report says so — or the refactor broke
something.

## 1b. Is the identity identical? — structural changes only

Where `Вид` in the baseline was `структурный` or `оба`, behaviour identity is not the
question. Run the same framework check that produced the baseline, and diff the output:

| Baseline item | Before | After | Same |
|---|---|---|---|
| framework consistency check | <output> | <output> | ✔ |
| proposed migrations / schema diff | none | **none** | ✔ |
| string references to the moved thing | <n, listed> | <n, updated> | ✔ |
| type-check / full import graph | <output> | <output> | ✔ |

**A proposed migration after a pure move is a failure, not a formality.** The framework is
telling you the thing you moved is not the thing that was there — a renamed table, a
changed content type, a new permission codename. Accepting it silently is how a refactor
ships a data migration nobody reviewed.

## 1c. Does the declared contract still hold?

Phase 4 wrote `Не меняем` — the public signature, the error types, the ordering, the call
count. **That list is checked here explicitly, item by item**, and it is not the same
check as the baseline table: the baseline records what the code did, this records what the
plan promised would not move.

| Не меняем (из фазы 4) | Проверено чем | Держится |
|---|---|---|
| <the promise> | <grep, test, diff of signatures> | ✔ / **✘** |

A promise nobody checked is a promise, not a property. This table is why phase 6 is
mechanical rather than a judgement call — which is what phase 4 said when it wrote the
list.

## 2. Is the code actually better?

For `clean` mode, against the findings from phase 3 rather than against a feeling:

| Finding | Addressed | How |
|---|---|---|

Then the mechanical checks:

```bash
<the project's linter and formatter, in check mode>
```

Paste the output. And read the result beside its nearest sibling once more — fit is easier
to judge after the code exists.

**Better means easier for the next person to change.** If the diff is mostly moved lines
and the next change is no easier, the refactor was motion.

## 3. Did the metric move?

For `fast` mode, same method and same data size as the baseline. Different conditions
produce a number that means nothing.

```
до:     <numbers, spread>
после:  <numbers, spread>
цель:   <from phase 1>
```

**Compare against the spread, not against the midpoint.** An improvement inside the
baseline range is not an improvement. Where the target was a user-visible threshold, say
whether it was crossed — the percentage matters less than which side of the line it lands.

And check the other direction: a `clean` refactor should not have made anything slower. A
tidy-up that triples the query count is a common and invisible outcome, which is why the
baseline included the count.

## Say what was not verified

```
Проверено:     <behaviour items, linter, metric — with output>
Не проверено:  <non-empty, always>
```

Always contains something: behaviour under concurrency, the case needing a specific
tenant, the platform not run.

## Ends with

```
Поведение:    <items> / <total> идентичны — <differences, if any>
Идентичность: <framework check clean, zero proposed migrations — or "не применимо">
Контракт:     <"Не меняем" items> / <total> держатся
Код:          <findings addressed> / <total>, линтер <output>
Метрика:      до <…> → после <…>, цель <met | not>
Регресс:      <nothing became slower — or what did>
Не проверено: <non-empty>
```
