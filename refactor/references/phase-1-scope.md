# Phase 1 — Scope

What is being improved, in which mode, and where the boundary is.

## Establish the unit

| The task names | The unit is | Watch for |
|---|---|---|
| A function or a call | that function and what it calls | it usually spreads one level further than expected |
| A block inside a longer function | the block, and whether extracting it is the refactor | extracting changes call order — that is behaviour |
| A screen or a feature | the feature's own files, not everything it imports | a shared helper touched here affects other features |
| "This module is a mess" | **narrow it** — pick the worst part | a whole-module refactor lands or does not land |

**Narrow aggressively.** A refactor that grows never lands, and an unlandable refactor is
worse than none: the branch rots, and the next person inherits both the mess and a stale
attempt at fixing it.

## Draw the boundary in writing

```
В работе:    <files, functions — named>
Не трогаем:  <adjacent things, however tempting>
Причина:     <why the boundary is here>
```

`Не трогаем` is the field phase 5 defends. Without it written down, the boundary moves
every time something ugly appears next to something being edited.

## The mode

```
Режим: clean | fast | both
```

Take it from the task where it is stated. Where it is not, infer and say so:

| The task says | Mode |
|---|---|
| "тормозит", "долго", a number | `fast` |
| "каша", "не читается", "тяжело менять" | `clean` |
| "пробегись по этому куску" | `both` |

## Context the task brought

Large refactor requests often arrive with evidence — analytics, a timing, a complaint,
a review comment. Record it: it is the target, and without a target an optimisation
succeeds by definition.

```
Что известно:  <timings, frequency, user complaints, review comments>
Цель:          <what improvement would count as success>
```

Where nothing came with the task, say so — phase 2 will have to establish the baseline
from scratch, and that is more work than the refactor sometimes.

## Is refactoring the right answer at all

Two cases where it is not, and both are worth saying out loud:

**The code is fine and the problem is elsewhere.** A slow call over an unindexed table is
not a code-quality problem, and tidying it will not help.

**The right answer is to replace it.** Where the structure is wrong rather than untidy,
incremental refactoring converges slowly or not at all. Say so — it is a different
decision with a different risk profile, and it belongs to the engineer.

## Ends with

```
Единица:     <what is being improved>
Режим:       <clean | fast | both, with why>
Граница:     <in, out, reason>
Контекст:    <what the task brought>
Цель:        <what success looks like>
Оговорка:    <if refactoring is not the right answer — say it here>
```
