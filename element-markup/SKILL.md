---
name: element-markup
description: Marks up one UI element in three layers at once — accessibility semantics, analytics event, and test identifier — for Vue or Flutter. Use when writing an interactive component, when an icon-only button needs an accessible name, when a modal needs focus handling, when a custom control needs keyboard support, or to check whether an existing element is marked up correctly. Триггеры — "как разметить кнопку", "aria-label", "доступное имя", "фокус в модалке", "какое событие логировать", "test-id", "Semantics виджет".
---

# Element Markup

One element, one pass, three layers. A developer marks up a `<button>` once — asking them
to invoke three skills for it guarantees they invoke none.

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

**Headline for this skill:** the markup, ready to paste, and which of the three layers you skipped and why.

## Native before ARIA

The first question, every time: **is there a native element that already means this?**

A `<button>` is focusable, keyboard-operable, and announced as a button with no
attributes at all. A `<div role="button" tabindex="0">` reproduces one third of that and
needs hand-written key handlers for the rest. The generated-markup failure mode is piling
ARIA onto an element that was already semantic, or onto one that should have been
replaced.

Reach for ARIA only where no native element carries the meaning. Then say so explicitly.

## The three layers

| Layer | Applies when | Skip when |
|---|---|---|
| **Semantics** | always | never |
| **Analytics** | the element is interactive and its use answers a question someone asked | decorative, or nobody is asking |
| **Test id** | the element cannot be found by role and accessible name | it can — then the id is redundant |

State which layers were skipped and why. A silent skip is indistinguishable from an
oversight.

**The third layer inverts the usual instinct.** An element with a correct accessible name
is already findable by tests through role and name. Adding a test id on top duplicates
identity and lets the accessible name rot unnoticed, because the test no longer depends
on it. Prefer the accessible name; add an id only for elements with no stable name —
rows in a data grid, generated lists, canvas regions.

## Procedure

### 1. Identify the element and its platform
**Read `references/vue.md` or `references/flutter.md` before continuing.** Each carries
worked markup for all twelve cases; this body carries none, deliberately.

### 2. Semantics
Native element first. Accessible name that describes **the action, not the icon** —
`Export associate list`, never `Download icon`. Terms come from `.dev-agent/lexicon.md`;
a name using a `forbidden` synonym is wrong even when it reads well.

*Done when:* the element has a role and an accessible name, and any ARIA present is
justified by the absence of a native equivalent.

### 3. Keyboard and focus
Focusable in visual order. Focus visible. For a dialog: focus moves in, is trapped,
Escape closes, focus returns to what opened it. For anything custom: every key in its
APG pattern.

*Done when:* the element can be operated without a pointer, described key by key.

### 4. Announcements
Content that changes without a navigation needs a live region, at the right insistence:
polite for status, assertive only for errors that interrupt.

*Done when:* dynamic changes are either announced or explicitly judged not worth
announcing.

### 5. Analytics
**Read `references/analytics.md` before this phase.** It carries the decision procedure,
the naming rule, and what to do when no tracking plan exists — which is the current state
of this product.

*Done when:* either an event is specified against the existing schema, or the reason for
no event is stated.

### 6. Test id
Only if step 2 did not already make the element findable.

*Done when:* the id is stable against text and style changes, or its absence is
justified.

## Checking an existing element

Second mode: given markup, produce a diff. Same six steps, output is
`before → after → why` per change, ordered by severity — missing accessible name and
missing keyboard access before anything cosmetic.

## Non-goals

- Auditing a whole screen: `screen-review`. This skill's unit is one element.
- Deciding which elements a screen has: `screen-blueprint`.
- **Visible text**: `interface-copy`. The accessible name is here; the label a sighted
  user reads is there. When they differ, the visible text must be contained in the
  accessible name, or voice control breaks.
- Rewriting the tracking plan: add to it under its own rules.
