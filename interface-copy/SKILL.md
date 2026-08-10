---
name: interface-copy
description: Writes and revises every piece of text a user sees inside the interface — button labels, field labels, validation and server error messages, empty states, confirmation dialogs, toasts, loading text, permission prompts, onboarding hints, and limit notices — in English, using the product's own vocabulary and tone. Use when a screen needs its strings written, when a placeholder like "Error" or "No data" is still in the code, or when auditing an existing screen's wording. Writes .dev-agent/screens/<slug>.strings.md. Триггеры — "что написать на кнопке", "текст ошибки", "пустое состояние", "переписать тексты экрана", "микротексты", "строки для экрана".
---

# Interface Copy

Placeholders reach production because nobody owns the words. This skill owns them.

**The screen already decided what states exist.** This skill answers what is written in
them. If a state is missing, say so and send the developer to `screen-blueprint` — do not
invent the state and write text for it.

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

**Headline for this skill:** the strings, ready to paste, and anything that needs a decision rather than a wording choice.

## Before writing anything

Read from `PRODUCT_REPO/.dev-agent/`, resolved from `PRODUCT_REPO` and not from the
working directory:

| File | Use |
|---|---|
| `lexicon.md` | canonical terms are mandatory; every `forbidden` synonym is banned |
| `tone-of-voice.md` | address, length, stance on the user's mistakes |
| `red-lines.md` | checked in the final phase, every run |
| `screens/<slug>.blueprint.md` | the list of states and slots that need text |

Missing file: name it, offer the skill that produces it (`product-lexicon` or
`screen-blueprint`), then continue with assumptions marked as assumptions in the output.
Never stop because an input is absent.

**Read `references/style-rules.md` before phase 2** — capitalisation, punctuation and
number rules are decided once, there, not re-argued per string.

## Phases

### 1. Inventory the slots
List every place on the screen that carries text. From the blueprint when it exists;
from the code when it does not.

*Done when:* every slot has a type — action, label, hint, placeholder, validation, server
error, empty state, confirmation, toast, loading, permission, onboarding, limit.

### 2. Write
One pass per slot type, using the templates in **`references/patterns.md`** — read it
before this phase. A pattern gives the shape of the string, never the string itself.

*Done when:* every slot has a string, and every action slot has 2–3 alternatives with one
recommended.

### 3. Make it translatable
Extract to keys, kill concatenation, add translator context. **Read
`references/flutter.md` or `references/vue.md` before this phase** — the two platforms
store strings completely differently, and this project runs both.

*Done when:* no string is assembled from fragments at runtime, every key carries context,
and every count-dependent string uses the platform's plural mechanism.

### 4. Check the red lines
Run every generated string against `red-lines.md`. This phase runs on every invocation,
not on request.

*Done when:* violations are listed separately with the offending string quoted, or the
list is empty and that is stated.

### 5. Write the artifact
`PRODUCT_REPO/.dev-agent/screens/<slug>.strings.md`: a table of
`key → string → translator context → where used`, plus paste-ready blocks in each target
platform's format.

*Done when:* the file exists and the platform blocks can be pasted without editing.

## Text is not always the answer

A screen that needs three sentences of explanation usually needs a simpler screen. When
the slot inventory shows explanation piling up around one control, say that the problem
is the control, name it, and route to `screen-review`. Writing better text over a
confusing interface hides the defect and makes it permanent.

## Locale cost

This product ships seven locales, one of them right-to-left. Every new or changed string
multiplies by seven. State the count when proposing a rewrite of existing copy — it turns
a wording preference into a decision with a price.

## Non-goals

- Which states a screen has: `screen-blueprint`.
- Text that leaves the product — email, push, release notes, support replies:
  `outbound-writing`.
- Accessible names and analytics event names: `element-markup`. Visible labels are here;
  the accessible name of an icon-only control is there.
- Marketing pages and landing copy.
- Legal wording: produce the human sentence and flag it for a lawyer; the flag is the
  deliverable, not an opinion.
- Editing product code: the skill produces strings and says where they go.
