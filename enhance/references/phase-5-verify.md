# Phase 5 — Verify

The plan checked against the code, by reading. No test infrastructure is started —
deliberately.

**What this phase is:** confirmation that what was agreed is what exists, and that nothing
else came along with it.

**What it is not:** proof that the code runs. Reading cannot provide that, and claiming it
does is the failure this phase most easily produces.

## Trace the plan, step by step

One row per plan step, and the third column is the point:

| Шаг плана | Где в коде | Соответствует? |
|---|---|---|
| 1. <before → after> | `<path>:<line>` | да / **нет — <what differs>** |

A step marked `нет` is not a failure of the phase — it is the phase working. Divergences
agreed during phase 4 appear here with their agreement noted; divergences nobody agreed to
are findings.

**Trace the plan, not the diff.** Reading the diff and confirming it looks right verifies
that you did what you did. Only the plan says what should have been done.

## Then trace the other direction

Every change in the diff maps back to a plan step. Anything that does not is one of:

| Unmapped change | What to do |
|---|---|
| A necessary consequence the plan missed | record it — the plan was incomplete |
| An improvement made in passing | remove it, or state it as a deliberate exception |
| A leftover — debug output, commented code, a stray rename | remove it |

Unmapped changes are how a reviewed change contains something nobody reviewed.

## Read the logic against the requirement, not against the plan

The plan can be wrong. Take the requirement from phase 1 and walk the new code as the
system will:

- the ordinary case — does it now do what was asked
- the case the ticket did not mention — does it still do what it did before
- the boundary — empty, zero, missing, the first, the last
- the case the change was **not** meant to affect — is it untouched

**The fourth is the one that catches real defects.** An enhancement that changes behaviour
for a case nobody discussed is a regression, and it is invisible in a diff that looks
exactly like the plan.

## Convention check — run it, do not read it

```bash
npm run lint && npm run format:check    # or the project's equivalent, found in phase 4
```

Paste the output. A change that fails the project's own formatter is not a style
disagreement — it is a broken build waiting for CI, and it is the cheapest failure to
catch here.

Then read the change beside its nearest sibling one more time. Fit is easier to see after
the code is written than before.

## Generated twins — the one thing reading can decide

Reading cannot tell you whether the code runs. It **can** tell you whether the change made
a committed generated file stale, and that is the failure mode this phase would otherwise
pass straight through:

```bash
ls <changed file with the generated suffix stripped>.freezed.* <…>.g.* 2>/dev/null
```

A hand-written source with a committed generated twin, changed in a way the generator
cares about — a field added, an annotation changed, a signature altered — is **not
finished**. The change compiles for nobody until the twin is regenerated and committed.

Name the command and say it is outstanding. Do not run it: generation rewrites hundreds of
files and a diff nobody asked for is worse than a missing one.

## Say plainly what was not verified

```
Проверено чтением:  <what>
Не проверено:       <what needs running — and it always includes "does it actually run">
```

The second line is mandatory and never empty. A change verified by reading is verified by
reading; presenting that as tested is the one thing this phase must not do.

Where the change is worth an automated test and the project has a place for one, say so.
Where the project has almost no tests, say that too — it changes how much the manual check
is worth.

## Ends with

```
Трассировка:  <steps> / <total> соответствуют
Расхождения:  <each, with whether it was agreed>
Непокрытое:   <diff changes not mapped to a plan step>
Побочное:     <behaviour changed for cases nobody asked about — must be empty>
Регенерация:  <command outstanding, or "не требуется — <why>">
Не проверено: <non-empty, always>
```
