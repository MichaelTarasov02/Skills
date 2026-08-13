# Routing

> **Examples below are shapes, not facts about your codebase.** Measure before you quote
> any of them.

Read before phase 1. Deciding the route wrong costs more than any single phase: running
all five on a rule change produces three empty sections and buries the one that mattered.

## Read the task for what it touches, not what it says

The wording rarely names the layers. "Сделай отчёт" can be a screen over an existing
endpoint, a new query plus a screen, or a new table plus everything above it — and the
three are different weeks.

Answer five questions from the task and the code, before asking anything:

| Question | Look at | If yes |
|---|---|---|
| Does a user see something new or different? | the task, plus which screens exist | strings and markup phases apply |
| Does anything get stored that is not stored now? | the schema | **full** data design applies |
| Does it read data that already exists? | the schema | data mode runs `read` — establish what is readable and what it costs to query, design nothing |
| Does an existing contract change shape? | the endpoint and its callers | old clients matter; compatibility is a phase-2 output |
| **Does a user write to something that already exists?** | the model, and whether anything writes it today | **data mode runs `write` — the contract, the validation, and who may do it** |
| Does a rule change without any interface changing? | settings, validators, permissions | the release note carries the whole feature |

**The write row is the one that gets lost between the others.** Nothing new is stored, so
row two says no; no existing contract changes shape, so row four says no; and the feature
lands on `read`, design nothing — which is how a settings screen reaches
implementation with no write contract, no validation rules, and nobody having decided who
is allowed to change the value.

A settings screen is the canonical case and it is never a read. Three things need
designing even though the column already exists:

| | Because |
|---|---|
| **Who may change it** | an existing field has an existing audience for *reading*; writing is a different permission and usually a narrower one |
| **What the value may be** | a column with no validator has one now, and the bounds are a product decision |
| **What happens to what was computed under the old value** | the retroactivity question — route it to `improve` where it needs designing |

Where the field feeds money, hours, compliance or discipline, the third is a blocker
rather than a note.

**The difference between rows two and three is the most common mis-route.** A new report
over existing columns needs `data` mode to answer *what can be queried and at what cost* —
not to propose tables. Running full schema design there produces a migration nobody asked
for; skipping data mode entirely produces a screen promising values the query cannot
deliver.

Measured on one task: a report request that looked like new storage turned out to read ten
existing columns. Read-only data mode, no migration, and the whole question became the
query and its indexes.

The last question is the one that gets under-served. A rule change is invisible in the diff to
everyone except the users it surprises, and its release note is the only place anyone will
learn about it.

## Routes

| Route | Phases | Skipped, and why |
|---|---|---|
| **New screen, new storage** | 1 → 2 (screen + data `schema`) → 3 → 4 → 5 | none |
| **New screen over existing data, read-only** | 1 → 2 (screen; data `read`) → 3 → 4 → 5 | schema design — nothing is stored that is not stored now |
| **New screen that writes existing data** | 1 → 2 (screen; data `write`) → 3 → 4 → 5 | schema design only — the contract, validation and permission still need designing |
| **Existing screen changes** | 1 → 3 → 4 → 5 | design, unless the state matrix changes — then insert 2 |
| **Backend or data only** | 1 → 2 (data) → 4 → 5 | strings and markup: nothing is rendered |
| **Rule change, no interface** | 1 → 4 → 5 | design and build: nothing to design or write |
| **Finishing half-built work** | 4 → back to whatever it names | intake and design already happened, possibly in someone's head |

The last route is the most common and the least planned for. Starting at the check phase
tells you what is missing; then you go back for exactly that and no more.

## Mixed features are normal

Most real features are a screen **and** a schema change **and** a rule. Run the phases in
order, and let phase 2 produce both a blueprint and a data design — they are two artifacts
from one phase, not two runs.

Where the parts can ship separately, say so in phase 1. A schema migration that can land a
release ahead of the screen removes the deploy-window problem entirely, and nobody
suggests it if the feature is treated as one unit.

## When the route is unclear

Two questions settle nearly every case:

> Пользователь увидит что-то новое, или меняется только поведение?
> Появляется что-то, что раньше не хранили?

Ask both together, then state the route. Do not ask a third — the remaining ambiguity is
cheaper to carry as a stated assumption than to resolve by conversation.

## State the route, and what it skips

```
Маршрут:     <название>
Фазы:        <какие>
Пропускаю:   <какие и почему>
Артефакты:   <что появится на выходе>
```

`Пропускаю` is the line the engineer corrects. "Design skipped — состояния не меняются"
is a claim they can refute in four words, and refuting it early is worth more than
anything else in this file.
