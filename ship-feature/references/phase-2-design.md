# Phase 2 — Design ⛔ gate

What gets built, before anything is built. Changing a state matrix costs a sentence;
changing it after the screen exists costs the screen.

**Delegate to `spec`** — `screen` mode for the interface, `data` mode for storage and
contracts. Most features need both, and they are two artifacts from one phase.

## Order: data before screen

The schema decides what the screen can show. Designing the screen first produces a layout
that assumes data nobody stores, and the mismatch surfaces during implementation, when it
is expensive.

Where both apply, run `data` first and let its output constrain the screen.

## What this phase adds on top of `spec`

**The seam between the two artifacts.** `spec` produces a blueprint and a design; the
pipeline checks they agree:

| Check | The failure it catches |
|---|---|
| Every value the screen shows exists in the schema | a column nobody is storing |
| Every state the screen has is reachable from the data | an "empty" state where the query cannot return empty |
| Every field added has a reader | storage nobody consumes |
| The permission that guards the screen matches the one scoping the query | a screen that hides what the API returns |

The last one is a security finding, not a design nit. A screen filtered client-side over
an endpoint that returns everything leaks whatever the filter hides.

## Reuse before invention

Both artifacts name existing pieces or explain why not: components from the inventory,
tables that could take a column instead of a new table, endpoints that could take a
parameter instead of a new route.

A design proposing a new component next to one that already does the job is a design that
will be sent back — and correctly.

## The gate

Show both artifacts. Ask explicitly:

> Состояния и схема — так? Иду писать строки и разметку?

What to look for while waiting: a state marked not-applicable that the engineer knows is
reachable, and a table they know is being migrated this week.

## Ends with

```
Артефакты:    .dev-agent/screens/<slug>.blueprint.md
              .dev-agent/data/<slug>.design.md
Согласовано:  <what the seam check confirmed>
Расхождения:  <anything the two artifacts disagree about — must be empty to proceed>
Открыто:      <decisions left, each with who decides>
```
