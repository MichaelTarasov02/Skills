---
name: ship-feature
description: Takes a feature from a two-line ticket to an open PR — works out what it actually requires and what blocks it, designs the screens and the data, writes the strings and the markup, checks it before the PR, and drafts the PR description and release note. Use when starting work on a feature, when a ticket is vague and the work is not, or when a feature is half done and needs finishing properly. Триггеры — "сделай фичу", "взял задачу", "с чего начать", "доведи до PR", "нужно реализовать", "сделай экран целиком".
---

# Ship Feature

The daily loop, as one pipeline. Five phases, two gates, and a route that depends on what
the work actually is.

**What this adds over calling the skills yourself:** the routing and the carry. Which
skills a feature needs is decided once, from the task; and each phase hands the next one
its artifact, so nothing gets re-derived and nothing gets skipped because it was somebody
else's step.

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

**Headline for this skill:** at every phase, what is decided and what is still open. At
the end, what is ready and what is not done.

## The pipeline

| # | Phase | Reference | Ends with |
|---|---|---|---|
| 1 | **Intake** | `references/phase-1-intake.md` | requirements, blockers, the route |
| 2 | **Design** ⛔ | `references/phase-2-design.md` | states, schema, contracts — **gate** |
| 3 | **Build** | `references/phase-3-build.md` | strings and markup, ready to paste |
| 4 | **Check** ⛔ | `references/phase-4-check.md` | ranked findings, what is not done — **gate** |
| 5 | **Ship** | `references/phase-5-ship.md` | PR description, release note, what to test |

## `ship-feature` or `improve` — the difference is the code

Both take a feature ticket, and their trigger phrases sit next to each other. They produce
different things, and picking wrong is the most expensive routing mistake in the agent:

| | `ship-feature` | `improve` |
|---|---|---|
| **Writes the implementation** | **no** — it produces the spec, the strings, the markup and the checks | **yes** — phase 4 writes the code |
| The developer wants | to be handed everything they need to write it themselves | the thing built |
| Ends with | artifacts and a PR description | working code, tests run, a report against the goal |
| Spans sessions | no | yes — it splits and resumes |
| The risk it manages | starting the wrong work | building something that does not connect to what exists |

**Ask in one line when it is not obvious**, because the answer changes everything
downstream:

> Тебе спецификацию и тексты, чтобы писать самому, или сделать целиком?

Where the answer is "целиком", say you are switching and switch. A pipeline that produces
a beautiful blueprint for someone who wanted working code has wasted the whole run, and
the mistake only becomes visible at the end.

## Route before you start

**Read `references/routing.md` before phase 1.** Which phases apply depends on the work,
and running all of them on a backend-only change wastes an hour producing empty sections.

| The feature is | Phases that matter |
|---|---|
| A new screen | all five — and phase 2 names the data shape |
| A change to an existing screen | 1, 3, 4, 5 — design only if states change |
| Backend or data only | 1, 2 (data — name the shape), 4, 5 — no strings, no markup |
| A rule change with no interface | 1, 4, 5 — and the release note matters most |
| Half-built, needs finishing | start at 4; work backwards for whatever it names as missing |

Say the route out loud in phase 1. A route stated is a route the engineer can correct.

## The two gates

**After phase 2:** the design is agreed before code exists. Changing a state matrix costs
a sentence; changing it after the screen is built costs the screen.

**After phase 4:** nothing is declared ready before the findings are seen. The gate is not
about permission to open a PR — it is about the engineer knowing what they are opening it
with.

Do not pass a gate by assuming agreement.

## Carry the artifacts forward

Each phase writes what the next one reads. This is what makes the pipeline worth more than
the skills run separately:

```
features/<slug>.intake.md
        └→ screens/<slug>.blueprint.md ─┬→ screens/<slug>.strings.md ─┐
        └→ data/<slug>.design.md        └→ screens/<slug>.markup.md  ─┴→ reviews/<slug>.review.md → PR
```

**Full paths, not bare names.** A phase looking for `blueprint.md` finds nothing; the
artifacts live under `.dev-agent/` at the paths above, and those paths are the contract.

Phase 3 produces **two** files, not one. Markup written only into the chat is markup phase
4 cannot check and a later session cannot find — which is the exact failure the carry
exists to prevent.

A phase that cannot find its input says so, names the phase that should have produced it,
and continues on stated assumptions — it never silently re-derives what was already
decided, because a re-derivation quietly disagreeing with the original is the worst
outcome available here.

## What this delegates

| Phase | Skill | Mode |
|---|---|---|
| 1 | `spec` | `task` |
| 2 | `spec` | `screen`, `data` — and which data shape: `read`, `write` or `schema` |
| 3 | `copy` | interface channel |
| 3 | `craft` | `markup` |
| 4 | `review` | `screen`, `change`, `perf` |
| 5 | `copy` | team and user channels |

Say which you invoked. A phase that could have delegated and did not usually produced a
shallower answer — and it will not match what the next phase expects to read.

Where the project has not been onboarded, `setup` runs first. Everything downstream reads
its config, and a pipeline started without it guesses at the platform.

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

- **Deciding whether to build it, or its priority.** That belongs to the product.
- **Writing the implementation.** This produces the spec, the strings, the markup and the
  checks; the code between them is the developer's.
- **Opening the PR, committing, or pushing.** Drafts are produced; the actions are a
  person's.
- An estimate in days.
- Finishing work the check phase says is not done. It reports; scaling down is a decision.
