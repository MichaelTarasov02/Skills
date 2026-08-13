---
name: setup
description: Learns the project so every other skill stops guessing — platforms, where UI strings live, design system, how loading and error states are modelled, analytics SDK, plus the product's vocabulary, tone of voice and what may never be promised to users. Reads the code before asking anything. Use when installing Dev Agent on a repository, when a term needs naming, when the same thing is called differently in UI and code, or when the project changed enough that the agent's context is stale. Writes .dev-agent/. Триггеры — "настрой агента", "онбординг", "подключи Dev Agent", "как назвать сущность", "глоссарий продукта", "термины разъехались", "tone of voice", "обнови контекст проекта".
---

# Setup

Everything the other skills know about the project comes from here. Get this wrong and
they work confidently wrong.

**Never ask for what can be read.** A question whose answer sat in `pubspec.yaml` is a
defect. The measure of a good setup is how few questions it needed.

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

**Headline for this skill:** what the agent now knows about this project, and what it
still needs from a human.

## Modes — say which one out loud

| Mode | Trigger | Produces |
|---|---|---|
| **`full`** | first run on a repository, or "настрой агента" | everything below |
| **`term`** | one entity needs a canonical name | one term card in `lexicon.md` |
| **`drift`** | "термины разъехались", or a rename is planned | the drift report and a migration plan |
| **`refresh`** | the project moved on | a diff against what is already recorded |

`full` on an already-configured repository degrades to `refresh` automatically. Say so
rather than rescanning from zero.

## Source priority — fixed

**Code → supplied files → what the user said.**

Code is the only source that cannot be out of date about how things are now. When the
user says one thing and the code says another, show the discrepancy and take the code.
Choosing silently is the failure: the person who said it will keep believing it.

Before asking anything, check the standard places: `README`, `CONTRIBUTING`,
`package.json`, `pubspec.yaml`, `l10n.yaml`, `.env.example`, `docs/`, ADRs.

## Outputs

All under `PRODUCT_REPO/.dev-agent/`, resolved from the product repository and never from
the working directory — this skill runs from a plugin cache.

| File | Holds | Modes |
|---|---|---|
| `config.yaml` | machine-readable: platforms, paths, i18n, analytics | full, refresh |
| `project.md` | what the product is, who uses it | full, refresh |
| `onboarding.md` | known / assumed / unknown, with sources | full, refresh |
| `lexicon.md` | canonical terms, grep-stable | all |
| `tone-of-voice.md` | how the product speaks | full |
| `red-lines.md` | what it must never say | full |
| `component-inventory.md` | what exists, so nobody builds it twice | full, refresh |

## Required minimum

`full` is complete when these eight are filled, each tagged `code` / `file` / `user` /
`assumption`.

| Field | Which skill goes blind without it |
|---|---|
| What the product does, who uses it | `spec`, `copy` |
| Platforms and their roots | `spec`, `craft`, `review` |
| Interface language | `copy` |
| Where UI strings live | `copy` |
| Design system: own, external kit, or none | `spec`, `review` |
| How loading and error states are modelled | `spec` |
| Analytics SDK, and whether a naming scheme exists | `craft`, `review` |
| Red lines: what may never be promised, what is regulated | `copy` |

Desirable, non-blocking: product type and industry, issue tracker, PR process, test
infrastructure, which personal data is processed and under which regulation, existing
outbound channels, known pain points.

**Prove the minimum, do not assert it.** Each of the eight maps to a key that must be
present — including when the answer is `null`. Run this before declaring `full` complete
and paste the output:

```bash
cd <PRODUCT_REPO> && N=$(grep -c '^  - id: ' .dev-agent/config.yaml) && echo "platforms: $N" && \
for k in '^product:' '^interface:' '^backend:' '^red_lines:'; do
  printf '%-16s %s  (want 1)\n' "$k" "$(grep -c "$k" .dev-agent/config.yaml)"
done && \
for k in '^    framework:' '^    strings:' '^    design_system:' '^    state_approach:' '^    analytics:'; do
  printf '%-22s %s  (want %s)\n' "$k" "$(grep -c "$k" .dev-agent/config.yaml)" "$N"
done
```

**Anchor every pattern.** An unanchored `analytics` matches `firebase_analytics` too and
reports four where there are two — a check that counts substrings passes a file that is
missing the key.

A count below the platform count is a platform missing that field, not a formatting
question. `red_lines` is the line that is normally zero, because it is the only one of the
eight that cannot be read out of code — which is why it is the field a tired setup drops.

## Asking

**Four questions per round, three rounds, then stop.** Whatever is unanswered becomes an
assumption tagged in `onboarding.md`. Setup may not end empty because someone got tired
of answering.

**Offer options.** "What design system do you use?" costs a paragraph. "I see components
in `src/components/` with no Storybook — is that (a) your own system, (b) components with
no system, or (c) wrappers over an external kit?" costs a letter.

## Phases

### 1. Mode and sources
Name the mode. List every source that will be read; name the unreadable ones rather than
skipping them silently.

### 2. Scan the stack
**Read the scan recipe for every platform present before this phase** —
`references/scan-flutter.md`, `references/scan-vue.md`, `references/scan-backend.md`. The
backend is not optional: the data domain in `spec` reads from it, and half the product's
vocabulary lives in model field names.

Each recipe is executable: which file, what to look for, how to read it. A monorepo
holding several platforms is normal, not an exception.

*Done when:* every required field is filled from code, or marked not determinable from
code with the file that was checked.

### 3. Extract the vocabulary
Terms come out of string values and identifiers — feature directories, view names, model
classes, API fields. **Extract, never invent.** A term the skill made up is a defect.

*Done when:* every candidate carries a frequency count and at least one path. A candidate
with no location in code is dropped.

### 4. Find the drift
| Shape | Signature |
|---|---|
| **Key–value drift** | the identifier says one word, the string it holds says another |
| **Synonym set** | several words carry one concept across platforms or layers |
| **Overloaded word** | one word carries several concepts |
| **False synonym** | two words look like a synonym set and name different things |

**Rule out the fourth before reporting any of the first three.** Two words with lopsided
counts read as a synonym set and a rename waiting to happen. Often they are two entities,
and the rare one is rare because it is narrower — not because it is losing.

The check is cheap and decisive: **do both forms exist as their own type?**

```bash
grep -rnE "^class (Alpha|Beta)\b" --include=models.py .   # backend types
grep -rnE "class (Alpha|Beta)\b" --include='*.dart' lib   # client types
```

Two classes with their own fields, their own table and their own foreign keys are two
concepts until something proves otherwise. Open both and compare what they hold — a flat
row of imported identifiers beside a model with behaviour and lifecycle is an import
record beside a domain entity, not an old name beside a new one.

A false synonym filed as a synonym set produces a canonical form, a `forbidden` entry that
bans a live entity's name, and a migration plan that merges two tables' vocabulary. It is
the most expensive mistake this phase can make, and it is invisible from counts alone.

*Done when:* each finding names both forms, counts each, cites paths, and — for anything
proposed as a synonym set — says which check ruled out the false-synonym case.

### 5. Propose canonical forms
Decide by: which form the user already sees most, which the domain uses, which survives
translation. **Read `references/term-format.md`** — other skills grep this file, the
shape is a contract.

*Done when:* every proposal carries a status and a reason. Nothing is `approved` without
a human answer in this session.

### 6. Tone and red lines
Tone: address, sentence length, stance on humour, stance on the user's mistakes.
Red lines are checkable prohibitions — `copy` runs generated text against them, so
"never state a restoration time" works and "be careful with promises" does not.

### 7. Component inventory
What exists per platform, with paths, so `spec` reuses instead of inventing.

### 8. Write, or diff
First run writes. Every later run **diffs**: what is new, what changed, what vanished
from the code. Fields tagged `user` survive a rescan — a human answered them.
**Read `references/config-schema.md`** before writing `config.yaml`.

*Done when:* the documented grep commands return values, proven with their output.

## Confidence is reported, not averaged

`onboarding.md` has three sections: **known** (with source), **assumed** (with basis),
**unknown** (with the consequence — which skill suffers). The third may not be empty by
default; a setup that knows everything did not look hard enough.

Asymmetries between platforms are recorded per platform, never averaged. Mobile localised
and web not, mobile with analytics and web without — each matters to a different skill.

## When inputs are missing

| Situation | Behaviour |
|---|---|
| `.dev-agent/` absent | create it, run `full` |
| Repository unreachable | say so, offer to build from conversation, mark every term `proposed` |
| One platform only | say which, skip the others, emit no empty sections |
| No platform recognised, but the directory has code | name what markers were looked for and which were absent, then ask what the stack is — one question, with the candidates you did see |
| Directory is empty | say so plainly; offer to build from conversation with everything tagged `assumption` |
| Existing `lexicon.md` with approved terms | diff mode; approved entries are never rewritten silently |

## Non-goals

- Naming the product for the market — that is branding, and it belongs to the product.
- Interface strings: `copy`. This skill supplies the vocabulary they use.
- Renaming in code: produce the migration plan, the developer runs it.
- A tracking plan: `product-tracking-design-tracking-plan`.
- Code quality or architecture review: `review`.
- Writing anywhere except `.dev-agent/`.
