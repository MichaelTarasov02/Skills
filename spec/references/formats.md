# Artifact formats

> **Examples below are shapes, not facts about your codebase.** Field names, counts and
> paths are illustrative. Measure before you quote any of them.

Three artifacts, one per mode. Other skills read them mechanically, so every shape here
is a contract rather than a preference. Phase 6 is not complete until the extraction
commands have been run against the produced file and their output pasted.

| Mode | Artifact | Read by |
|---|---|---|
| `task` | `features/<slug>.intake.md` | `review` traces acceptance criteria to implementation |
| `screen` | `screens/<slug>.blueprint.md` | `copy` takes text slots, `craft` takes elements, `review` takes the state matrix |
| `data` | `data/<slug>.design.md` | `craft` builds against it, `review` checks the migration |

---

## `intake.md`

### Sections, exact headings

```markdown
# Intake: <Feature Name>

## Understood
## Ambiguous
## Facts
## Questions
## Assumptions
## Acceptance criteria
## Scope
## Success metric
## Data
## Work breakdown
```

### Prefixed lines

```
- FACT: <what the code says> — <file:line> (<the measurement that shows it>)
- Q1 [blocker]: <the decision>
  Recommend: <your option>. <one line of reasoning>
- A1: <the assumption> — cost if wrong: <what it costs>
- AC1: <checkable statement>
```

```bash
grep    '^- FACT'    .dev-agent/features/<slug>.intake.md
grep -A1 '^- Q[0-9]' .dev-agent/features/<slug>.intake.md   # -A1 — see below
grep    '^- A[0-9]'  .dev-agent/features/<slug>.intake.md
grep    '^- AC[0-9]' .dev-agent/features/<slug>.intake.md
```

**Questions are retrieved with `-A1`, and the reason is load-bearing.** `Recommend:` sits
on the line after the question and carries no prefix, so a bare `grep '^- Q[0-9]'` returns
the question **without the recommendation** — and a downstream skill then shows the
developer a bare question, which is the one thing this skill's own rule forbids.

Consequence for the writer: `Recommend:` is always the **immediately following line**,
never separated by a blank line and never split across two. A question whose recommendation
is two lines down is a question that arrives without one.

`^- A[0-9]` does not match `- AC1` — `AC` is `A` followed by `C`, not by a digit. That is
why assumptions and criteria can share the `A` prefix; do not "fix" it by renaming either.

`FACT` is the record of what the customer did not have to answer. Every assumption states
what being wrong would cost; without it, an assumption is a silent decision wearing a
label. Banned inside a criterion: `properly`, `correctly`, `as expected`, `works`,
`handles` — each moves the decision to whoever reads it later.

Three questions maximum. The fourth would have been a question; it is an assumption.

---

## `blueprint.md`

### Sections, exact headings

```markdown
# Blueprint: <Screen Name>

## Placement
## States
## Text slots
## Interactive elements
## Boundary data
## Components
## Open questions
```

### Prefixed lines

```
- SLOT: empty.no-results | type: empty-state/filter | context: <what the reader needs to know>
- ELEM: export-button | role: button | action: <what it does> | state: <when disabled>
```

```bash
grep '^- SLOT:' .dev-agent/screens/<slug>.blueprint.md
grep '^- ELEM:' .dev-agent/screens/<slug>.blueprint.md
```

`type` uses the vocabulary `copy` knows: `action`, `label`, `hint`, `placeholder`,
`validation`, `error`, `empty-state/created`, `empty-state/filter`, `empty-state/access`,
`confirmation`, `toast`, `loading`, `permission`, `onboarding`, `limit`.

States get one subsection each, named from `screen.md`. A state that cannot occur is
present with `- not applicable: <reason>` and nothing else — an omitted state is
indistinguishable from a forgotten one.

---

## `design.md` (data)

### Sections, exact headings

```markdown
# Data design: <name>

## What already exists
## Proposal
## Migration
## API
## Access
## Indexes
## Frozen
## Open questions
```

### Prefixed lines

```
- TABLE: shift | status: existing | migrations in 6 months: 34
- COLUMN: shift.meal_break_waived | type: boolean | nullable: yes | reason: <why>
- BREAKS: <what stops working for old clients> | mitigation: <additive | new endpoint | version>
- FROZEN: <column> | depended on by: <which historical records>
```

```bash
grep '^- TABLE:'  .dev-agent/data/<slug>.design.md
grep '^- COLUMN:' .dev-agent/data/<slug>.design.md
grep '^- BREAKS:' .dev-agent/data/<slug>.design.md
grep '^- FROZEN:' .dev-agent/data/<slug>.design.md
```

`BREAKS` is the line `review` looks for before a deploy. An empty `BREAKS` list is written
as empty and stated, never omitted — the difference between "nothing breaks" and "nobody
checked" is the whole point of the section.

`FROZEN` names what may never be renamed and which records depend on it. A design without
this section invites a rename that silently changes historical answers.

---

## Open questions — every artifact

One per line, each naming who decides. An empty section is written as empty rather than
omitted. A missing section reads as a forgotten one.
