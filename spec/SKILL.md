---
name: spec
description: Works out what to build before any code is written — breaks down a vague task into checkable requirements and the questions that block it, designs a screen with its full state matrix, and designs data schemas, migrations and API contracts. Use when picking up a task, when a ticket is two sentences long, when starting a screen without a complete design, when adding or changing tables and endpoints, or when a bug report needs turning into reproduction steps. Writes .dev-agent/features/, screens/, data/. Триггеры — "разобрать задачу", "что тут неясно", "критерии приёмки", "спроектировать экран", "какие состояния нужны", "нет макета", "схема таблиц", "миграция", "контракт API", "как хранить".
---

# Spec

Everything before the first line of code. A problem caught here costs a fraction of the
same problem caught at review.

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

**Headline for this skill:** what this actually requires, what must be decided before
code, and your recommendation for each decision.

## Modes — name the one you are in

| Mode | The request looks like | Read before working | Produces |
|---|---|---|---|
| **`task`** | "вот задача", a two-line ticket, a complaint | `references/hidden.md` | `features/<slug>.intake.md` |
| **`screen`** | "нужен экран", "какие состояния" | `references/screen.md` | `screens/<slug>.blueprint.md` |
| **`data`** | "как хранить", "схема", "миграция", "endpoint", "экран настроек" | `references/data.md` | `data/<slug>.design.md` |

`data` has three shapes — `read`, `write`, `schema` — and they use different halves of
their reference. Name the shape as well as the mode; the pipelines route by it, and
`write` mistaken for `read` is how a settings screen ships with no validation and no
decision about who may change the value.

Most real requests are **two modes**. "Сделай отчёт по пропущенным перерывам" is `task`
plus `data` plus `screen`. Run each in that order, say that you are doing so, and let the
earlier ones feed the later — the questions from `task` decide the shape of the data, and
the data decides what the screen can show.

Running one mode when the request needs three is the most common way this skill
under-delivers.

## Facts and decisions

The rule the whole skill turns on:

> **A fact can be looked up. A decision belongs to a person.**

Before any question reaches the developer, search the repository. Roles, limits, field
names, existing behaviour, what the model already stores, which endpoint already returns
this — all facts, all retrievable. Asking a person for a fact that sits in a model file
wastes the one thing this skill spends: their patience.

Read `.dev-agent/config.yaml` first; it names the platforms, the roots and the framework
majors. Getting the major wrong produces advice that does not compile.

## Every question carries your recommended answer

A question with three options and no recommendation hands back the thinking you already
did. You read the code; the person answering did not.

```
- Q2 [blocker]: <the decision>
  Recommend: <your option>. <one line of reasoning from the evidence you gathered>
```

They overrule it in a word. Without it, the question sits unanswered for a day.

## Question or assumption — no third option

| Lands in | When | Consequence |
|---|---|---|
| **Question** | work cannot start, or starting wrong wastes real effort | blocks; ranked first |
| **Assumption** | work can proceed and the cost of being wrong is bounded | does not block; written down and marked with that cost |

Deciding quietly on the customer's behalf is the failure this prevents. An unmarked
decision is indistinguishable from a requirement, and nobody questions it again.

**Budget: three questions.** Everything past the third becomes an assumption. A developer
came to start work, not to fill in a form.

## Shared phases

Every mode runs these; the mode reference says what each means for it.

### 1. Establish the mode and the facts
Name the mode or modes. Search the repository for everything answerable by evidence.

*Done when:* each resolved point cites the file that resolved it. This phase is what keeps
the question count low.

### 2. Separate clear from ambiguous
For each ambiguous point, list the readings it permits. One reading means it was not
ambiguous.

### 3. Hidden requirements
**Read `references/hidden.md` before this phase** and run the checklist for every platform
the change touches.

*Done when:* each item is answered, marked not applicable, or turned into a question or
assumption.

### 4. Design
The mode's own work — requirements, state matrix, or schema. Follow the mode reference.

### 5. Checkable criteria
Each one verifiable by someone who did not write it.

*Done when:* no criterion contains "properly", "correctly", "as expected", "works", or a
word whose meaning depends on the reader.

### 6. Write
**Read `references/formats.md`** — three skills read these artifacts mechanically, so the
shapes are contracts.

*Done when:* the documented extraction commands return values, proven with their output.

## When the requirement conflicts with reality

Name the conflict, give two or three alternatives, state the consequence of each, and say
which you would take. Which one wins is theirs to decide; leaving them without a
recommendation is not neutrality, it is withheld work.

## Non-goals

- Writing the strings: `copy`. Name the slot and its type; filling it belongs there.
- Accessibility markup and analytics events: `craft`.
- Judging something already built: `review`.
- Finding why something broke: `debug`.
- Visual language — colour, type, style. The spec assembles from what exists.
- **A number for how long it will take.** Break the work into parts a non-developer can
  read; the number is the developer's to say.
- Deciding whether the feature is worth building, or its priority.

**These restrict what you decide, never what you recommend.** Naming the approach you
would take, and why, is part of the answer — the developer asked for help, not a form.
