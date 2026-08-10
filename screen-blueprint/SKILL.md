---
name: screen-blueprint
description: Specifies a screen before it is built — the full state matrix (empty, loading, partial, error, offline, no access, success), boundary data, dead ends, optimistic updates, flow, action hierarchy, form structure, navigation placement, and which existing components to reuse. Use when starting a screen without a complete design, when adding a screen to the product, or to check which states an existing screen is missing. Writes .dev-agent/screens/<slug>.blueprint.md. Триггеры — "спроектировать экран", "какие состояния нужны", "матрица состояний", "нет макета", "куда встроить экран", "как устроить форму".
---

# Screen Blueprint

Screens get built for the happy path. Empty, no-access and offline are discovered in
production. This skill front-loads them.

**The state matrix is the deliverable, not an appendix.** A blueprint without all seven
states answered is not finished. Everything else here supports it.

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

**Headline for this skill:** which states this screen needs that nobody asked for, and which components already exist to build them.

## Inputs

From `PRODUCT_REPO/.dev-agent/`, resolved from `PRODUCT_REPO`:

| File | Use | If absent |
|---|---|---|
| `features/<slug>.intake.md` | requirements, permissions, limits | ask at most three questions, then continue on marked assumptions |
| `component-inventory.md` | what already exists | scan the repository directly and say the inventory is unverified |
| `config.yaml` | platforms and their roots | detect from the repository |

Neighbouring screens in the codebase are an input too, and often the best one: they show
the conventions this screen must not break.

## Phases

### 1. Detect the state convention
Find how this repository already models loading and failure, and follow it. **Read
`references/flutter.md` or `references/vue.md` before this phase.**

*Done when:* the existing convention is named with a file path, or its absence is stated.

### 2. Fill the state matrix
**Read `references/state-matrix.md` before this phase.** Seven states, each answered or
explicitly marked not applicable with a reason.

*Done when:* every state has content or a reason it cannot occur. "Probably fine" is not
a reason.

### 3. Boundary data
Long values, zero rows, very many rows, missing images, emoji, truncation.

*Done when:* each boundary names what the screen does, not merely that the case exists.

### 4. Flow and hierarchy
Steps counted, dead ends found, back path confirmed. One primary action; the rest ranked
or moved out of sight.

*Done when:* every path off this screen has a destination, including failure paths.

### 5. Form structure
Field order, grouping, required marking, when validation fires, what survives an error.

*Done when:* the moment of validation is stated per field, and input preservation on
failure is answered. Skip the phase entirely when the screen has no form, and say so.

### 6. Reuse before invention
Search `component-inventory.md` and the code. Proposing a new component is allowed only
with a stated reason the existing ones fail.

*Done when:* every element in the blueprint names an existing component or carries that
reason.

### 7. Write the blueprint
**Read `references/blueprint-format.md`** — three other skills grep this file, so the
shape is a contract, not a preference.

*Done when:* the text slots and the interactive elements can each be extracted by the
documented commands, proven with their output.

## The boundary that matters most

This skill says *a "filter matched nothing" empty state is needed here*. It never writes
that text — `interface-copy` does. Naming the slot and its type is the whole job; filling
it is someone else's.

Same for `element-markup`: the blueprint lists interactive elements, it does not mark
them up.

## Non-goals

- Strings: `interface-copy`.
- Accessible names and analytics events: `element-markup`.
- Judging a screen already built: `screen-review`.
- Visual language — colour, type, style. The blueprint assembles from what exists.
- Screen code. The blueprint is what the developer builds from.
