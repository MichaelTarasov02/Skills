# Blueprint format

Read before phase 7. Three skills read this file mechanically. The shape is a contract.

## Consumers

| Skill | Extracts |
|---|---|
| `interface-copy` | text slots — where a string is needed and of what type |
| `element-markup` | interactive elements — what needs semantics, an event, a test id |
| `screen-review` | the state matrix — to check what was actually implemented |

## Required sections, exact headings

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

Headings are matched literally. Renaming one breaks the consumer that reads it.

## Text slots — one per line, fixed prefix

```
- SLOT: empty.no-results | type: empty-state/filter | context: associate list filtered by date range
- SLOT: error.load-failed | type: error | context: report request failed, retry available
- SLOT: action.primary | type: action | context: exports the filtered list to Excel
```

Retrieved by:

```bash
grep '^- SLOT:' .dev-agent/screens/<slug>.blueprint.md
```

`type` uses the vocabulary `interface-copy` knows: `action`, `label`, `hint`,
`placeholder`, `validation`, `error`, `empty-state/created`, `empty-state/filter`,
`empty-state/access`, `confirmation`, `toast`, `loading`, `permission`, `onboarding`,
`limit`.

## Interactive elements — one per line, fixed prefix

```
- ELEM: date-range-picker | role: input | action: filters the list | state: enabled unless loading
- ELEM: export-button | role: button | action: downloads Excel | state: disabled while loading
```

Retrieved by:

```bash
grep '^- ELEM:' .dev-agent/screens/<slug>.blueprint.md
```

## States — one subsection per state

```markdown
### Empty — filter matched nothing
- shows: the filter summary and a clear-filters action
- slot: empty.no-results
- component: a-empty with overridden description
```

State subsections carry the state name from `state-matrix.md`. A state that cannot occur
is present with `- not applicable: <reason>` and nothing else.

## Open questions

Everything the blueprint could not settle, one per line, each naming who decides. An
empty section is written as empty rather than omitted — a missing section is
indistinguishable from a forgotten one.

## Proving the contract

Phase 7 is not complete until both `grep` commands above have been run against the
produced file and their output pasted. The format is only real if it retrieves.
