# Coverage report format

> **Examples below are shapes, not facts about your codebase.** Field names, counts and
> paths in them are illustrative and were true of one repository at one moment. Measure
> before you quote any of them. A reference file that hands you a number is handing you a
> hypothesis.


Filled in phase A7. One row per use case ID from the build prompt.

| ID | Skill section | Evidence | Status |
|---|---|---|---|
| L1 | `## Naming a new entity` | run on `whereami-flutter-2`, output pasted below | closed |

## Evidence — runs only

Admissible: command output, a path to a produced artifact, a quotation from that
artifact.

Not admissible: "the skill handles this", "covered by section X", "would work". The
section reference lives in column two and is not evidence — it says *where*, not
*whether*.

## Status values

| Status | Meaning |
|---|---|
| `closed` | the run produced what the prompt called closed |
| `partial` | produced something short of it; state exactly what is missing |
| `open` | not produced; state why |

## Reading the report

A first build whose report contains no `partial` and no `open` usually means the runs
were too gentle, not that the skill is complete. Look again at whether each run actually
exercised the hard part of its case before treating an all-clear as good news.

An `open` row with a stated reason is a finished report. A `closed` row without evidence
is not.
