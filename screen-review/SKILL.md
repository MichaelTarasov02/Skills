---
name: screen-review
description: Reviews a finished screen before handoff — comprehensibility, visual hierarchy, component states, dark theme, responsive behaviour, contrast with measured numbers, WCAG audit, text expansion, RTL, and whether the implementation matches its blueprint. Produces ranked findings, each with a specific edit. Use when a screen works but has not shipped, when something looks amateurish and it is unclear why, or to check what the implementation left out. Writes .dev-agent/reviews/<slug>.review.md. Триггеры — "отревьюй экран", "выглядит плохо", "что тут не так", "проверь доступность экрана", "тёмная тема ломается", "перед сдачей".
---

# Screen Review

The only skill here that judges rather than produces. It answers the question a developer
cannot ask themselves: is this understandable to someone seeing it for the first time?

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

**Headline for this skill:** the blocking findings first, each with its edit. Everything else below them.

## A finding without a specific edit is not a finding

Every item carries three parts: **what is wrong**, **why it hurts the user**, **what
exactly to change**. "Improve the hierarchy" fails all three — it names no defect, no
consequence, and no action. Formulations like *improve*, *make clearer*, *polish*, *look
into* are not findings; they are the feeling that preceded a finding.

The test: could a developer who did not read this review apply the edit from the text
alone? If not, keep working on the finding.

## Ranking is mandatory

| Rank | Meaning |
|---|---|
| **Blocking** | ships broken for someone: unusable by keyboard, unreadable contrast, a state that renders nothing |
| **Important** | works, but costs the user time or confidence |
| **Nice** | noticeable to a designer, invisible to a user in a hurry |

A developer before handoff cannot fix forty items. They can fix five. An unranked list
transfers the prioritisation back to the person with the least context.

Cap the report: every blocking item, the important ones, and nice-to-have only where the
edit is trivial.

## Look before you read

For web, **open the screen and look at it first**; read code only when that fails. A
rendered screen shows overlap, contrast and truncation that no amount of CSS reading
surfaces. Use Playwright: default width, narrow, dark theme, and with strings expanded.

For Flutter there is no equivalent shortcut — review runs from widget code and theme
data, optionally against a simulator screenshot. Say which path was used. Presenting a
code review as though a screen had been seen misrepresents the evidence.

## Phases

### 1. Comprehensibility
**Read `references/heuristics.md` before this phase.** Name what the user does here, what
the primary action is, and what is unclear. Separate *needs text* from *needs a simpler
screen* — the second is the real finding when explanation piles up around one control.

*Done when:* every unclear point cites the heuristic it violates, not an impression.

### 2. Visual
**Read `references/visual.md` before this phase.** Spacing scale, typographic hierarchy,
alignment, density, depth.

*Done when:* every visual finding names the measurable cause — a value off the scale, two
weights doing one job, an edge unaligned by a specific amount.

### 3. States
Component states — hover, active, focus, disabled, loading, selected — and whether the
screen's own states from the blueprint exist at all.

*Done when:* missing states are listed by name.

### 4. Contrast and size — with numbers
Compute ratios. Report as `foreground on background = X.XX:1, threshold Y`.

*Done when:* no contrast finding is stated without its measured value.

### 5. Adaptation
Widths, dark theme, text expanded by 30%, RTL. **Read `references/vue.md` or
`references/flutter.md` before this phase.**

*Done when:* each dimension has either a finding or an explicit pass.

### 6. Blueprint comparison
If `.dev-agent/screens/<slug>.blueprint.md` exists, compare the state matrix against the
implementation.

*Done when:* every state in the blueprint is marked implemented or missing. Skip only
when no blueprint exists, and say so.

### 7. Write
`.dev-agent/reviews/<slug>.review.md`, ranked. `feature-handoff` reads it.

*Done when:* every finding has its three parts and a rank.

## Where this stops and element-markup starts

Both touch accessibility; the line is the unit. **A screen has a review, an element has
markup.** Focus order across the screen, contrast of the palette, the audit as a whole —
here. How one button gets its accessible name — there. A finding about a single element
names the defect and routes to `element-markup` rather than writing the markup.

## Non-goals

- Redesigning the screen: `screen-blueprint`.
- Rewriting copy: name the problem, route to `interface-copy`.
- Marking up elements: `element-markup`.
- Code quality, architecture, performance. This is a review of the interface, not the
  implementation.
- **Fixing.** The skill finds and formulates. The developer edits — unless they ask
  otherwise.
