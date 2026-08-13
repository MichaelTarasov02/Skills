# Phase 5 — Ship

The texts that carry the work out of the branch. Drafted here, sent by a person.

**Delegate to `copy`** — team channel for the PR description, user channel for the release
note. Two audiences, two registers, never one text serving both.

## The PR description writes itself from the artifacts

Everything it needs already exists:

| Section | Comes from |
|---|---|
| What changed for the user | `intake.md`, the problem statement |
| Why | `intake.md`, the reason the task existed |
| What to check | `review.md`, plus the manual steps where tests are thin |
| Risk | `review.md` regression section, and the shared files touched |
| Known limitations | `review.md`, the not-done section |

The last row is the one that gets omitted and matters most. A reviewer who discovers a
limitation themselves reviews the whole change with suspicion; one who was told about it
reviews the rest.

**Written for someone who does not read the language of the code.** Opening with a file
list makes the reviewer reconstruct the point.

## The release note is a different document

Not a summary of the PR. What a user can now do that they could not before — and if the
answer is "nothing they will notice", say that plainly rather than dressing internals as
news.

For a rule change with no interface, this note is the entire feature as far as anyone
outside the team is concerned. Give it the attention the screen would have got.

## Dates

None. Not in the PR, not in the release note, not in a reply to whoever asked for this.
The release mechanism is a fact — "в следующей сборке"; a date is a promise nobody
authorised.

## Ends with

```
PR:           <draft — what changed, why, what to check, risk, limitations>
Release note: <user version, and the internal one if the release process wants it>
Not sent:     <both — sending belongs to a person>
Тестировать:  <the manual steps, where automation does not cover it>
```
