# Phase 5 — Test

Tests written and run, then the specification and the goal checked. Three separate things,
and the third is the one that gets skipped.

## Write tests where the project has a place for them

```bash
ls test/ tests/ __tests__/ 2>/dev/null
find . -name '*_test.*' -o -name '*.test.*' -o -name 'test_*.py' | wc -l
<the project's test command>
```

Where a test suite exists, add to it, matching the shape of the nearest existing test —
same helpers, same fixtures, same naming. A test written in a foreign style is a test the
team stops running.

Where the project has almost none, say so and write what is cheap anyway: the rule the
feature exists for, in one test, is worth more than none and costs little.

**What to test, from the specification's list:**

| Test | Do not test |
|---|---|
| The rule the feature exists for | glue, wiring, getters |
| The boundary someone will get wrong | framework behaviour |
| The bridge that silently under-counts if broken | layout |

**Run them and paste the output.** A test written and not run is a test that does not
compile as often as anyone would like.

## Then check the specification

One row per specification step:

| Шаг | Где в коде | Соответствует |
|---|---|---|

And the other direction: every change in the diff maps back to a step. Anything unmapped
is a consequence the spec missed, an improvement made in passing, or a leftover — and each
has a different answer.

Bridges get their own check. A coupling item marked done in phase 4 and not visible here
was not done.

## Then check the goal — the part that gets skipped

The specification can be fully implemented and the feature still not do what it was for.
Take `Успех` from phase 1 and answer it directly:

```
Цель:        <from phase 1>
Проверка:    <what you did to establish it — a run, a query, a walk through the flow>
Достигнута:  да / частично — <what is missing> / нет — <why>
```

"All steps done" is not the same answer. A report that says the spec is complete and never
mentions the goal has answered the easier question.

Where the goal cannot be checked without production data or a real user, say that plainly
and name what would check it.

## Say what was not verified

```
Проверено:     <tests run, with output; spec traced; goal checked how>
Не проверено:  <non-empty, always>
```

The second line always contains something on a change of this size: performance under real
data, behaviour on the other platform, the case that needs a specific tenant
configuration.

## Ends with

```
Тесты:        <written> / <run> — <output>
Спецификация: <steps> / <total>, мосты <n> / <n>
Непокрытое:   <diff changes not mapped to a step>
Цель:         <achieved | partially | not — with evidence>
Не проверено: <non-empty>
```
