# Phase 4 — Verdict ⛔ gate

State which branch, what follows from it, and what it costs. Then stop. Nothing is edited
until this is accepted.

A fix applied to a misdiagnosis is worse than no fix: it removes the symptom, leaves the
cause, and consumes the evidence that would have found it.

## The verdict, in the reader's order

```
Что это:      <одна фраза — что произошло на самом деле>
Ветка:        defect | by design | user error | unresolved
Почему:       <правило, цитатой, с путём — и что наблюдалось>
Кого задело:  <сколько аккаунтов, с какого момента, как узнать точнее>
Что дальше:   <fix | вопрос продукту | ответ пользователю>
Цена:         <объём правки и что она задевает — или объём решения>
```

**Blast radius before cost.** The person deciding needs the scale before the estimate.

**Measure it in the unit the branch calls for** — the dimensions are different, and using
the wrong one understates the problem:

| Branch | Measured in | Because |
|---|---|---|
| Defect | accounts, and since when | it decides urgency and whether to backfill |
| By design | **how many places share the undecided rule** | one screen is a ticket; twenty screens is a product decision worth making once |
| User error | how many people made the same mistake | one is support; five is an interface defect |
| Any, where the rule has siblings | **how many of the N symmetric cases carry the guard** | 3 of 4 is an oversight with a one-line fix; 1 of 4 is a policy nobody wrote down |

The last row changes the verdict as often as it changes the estimate. A guard present in
most sibling cases and missing in one is a defect; a guard present in one and missing in
most was never the rule. Count before deciding which — the count is the evidence, and it
takes one grep.

Measured on one investigation: a screen showed nothing distinguishable between "no data"
and "load failed". Counted per account it looked like one customer's annoyance. Counted
per screen — 2 of 70 table screens had a real error state — it was a product-wide gap that
had never been decided, and deciding it once fixed sixty-eight screens.

Where the number is unknown, say what query or grep would produce it. An unquantified
blast radius is the most common reason a verdict gets accepted and then reopened.

## What follows, per branch

### Defect

Propose the fix at the level of the cause, not the symptom. A null check at the crash site
when the value should never have been null is a plaster over a hole.

State what the fix touches. Where it lands in shared code, name the dependants — narrowed
by what actually changes, not by what imports the file.

Then ask for approval and stop.

### By design, wrong for the product

**Do not propose a code change.** Produce the question, and delegate the writing to `copy`
in the team-channel shape — context, options, recommendation, cost of waiting:

```
Система отработала по правилу <X>, заданному <когда и кем, если видно>.
Пользователь ожидал <Y>, и ожидание разумное — <почему>.

Варианты:
(а) оставить как есть — <кого это продолжит задевать>
(б) поменять правило — <объём, что ещё зависит от него>
(в) поменять интерфейс, чтобы правило перестало удивлять — <объём>

Рекомендую <…>, потому что <…>.
```

The recommendation matters. A product owner handed three options and no opinion sends it
back for one.

### User error

Two outputs, and the second is the one teams skip:

1. **The reply** — delegate to `copy`, reply channel. What happened, why, what to do now.
   Never blame, never quote internals, never promise a date.
2. **Did the interface invite it?** If yes, that is a design finding regardless of the
   verdict, and it goes to `review`. If this is the fifth report of the same
   misunderstanding, the interface is the defect and the verdict changes.

Closing a user-error ticket without asking the second question is how the same ticket
arrives again next week.

### Unresolved

A legitimate outcome. Report the narrowest region the evidence allows, what was ruled out
with what, and **the single next step** that would settle it — plus what access or data
that step needs.

Do not fix an unresolved bug. The exception is a change correct regardless of the
diagnosis — a missing error state, an unhandled null — and it ships with a plain statement
that it may not be the reported cause.

## The gate

Ask explicitly, and wait:

> Ветка — <…>. Иду <править код | писать вопрос продукту | писать ответ>?

Approval of the **verdict** is not approval of the **fix**. Where the fix is larger than a
few lines or touches shared code, show its shape before writing it.
