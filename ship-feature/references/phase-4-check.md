# Phase 4 — Check ⛔ gate

Before the PR, not after review comments.

**Delegate to `review`** — `screen` mode for the interface, `change` mode for the diff,
`perf` mode where the feature touches lists, queries or images. Run every mode the route
called for.

## What this phase adds on top of `review`

**Tracing back to phase 1.** `review` checks the change; the pipeline checks the change
against what was agreed:

| Trace | The failure it catches |
|---|---|
| Every acceptance criterion from `intake.md` → where it is implemented | a requirement everyone forgot, including the person who wrote it |
| Every state from `blueprint.md` → implemented or explicitly dropped | the state that always gets dropped: no access, or offline |
| Every assumption from `intake.md` → still true | an assumption invalidated during the work and never revisited |

The third is the quiet one. Assumptions are made under time pressure in phase 1 and become
requirements by phase 4 because nobody re-read them.

## Findings go to the engineer, not into a silent fix

This phase reports. Fixing what it finds is a decision — some findings are worth shipping
with, and that is legitimate as long as it is stated.

Rank as `review` does: blocking, important, nice. A feature can ship with `nice` open; a
`blocking` finding shipped is a decision someone must make out loud.

## The not-done section

Mandatory, and not empty by default. What was cut, what is deferred, what the tests do not
cover. This is the section the PR description quotes from, and the one that keeps a
reviewer from assuming coverage nobody claimed.

## The gate

> Блокирующих — <n>. Открываем PR с этим?

Not permission to open the PR — the engineer's own decision. The gate exists so they open
it knowing what is inside.

## Ends with

```
Артефакт:     .dev-agent/reviews/<slug>.review.md
Трассировка:  <criteria implemented> / <total>, <states implemented> / <total>
Допущения:    <still true | invalidated — with which>
Находки:      <blocking> / <important> / <nice>
Не сделано:   <non-empty>
```
