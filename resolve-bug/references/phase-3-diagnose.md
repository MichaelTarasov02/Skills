# Phase 3 — Diagnose

Run the plan. Kill hypotheses. Arrive at a cause that explains **every** observed detail,
not most of them.

**Read `references/branches.md` before starting.** The branches are not a conclusion drawn
at the end — they are three lines of investigation run in parallel, and evidence for one
is evidence against the others.

## Delegate the technique, keep the judgement

`debug` owns the mechanics. Use its mode and bring back the result:

| Situation | Mode |
|---|---|
| Still cannot make it happen | `reproduce` |
| Have the failure, need the location | `locate` |
| Worked before | `regression` |
| Slow, cause unknown | `slow` |

This phase decides what the result *means* — which branch it supports. That is the part
`debug` does not do.

## Evidence, and what does not count

| Counts | Does not count |
|---|---|
| A quoted rule with its file and line | "the code should handle that" |
| A log line with its timestamp | "there was probably an error" |
| A config value read from the account | "their setup is probably standard" |
| A reproduction that fails on demand | "I could see how it might happen" |
| A commit that introduced the behaviour | "it was probably the recent refactor" |

Every claim in the output carries its evidence inline. A finding whose support is
"analysis" is a hypothesis that lost its label.

## The strongest evidence is usually not in the running code

Three sources sit outside what a grep for live code returns, and each one decides a branch
on its own. Check all three before naming a branch:

| Source | What it proves | How to look |
|---|---|---|
| **Commented-out code doing the expected thing** | someone implemented this behaviour and disabled it — that is intent, and it moves the verdict off "by design" | `grep -n "^ *#.*<concept>\|^ *//.*<concept>"` |
| **A test asserting the expected behaviour** | the behaviour was specified; a passing test with a skipped marker or a deleted assertion is a rule that was retired without a decision | `grep -rn "<concept>" --include='test_*' --include='*_test.*'` |
| **The commit that removed it** | who removed it, when, and what the message claimed | `git log -S '<the removed expression>' -- <file>` |

**Commented-out code is the one that gets missed**, because every search habit filters
comments out. It is also the most decisive: a disabled implementation of exactly what the
user expected is not an undecided product question — it is a decision that was made, and
reversed, and the reversal is what needs explaining.

Where you find one, `git log -S` on the expression names the commit and the message. If
the message says why, the branch is settled. If it says "wip" or "temp", the behaviour was
disabled for a reason nobody recorded, and that is a defect until someone remembers
otherwise.

## A cause explains everything, or it is not the cause

The strongest check available, and the most often skipped: list every observed detail and
confirm the candidate cause accounts for all of them.

```
Observed                              Explained by candidate cause?
the shift did not close               yes
only for this account                 yes — the setting is on
only after 14:00                      NO
the second attempt worked             NO
```

Two unexplained details mean the cause is incomplete — and what hides in the gap is either
the real cause or a second one. Stopping here produces a fix that removes some of the
symptom, which is worse than none, because the remainder gets attributed to something
else.

## Rule combinations

When single-rule hypotheses die and the symptom is account-specific, compare full
configurations:

```
account with the symptom     vs     account without
  <every setting>                     <every setting>
```

The differing settings are the candidate set, usually few. Change one at a time. The
combination that reproduces is the cause — and neither rule alone is wrong, which is why
reading either file showed nothing.

## Keep the kill list

Every hypothesis that dies is recorded with what killed it. This is not bookkeeping: it is
what stops the next person — or you, next week — re-checking the same three things.

```
H1  killed — accounts with the same setting close normally (3 checked)
H2  killed — the branch does not exist in this version
H3  alive  — settings differ exactly here
```

## Ends with

```
Cause:        <the mechanism, or the narrowest region the evidence allows>
Branch:       <defect | by design | user error | unresolved>
Evidence:     <per claim, inline>
Explains:     <every observed detail, marked>
Unexplained:  <anything the cause does not account for>
Killed:       <each hypothesis and what killed it>
Blind spots:  <catch sites, unlogged paths that could hide this>
```

`Unexplained` empty is the goal. `Unexplained` non-empty is an honest result and goes to
phase 4 as such — a partial diagnosis stated as partial is useful; stated as complete it
is a trap.
