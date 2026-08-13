# Phase 2 — Design ⛔ gate

How the new functionality merges into what exists. The phase where large changes are won
or lost.

**Read `references/coupling.md` before starting.** Most of this phase's value is the map of
what else must change.

## Understand the system before extending it

Read what exists, in this order:

| Read | For |
|---|---|
| Documentation, if any | the intended structure — then verify it against the code |
| `.dev-agent/config.yaml`, `lexicon.md` | platforms, conventions, whether this concept is already named |
| The nearest comparable feature | the shape a feature of this kind takes here |
| The models the change touches | what is stored, what is derived, what is frozen |

**Where documentation and code disagree, the code wins and the disagreement is a finding.**
Documentation describing structure the code abandoned is worse than none: it produces
designs that fit a system nobody has.

**The nearest comparable feature is the highest-value read.** A product that has built
something of this kind before has a shape for it — where the model lives, how the screen
reaches it, which layer owns the rule. A design ignoring that shape produces functionality
that works and looks imported from another codebase.

## Design the merge, not the feature in isolation

| Question | Why it decides the design |
|---|---|
| Where does this belong | the module that owns the concept, not the one you opened first |
| What does it extend | an existing base, builder, or pattern — or genuinely nothing |
| What does it need from what exists | settings, permissions, rules it must respect |
| What must know about it | the coupling map |
| What can it not break | frozen calculations, historical records, contracts |

Delegate the pieces that have owners: `spec` in `screen` mode for interface states, `data`
mode for schema and contracts. This phase decides how they fit together — the seams
between them are its own work.

## Where the change alters a rule, decide what happens to the past

The row above asks what the change must not break. This asks the harder half: **a rule
that is computed on read has no history, so changing it changes what already happened.**
Nothing fails, nothing is written, and every report issued before the deploy stops
reproducing.

`enhance` routes exactly this decision here, because it is a design decision and not a
small change. There are three shapes and they cost very differently:

| Shape | What it is | Cost |
|---|---|---|
| **Retroactive** | the new rule applies to everything, past included | free — and correct only when the old answers were wrong |
| **Effective-dated** | the rule carries a date; each record is evaluated against the rule in force when it happened | a version table, and every read site learns to pass a date |
| **Snapshotted** | the answer is computed once and stored on the record | a column, a backfill, and a new source of truth that can drift from the calculation |

**Retroactive is the default and is usually not stated**, which is the failure. Say which
of the three, and say why the other two were rejected.

Two facts decide it, and both are lookups:

```bash
grep -rn '<the calculation>' <roots> | grep -v migrations   # computed on read, or stored?
grep -rniE 'signed|approved|audit|snapshot|immutable' <models file> | head
```

- **Is anything downstream legally or contractually fixed?** Signed documents,
  disciplinary records, payroll runs, audit trails. Where the answer fed one of those, a
  retroactive change makes a signed record disagree with the system that produced it.
- **How many existing records change answer?** Give the query. A retroactive change
  presented without its population is the most common way a design gets approved and then
  reverted.

Where the answer is "nobody can tell, and it feeds payroll", that is a `Блокирует: да`
question for the product owner, not a default the design picks quietly.

## The coupling map is the deliverable

Run the list from `coupling.md` and record every candidate, including the ones that turn
out unaffected:

```
| Что | Нужно обновить | Размер | Если не | Рекомендую |
```

A candidate marked "correctly unaffected" is worth as much as one marked "needs updating"
— it is the difference between checked and not considered.

## Gaps in the task get filled here, not later

By the end of design you know what the task did not say: the text for a new screen, the
name of a new entity, the default for a new setting, what happens in a case nobody
mentioned.

Fill each, mark it, ask for approval — never implement a hole and never hand it back
empty. Delegate text to `copy`; it reads the lexicon and the tone.

```
⚠️ В задаче не было <what>.
   Предлагаю: <the proposal>
   Основание: <lexicon / соседняя фича / tone-of-voice>
```

## The gate

Show the design, the coupling map and the filled gaps. Ask:

> Так ложится? Мосты — все нужные? Иду писать спецификацию?

What to watch for while waiting: a bridge the engineer knows is unnecessary because that
report is being retired, and one they know is missing because a consumer lives outside this
repository.

## Ends with

```
Ложится:      <where, and what it extends>
Артефакты:    .dev-agent/screens/…, .dev-agent/data/…
Связанность:  <the map — every candidate, decided>
Пропуски:     <filled, each with its basis, awaiting approval>
Не трогаем:   <frozen things, and what would break>
Открыто:      <decisions left — must be empty to proceed>
```
