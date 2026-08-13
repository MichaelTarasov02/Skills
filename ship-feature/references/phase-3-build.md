# Phase 3 — Build

Strings and markup, ready to paste. The code between them is the developer's.

**Delegate:** `copy` for every string the screen carries, `craft` for the markup of each
interactive element. Both read the blueprint from phase 2 — that is what the blueprint is
for.

## Order: strings before markup

The accessible name of an icon-only control depends on what the action is called, and the
action is named in the strings. Doing markup first produces names that later disagree with
the visible labels — and a mismatch between the two breaks voice control, which nobody
notices until someone uses it.

## Work from the blueprint, not from the screen in your head

```bash
grep '^- SLOT:' .dev-agent/screens/<slug>.blueprint.md   # every string needed
grep '^- ELEM:' .dev-agent/screens/<slug>.blueprint.md   # every element to mark up
```

A slot with no string and an element with no markup are the two things this phase must not
leave. Count them at the start and at the end; the numbers match or the phase is not done.

**Do not add slots here.** A place needing text that the blueprint does not have means the
design missed a state — that goes back to phase 2, briefly, rather than being invented
now. Inventing it produces text for a state the code will not render.

## Leverage

Before marking up an element, check whether it is an instance of a shared component. Where
it is, the fix belongs in the component and covers every other call site with it.
`craft` owns this check; the pipeline's job is to not skip it because one element looked
quick.

## The locale cost lands here

Every new string multiplies by the number of locales. Report the count once, at the end of
this phase, so it reaches the engineer while the work is still adjustable rather than at
review.

## Ends with

```
Строки:       .dev-agent/screens/<slug>.strings.md — <n> ключей, ×<locales>
Разметка:     <elements marked up, and which are shared components>
Слоты:        <blueprint slots> → <strings written>   ← must match
Элементы:     <blueprint elements> → <marked up>      ← must match
Пропущено:    <layers skipped — analytics or test ids — with the reason>
```
