# Splitting across sessions

> **Examples below are shapes, not facts about your codebase.** Measure before you quote
> any of them.

Read before phase 3. Where the work will not fit in one session, the specification becomes
a numbered series of prompts.

**The split is approved with the specification, not discovered during implementation.**
Running out of session halfway through is how half-built functionality gets merged: the
code compiles, the feature does not exist, and the next session starts by reconstructing
what the last one was doing.

## Decide whether to split at all

Rough signals, in order of reliability:

| Signal | Suggests |
|---|---|
| More than one layer changes (schema, backend, both clients) | split by layer |
| The plan has more than ~10 steps | split |
| Any step depends on a decision not yet made | split at that seam |
| A migration is involved | split — the migration ships first, alone |
| Everything is in one module and the plan is short | do not split |

**When in doubt, do not.** A split that was not needed costs a handover; a missing split
costs a half-finished merge. But the handover is cheap and predictable, and the half-merge
is neither — so bias toward splitting once the plan passes ten steps.

## Every part leaves the project working

The rule the split exists to satisfy. After each part:

- the project builds
- the tests that passed still pass
- nothing user-visible is half-done — a screen either does not exist yet or works

Where that is impossible, the part is behind a flag, and turning the flag on is its own
final part.

## Order

| Part | Contains | Why here |
|---|---|---|
| 1 | schema and migration | ships alone, reversible, nothing depends on it yet |
| 2 | backend logic and contract | the client can be written against it once it exists |
| 3 | one client | the second client copies it |
| 4 | the other client, bridges, the flag | the coupling work lands last, when the shape is settled |

Adjust for the actual change; keep the property that each part is useful, reversible and
reviewable alone.

## Each part is a self-contained prompt

A part that requires the previous conversation is a part that cannot be run in a fresh
session — which is the entire reason for splitting.

```markdown
# Часть N из M: <название>

## Контекст
<what the feature is, in three sentences — not the whole spec>

## Что уже сделано
<parts 1..N-1, one line each, with the artifacts they produced>

## Что делает эта часть
<the steps, each before → after → why>

## Чего не делает
<explicitly — the later parts, so nothing gets pulled forward>

## Конвенции
<the siblings whose shape to copy>

## Готово, когда
<checkable — the project builds, these tests pass, this behaviour exists>
```

`Чего не делает` is the field that keeps parts from growing. Without it every part absorbs
a little of the next one, and the last part turns out to be most of the work.

## Where the parts live

`.dev-agent/features/<slug>/part-N.md`, beside the specification. They are the artifact
phase 3 produces; phase 4 consumes them one at a time.

## Handover between parts

Each part ends by updating one file — what was done, what the next part assumes, anything
learned that changes a later part:

```
.dev-agent/features/<slug>/progress.md
```

A plan written before any code met the code exactly once. Parts three and four will need
adjusting, and the adjustment belongs here rather than in someone's memory.

**A handover file nobody reads is not a handover.** `progress.md` is the file the *next*
session opens before anything else — see *Before phase 1: is this already in progress?* in
`SKILL.md`. Write it for a reader with no memory of this conversation:

```markdown
# <slug> — прогресс

- Часть: N из M выполнена
- Следующая: part-<N+1>.md
- Артефакты: <files this part produced or changed>
- Проверено: <what was run, with output>
- Изменилось в плане: <what parts N+1..M must now do differently, and why — or "ничего">
- Не делать снова: <phases 1–3 already ran; the spec is spec.md and stands>
```

The last two lines are what stop the next session from re-deriving the design. Without
them it starts at phase 1, produces a second specification, and the two disagree in ways
that surface when the parts fail to fit.

**Delete `progress.md` when the last part lands.** A finished feature that still looks
mid-flight sends every later session down the resume path.
