# Phase 1 — Intake

Turn the ticket into requirements, blockers and a route. Ends before any design decision.

**Delegate to `spec` in `task` mode.** It owns the technique: facts looked up before
questions asked, hidden requirements, checkable criteria, three-question budget. This
phase adds the route and the artifact hand-off.

## What this phase adds on top of `spec`

| Addition | Why the pipeline needs it |
|---|---|
| The route | decides which later phases run at all |
| Split points | parts that can ship separately, said now rather than discovered at deploy |
| Existing work | whether any of this already exists somewhere in the product |

## Look for it before building it

The cheapest feature is the one already written. Before designing anything:

```bash
grep -ril '<the entity>' <screens root> | head
grep -rn '<the operation>' <api root> | head
```

Half of "make a report" requests are a filter on a report that exists. Say so in phase 1,
not after the screen is built — and where something close exists, name it and ask whether
extending beats adding.

**Look for the pattern, not only for the entity.** A product that has built this kind of
thing before has a shape for it — a builder, a base class, a directory of siblings — and
the new one belongs inside that shape:

```bash
ls <the module that produces things of this kind>/ | head
grep -rl 'class .*<Kind>' <backend root> | head
```

Measured on one task: nine report builders already existed on the backend and seven report
screens on the front end. The question was never "how do we build a report" — it was
"which builder does this extend", and answering it in phase 1 removes most of phase 2.

Where a shape exists and the new work does not fit it, that is worth saying too: either
the shape needs extending, or this is genuinely a different kind of thing. Both are
findings; neither is "write it fresh and hope".

## Split points

A feature that can land in pieces should, and nobody proposes it if the ticket is treated
as one unit:

| Split | When it works |
|---|---|
| Schema first, screen next release | any new storage — removes the deploy-window problem entirely |
| Endpoint first, client next | mobile especially: the client release lags anyway |
| Behind a flag | the rule change is risky or needs a staged rollout |

Say which splits are available and which you recommend. The decision is the engineer's;
the observation is yours.

## Ends with

```
Маршрут:      <route, phases, what is skipped and why>
Требования:   <from spec's intake — with the blockers first>
Уже есть:     <what exists that this could extend>
Разделить:    <split points, with a recommendation>
Артефакт:     .dev-agent/features/<slug>.intake.md
```

Do not proceed while a blocking question is open. A design built on an unanswered blocker
is a design that gets rebuilt.
