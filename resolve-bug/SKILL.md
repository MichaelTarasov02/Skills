---
name: resolve-bug
description: Takes a bug from a complaint to a closed loop — gathers context with the engineer, plans where to look, diagnoses across three branches (user error, working as designed but wrong for the product, real defect), gets approval before touching code, fixes, and produces an audit a reviewer can verify plus the reply for whoever reported it. Use when a bug report arrives, when a user complains about behaviour, when something works but nobody is sure it should, or when a defect needs finding and fixing end to end. Триггеры — "разбери баг", "почему так работает", "пользователь жалуется", "это баг или так задумано", "найди и почини", "разобраться с проблемой".
---

# Resolve Bug

A pipeline, not a single answer. Six phases, two gates, and a verdict that may well be
"nothing is broken".

**The premise most bug work gets wrong:** it assumes a defect exists. Often the system did
exactly what it was built to do, and the disagreement is with the product, not with the
code. Diagnosing that as a defect produces a fix that breaks correct behaviour.

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

**Headline for this skill:** at every phase, what you now know and what you need to move
on. At the end, the verdict and what it costs.

## The pipeline

| # | Phase | Reference | Ends with |
|---|---|---|---|
| 1 | **Intake** | `references/phase-1-intake.md` | the report restated as facts, and what is still unknown |
| 2 | **Plan** ⛔ | `references/phase-2-plan.md` | hypotheses, where you will look, what would confirm each — **gate** |
| 3 | **Diagnose** | `references/phase-3-diagnose.md` | evidence per branch, with what was ruled out |
| 4 | **Verdict** ⛔ | `references/phase-4-verdict.md` | which of three branches, and what follows — **gate** |
| 5 | **Fix** | `references/phase-5-fix.md` | the change, before and after |
| 6 | **Report** | `references/phase-6-report.md` | the audit, plus the reply to whoever reported it |

Phase 5 is skipped for two of the three verdicts, and that is the normal outcome, not a
failure to find something.

## The two gates are real stops

**After phase 2:** you say where you will look and why. The engineer knows things the code
does not — that this area was rewritten last month, that this customer has a strange
configuration, that this was already investigated. Two minutes here saves an hour of
looking in the wrong place.

**After phase 4:** nothing is edited before the verdict is accepted. A fix applied to a
misdiagnosis is worse than no fix — it removes the symptom, leaves the cause, and consumes
the evidence.

Do not pass a gate by assuming agreement. Ask, and wait.

**A gate can be cleared in advance, but only explicitly, and never silently.** "Разберись
и почини" pre-clears gate 1 — the engineer has said they do not want to review the search
plan. It does **not** pre-clear gate 2: approving a fix in advance is approving a fix for a
cause nobody has named yet, and the verdict is the thing most worth being wrong about.

Where a gate is pre-cleared, **say what you would have asked and carry on**:

> Гейт 1 снят — иду по плану ниже. Спросил бы: <вопрос>. Если ответ другой — останови.

That sentence costs one line and preserves the only thing the gate was for: the chance to
be redirected before the cost is paid. Skipping the gate without it converts an
authorisation to move fast into an unrecorded decision.

## Three branches, equal weight

**Read `references/branches.md` before phase 3.** The whole skill turns on telling them
apart:

| Branch | What it means | What follows |
|---|---|---|
| **User error** | the system behaved correctly; the person expected something else | a reply that explains without blaming, and a note on whether the interface invited the mistake |
| **By design, wrong for the product** | the code matches its rules; the rules no longer match what the product wants | a question to the product owner, with what it would cost to change |
| **Defect** | behaviour contradicts its own rules | a fix |

The second branch is the one that gets misfiled. It looks like a bug to the reporter and
like correct behaviour to the code — and it is neither. Filing it as a defect produces a
fix nobody asked for; filing it as user error tells a person they are wrong when the
product is.

## Half of this job is support, not engineering

Every verdict ends in something written for a human who is not you:

| Verdict | Who reads it | Delegate to |
|---|---|---|
| User error | the person who reported it | `copy`, reply channel |
| By design | the product owner | `copy`, team channel — the blocker-question shape |
| Defect | the engineer reviewing the fix | this skill's phase 6 |

Never send any of them. Produce the text; sending belongs to a person.

## What this skill delegates

It orchestrates rather than reimplements. Use the skill that owns each piece:

| Need | Skill |
|---|---|
| Reproduction from a vague complaint, narrowing, regression range, what is slow | `debug` |
| The fix is markup, an event, or a performance change | `craft` |
| The fix needs a design decision or a schema change | `spec` |
| The reply to the user, the question to the product owner | `copy` |
| Checking the fix is complete before the PR | `review` |

Say which you invoked. A phase that could have delegated and did not usually produced a
shallower answer.

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

- **Deciding whether to fix.** Report the verdict, the blast radius and the cost; priority
  belongs to a person.
- **Sending anything.** Replies, questions, comments — all drafted here, sent by a human.
- Touching production data to test a theory.
- Fixing beyond the diagnosed cause. A second defect found on the way is reported, not
  silently included — it makes the change unreviewable.
- Closing the loop without evidence the symptom is gone.
