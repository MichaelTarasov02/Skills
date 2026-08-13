---
name: copy
description: Writes every piece of text the product produces — button labels, field labels, validation and server errors, empty states, confirmation dialogs, toasts, loading text, permission prompts, plus release notes, store listings, push, transactional email, replies to user complaints, PR descriptions, breaking-change announcements, status updates and escalations. Use when a screen needs strings, when a placeholder like "Error" is still in the code, when a release needs notes, or when something must be said to users or the team. Writes .dev-agent/screens/<slug>.strings.md. Триггеры — "что написать на кнопке", "текст ошибки", "пустое состояние", "микротексты", "release notes", "что нового", "описание PR", "ответить пользователю", "анонс breaking change", "статус по задаче".
---

# Copy

One job: **turn technical into human for a named reader.** Everything else — length,
tone, what may be said at all — follows from who is reading and where.

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
that substitution is invisible until it ships.

**Team channels follow the team's language.** A PR description in English for a team that
writes Russian in the tracker is technically correct and practically unread.

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

**Headline for this skill:** the text, ready to paste or send. Notes about it come after
it, never before.

## Pick the reader first

| Reader | Channel | Language | Read before writing |
|---|---|---|---|
| User, inside the product | buttons, labels, errors, empty states, dialogs, toasts, loading, permissions, limits | product's | `references/interface.md` |
| User, outside the product | release notes, store listing, push, email, reply to a complaint | product's | `references/outbound-user.md` |
| Team | PR description, breaking change, status, blocker, escalation, review reply | team's | `references/outbound-team.md` |
| Inward | feature documentation, demo script | team's | `references/internal.md` |

Writing before choosing produces a message shaped like the last one written, in the wrong
register for this reader.

**Read `references/style.md` before writing anything** — capitalisation, punctuation and
number rules are decided once, there, not re-argued per string.

## Inputs

From `PRODUCT_REPO/.dev-agent/`, resolved from the product repository:

| File | Use | If absent |
|---|---|---|
| `lexicon.md` | canonical terms are mandatory; every `forbidden` synonym is banned | say so, offer `setup`, mark terms unverified |
| `tone-of-voice.md` | register for user channels | fall back to plain declarative prose and say so |
| `red-lines.md` | the final check, every run | **name the gap loudly** — without it nothing catches a promised date |
| `screens/<slug>.blueprint.md` | the list of states and slots needing text | work from the code and say the slot list may be incomplete |

A missing file never stops the work. It changes what the output may claim, and the output
says which.

## Phases

### 1. Reader and channel
Name both. Name what this reader already knows and what they need to decide or do.

### 2. Gather from the source
For interface text: the screen, its blueprint, its existing strings. For release notes and
PR descriptions: **the diff, not the ticket** — a ticket says what was intended, the diff
says what shipped, and they differ often enough that trusting the ticket is how a release
note describes a feature that got cut.

*Done when:* every claim traces to something read, not recalled.

### 3. Write
Follow the channel reference. Length limits there are hard, not advisory — store listings
and push payloads truncate silently.

*Done when:* every slot has a string, and every action has 2–3 alternatives with one
recommended.

### 4. Terms and tone
Canonical terms from `lexicon.md`; `tone-of-voice.md` for user channels.

*Done when:* no `forbidden` synonym survives.

### 5. Make it translatable
Interface text only. **Read `references/i18n.md` before this phase.**

**What this phase means depends on whether the platform has an i18n layer**, and the two
answers are different jobs. Read it from `config.yaml` → the platform's `strings.library`,
and say which you found:

| Library | The work | Done when |
|---|---|---|
| present | extract to keys, kill concatenation, add translator context | no string is assembled from fragments at runtime, every key carries context, and every count-dependent string uses the platform's plural mechanism |
| **absent** | write the strings inline where they belong, and **record the gap** | every string is placed, concatenation is still killed, and the artifact says the platform is single-language by construction |

**Do not introduce an i18n layer as a side effect of writing copy.** That is a change to
the build, and it belongs to whoever owns the build.

The failure this split prevents: a completion criterion that cannot be met. A platform
with no plural mechanism can never satisfy "uses the platform's plural mechanism", so the
phase either never closes or closes while pretending — and both are worse than saying the
platform has no i18n and costing that out.

Where one platform is localised and another is not, **say it every time**. Wording agreed
for both exists in translated form on one side only, and that asymmetry decides what a
release note may claim.

### 6. Red lines — every run
**Read `references/red-lines-check.md` before this phase.** Run every produced string
against `red-lines.md`. Not optional, not on request.

*Done when:* the report has three buckets — violations quoted, correct-but-matched as a
count, ambiguous as a short list. One flat list of keyword hits is not a check.

### 7. De-slop
Strip what generated text accumulates: "we're excited to", "a bunch of", "under the
hood", "nothing flashy", "seamless", "delightful", "simply", "just".

*Done when:* every sentence carries a fact the reader did not have.

## Where the text lands

Interface strings go to `.dev-agent/screens/<slug>.strings.md`. **Everything else has a
home too, and it is the artifact of the work that produced it** — not the chat.

| Text | Goes into |
|---|---|
| Reply to whoever reported a bug, question to the product owner | `bugs/<slug>.md`, under `## Тексты` |
| PR description, release note for a change | `changes/<slug>.md` |
| The same, for a large piece of work | `features/<slug>/report.md` |
| The same, for a refactor | `refactors/<slug>/report.md` |
| Anything with no pipeline behind it | it lives in the chat — **say so**, and offer to place it |

Append; never overwrite the pipeline's own sections.

A reply drafted carefully, checked against the red lines and never written down is a reply
that gets rewritten from memory tomorrow, without the check. The artifact is also what
lets the next person see what was already said to this customer — which is the difference
between a follow-up and a contradiction.

**Producing the text is finishing the job. Sending it is not this skill's, and not the
agent's.**

## Text is not always the answer

A screen needing three sentences of explanation usually needs a simpler screen. When
explanation piles up around one control, say the control is the problem, name it, and
route to `review`. Writing better text over a confusing interface hides the defect and
makes it permanent.

## Non-goals

- Which states a screen has: `spec`.
- Accessible names and analytics event names: `craft`. Visible labels are here; the
  accessible name of an icon-only control is there.
- **Sending.** The skill produces text. Sending, posting, commenting, opening a PR —
  all belong to a person. Producing the draft is finishing the job, not half of it.
- Marketing pages and landing copy.
- Legal wording: produce the human sentence and flag it; the flag is the deliverable.
- **Dates and durations, in any channel.** "Soon", "shortly", "in the next release" are
  dates wearing softer words. The substitute is a fact plus an owner: what is done, what
  is outstanding, and who resolves it.
- Editing product code: produce the strings and say where they go.
