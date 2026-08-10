# Intake format

> **Examples below are shapes, not facts about your codebase.** Field names, counts and
> paths in them are illustrative and were true of one repository at one moment. Measure
> before you quote any of them. A reference file that hands you a number is handing you a
> hypothesis.


Read before phase 8. `screen-blueprint` and `feature-handoff` read this file
mechanically.

## Consumers

| Skill | Extracts |
|---|---|
| `screen-blueprint` | requirements and constraints that shape the screen |
| `feature-handoff` | acceptance criteria, to trace each one to its implementation |

## Required sections, exact headings

```markdown
# Intake: <Feature Name>

## Understood
## Ambiguous
## Questions
## Assumptions
## Acceptance criteria
## Scope
## Success metric
## Data
## Work breakdown
```

## Questions — ranked, fixed prefix

```
- Q1 [blocker]: Which meal break does "missed" refer to — the first, the second, or either?
- Q2 [blocker]: Does a Manager see all associates, or only their own company?
- Q3 [later]: Should the report cover shifts still in progress?
```

`[blocker]` questions come first and are numbered first. Retrieved by:

```bash
grep '^- Q[0-9]' .dev-agent/features/<slug>.intake.md
```

Three questions maximum in quick mode. The fourth would have been a question; it is an
assumption instead.

## Assumptions — fixed prefix, each with its cost

```
- A1: Report covers completed shifts only — cost if wrong: in-progress shifts need a
  separate state, roughly one extra query
```

Every assumption states what being wrong would cost. An assumption without a cost is a
silent decision wearing a label.

```bash
grep '^- A[0-9]' .dev-agent/features/<slug>.intake.md
```

## Acceptance criteria — fixed prefix, checkable

```
- AC1: A Manager opening the report for a date range sees every associate whose
  signed_lunch1_start falls outside threshold_lunch1_start..threshold_lunch1_end
- AC2: An associate without the Manager role opening the report URL sees the
  no-permissions screen
```

Banned inside a criterion: `properly`, `correctly`, `as expected`, `works`, `handles`.
Each of them moves the decision to whoever reads it later.

```bash
grep '^- AC[0-9]' .dev-agent/features/<slug>.intake.md
```

## Facts looked up

Every fact resolved from the codebase is recorded with its source, so the next person
does not re-ask it:

```
- FACT: <what the code says> — <file:line> (<the measurement that shows it>)
```

This section is the record of what the skill saved the customer from answering.

## Work breakdown

Parts a non-developer can read. No numbers, no units of time. If a part cannot be
described without naming a duration, it is not broken down far enough.

## Proving the contract

Phase 8 is complete when the three `grep` commands have been run against the produced
file and their output pasted.
