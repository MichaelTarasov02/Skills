# Phase 4 — Plan ⛔ gate

The steps, each one behaviour-preserving on its own.

## Every step is a named transformation

Not "clean up the function" — a specific move with a known safety property:

```
N. <transformation> в <path>:<place>
   было:      <shape>
   станет:    <shape>
   почему:    <which finding this addresses>
   поведение: <why it cannot change — or what pins it if it might>
```

The named moves, each safe for a different reason:

| Move | Preserves behaviour because |
|---|---|
| Extract a function | the same statements run in the same order |
| Rename | nothing but the identifier changes |
| Inline | the call is replaced by its body |
| Introduce a variable | the expression is evaluated once, in the same place |
| Replace a condition with a guard clause | the branches are the same, read differently |
| Move a member | callers are updated together |
| Batch a query | **not automatically safe** — ordering and laziness change |

The last row is the point of the table. Performance moves are usually *not* automatically
behaviour-preserving, and each one needs its own sentence saying what pins it.

## Small steps, each independently revertible

A refactor lands as a sequence of small changes, each leaving the project working and each
revertible alone. This is not neatness — it is the only way to find which step broke
something when the tests go red at step nine.

Where a step cannot preserve a working state, it is two steps.

## Order

| Order | Reason |
|---|---|
| Behaviour-pinning first | write the characterisation tests before touching anything |
| Then structural moves | extract, rename, inline — safe, mechanical |
| Then performance changes | riskier, and easier to verify against a tidied structure |
| Never mixed within a step | a step that both restructures and optimises is unreviewable |

**Never mix a structural move and a performance change in one step.** When behaviour
shifts, that step is the one you cannot bisect.

### The order inverts when phase 3 recorded a conflict

The table above assumes the two kinds of work are independent, which is the usual case.
**Where phase 3's audit filled `Конфликт:` — the readable shape and the fast shape are not
the same shape — performance goes first**, and the tidying is done afterwards, on the
structure that survived.

| `Конфликт` in phase 3 | Order |
|---|---|
| empty | structural moves, then performance — as above |
| non-empty | **performance first**, then tidy what remains |

The reason is asymmetric cost. A structure optimised for readability sometimes cannot be
made fast without partly undoing it; the reverse is rare. Tidying first in that case means
doing the tidying twice, and the second pass happens under the pressure of a change that
is already late.

**Say which order you took and why**, in one line. Where the conflict is a genuine
trade-off rather than a sequencing problem — the fast shape will stay harder to read — that
is a decision for the gate, not a preference to exercise inside the plan:

```
Порядок:   производительность → чистка, потому что <the conflict from phase 3>
Компромисс: <what stays less readable, and what it buys> — или "нет"
```

## Say what will not change

```
Не меняем:  <the public signature | the error types | the ordering | the call count>
```

This is the contract the QA phase checks. Listing it here makes phase 6 mechanical instead
of a judgement call.

## The gate

```
Шаги:       <numbered, each with its behaviour argument>
Порядок:    <and that each leaves the project working>
Не меняем:  <the contract>
Риск:       <the steps where behaviour could move, and what pins them>
Ожидаем:    <the metric target, for fast mode>

План такой. Иду делать?
```

Two things to watch for while waiting: a step the engineer knows is riskier than it looks
because something external depends on it, and a finding they would rather leave alone.
