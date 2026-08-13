# Phase 5 — Implement

The plan, one small step at a time, with the baseline check after each.


## Defend the boundary — it is this phase's job, not phase 1's

Phase 1 wrote `Не трогаем`. **Re-read it before each step**, because the boundary is not
crossed by decision — it is crossed one tempting line at a time, while already inside a
file for another reason.

```
Не трогаем (из фазы 1):  <paste it here, verbatim>
```

Anything outside it that turns out to be wrong is **recorded and left**:

```
Замечено вне границы:  <what> — <rough size> — не трогаю
```

A refactor that grows is a refactor that does not land, and an unlandable refactor leaves
the next person with both the mess and a stale branch attempting to fix it. Where the
boundary genuinely has to move — the change is impossible without it — that is a sentence
back to the engineer, not a decision taken inside the implementation.

## The rhythm

```
one step  →  run the behaviour check  →  green  →  next step
                                      →  red    →  stop, understand, revert if unclear
```

**Run the check after every step, not at the end.** The whole reason for small steps is
that a red check names the culprit. Batching five steps and then checking gives you a
failure and five suspects.

Where the check is characterisation tests, this is seconds. Where it is manual, it is the
cost of doing this work safely — and if that cost is too high, the baseline was too weak
and phase 2 should have said so.

## Defend the boundary

Phase 1 wrote what is out of scope. Things will appear during the work that are ugly,
adjacent and quick:

| Temptation | What it costs |
|---|---|
| Tidy the function next door | the diff stops being reviewable as one change |
| Fix the bug you just understood | behaviour changes inside a behaviour-preserving change |
| Rename something outside the scope | the diff fills with noise that hides the real moves |
| Optimise something you noticed | unmeasured, unplanned, unverifiable |

Record each. Size each. Leave each. The report has a section for exactly this.

## Ask rather than decide

Where the plan meets something it did not anticipate — a caller with a different
assumption, a behaviour that turns out to be depended on, a move that is not as safe as it
looked — stop and ask.

A refactor that improvises is a refactor whose behaviour argument no longer holds, and
nobody can tell from the diff where that happened.

## Keep the two kinds of change separate in the history

Structural moves and performance changes in separate commits, even when they land in one
pull request. When something regresses, the bisect is then meaningful.

## Ends with

```
Шаги:        <done, mapped to the plan>
Проверка:    <the behaviour check, run after each step — with output>
Отклонения:  <where the plan was wrong, and what was agreed>
Не трогал:   <the temptations, named and sized>
Коммиты:     <structural and performance, separated>
```
