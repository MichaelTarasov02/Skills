---
name: project-onboarding
description: Installs Dev Agent on a repository — works out what the product is, which platforms it runs on, where UI strings live, what design system exists, how loading and error states are modelled, which analytics SDK is present, and what may never be promised to users. Reads everything available before asking anything. Use when setting the agent up on a new project, or when the project has changed enough that its context is stale. Writes .dev-agent/project.md, config.yaml, onboarding.md. Триггеры — "настрой агента на проект", "онбординг", "подключи Dev Agent", "агент не знает про проект", "обнови контекст проекта".
---

# Project Onboarding

Without this, the other eight skills work blind. With a bad version of this, they work
confidently wrong.

**Never ask for what can be read.** A question whose answer sat in `pubspec.yaml` is a
defect. The measure of a good onboarding is how few questions it needed.

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

**Headline for this skill:** what the agent now knows about this project, and what it still needs from a human.

## Three input modes

Determine the mode from what arrived with the request, and say which one it is.

| Mode | Arrived | Behaviour |
|---|---|---|
| **A. Files** | paths, globs or URLs describing the product | **read, do not ask.** A question is allowed only if a required field is still empty after every source is read |
| **B. Text** | the product described in words | read it, compare against the required minimum, ask **only about the gaps** — never re-ask what was already said |
| **C. Nothing** | only "set the agent up here" | scan the code first, then ask about what code cannot show |

Modes combine. Exhaust every available source before the first question, in every mode.

Before asking anything, check: the code, the supplied files, and the standard places —
`README`, `CONTRIBUTING`, `package.json`, `pubspec.yaml`, `l10n.yaml`, `.env.example`,
`docs/`, ADRs.

## Source priority — fixed

**Code → supplied files → what the user said.**

Code is the only source that cannot be out of date about how things are now. When the user
says one thing and the code says another, show the discrepancy and take the code. Choosing
silently is the failure: the person who said it will keep believing it.

## Required minimum

Onboarding is complete when these eight are filled. Every field is tagged with its origin:
`code` / `file` / `user` / `assumption`.

| Field | Which skill goes blind without it |
|---|---|
| What the product does, who uses it | `feature-intake`, `interface-copy`, `screen-blueprint` |
| Platforms and their roots | `screen-blueprint`, `element-markup`, `screen-review` |
| Interface language | `interface-copy`, `outbound-writing` |
| Where UI strings live | `interface-copy` |
| Design system: own, external kit, or none | `screen-blueprint`, `screen-review` |
| How loading and error states are modelled | `screen-blueprint` |
| Analytics SDK, and whether a naming scheme exists | `element-markup`, `feature-handoff` |
| Red lines: what may never be promised, what is regulated | `interface-copy`, `outbound-writing` |

Desirable but non-blocking: product type and industry, tone of voice, issue tracker,
PR process, test infrastructure, which personal data is processed and under which
regulation, existing outbound channels, known pain points.

## Asking

**Four questions per round, three rounds, then stop.** Whatever is still unanswered
becomes an assumption, tagged in `onboarding.md`. Onboarding may not end empty because
someone got tired of answering.

**Offer options.** "What design system do you use?" costs the reader a paragraph.
"I see components in `src/components/` with no Storybook — is that (a) your own design
system, (b) a set of components with no system, or (c) wrappers over an external kit?"
costs them a letter.

## Phases

### 1. Mode and sources
Name the mode. List every source that will be read.

*Done when:* the mode is stated and unreadable sources are named rather than skipped.

### 2. Scan
**Read `references/scan-flutter.md` and `references/scan-vue.md` before this phase.**
Each is an executable recipe: which file, what to look for, how to read it. A monorepo
holding both platforms is the normal case, not an exception.

*Done when:* every required field is either filled from code or marked as not
determinable from code, with the file that was checked.

### 3. Reconcile
Compare what was scanned against what was said or supplied.

*Done when:* every discrepancy is listed with both versions and the code's version marked
as authoritative.

### 4. Gaps and questions
What remains empty, asked in batches under the limit.

*Done when:* every required field has an answer or a tagged assumption.

### 5. Write
`project.md`, `config.yaml`, `onboarding.md`. **Read `references/config-schema.md`
before this phase** — eight skills grep `config.yaml`, so its shape is a contract.

*Done when:* the documented grep commands return values, proven with their output.

### 6. Delegate
Invoke `product-lexicon`. It produces the vocabulary, tone and component inventory —
this skill does not.

*Done when:* the four lexicon artifacts exist, or the reason they do not is stated.

## Repeat runs

`.dev-agent/` already present: show what changed in the project since last time and extend.
Never overwrite. Fields tagged `user` survive a rescan — a human answered them, and the
scanner has no standing to replace that.

## Confidence is reported, not averaged

`onboarding.md` has three sections: **known** (with the source), **assumed** (with the
basis), **unknown** (with the consequence — which skill suffers). The third may not be
empty by default; an onboarding that knows everything did not look hard enough.

## Non-goals

- Glossary and tone of voice: `product-lexicon`. This skill orchestrates rather than
  duplicates.
- A tracking plan: `product-tracking-design-tracking-plan`.
- Code quality or architecture review.
- Product decisions and advice about what to build.
- Writing anywhere except `.dev-agent/`.
