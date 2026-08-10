---
name: product-lexicon
description: Builds and maintains the product's language — canonical terms, tone of voice, red lines, and component inventory — by extracting them from the codebase and UI strings rather than inventing them. Use when a new entity needs a name, when the same thing is called differently in UI and code, when renaming a term across the product, or when setting up Dev Agent on a repository. Writes .dev-agent/lexicon.md, tone-of-voice.md, red-lines.md, component-inventory.md. Триггеры — "как назвать сущность", "глоссарий продукта", "термины разъехались", "переименовать термин", "tone of voice", "инвентарь компонентов".
---

# Product Lexicon

Every other Dev Agent skill writes user-facing text. Without a shared vocabulary they
each invent one, and the product ends up calling the same thing three names. This skill
is where that vocabulary comes from.

**Extract, never invent.** Terms come out of the code and the UI strings. The skill
proposes a canonical form and marks it `proposed`; only a human moves it to `approved`.
A term the skill made up is a defect, not a contribution.

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

**Headline for this skill:** the canonical term, the size of the drift, and what to change first.

## Outputs

All four land in `PRODUCT_REPO/.dev-agent/`. Resolve that path from `PRODUCT_REPO`, never
from the working directory — this skill runs from a plugin cache.

| File | Holds |
|---|---|
| `lexicon.md` | canonical terms, grep-stable |
| `tone-of-voice.md` | how the product speaks |
| `red-lines.md` | what it must never say |
| `component-inventory.md` | what already exists, so nobody builds it twice |

## Phases

### 1. Locate platforms and sources
Detect which platforms the repository holds and where strings and components live.
**Read `references/flutter.md` and `references/vue.md` before this phase** — they name the
exact files and what to pull from each.

*Done when:* every detected platform has a named string source and a named component root,
with paths. A platform that is absent is stated as absent.

### 2. Extract term candidates
Pull nouns and noun phrases from string values, then from identifiers: feature
directories, view names, model classes, API fields.

*Done when:* every candidate carries a frequency count and at least one path. A candidate
with no location in code is dropped — it came from imagination.

### 3. Find drift
Three shapes, all of them real and all worth reporting separately:

| Shape | Signature |
|---|---|
| **Key–value drift** | the identifier says one word, the string it holds says another |
| **Synonym set** | several words carry one concept across platforms or layers |
| **Overloaded word** | one word carries several concepts |

*Done when:* each finding names both forms, counts occurrences of each, and cites paths.
A count without a path is not a finding.

### 4. Propose canonical forms
For every drift, propose one winner. Decide by: which form the user already sees most,
which form the domain uses, which form survives translation. State the reason.

*Done when:* every proposal carries a status and a reason. Nothing is marked `approved`
without a human answer in this session.

### 5. Tone of voice and red lines
Tone: address, sentence length, stance on humour, stance on the user's mistakes.
Red lines are phrased as checkable prohibitions — `interface-copy` and `outbound-writing`
run generated text against them, so "never state a restoration time" works and "be
careful with promises" does not.

*Done when:* every red line is checkable by reading a candidate string against it.

### 6. Component inventory
List what exists per platform, with paths, so `screen-blueprint` can reuse instead of
inventing.

*Done when:* each entry has a path that resolves.

### 7. Write, or diff
First run writes the four files. Every later run **diffs**: what is new, what changed,
what disappeared from the code. Never overwrite a file that holds approved terms.

*Done when:* on a repeat run, the diff is shown before anything is written.

## Term format

Other skills grep this. The shape is fixed — see `references/term-format.md` for the
full field list and the grep contract.

## When inputs are missing

| Situation | Behaviour |
|---|---|
| `.dev-agent/` absent | create it, run the full first pass |
| Repository unreachable | say so, offer to build the lexicon from conversation, mark every term `proposed` |
| Only one platform present | say which, skip the other, emit no empty sections |
| Existing `lexicon.md` with approved terms | diff mode; approved entries are never rewritten silently |

## Non-goals

- Naming the product for the market is branding — that decision lives with the product.
- Interface strings belong to `interface-copy`; this skill supplies the vocabulary they
  use.
- Renaming in code: the skill produces the migration plan and hands it to the developer,
  who runs it.
- Domain modelling: a working vocabulary is the goal, not a DDD model. For that, reach
  for `domain-modeling`.
