# Artifact contract

Read before phases A1 and B2. The skills are wired together by **files, not by calls**.
This file is what makes them an agent rather than twelve separate tools.

Everything lives in `PRODUCT_REPO/.dev-agent/`, never inside the plugin. The plugin is the
tool; the repository holds the knowledge.

## The roster this contract is written against

Eight tools and five pipelines. A row naming anything else is stale, and a stale row is
worse than a missing one — B2 will confirm a reader that does not exist and report the
chain healthy.

| Tools | Pipelines |
|---|---|
| `setup` `spec` `copy` `craft` `review` `debug` `handoff` `forge` | `resolve-bug` `enhance` `improve` `refactor` `ship-feature` |

## Project knowledge — written once by `setup`, read by everything

| File | Written by | Read by |
|---|---|---|
| `config.yaml` | `setup` | all — platforms, roots, framework majors, i18n, analytics |
| `project.md` | `setup` | all |
| `onboarding.md` | `setup` | a human: known / assumed / unknown |
| `lexicon.md` | `setup` | `copy`, `spec`, `craft` |
| `tone-of-voice.md` | `setup` | `copy` |
| `red-lines.md` | `setup` | `copy` |
| `component-inventory.md` | `setup` | `spec`, `review` |

## Work artifacts — one per piece of work

| File | Written by | Read by |
|---|---|---|
| `tickets/<KEY>.md` | `handoff` `ticket` | `spec` `task`, every pipeline, `handoff` `record` |
| `handoff/<KEY>.md` | `handoff` `record` | `handoff` `publish`, the next session on that ticket |
| `features/<slug>.intake.md` | `spec` `task` | `spec` `screen`, `copy`, `review`, `ship-feature`, `improve` |
| `screens/<slug>.blueprint.md` | `spec` `screen` | `copy`, `craft`, `review`, `ship-feature` |
| `data/<slug>.design.md` | `spec` `data` | `craft`, `review`, `improve`, `ship-feature` |
| `screens/<slug>.strings.md` | `copy` | `craft`, `review`, `ship-feature` |
| `screens/<slug>.markup.md` | `craft` `markup` | `review`, `ship-feature` |
| `reviews/<slug>.review.md` | `review` | `copy` (PR description), `ship-feature` |
| `bugs/<slug>.md` | `resolve-bug`; `debug` when standalone and the run was long or unresolved | `copy` (the reply), `review`, `debug` on the next report of the same symptom |
| `changes/<slug>.md` | `enhance` | `review`, `copy` |
| `features/<slug>/spec.md` | `improve` | `improve` later sessions, `review` |
| `features/<slug>/part-N.md` | `improve` | `improve` later sessions |
| `features/<slug>/progress.md` | `improve` | `improve` later sessions — the only cross-session state |
| `features/<slug>/report.md` | `improve` | `copy`, `review` |
| `refactors/<slug>/baseline.md` | `refactor` | `refactor` phase 6 — **the gate depends on it** |
| `refactors/<slug>/report.md` | `refactor` | `review`, `copy` |
| `.telemetry/tracking-plan.yaml` | plugin `product-tracking-skills` | `craft`, `review` |

`ship-feature` writes nothing of its own. It routes, and carries the artifacts above
between phases. A pipeline that invents a private artifact instead of writing the tool
skill's one has broken the chain for everything downstream.

## Two naming conventions, and when each applies

| Shape | For | Example |
|---|---|---|
| `<kind>/<slug>.<phase>.md` | work that finishes in one session | `features/login.intake.md` |
| `<kind>/<slug>/<file>.md` | work that spans sessions or produces several files | `refactors/login/baseline.md` |

Choose by whether a second session must find the state, not by taste. Adding a third
convention is how a reader ends up grepping two of the three.

## Absence is a supported state

A reader that stops because a file is missing has failed. Every reader handles absence in
three moves: **name what is missing, offer the skill that produces it, continue on
assumptions marked as such in its own output.**

This is checked in B2 by opening each reader and citing the line where it does this.

## Grep stability

Several artifacts are consumed by skills rather than by people, so their shape is part of
the contract:

| Artifact | Must yield | Anchor |
|---|---|---|
| `lexicon.md` | one term by its canonical name | `grep -A8 '^### <Term>$'` |
| `*.blueprint.md` | the text slots and the interactive elements | `- SLOT:` / `- ELEM:` |
| `*.intake.md` | the open questions and the acceptance criteria | `- Q[0-9]` / `- AC[0-9]` |
| `*.markup.md` | one entry per element, by the blueprint's own name | `### ELEM:` |
| `tickets/<KEY>.md` | the gaps and the linked tickets | `- GAP:` / `- LINK:` |

**Anchor every lookup to end of line.** Names are frequently prefixes of one another, and
the unanchored form hands the caller a neighbouring entry's fields.

Any skill producing such an artifact states its grep-stable shape in specification field 8
and proves it in A6 with the output of an actual search.

## Changing the contract

A new file or a changed shape touches every reader. Add the row here first, then update
the readers, then re-run B2. Editing a producer without touching this table is how the
chain quietly breaks — and a rename that stops at `SKILL.md` leaves this table pointing at
skills that no longer exist, which B2 cannot detect because it trusts the table.

**B2 begins by checking that every name in this file is a real skill:**

```bash
cd <plugin>/skills/forge && comm -23 \
  <(grep -ohE '`[a-z-]+`' references/artifact-contract.md | tr -d '`' | sort -u) \
  <({ ls ../; printf '%s\n' task screen data change perf markup reproduce \
       locate regression slow clean fast both product-tracking-skills; } | sort -u)
```

The second list is the real skills plus the mode names and the one external plugin this
file may legitimately mention. **Anything printed is a stale skill name.** Keeping the
exception list explicit is the point: a check that prints four expected lines every run is
a check nobody reads, and this table is exactly where a rename goes to hide.
