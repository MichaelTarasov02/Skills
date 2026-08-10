# Team channels

> **Examples below are shapes, not facts about your codebase.** Field names, counts and
> paths in them are illustrative and were true of one repository at one moment. Measure
> before you quote any of them. A reference file that hands you a number is handing you a
> hypothesis.


Six shapes, one audience: colleagues who have their own work and are reading yours.

## PR description

The reviewer needs to know what to look at, not what you typed.

```markdown
## What changed for the user
Completing a document sequence no longer bounces back to the project list.

## Why
The completion callback fired before the repository confirmed, so the page
unmounted mid-write.

## What to check
- complete a sequence from the alert entry point, not only from the project page
- resignation flow — touched by the same listener change

## Risk
constants.dart and environment.dart changed; both are shared.
```

"What changed for the user" comes first and is written for someone who does not read Dart.
A description that opens with a file list makes the reviewer reconstruct the point.

## Breaking change

```markdown
**Who this affects:** anyone calling POST /sequence/complete
**What breaks:** the response no longer includes `legacy_status`
**What to do:** read `status`; values map 1:1
**When:** the field is removed in the release after next
**Checklist:** [ ] client updated  [ ] tests updated  [ ] staging verified
```

Affected parties first. Half the readers stop after that line, correctly, because it does
not concern them — and that is the line's job.

## Status update

Three parts, no jargon, no dates:

```
Done: the report query and the permission guard.
Left: empty and error states.
Blocked on: which meal break counts as missed — waiting on product.
```

If a status update needs a paragraph, it is a status update plus a blocker question, and
the question is being buried.

## Blocker question

The reader must be able to answer in one message. That requires the context, the options,
and what waiting costs:

```
Blocked on the missed-meal-break report: the model stores two meal breaks
(signed_lunch1, signed_lunch2), and the requirement says "meal break" singular.

Options:
(a) first only — one query, matches most shifts
(b) either — two queries, matches the legal definition
(c) both listed separately — most work, most precise

Cost of waiting: the query is the first piece; everything else follows from it.
```

Recommend one. A question with three options and no recommendation asks the reader to do
the thinking you already did.

## Escalation

Facts, consequence, options. No adjectives, no history of who said what.

```
The report cannot ship this week: three blocking questions have been open since
Monday and the query shape depends on all three.

Consequence: either the date moves, or it ships covering the first meal break only,
which under-reports.

Options: (a) move the date (b) ship narrowed, with the limit stated in the UI.
```

Emotion in an escalation shifts the conversation to how it was raised. Remove every
sentence that would read differently if the reader were the cause.

## Code-review reply

Separate taste from substance, and answer them differently.

| Kind | Reply |
|---|---|
| Substantive — correctness, security, a real edge case | agree and fix, or disagree with a concrete counter-case |
| Taste — naming, structure, style with no functional difference | take it. The cost of arguing exceeds the cost of the change |
| Unclear which | ask what breaks if it stays — the answer sorts it |

Never "this is a matter of preference" as a closing move. Either it is, and you take the
suggestion, or it is not, and you name the failure it prevents.
