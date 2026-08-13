# Channels that reach the user

> **Examples below are shapes, not facts about your codebase.** Measure before
> you quote any of them.

Four readers, four sets of constraints. Pick one before writing.

> **Examples below are shapes, not facts about your codebase.** Measure before you
> quote any of them.

Four readers, four sets of constraints. Pick one before writing.

## Release notes and store listings

> **Examples below are shapes, not facts about your codebase.** Field names, counts and
> paths in them are illustrative and were true of one repository at one moment. Measure
> before you quote any of them. A reference file that hands you a number is handing you a
> hypothesis.

### Two versions, produced together

| Version | Reader | Contains |
|---|---|---|
| **User** | someone deciding whether to update | what they can now do that they could not before |
| **Internal** | the team | what shipped, what to watch, what rolled back |

The internal version may name tickets, files and risks. The user version may not.

### Check whether prefixes classify anything at all

```bash
T=$(git log --oneline -100 | wc -l)
C=$(git log --oneline -100 | grep -cE ' (feat|fix|chore|build|refactor|docs|test|perf)(\(.+\))?:')
echo "$C of $T carry a conventional prefix"
```

Measured on one repository: **28 of 100**. The other 72 were ticket ids and bare text.
Below roughly half, prefix classification is not a shortcut — it is a sample.

### Filter by path before reading diffs

Reading 72 diffs to write three lines is the wrong trade. Paths classify mechanically and
cost nothing:

```bash
for c in $(git log --format=%h <range>); do
  n=$(git show --name-only --format="" $c | grep -cE '<user-visible path patterns>')
  t=$(git show --name-only --format="" $c | grep -c .)
  [ "$n" -gt 0 ] && echo "$c  user-visible $n/$t"
done
```

User-visible patterns are the directories holding screens, widgets and strings — take them
from `config.yaml`, not from memory. Everything under data sources, repositories, build
config and generated code is invisible by construction.

Measured on the same repository: **12 of 25** commits touched a user-visible path. That is
the set worth reading, and the ratio inside each commit is a second signal — a commit with
one user-visible file out of ten is a refactor that brushed a screen, not a feature.

### Deriving from commits

```bash
git log --oneline <previous-build>..<this-build>
```

Category per commit, from Conventional Commits where the repo uses it:

| Prefix | User-facing? | Category |
|---|---|---|
| `feat:` | usually | Added |
| `fix:` | usually | Fixed |
| `EPEOPLE-NNNN` | read the diff — the ticket id says nothing about visibility | depends |
| `build:`, `chore:`, `refactor:` | no | internal only |

This repository tags most work with a bare ticket id, so the prefix cannot classify it.
**Read the diff.** A change touching `lib/features/*/pages/` is user-visible; one touching
`lib/data_sources/` usually is not.

### The failure this file exists to prevent

The current default store text reads:

> "This update brings a bunch of behind-the-scenes fixes and tweaks… Nothing flashy to
> call out, just lots of little upgrades working together…"

It survives every release because it fits every release. It also tells the reader nothing,
in seven languages. A user deciding whether to update learns exactly as much as from a
blank field.

The replacement rule: **name one thing that changed for the user, or say plainly that this
build is fixes only and name what area they touch.** "Fixes to shift signing and project
loading" is short, true, and worth reading. "Lots of little upgrades" is neither.

### Store listing constraints

Store notes live in `DEFAULT_RELEASE_NOTES.md` / `RELEASE_NOTES.md`, split `# ANDROID` and
`# iOS`, with one block per locale.

| | |
|---|---|
| Google Play | 500 characters per locale |
| App Store | 4000 characters, but only ~3 lines visible before "more" |
| Locales | seven, and **the codes differ from the ARB files** |

| ARB file | Store tag |
|---|---|
| `intl_he.arb` | `<iw-IL>` |
| `intl_tl.arb` | `<fil>` |
| `intl_es.arb` | `<es-ES>` |
| `intl_fr.arb` | `<fr-FR>` |
| `intl_ru.arb` | `<ru-RU>` |
| `intl_zh.arb` | `<zh-CN>` |
| `intl_en.arb` | `<en-US>` |

`he` → `iw-IL` and `tl` → `fil` are the two that get mistyped; both are legacy codes the
stores still require. A wrong tag means that locale silently falls back to English.

Put the most important line first — on both stores the rest is behind a tap.

### Structure

```markdown
### What's new — 4.46.0

Shift signing now completes without returning to the project list.

Also fixed: project data loading on slow connections.
```

Two or three lines. Categories only when there is more than one item per category —
a heading over a single bullet is scaffolding.

### Internal version

```markdown
### 4.46.0 (287)

EPEOPLE-8815 — complete sequence flow
- complete_sequence_cubit.dart +91; sequence_repository.dart +50
- also touched: constants.dart, environment.dart — shared, regression risk
- watch: document signing from an alert, resignation flow

feat: project_data_source — full project fetch
```

## Push and in-app

| Android | ~50 chars | ~100 chars collapsed |

Beyond that it truncates without warning. Write to the smaller of the two and stop.

### Structure

Subject, verb, and the reason it is worth interrupting someone. The notification says what
happened and what waits; the app says the rest.

```
Meal break starts in 5 minutes
Sign in to record it before the window closes.
```

Not `Reminder` and not `You have a new notification` — both spend the interruption on
nothing.

### Frequency and grouping

Every notification needs an answer to: **what if five arrive at once?**

| Situation | Behaviour |
|---|---|
| Several of the same kind | collapse into a count, not five lines |
| Several kinds at once | one per kind, with a cap |
| The user has not opened the previous one | do not send the next of the same kind |

Grouping is part of the copy, not a platform detail. A grouped notification needs its own
text (`3 shifts need signing`), and if it has not been written, the app will show the last
one and hide the rest.

### Timing

A work-tracking product sends into people's actual shifts. Anything not tied to a moment
that matters to the recipient waits for working hours in **their** timezone — which this
product knows, and should use.

Never send during a meal break to say a meal break is happening.

### What a push may never carry

The lock screen is visible to anyone near the phone. Never in a notification: amounts,
document contents, health or compliance detail, disciplinary matters, another person's
name.

`A document needs your signature` is right. `Your disciplinary notice is ready` is a
disclosure to whoever is standing nearby.

### In-app

Same text, different constraints: more room, no lock-screen exposure, and the user is
already present — so an in-app message must justify interrupting what they came to do.
If the information can wait for the screen they are heading to, it is not a notification.

## Transactional email

| Preheader | ~90 chars | the sentence after the subject in the inbox list |
| Body | as short as the facts allow | what happened, what it means, one action |
| CTA | one | the single thing to do |
| Plain-text version | mirrors the body | half of enterprise mail clients block images |

The preheader is the most-wasted field in transactional email: left empty, clients fill it
with whatever markup comes first, usually "View this email in your browser".

### One action

Transactional mail carries one action. A second link competes with the first and lowers
both. If two things genuinely need doing, they are two emails or one email plus a screen
that holds both.

The CTA names the outcome — `Sign the document`, not `Click here` and not `Learn more`.

### Without images

Write so the email works with images blocked. That means: no meaning carried by an image
alone, alt text on every image that carries any, and a plain-text version that is a real
message rather than a stripped shell.

### Identity and trust

A work product's email lands beside payroll and HR mail, where users are alert to
phishing. Say which company and which account it concerns, state why they are receiving
it, and never ask for credentials — legitimate mail sends people to the app, it does not
collect.

### Locales

Seven. An email template with a hard-coded English fragment around a translated body is
the common defect — check the wrapper, not only the message.

Hebrew reverses direction: the template needs `dir="rtl"` support, not only translated
strings.

### Never in an email

Amounts and document contents unless the email exists specifically to deliver them; any
other person's data; and any date by which something will be fixed.

## Replying to a user

4. What happens next, without a date

```
You're seeing the associate list stay empty after you pick a date range.

That happens when the report request fails — the error appears briefly and then
the table is left blank, so it looks like there's simply no data.

For now: reload the page and pick the range again. If it stays empty, the data
for that range didn't load rather than being absent.

I've logged the missing error state. Someone will follow up here when it's fixed.
```

### Never

| Never | Because |
|---|---|
| a date or duration | it is the first thing forgotten and the only thing remembered |
| "known issue" | tells them others suffer too and nothing is happening |
| an internal cause — cubit, endpoint, cache | they cannot act on it and it reads as an excuse |
| "working as intended" | if they reported it, the intent is wrong |
| blame the user, however gently | "you may have clicked twice" ends the conversation |

### The apology question

Apologise once, briefly, when the product actually failed them. Do not apologise in every
paragraph — repetition reads as evasion. And do not apologise for something that worked
correctly; explain it instead.

### When there is no answer yet

Say that. A reply that says "I don't have the cause yet, here's what I've ruled out, I'll
come back when I know" is more useful than a confident guess that turns out wrong — which
costs a second message and the reader's trust in the first.

### Reproduction

If the report is unclear, ask for what is missing — and ask for **one** thing. A reply
containing five questions gets none answered. Pick the one that would narrow it most.

Route the answers to `resolve-bug`, which owns the loop from a complaint to a verdict — or to `debug` `reproduce` when only the steps are needed.

### Legal and compliance ground

This product covers meal breaks, disciplinary records and payroll. A reply touching any of
those states what the system recorded, never what the law requires or what the employer
should do.

```
⚖️ Needs review — the reply touches meal-break compliance
```

Quote what the product shows. Interpretation belongs to the employer and their counsel.
