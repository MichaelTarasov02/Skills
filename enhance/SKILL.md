---
name: enhance
description: Takes a small change to existing code from ticket to finished work — understands the business rule behind it, reads the code it lands in, writes a plan naming exactly what changes where, implements it in the project's own conventions without duplication, verifies the logic against the plan by reading, and reports what changed and why. Use for enhancements — extending a feature that already exists, finishing something half-built, adjusting a rule. Not for new functionality that needs designing. Триггеры — "доработай", "поправь логику", "добавь в существующее", "доделай фичу", "небольшая правка", "измени поведение".
---

# Enhance

A change to code that already exists. Six phases, one gate.

**The dominant risk is not doing it wrong — it is not fitting in.** New code gets judged
on whether it works; a change to existing code gets judged on whether it looks like it
was always there. Duplication, a second way of doing something the codebase already does,
a helper reinvented forty lines from its twin — these pass review more often than they
should and cost more than a bug.

**The existing code is most of the specification.** Whatever the ticket says, the
surrounding code has already decided the shape, the naming, the error handling and the
layering. Reading it is not preparation for the work; it is the larger half of it.

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

**Headline for this skill:** what the change actually is once the code is read, and what
in the code disagrees with the ticket.

## The pipeline

| # | Phase | Reference | Ends with |
|---|---|---|---|
| 1 | **Understand** | `references/phase-1-understand.md` | the business rule, and what the ticket leaves unsaid |
| 2 | **Explore** | `references/phase-2-explore.md` | where it lands, what it touches, questions for the engineer |
| 3 | **Plan** ⛔ | `references/phase-3-plan.md` | exactly what changes where, and the consequences — **gate** |
| 4 | **Implement** | `references/phase-4-implement.md` | the change, in the project's conventions |
| 5 | **Verify** | `references/phase-5-verify.md` | the plan checked against the code, by reading |
| 6 | **Report** | `references/phase-6-report.md` | what changed, why, and what it cost |

## Read the conventions before writing a line

**Read `references/conventions.md` before phase 4** — and skim it during phase 2, because
what the code already does constrains what the plan may propose.

The project's conventions are **detected, never prescribed**. A change written in the
style of a style guide, next to fifty files written another way, is a change that reads as
foreign no matter how correct it is.

## Enhancement or improvement — decide in phase 2 and be willing to stop

This skill is for extending what exists. It is not for new functionality that needs
designing, and the difference is not size:

| | Enhancement — this skill | Improvement — stop and route to `improve` |
|---|---|---|
| The shape exists | yes — you are filling it in or adjusting it | no — the shape has to be invented |
| The decisions are made | yes — the surrounding code made them | no — someone must decide how this works |
| The blast radius | one area, known from reading | unknown until designed |
| The question is | "how does this fit here" | "what should this be" |

**Say so and stop when a task turns out to be the second.** Enhancement machinery applied
to work that needs designing produces a change that fits the code and misses the point.
Growing this pipeline into a redesign mid-flight is how that happens.

## One interruption, not three

The phases each permit a question — the reason in phase 1, up to three in phase 2, the
gate in phase 3. Taken literally that is **three separate stops on a change sold as
small**, and a pipeline that interrupts three times is a pipeline people stop invoking.

**The budget is one round for the whole run, and it lands at the phase-3 gate**, batched
with the plan. Everything phase 1 and phase 2 wanted to ask is carried there and asked
once, with your recommended answer attached to each.

Two exceptions, and only two:

| Ask earlier when | Because |
|---|---|
| The answer decides whether this is `enhance` at all | continuing produces work that gets thrown away |
| Phase 2 cannot find the place without it | there is nothing to plan |

Anything else waits. A question asked at the gate arrives with the plan beside it, which
is when the engineer can actually judge it — the same question asked in phase 1 arrives
with no context and gets a worse answer.

Where a question was carried rather than asked, the plan says so: `Спросил бы раньше:
<вопрос>` — so the engineer can see what was held back rather than discovering it in the
diff.

## Contradictions are findings, not obstacles

The ticket and the code will disagree. When they do:

| Disagreement | What it usually means |
|---|---|
| The ticket describes behaviour the code does not have | either it was removed, or the ticket describes intent rather than reality |
| The ticket asks for something already there | the request is about a case that path does not cover |
| Two rules the change must satisfy conflict | the product has not decided; the change cannot decide for it |

Surface each one before phase 3. A plan built over a contradiction implements one side of
it silently, and which side was chosen becomes invisible the moment the PR merges.

## Filling gaps in the task

Tasks arrive with holes — no text for a new state, no error message, no name for
something. **Do not implement the hole and do not hand it back empty.**

Fill it, mark it, ask only for approval:

```
⚠️ В задаче не было текста для <место>.
   Предлагаю: «<текст>»
   Основание: <lexicon / tone-of-voice / соседний экран>
   Подтверди или поправь — реализую с ним.
```

Delegate the writing to `copy`; it reads the lexicon, the tone and the red lines. The
engineer's job is to look and approve, not to write.

The same applies to a missing default, a missing name, a missing edge-case decision. Fill,
flag, ask. **Never fill silently** — an unmarked gap becomes a requirement nobody agreed
to, and it is indistinguishable from a requirement someone did agree to.

## Bottlenecks found on the way

A change that reveals something structurally wrong nearby — a helper duplicated three
times, a function that grew past reading, a rule that should be data — reports it and does
**not** fix it. Fixing it makes the change unreviewable, and unreviewable changes get
approved without being read.

Name it, size it, and let the engineer decide whether it becomes its own task.

## What this delegates

| Need | Skill |
|---|---|
| The task is vague and hidden requirements are missing | `spec`, `task` mode |
| The change touches markup, an event, or performance | `craft` |
| Checking the change before the PR | `review`, `change` mode |
| The PR description | `copy`, team channel |
| The project's vocabulary and platform facts | `setup` output — `config.yaml`, `lexicon.md` |

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

- **Designing new functionality.** That is `improve`; this skill stops and says so.
- Refactoring beyond the change. Nearby problems are reported.
- **Committing, pushing, opening the PR.** Drafts are produced; the actions are a person's.
- Running test infrastructure. Phase 5 verifies by reading, deliberately.
- Deciding priority, or whether the change is worth making.
