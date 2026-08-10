---
name: outbound-writing
description: Writes everything that leaves the code as text — release notes and store listings, push and in-app notifications, transactional email, replies to user complaints, PR descriptions a non-developer can read, breaking-change announcements, status updates, blocker questions, escalations, code-review replies, feature documentation, and a two-minute demo script. Use when a feature is done and someone must be told, or when a message needs writing for any audience outside the code. Триггеры — "release notes", "что нового", "описание PR", "ответить пользователю", "анонс breaking change", "статус по задаче", "текст пуша", "сценарий демо".
---

# Outbound Writing

One job in every channel: **turn technical into human for a named audience**. The channel
decides tone, length and what may be said at all.

## Language

Answer in the language the request was written in. Findings, explanations, questions,
reports and section headings you produce for a developer follow their language — Russian
request, Russian answer.

**Text destined for the product's users is exempt.** Interface strings, release notes,
store listings and email stay in the product's interface language, taken from
`.dev-agent/config.yaml` → `interface.language`, whatever language the request used.
Mixing the two — an English report about Russian button labels, or the reverse — is the
failure this rule prevents.

**This skill splits it by channel**, because both kinds of text are its output:

| Channel | Language |
|---|---|
| Release notes, store listing, push, email, reply to a user | the **product's** interface language |
| PR description, breaking change, status, blocker, escalation, review reply | the **team's** language — the one the request came in |
| Feature documentation, demo script | the team's language |

A PR description in English for a team that writes Russian in the tracker is technically
correct and practically unread.

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

**Headline for this skill:** the text, ready to send. Notes about it come after it, not before.

## Pick the channel first

| Audience | Channel | Read before writing |
|---|---|---|
| User | release notes, store listing | `references/channels/release-notes.md` |
| User | push, in-app | `references/channels/push.md` |
| User | transactional email | `references/channels/email.md` |
| User | reply to a complaint | `references/channels/reply.md` |
| Team | PR description, breaking change, status, blocker, escalation, review reply | `references/channels/team.md` |
| Inward | feature documentation, demo script | `references/channels/internal.md` |

Writing before choosing produces a message shaped like the last one written, in the wrong
register for this reader.

## Inputs

From `PRODUCT_REPO/.dev-agent/`, resolved from `PRODUCT_REPO` and not from the working
directory:

| File | Use | If absent |
|---|---|---|
| `lexicon.md` | canonical terms for user-facing channels | say so, offer `product-lexicon`, mark terms as unverified |
| `tone-of-voice.md` | register for user channels | fall back to plain declarative prose and say that is what happened |
| `red-lines.md` | the phase 5 check | **name the gap loudly** — without it, nothing catches a promised date. Continue, and flag every sentence that commits to anything |
| `features/<slug>.intake.md` | what was asked | work from the diff alone and say the intent is unverified |
| `features/<slug>.handoff.md` | what is not done | omit the "known limitations" section rather than inventing it |

A missing file never stops the work. It changes what the output may claim, and the output
says which.

## Rules that hold in every channel

**The diff is the source, not the ticket.** For release notes and PR descriptions, read
what changed in the code. A ticket says what was intended; the diff says what shipped, and
they differ often enough that trusting the ticket is how a release note describes a
feature that got cut.

**Terms come from `lexicon.md`.** Release notes that name an entity differently from the
interface are defective, however well they read. `forbidden` synonyms are banned here as
strictly as in the interface.

**Two versions, never merged.** Release notes and breaking-change announcements exist for
users and for the team. Different facts, different tone. One text serving both serves
neither: the user gets internals, the team gets marketing.

**No dates, no durations, ever.** Not in a reply to a complaint, not in an escalation, not
in a status update. "Soon", "shortly", "in the next release" are dates wearing softer
words. This is the most expensive habit in outbound writing and the hardest to drop, since
it is what the reader asked for.

**Say what is known, name who decides the rest.** The substitute for a date is a fact plus
an owner: what is done, what is outstanding, and who resolves it.

## Phases

### 1. Channel and audience
Name both. Name what this reader already knows and what they need to decide.

*Done when:* the channel file has been read and the reader's decision is stated.

### 2. Gather from the source
Diff, commit range, `intake.md`, `handoff.md`. For a complaint, the reproduction steps.

*Done when:* every claim in the draft traces to something read, not recalled.

### 3. Write for the channel
Follow the channel file's structure. Length limits there are hard, not advisory —
store listings and push payloads truncate silently.

### 4. Lexicon and tone
Canonical terms; `tone-of-voice.md` for user channels.

*Done when:* no `forbidden` synonym survives.

### 5. Red lines — every time
Run the text against `red-lines.md`. This phase is not optional and not on request.

*Done when:* violations are quoted and listed, or the absence is stated explicitly.

### 6. De-slop
Strip the padding that generated text accumulates: "we're excited to", "a bunch of",
"under the hood", "nothing flashy", "seamless", "delightful". A release note that says
only that improvements happened has said nothing and cost the reader a minute.

*Done when:* every sentence carries a fact the reader did not have.

## Non-goals

- Interface strings: `interface-copy`.
- **Sending.** The skill produces text. Sending, posting, commenting, opening a PR — all
  belong to a person. Producing a draft is finishing the job, not half of it.
- Marketing copy and landing pages.
- Legal wording: raise the flag, phrase the question.
- Commits and PRs. The description is written here; the PR is opened by the developer.
