---
name: refactor
description: Improves code without changing what it does — audits a block, a call or a feature against clean-code rules and against performance, captures a baseline of current behaviour and timings, plans the change, implements it, then proves behaviour is identical and the metric improved. Runs in three modes — clean, fast, or both. Use when code works but is hard to read, when a call is slow, when a block needs tidying before it grows. Триггеры — "отрефактори", "почисти код", "ускорь", "оптимизируй запрос", "здесь каша", "переписать этот кусок", "тормозит этот вызов".
---

# Refactor

Improving code without changing what it does. Seven phases, two gates.

**The risk here is unlike the other pipelines.** Elsewhere the danger is building the
wrong thing; here it is **changing behaviour while believing you did not**. The pull
request says "no functional changes", so nobody looks for them — and a behaviour change
introduced under that banner is found in production, by a user, weeks later.

Everything below exists to make that impossible to do silently.

## Language

Answer in the language the request was written in. Findings, explanations, questions,
reports and section headings you produce for a developer follow their language — Russian
request, Russian answer.

**Text destined for the product's users is exempt.** Interface strings, release notes,
store listings and email stay in the product's interface language, taken from
`.dev-agent/config.yaml` → `interface.language`, whatever language the request used.
Mixing the two — an English report about Russian button labels, or the reverse — is the
failure this rule prevents.

**A missing `.dev-agent/config.yaml` is not a blocker, and not a question either.**
Detect the interface language from the code — the default locale in the i18n config, or
the language the strings are actually written in — state what you detected and from which
file, and offer `setup` once. **Never fall back to the language of the request:** a
Russian request about an English product must still produce English button labels, and
that substitution is invisible until it ships. The same applies to every other platform fact this
skill needs — read the manifest (`pubspec.yaml`, `package.json`, `requirements.txt`),
name the major you found and the file it came from. Advice written for the wrong major
does not compile while looking plausible enough to paste.

## Answer in the conversation, not only in the file

The developer reads the chat. The artifact is for the skills downstream. Lead with what
was asked, in this order:

1. **The answer** — what to do, as a recommendation, not a menu
2. **What blocks it** — decisions only they can make, each carrying your recommended
   option and the reason for it
3. **The cost of being wrong** — for anything decided on their behalf
4. **Where the detail lives** — one line naming the artifact

Never open with what you verified, which reference files you read, or how you reconciled
your own numbers. That is the record of your process, not the answer to their question.
Evidence belongs attached to the claim it supports, never in the headline.

A developer who reads only the first ten lines must be able to act.

**Headline for this skill:** what is wrong with the code, what it would cost to fix, and
whether the behaviour can be pinned well enough to fix it safely.

## Modes

| Mode | Audits | Success is |
|---|---|---|
| `clean` | readability, structure, duplication, naming | the code is easier to change, behaviour identical |
| `fast` | queries, allocations, rendering, round trips | the metric improved, behaviour identical |
| `both` | both, in that order | both, and neither traded for the other |

Default is `both` — they are usually found together, and a block worth reading is a block
worth measuring. Say the mode in phase 1.

**In `both`, do the performance work first when the two conflict.** A structure optimised
for readability sometimes cannot be made fast without partly undoing it; the reverse is
rarer. Where a genuine trade-off appears, it is a decision for the gate, not a preference
to exercise quietly.

## The pipeline

| # | Phase | Reference | Ends with |
|---|---|---|---|
| 1 | **Scope** | `references/phase-1-scope.md` | what is in, what is out, the mode |
| 2 | **Baseline** ⛔ | `references/baseline.md` | behaviour and timings captured — **gate** |
| 3 | **Audit** | `references/phase-3-audit.md` | findings, ranked, with what each costs |
| 4 | **Plan** ⛔ | `references/phase-4-plan.md` | the steps, each behaviour-preserving — **gate** |
| 5 | **Implement** | `references/phase-5-implement.md` | the change, in small reversible steps |
| 6 | **QA** | `references/phase-6-qa.md` | behaviour identical, style clean, metric moved |
| 7 | **Report** | `references/phase-7-report.md` | before and after, on both axes |

## No baseline, no refactor

**Read `references/baseline.md` before phase 2.** The gate after it is not ceremony.

Refactoring without a way to tell whether behaviour changed is not refactoring — it is
rewriting and hoping. Where behaviour cannot be pinned, the honest options are: write
characterisation tests first, narrow the scope to something that can be pinned, or do not
do it.

That is a decision for the engineer, and it is what the gate asks.

For `fast`, the same applies to the metric. An optimisation with no before-number cannot
be shown to have worked, and "it feels faster" has approved more useless changes than any
other sentence in software.

## Behaviour includes the parts nobody thinks of as behaviour

| Also behaviour | Why it bites |
|---|---|
| Error messages and error types | a caller catching a specific type stops catching |
| Ordering of results | a list nobody sorted was still in a stable order |
| Null versus empty | a caller checking one and not the other |
| Timing and laziness | code that ran eagerly and now runs on access, or the reverse |
| Number of queries or calls | a side effect that fired once now fires per row |
| Log output | something downstream parses it |
| **Identity — module path, class name, route name, table name** | nothing imports it; migrations, stored payloads and catalogues name it as a *string*, so no test and no compiler sees it move |

An audit that only reads the happy path finds none of these, and each is a real production
incident that began with "no functional changes".

**The last row is a different kind of behaviour and needs a different baseline.** A
structural refactor — splitting a file, moving a class, extracting a package — changes
nothing a characterisation test can observe, and everything that a migration, a serialised
payload or a string catalogue depends on. `references/baseline.md` carries the identity
inventory for exactly this; phase 2 names which of the two baselines applies before
capturing either.

## Scope discipline

A refactor that grows is a refactor that never lands. Phase 1 draws the boundary and
phase 5 defends it: anything outside is recorded and left, however tempting and however
adjacent.

**Do not mix a behaviour change into this work.** If the audit finds an actual bug — and
it often does — that is a finding, reported separately. Fixing it inside a refactor
destroys the one property that makes the change reviewable: that behaviour is supposed to
be identical.

## What this delegates

| Need | Skill |
|---|---|
| Measuring what is slow when the bottleneck is unknown | `debug`, `slow` mode |
| The project's conventions and clean-code baseline | `skills/enhance/references/conventions.md` |
| Fixing a specific known bottleneck | `craft`, `perf` mode |
| Checking the change before the PR | `review`, `change` and `perf` modes |
| The PR description | `copy`, team channel |
| A bug found during the audit | `resolve-bug` — separately, not here |

## A ticket reference is an input, not decoration

Where the request carries a tracker key or link — `ABC-1234`, a browse URL, or the key
sitting in the current branch name — **run `handoff` `ticket` before phase 1.**

```bash
git rev-parse --abbrev-ref HEAD | grep -oE '[A-Z][A-Z0-9]+-[0-9]+'
```

Working from the developer's retelling of a ticket loses three things that are only in the
ticket itself: the decisions made in its comments, the sibling tickets for the other
platforms, and the labels that say which platform owns it. Each of those changes the work.

The fetched task lands in `.dev-agent/tickets/<KEY>.md`, and its `GAP` lines marked as
another platform's are **blockers this pipeline cannot clear** — surface them at the first
gate rather than discovering them mid-implementation.

Where no tracker is reachable, say so once and continue from what the developer wrote.
A missing integration is never a reason to stop.

**When the finished work crosses a platform seam** — an endpoint, a payload field, an enum
value, a status transition, a shared string key — **run `handoff` `record` at the end.**
The other platform's developer is otherwise reading your diff to find out what they may
call.

## What delegation means here

**Delegating is reading, not dispatching.** Load that skill's `SKILL.md` and the reference
its mode names, then do the work **in this context** — the same conversation, the same
accumulated evidence, the same artifacts.

It is not spawning a subagent. A subagent gets an isolated context: it cannot see the
facts this pipeline established, it cannot read the artifacts earlier phases wrote, and it
returns prose rather than a file. The carry between phases is the entire reason this
pipeline is worth more than calling the skills by hand, and dispatching is how it is lost
— silently, because the output still looks like an answer.

Three rules:

| | |
|---|---|
| **Name it** | say which skill and which mode, before using it — an unnamed delegation is indistinguishable from improvising |
| **Read its reference** | the mode's reference file is where the method lives; the `SKILL.md` alone is the routing |
| **Write its artifact** | where the delegated skill owns a file, write that file, at its documented path — never a private substitute |

A phase that could have delegated and did not usually produced a shallower answer, and it
will not match what the next phase expects to read.

## Non-goals

- **Changing behaviour.** The whole point. A desired behaviour change is `enhance` or
  `improve`.
- Fixing bugs found on the way. Report them; they get their own work.
- Rewriting rather than refactoring. Where the answer is "start over", say so — it is a
  different decision with a different risk profile.
- **Committing, pushing, opening the PR.**
- Optimising without a measurement, or tidying without a reason a reader would recognise.
