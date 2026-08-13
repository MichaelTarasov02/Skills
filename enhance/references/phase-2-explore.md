# Phase 2 — Explore

Where the change lands, what it touches, and what the code says that the ticket does not.

This is the phase that decides whether the work is an enhancement at all.

## Find the place, then read around it

```bash
grep -rn '<the rule in code terms>' <module>
git log --oneline -8 -- <the file>
```

The history matters as much as the file. A file touched three times this month is
contested — someone else may be editing it now, and the plan should say so. A file
untouched for two years is load-bearing in ways nobody remembers.

**Read the callers, not only the function.** A change to a function used in one place is
local; the same change to one used in forty is a different task wearing the same ticket.

```bash
grep -rn '<the function>' . --include='*.py' --include='*.dart' \
  | grep -v migrations | grep -v "def <the function>"
```

**Count call sites, not matches.** A bare `| wc -l` includes the definition, the tests,
the migrations and every comment that mentions the name — and for a function called
`get`, `run` or `check` it returns a number with no relationship to the blast radius.
Print the lines and read them; if there are more than a screen, that is itself the answer.

## Confirm what phase 1 assumed

Phase 1 recorded what the system does now. Verify it, and record the check — an
enhancement built on a wrong description of current behaviour is a rewrite that thinks it
is a tweak.

## Is the calculation frozen — and answer it in the dangerous direction

Snapshots, audit records, signed documents, historical reports. Both answers carry a
consequence and **the answer that sounds safe is the dangerous one**:

| Answer | What it actually means |
|---|---|
| **Frozen** — the value is stored | the change affects new records only. Existing rows keep the old meaning, and the plan must say from which date the two populations differ |
| **Not frozen** — computed on read | **the change rewrites the past.** Every historical record silently acquires the new answer the moment it deploys |

Writing `Заморожено: нет` reads as an absence of risk. It is the opposite: an unfrozen
rule is a rule with no history, so changing it changes what happened. Reports already
issued will not reproduce, records referencing the old outcome become inconsistent, and
nobody is notified because no row was written.

```bash
grep -rn '<the function>' --include='*.py' --include='*.dart' . | grep -v migrations
grep -n '<the value> = models\.\|<the value> = Column' <models file>   # stored anywhere?
```

**Say the retroactive population out loud**, with a number where one is obtainable: how
many existing records change answer. Where the count needs production data, give the query
and do not run it. A retroactive change presented without its population is the most
common way an enhancement turns into an incident.

Where the change must not be retroactive, that is a design decision — an effective date, a
stored flag, a version column — and it belongs to `improve`, not here.

## Surface the contradictions

By the end of this phase you should be able to name every place the ticket and the code
disagree:

| Found | Say it as |
|---|---|
| The behaviour described does not exist | "the ticket describes X; the code does Y — which is intended?" |
| It already does what is asked | "this already happens for A; the case that does not is B" |
| Two rules conflict | "satisfying X breaks Y; the product has not decided" |

Do not resolve these by choosing. A silent choice becomes invisible the moment the PR
merges.

## Enhancement or improvement — decide here

| Signal it is not an enhancement | Why |
|---|---|
| No place obviously owns this | the shape does not exist yet |
| The change needs a new concept named | naming is design |
| The blast radius cannot be established by reading | it is not small |
| Two or more layers change together | the seam has to be designed |

Where two or more fire, say so and stop. Route to `improve`. Continuing produces a
change that fits the code and misses the point.

## Questions for the engineer — collected here, asked at the gate

Only what the code cannot answer: whether this area is being worked on, whether the old
behaviour must stay reachable, which of two conflicting rules wins.

**Collect them; do not ask them here.** They go to the phase-3 gate with the plan beside
them, each carrying your recommended answer — see *One interruption, not three* in
`SKILL.md`. The same question asked now arrives without the plan, which is the context
that makes it answerable in a word instead of a paragraph.

The exception is the one that blocks this phase: without it you cannot find the place, so
there is nothing to plan. Ask that one, alone, and say why it could not wait.

## Ends with

```
Место:        <file and function, with why it is the right place>
Вызывающих:   <n> — <local | wide>
История:      <recent activity, and whether it is contested>
Подтверждено: <what phase 1 assumed, checked>
Заморожено:   <whether anything freezes the current calculation>
Противоречия: <each, unresolved>
Класс:        enhancement | improvement — <and if improvement, stop>
Вопросы:      <≤3, batched>
```
