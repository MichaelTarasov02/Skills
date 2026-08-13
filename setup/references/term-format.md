# Term format and grep contract

> **Examples below are shapes, not facts about your codebase.** Field names, counts and
> paths in them are illustrative and were true of one repository at one moment. Measure
> before you quote any of them. A reference file that hands you a number is handing you a
> hypothesis.


Other skills read `lexicon.md` mechanically. The shape below is the contract.

## Shape

```markdown
### Meal Break
- status: proposed
- definition: A legally mandated unpaid interval within a shift
- plural: Meal Breaks
- code: lib/features/time_tracking/, whereami/src/components/entities/
- strings: <count> keys named <other-form> (see drift note)
- forbidden: Lunch, Lunch break, Break time
- not: not a Rest Break — rest breaks are paid and shorter
```

## Fields

| Field | Required | Purpose |
|---|---|---|
| heading | yes | the canonical term, exactly as the user should see it |
| `status` | yes | `approved` / `proposed` / `disputed` |
| `definition` | yes | one sentence, no synonyms inside it |
| `plural` | yes | translators and count strings need it |
| `code` | yes | where it lives; a term with no path is not a term |
| `strings` | when applicable | which UI strings carry it |
| `forbidden` | yes | the synonyms that must never appear; this is what `copy` checks against |
| `not` | when confusable | the neighbouring concept it gets mistaken for |

`forbidden` is the field that does the most work downstream. A term without it lets the
drift come straight back.

## Two rules that make the file machine-readable

**`###` is reserved for term headings. Nothing else in the file may use it.** Narrative —
the measurement, the reasoning, what is not being proposed — sits at `##` or below `####`.
A run that put analysis at `###` produced nine `###` headings for four terms, and any
skill enumerating them mechanically picked up "The five leaks" as a term.

**Anchor every lookup to end of line.** Term names are frequently prefixes of one another
— an entity, its qualified variant, and the document that declines it. Measured on one
file: `grep '^### Meal Break'` returned two cards, `grep '^### Meal Break$'` returned one.
The unanchored form silently hands the caller a neighbouring term's fields.

## Grep contract

A term is retrievable by its canonical name alone:

```bash
grep -A8 '^### Meal Break$' .dev-agent/lexicon.md
```

Consequences for the writer: one blank line between entries, no nested headings inside an
entry, fields always in the order above. Prove it in the verification run with actual
command output.

## Status meanings

| Status | Means | Who may set it |
|---|---|---|
| `proposed` | the skill extracted and proposes it | the skill |
| `approved` | a human confirmed it in a session | a human only |
| `disputed` | two defensible forms, decision pending | the skill, when it cannot break the tie |

`disputed` is a legitimate resting state. Forcing a winner where the evidence is even
produces a confident wrong answer, which is worse than an open question.
