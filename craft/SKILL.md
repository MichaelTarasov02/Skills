---
name: craft
description: Finishes the implementation detail a feature needs but nobody specifies — accessibility semantics, analytics events and test identifiers for an element, and the performance work that keeps a screen fast — N+1 queries, missing indexes, unvirtualised lists, oversized images, unnecessary rebuilds. Use when writing a component, when an icon-only control needs an accessible name, when a modal needs focus handling, or when something is slow and you know where. Writes .dev-agent/screens/<slug>.markup.md. Триггеры — "как разметить кнопку", "aria-label", "доступное имя", "фокус в модалке", "какое событие логировать", "test-id", "тормозит", "N+1", "оптимизировать запрос", "список лагает".
---

# Craft

The detail between "it works" and "it is finished". Two kinds, one moment: you are in the
code and the feature is nearly done.

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
file, and offer `setup` once. **Never fall back to the language of the request.**

This applies here more than it looks: **an accessible name is user-facing text.** A
screen reader reads it aloud to the person using the product, so it follows the product's
interface language, never the language of the developer who asked for it.

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

**Headline for this skill:** the markup or the fix, ready to paste, and what you skipped
with the reason.

## Where the output lands

`markup` mode writes `PRODUCT_REPO/.dev-agent/screens/<slug>.markup.md` — the semantics,
the events and the test ids for the screen's elements, ready to paste. `perf` mode writes
nothing; its output is a change and a measurement, and it belongs in the report of
whatever pipeline invoked it.

**Producing markup only in the chat is the failure this exists to prevent.** `review`
checks the markup against the blueprint's element list, and a pipeline running across a
long session has no way to find something that was said and not written. One element per
entry, anchored so it can be looked up:

```markdown
### ELEM: <the element, exactly as the blueprint names it>
- role: <native element, or the ARIA role and why no native one carries it>
- name: <the accessible name>
- event: <name and properties, or "none — <reason>">
- test-id: <id, or "none — findable by role and name">
- shared: <the component this was fixed at, if it was — with its call-site count>
```

`### ELEM:` is the anchor other skills grep. Anchor lookups to end of line.

## Two modes

| Mode | The request looks like | Read before working |
|---|---|---|
| **`markup`** | "как разметить", "aria", "доступное имя", "какое событие", "test-id" | `references/markup-<platform>.md` |
| **`perf`** | "тормозит", "N+1", "лагает", "долго грузится" | `references/perf.md` |

They meet more often than they look: a list slow enough to need virtualisation also needs
its rows announced correctly, and the fix for one usually touches the other. Say when you
are doing both.

## Read the platform from config, not from memory

`.dev-agent/config.yaml` names the framework **major** and the dominant API style. Advice
written for the wrong major does not compile while looking plausible enough to paste.
Check before writing a line of markup.

If `config.yaml` is absent, detect the major from the manifest and say you did, then offer
`setup`.

---

## Mode `markup`

### When there is no reference for this platform

`references/markup-<platform>.md` exists for some platforms and not others, and the agent
is installed on repositories nobody anticipated. **A missing platform file is not a
blocker** — it changes where the answer comes from, and the output says so.

The rules that do not depend on the platform are the ones in this file: native before
ARIA, find the leverage, the three layers, obey the existing analytics scheme. They carry
most of the value.

What the platform file supplies is **syntax and the local kit's quirks**, and that is
recoverable from the codebase in two commands:

```bash
grep -rn "<the nearest equivalent element>" <root> | head -5   # read two, copy their shape
grep -rniE "aria-|semantics|accessibilityLabel|contentDescription" <root> | head -10
```

**Say which you did.** "Derived from three existing dialogs in this codebase" and "from the
platform reference" are different levels of confidence, and a reader deciding whether to
trust a keyboard-handling suggestion needs to know which one they have.

Where the codebase has no example either — the first dialog, the first live region — say
that too, and give the platform-independent requirement rather than invented syntax:
*focus moves in, Escape closes, focus returns to what opened it*. A requirement a developer
can implement beats syntax that does not compile.

### Native before ARIA

The first question, every time: **is there a native element that already means this?**

A button element is focusable, keyboard-operable and announced as a button with no
attributes at all. A div with a role and a tabindex reproduces one third of that and needs
hand-written key handlers for the rest. The generated-markup failure mode is piling ARIA
onto an element that was already semantic, or onto one that should have been replaced.

Reach for ARIA only where no native element carries the meaning — then say so explicitly.

### Find the leverage before fixing anything

A codebase with its own component layer has a few widgets standing between hundreds of
call sites and the semantics tree. Fixing the widget fixes them all.

Before proposing markup for one element, ask whether that element is an instance of a
shared component — and if it is, propose the fix there. Measured on one repository: three
custom button widgets covered 548 call sites, against 150 elements that looked like
individual problems.

**Report the leverage, not the raw count.** "150 elements lack an accessible name" is true
and useless. "Three widgets carry 548 of them" is the same fact turned into a morning's
work with a definite end.

### Three layers, each may be skipped

| Layer | Applies when | Skip when |
|---|---|---|
| **Semantics** | always | never |
| **Analytics** | the element is interactive and its use answers a question someone asked | decorative, or nobody is asking |
| **Test id** | the element cannot be found by role and accessible name | it can — then the id is redundant |

State which layers were skipped and why. A silent skip is indistinguishable from an
oversight.

**The third layer inverts the usual instinct.** An element with a correct accessible name
is already findable through role and name. Adding a test id on top duplicates identity and
lets the accessible name rot unnoticed, because the test stops depending on it. Prefer the
name; add an id only where no stable name exists — rows in a data grid, generated lists,
canvas regions — or where the name is localised and tests run under a non-default locale.

### Analytics obeys whatever scheme already exists

**The scheme is not always in a plan file.** Look in this order, and stop at the first
hit:

| Where | How to find it |
|---|---|
| `.telemetry/tracking-plan.yaml` | the documented plan, if the team keeps one |
| a constants class in the code | `grep -rn 'AnalyticsKeys\|EventNames\|class .*Analytics' lib src` |
| existing call sites | read two, copy their shape |

Measured on one repository: no plan file, but an `AnalyticsKeys` constants class holding
the names, and exactly one custom event using it. Concluding "no scheme exists" from the
absent plan file would have invented a second naming convention beside a real one.

**Check what the SDK already tracks for free.** A registered analytics navigation observer
records screen views automatically; session start and user identity are usually wired at
startup too. Proposing a "screen viewed" event on top of that duplicates data and splits
the same question across two sources.

```bash
grep -rn 'AnalyticsObserver\|logAppOpen\|setUserId' lib src
```

Where there is genuinely no scheme, no plan and no SDK — the layer is not applicable. Say
that rather than proposing an event into a crash reporter.

Event objects come from `lexicon.md`. A name carrying a `forbidden` synonym fossilises it
in the warehouse, where it outlives every UI rename.

---

## Mode `perf`

### Measure before advising

**Read `references/perf.md` before this phase.** Every recommendation names the measurement
that justifies it. "This looks slow" is a hypothesis; a count, a timing or a query log is
a finding.

The order is fixed: reproduce, measure, locate, fix, measure again. Skipping the last step
means you do not know whether the fix worked — and the most common outcome of an unmeasured
optimisation is code that is harder to read and exactly as slow.

### Fix the cause the measurement points at

The instinct is to fix what you recognise. The discipline is to fix what dominates. A
memoised component inside a screen doing an N+1 saves nothing measurable, and the memo
makes the next reader think the screen was optimised.

---

## Non-goals

- Deciding which elements a screen has: `spec`.
- Auditing a whole screen: `review`. This skill's unit is one element or one bottleneck.
- **Visible text**: `copy`. The accessible name is here; the label a sighted user reads is
  there. When they differ, the visible text must be contained in the accessible name, or
  voice control breaks.
- Finding *where* the slowness is when nobody knows: `debug`. This mode assumes you know.
- Rewriting the tracking plan: add to it under its own rules.
