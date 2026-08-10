---
name: feature-intake
description: Breaks down an incoming task before any code is written — separates what is clear from what is ambiguous, digs out the hidden requirements nobody wrote down, produces checkable acceptance criteria and scope boundaries, and turns a vague bug report into reproduction steps. Use when picking up a task, when a ticket is two sentences long, or when a complaint arrives that nobody can reproduce. Writes .dev-agent/features/<slug>.intake.md. Триггеры — "разобрать задачу", "что тут неясно", "критерии приёмки", "что спросить у заказчика", "непонятный баг-репорт", "что мы забыли".
---

# Feature Intake

A problem caught here costs a fraction of the same problem caught at handoff. This is the
cheapest skill in the agent, and the one most easily ruined by asking too much.

## Language

Answer in the language the request was written in. Findings, explanations, questions,
reports and section headings you produce for a developer follow their language — Russian
request, Russian answer.

**Text destined for the product's users is exempt.** Interface strings, release notes,
store listings and email stay in the product's interface language, taken from
`.dev-agent/config.yaml` → `interface.language`, whatever language the request used.
Mixing the two — an English report about Russian button labels, or the reverse — is the
failure this rule prevents.

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

**Headline for this skill:** what the feature actually requires, what must be decided before code, and your recommendation for each decision.

## Facts and decisions

The whole skill turns on one split, inherited from `grilling`:

> **A fact can be looked up. A decision belongs to a person.**

Before any question reaches the developer, search `PRODUCT_REPO` for the answer. Roles,
limits, field names, existing behaviour, what the model already stores — all facts, all
retrievable. Asking a person for a fact that sits in a model file wastes the one thing
the skill is spending: their patience.

What genuinely remains — which behaviour is wanted, what the product means by a word,
what happens in a case the code has never handled — those go to people.

## Two modes

| Mode | When | Question budget |
|---|---|---|
| **Quick** | default | **at most 3 questions**, then done |
| **Deep** | the developer says the task is genuinely murky, or quick mode hits three blockers and still cannot describe the outcome | one question at a time, until the outcome is agreed |

Quick is the default and stays the default. Everything past the third question becomes an
assumption, written into the artifact under its own heading. A developer came to start
work, not to fill in a form.

## Question or assumption — no third option

Every unclear point lands in exactly one place:

| Lands in | When | Consequence |
|---|---|---|
| **Question** | work cannot start, or starting the wrong way wastes real effort | blocks; ranked first |
| **Assumption** | work can proceed and the cost of being wrong is bounded | does not block; written down and marked |

Deciding quietly on the customer's behalf is the failure this rule exists to prevent. An
unmarked decision is indistinguishable from a requirement, and nobody will ever question
it again.

## Every question carries your recommended answer

Taken from `grilling`, and the half most easily dropped: *for each question, provide your
recommended answer.*

A question with three options and no recommendation hands back the thinking you already
did. You read the code; the person answering did not. Say which option you would take and
why — in one line, from the evidence you gathered.

```
- Q2 [blocker]: Which source defines "on time" — the threshold_* fields, the project
  constants, or a new rule?
  Recommend: the project constants. The threshold_* values are derived from the signed
  times themselves, so a criterion built on them returns either nothing or noise.
```

They can overrule the recommendation in a word. Without it they must reconstruct the
reasoning, and the question sits unanswered for a day.

The same applies to a conflict between requirement and reality: name the conflict, list
the options with their costs, **and say which one you would pick**. Choosing the priority
is theirs; having an opinion is yours.

## Phases

### 1. Split clear from ambiguous
Read the task. For each ambiguous point, list the readings it permits.

*Done when:* every ambiguous point has at least two stated readings. One reading means it
was not ambiguous.

### 2. Look up the facts
Search the codebase for every point that could be settled by evidence.

*Done when:* each resolved point cites the file that resolved it. This phase is what
keeps the question count low.

### 3. Hidden requirements
**Read `references/hidden-requirements-web.md` and
`references/hidden-requirements-mobile.md` before this phase** and run both checklists
against the task.

*Done when:* each checklist item is answered, marked not applicable, or turned into a
question or assumption.

### 4. Acceptance criteria
Each one checkable — someone else can tell whether it holds without asking the author.

*Done when:* no criterion contains "properly", "correctly", "as expected", or a word
whose meaning depends on the reader.

### 5. Scope
In, out, and deferrable without harm.

*Done when:* the out-of-scope list is non-empty, or its emptiness is explained. Everything
in scope means nothing was bounded.

### 6. Success metric
What confirms the feature helped, and what would show it hurt.

*Done when:* both directions are named. A metric that can only go up measures nothing.

### 7. Data and consent
What personal data the feature touches, where it lands, who else receives it, whether
explicit consent is required.

*Done when:* the data table is filled or the feature is stated to touch none, and
anything regulated carries a legal-review flag.

### 8. Write the artifact
**Read `references/intake-format.md`** — `screen-blueprint` and `feature-handoff` read
this file mechanically.

*Done when:* the questions and assumptions can each be extracted by the documented
commands, proven with their output.

## When the requirement conflicts with reality

Name the conflict, give two or three alternatives, state the consequence of each, and say
which you would take. Which one wins is theirs to decide; leaving them without a
recommendation is not neutrality, it is withheld work.

## Bug reports

A complaint is a task with the facts missing. Same phases, different phase 1: reconstruct
what the person did, what they expected, what happened instead. Whatever the code can
tell you about the path they took, look up rather than ask — a reporter who could answer
precisely would have written a bug report, not a complaint.

## Non-goals

- Screen design: `screen-blueprint`.
- Writing the implementation spec or picking the architecture.

**These non-goals restrict what you decide, never what you recommend.** Naming the
approach you would take, and why, is part of the answer — the developer asked for help,
not for a form. What stays out of bounds is deciding *for* them: priority, whether to
build it, and the estimate.
- **A number for how long it will take.** Break the work into parts a non-developer can
  read; the number is the developer's to say. The pull toward answering "about three
  days" is strong and it is out of bounds.
- Deciding whether the feature is worth building — that is the product's call.
- Legal opinions on consent: raise the flag and phrase the question.
