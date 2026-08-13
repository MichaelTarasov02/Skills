# Phase 4 — Implement

The specification, applied. Nothing outside it.

**Read `skills/enhance/references/conventions.md` before starting** — fit is judged the same way
here, and the method is the same. This phase adds only what changes at scale.

## Follow the spec, and stop when it is wrong

A large specification will be wrong somewhere: a case it did not anticipate, a coupling it
missed, an assumption the code contradicts. **Stop and say so.** Do not improvise inside
the implementation.

The larger the change, the more this matters: a small divergence in step 3 quietly
invalidates steps 7 and 11, and nobody notices until the tests.

## Work step by step, in the specified order

The order exists so the project builds between steps. Reordering to "do the interesting
part first" produces a half-hour where nothing compiles and a debugging session about
which half is broken.

After each step, or each small group: does it still build, do the existing tests still
pass. Finding a break at step 4 costs minutes; finding it at step 12 costs an evening.

## Bridges are steps, not afterthoughts

Every coupling item is its own numbered step, and it gets the same care as the core
feature. The temptation at step 9 of 12 — with the feature already working — is to treat
the remaining bridges as paperwork. They are the part that decides whether the numbers
reconcile next month.

## Do not let the change grow

| Temptation | Why not |
|---|---|
| Refactor something ugly nearby | makes the change unreviewable; report it instead |
| Fix a small unrelated bug | same, and it hides in a large diff |
| Pull work forward from a later part | breaks the property that each part is reviewable alone |
| Add a feature nobody asked for | it will ship, unreviewed, forever |

Report each. Size each. Leave each.

## Filling gaps stays visible

Anything the task did not specify and phase 2 filled: keep it marked in the report. A gap
filled in phase 2, approved, and then silently reworded in phase 4 is a decision nobody
reviewed.

New gaps discovered while implementing get the same treatment — fill, mark, ask for
approval. Do not decide silently because the phase is late.

## Handover, if split

At the end of each part, update `progress.md`: what was done, what the next part assumes,
and anything learned that changes a later part. A specification written before any code
met the code exactly once; parts three and four will need adjusting, and the adjustment
belongs in writing.

## Ends with

```
Реализовано:  <steps done, mapped to the spec>
Отклонения:   <where the spec was wrong, and what was agreed instead>
Мосты:        <each coupling item, done or explicitly deferred>
Пропуски:     <gaps filled, with their approval status>
Не делал:     <nearby problems, named and sized>
Передача:     <progress.md updated — part N of M, what changes for parts N+1..M>
Сборка:       <builds, existing tests pass — with output>
```
