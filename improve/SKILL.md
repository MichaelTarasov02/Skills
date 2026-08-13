---
name: improve
description: Takes a large change from task to shipped functionality — reads the business goal as a product analyst would and flags what should be settled before coding, designs how the new part merges into the existing system and where coupling forces other changes, writes a specification split into sessions if it is too big for one, implements in the project's conventions, writes and runs tests, and reports what was built against the goal. Use for new functionality, multi-area changes, anything needing design before code. Триггеры — "новая фича", "большая задача", "нужно спроектировать", "добавить функциональность", "как это ляжет в систему", "improvement".
---

# Improve

Large changes: new functionality, several areas, design before code. Six phases, two
gates.

**More gates than the other pipelines, deliberately.** The work is big enough that a wrong
turn costs days rather than an hour, so the engineer gets more places to redirect it. The
agent does the work; the gates are where they steer.

**Two symbols, and they mean different things.** ⛔ stops and waits for an answer. ⚠ raises
something and **carries on** — it is a flag in the output, not a question. Phase 1 is ⚠:
a product contradiction is worth stating and almost never worth halting for, and a heavy
pipeline that stops before it has read any code is a pipeline that gets abandoned at the
first phase.

Marking both with the same symbol is how a soft gate becomes a hard one in practice: the
runtime reads the table, not the paragraph.

**What separates this from `enhance`:** there, the surrounding code had already made the
decisions. Here the decisions do not exist yet, and the expensive failure is not bad code
— it is functionality that works and does not connect to what is already there.

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

**Headline for this skill:** what is being built, what it touches that nobody mentioned,
and what needs deciding before the next phase.

## Before phase 1: is this already in progress?

**Run this first, every time, before reading the task.** The pipeline splits work across
sessions, and a split only works if the next session knows it is the next session.

```bash
ls .dev-agent/features/*/progress.md 2>/dev/null
```

Anything returned is a feature mid-flight. Read its `progress.md` and its `spec.md`, then
decide:

| Situation | Route |
|---|---|
| The request is that feature's next part | **resume** — skip phases 1–3 entirely, go to phase 4 with `part-N.md` |
| The request is that feature, but the plan no longer fits | resume at phase 3, and say which part boundaries move and why |
| Unrelated | continue to phase 1, and say which in-progress features you found and ignored |

**Resuming is not re-deciding.** Phases 1–3 already ran, against context this session does
not have; running them again produces a second specification that disagrees with the first
in ways nobody notices until the parts stop fitting together. Where the existing spec is
genuinely wrong, say so and change it deliberately — but never by quietly re-deriving it.

State the route out loud: `Продолжаю <slug>, часть N из M` or `Новая работа; в работе
также: <list>`. A resume nobody announced is indistinguishable from a fresh start.

## The pipeline

| # | Phase | Reference | Ends with |
|---|---|---|---|
| 1 | **Brainstorm** ⚠ | `references/phase-1-brainstorm.md` | the goal, and what should be settled with the product first — **soft gate** |
| 2 | **Design** ⛔ | `references/phase-2-design.md` | how it merges, and everything coupling forces — **gate** |
| 3 | **Specify** ⛔ | `references/phase-3-specify.md` | the plan, split into sessions if needed — **gate** |
| 4 | **Implement** | `references/phase-4-implement.md` | the code, in the project's conventions |
| 5 | **Test** | `references/phase-5-test.md` | tests written and run, spec and goal checked |
| 6 | **Report** | `references/phase-6-report.md` | what was built, against what was wanted |

## The product-analyst pass is soft, and it is not optional

**Read `references/product-check.md` before phase 1.** Before touching the system, read
the task the way a product analyst would: what is the goal, does the described solution
reach it, does it contradict something the product already does.

**Soft means: raise it, do not block on it.** The engineer decides whether it is worth
taking back to the product owner. What this pipeline must never do is notice a
contradiction and implement anyway — a large change built over an unresolved product
question is a large change that gets reverted.

Most tasks pass this cleanly and the phase is three sentences. The ones that do not are
the ones worth the whole pipeline.

## Coupling is where large changes actually fail

**Read `references/coupling.md` before phase 2.** In a connected system, adding
functionality is rarely additive: something that already exists needs to know about the
new thing, and the places that need to know are not the places you are editing.

A screen that filters by a new field, an export that should include it, a permission that
should cover it, a report that now under-counts. Each is small; each is invisible from the
diff; and each is expensive once the feature has shipped without it.

Finding these is most of phase 2's value.

## Filling gaps in the task

Tasks arrive with holes — no text for the new screen, no empty state, no error message,
no name for the new entity. **Do not implement the hole and do not ask the engineer to
fill it.**

Fill it, mark it, and ask only for approval:

```
⚠️ В задаче не было текста для <место>.
   Предлагаю: «<текст>»
   Основание: <lexicon / tone-of-voice / соседний экран>
   Подтверди или поправь — реализую с ним.
```

Delegate the writing to `copy`; it reads the lexicon, the tone and the red lines. The
engineer's job is to look and approve, not to write.

The same applies to a missing name, a missing default, a missing edge-case decision. Fill,
flag, ask for approval. **Never fill silently** — an unmarked gap becomes a requirement
nobody agreed to.

## Splitting across sessions

**Read `references/splitting.md` before phase 3.** Where the work will not fit in one
session, the specification becomes a numbered series of prompts, each self-contained and
each leaving the project working.

The split is part of the specification and is approved with it. Discovering mid-implementation
that the work does not fit is how half-built functionality gets merged.

## What this delegates

| Need | Skill |
|---|---|
| Hidden requirements, acceptance criteria | `spec`, `task` mode |
| Screen states, schema, API contract | `spec`, `screen` and `data` modes |
| Any text the task did not provide | `copy` |
| Markup, analytics events, performance | `craft` |
| Checking before the PR | `review`, `change` mode |
| The project's platform facts and vocabulary | `setup` output |

Where the task turns out to be small and the shape already exists, say so and route to
`enhance`. Running this pipeline on a two-file change produces four ceremonial phases.

**Where the developer wants to write the code themselves, route to `ship-feature`.** It
covers the same ground and stops before the implementation: spec, strings, markup, checks,
PR description. This pipeline writes the code. That is the whole difference between them,
and it is worth one line of confirmation before phase 2 rather than a discovery at phase 4:

> Сделать целиком, или подготовить спецификацию и тексты, чтобы ты писал сам?

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

- **Deciding whether to build it, or its priority.** Raise the product question; the
  answer is theirs.
- **Committing, pushing, opening the PR.** Drafts are produced; the actions are a person's.
- Refactoring beyond what the design requires. Nearby problems are reported, sized, and
  left.
- Filling a gap in the task silently.
- Declaring the goal met without checking it in phase 5.
