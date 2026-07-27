# Layout Playbook

Every rule here was paid for by a failed run. Read it before building a deck, not after the export looks wrong.

The format is deliberate: **the defect, what it looked like, the rule, and how many runs it cost.** A rule without its failure story gets ignored, because the reasoning is what makes it stick when a layout is fighting you at 2am.

Add to this file when a run teaches something new. That is how the system gets better instead of merely repeating.

---

## 1. Route A is a narrow exception, not the default

**Cost: three runs. The most expensive lesson in the file.**

The system offers two ways to fill a slide. Route A stretches the primary component (`.hero`) so it grows into the band. Route B sizes the component to its content and centres it.

Route A looks like the obvious choice — it fills the band, and the fill metric goes to 100%. It is almost always wrong.

What it produced, three times:

- `.checks.hero` with 3 rows → each card ~370px tall holding ~90px of text, air pooled inside every card.
- `.stack.hero` with 4 layers → same, each layer a hollow box.
- `.ledger.hero` with 4 rows → same.
- `.scale.hero` with 2 arms → both arms hollow below their text.

**Rule: Route A needs six or more rows that stay tight when they share the height.** A six-row ledger of single-line entries qualifies. Anything with five or fewer rows is Route B. A `.pair` or `.scale` with two or three rows is Route B, always.

The test before you reach for `.hero`: imagine the rows spread to fill the height. If that opens visible gaps *between* or *inside* rows, it is not Route A.

**A 100% fill reading is not a pass.** It means the component touches both edges of the band, which is exactly what a hollow stretch does. Look at the render.

---

## 2. Centring is opt-in, and so is top-flow

**Cost: two runs, in both directions.**

The system CSS says it plainly: *"covers and single-statement slides earn air: opt in, don't default to it."*

Run one centred every slide → body slides landed at 35–46% fill and read as small blocks floating in a void.
Run two corrected by top-flowing everything → content stacked at the top with a dead lower third.

**Rule, by slide shape:**

| Slide carries | Use |
|---|---|
| One object (a table, a card, a pipeline, a chip field) | `.fill.centre` |
| Genuinely multiple blocks (heading + object + trailing line) | `.fill` top-flow |
| Cover and close | `.fill.centre` |

---

## 3. Top-flow glues the first eyebrow to the meta row

**Cost: one run, cosmetic but obvious in the export.**

The single-page `.sheet` gets a detach guard from the system. Slides using `.fill` without `.centre` do not, so the first eyebrow sits directly under the meta line with no air.

**Rule:** when a deck uses top-flow slides, add to the post's `styles.css`:

```css
.slide .fill:not(.centre) { margin-top: var(--s5); }
```

---

## 4. A wrapped pipeline leaves an arrow pointing at nothing

**Cost: one run. Caught only because the QA list names it explicitly.**

A `.strip` at default settings wraps when the nodes are too wide. The separator that lands at the end of a line points into empty space — a visible defect that reads as a broken diagram.

**Rule:** any pipeline of four or more nodes uses `.strip.nowrap`. The system shrinks the nodes so the row stays on one line and no separator dangles.

**Counter-rule, learned immediately after:** do not then scale `.strip.nowrap` nodes back up. Bumping them to 26px pushed a five-node pipeline past the 900px frame and threw a frame overflow. The nowrap defaults exist to hold the line. If a pipeline still reads small, wrap it in a panel (§5) rather than enlarging the nodes.

---

## 5. A lone pipeline needs a panel, not a stretch

**Cost: one run.**

A single thin strip across a wide band reads as unfinished no matter how it is aligned.

**Rule, straight from the system spec:** *"A lone strip or pipeline is Route B. Wrap it in a right-sized bordered panel and centre it."* A bordered card holding the tag, the pipeline, and its note reads as one deliberate object.

---

## 6. The single page drops its sign-off off the artboard

**Cost: two runs. The worst defect in the set, because the export still succeeds.**

The `.page` has no overflow gate. Content past the frame is silently cropped, and what gets cropped is the last block — the `.endnote` carrying the closing question. The PNG looks fine until you notice the post has no ending.

**Rule:** after exporting, assert the endnote's bottom edge sits inside the frame. `verify_visual.mjs` does this. If it fails, cut content — do not shrink type below the floors. A page at ~105 words fits; at ~112 it does not.

---

## 7. Colour is ink and edge, never fill

**Cost: zero runs — the system spec is unambiguous and following it worked first time.** Recorded so it stays followed.

Semantic colour marks a component through its text, its markers, and a thin edge: a coloured tag, a coloured marker, a 3px top rule, a left border. It does not flood the box with a translucent wash. Wash-filled cards read dated; a neutral card with a coloured edge keeps the contrast instant and looks modern.

---

## 8. Fill targets differ by theme, and the reference builds mislead

**Cost: one run of confusion.**

The fill model asks for roughly 70%+. The sparse theme's own section asks for centred content surrounded by air at 18–40 words per slide. These pull against each other.

**Resolution:** the sparse theme reaches the target with **fewer words at a larger size**, never with more text and never with a stretch. When a sparse slide reads thin, scale the component up — the system components are tuned for the denser theme and usually need a notch more size in a sparse deck.

**Do not calibrate against older reference builds.** One canonical sparse deck runs a 54-word median against a stated 18–40 budget, because it predates the current fill model. The written spec wins over any existing build. The spec says so itself.

---

## 9. Same source, different angle is allowed; same thesis is not

**Cost: one near-miss, caught before writing.**

Two posts may cite the same article. They may not argue the same thing to the same reader.

**Rule:** differentiate by thesis and by reader's job. A source about computer-use agents can support both "state tracking is the hard part" and "benchmark saturation is a procurement risk" — different claims, different readers, both legitimate. Name the neighbouring post in the spec and state the difference.

---

## 10. Word budgets have one sanctioned exception

The per-theme budget applies to prose. It may be exceeded on a `.checks` or `.ledger` slide **where the words are scannable rows rather than prose** — a reader parses rows far faster than paragraphs.

Trim first, then invoke the exception, and say in the README that you did. One deck ran 89 words on a checklist slide, trimmed to 81, and stopped there rather than gutting the five items that were the substance.

---

## 11. A bespoke object needs its `.page` variant sized on the first pass

**Cost: one failed export, then one clean run that proved the fix.**

Every post invents one object in its own `styles.css`. The slide version gets
attention because it is the money slide. The single-page version gets forgotten,
and the single page has no overflow gate — so the object pushes the `.endnote`
off the artboard and the export still reports success.

This showed up twice in consecutive runs. First as the defect: a funnel written
at slide scale cropped the sign-off at 85 words. Then as the fix: the next post
wrote `.page` overrides for its form object in the same pass as the slide styles,
and the endnote landed first time.

**Rule: when you write a bespoke object, write its `.page` block immediately,
at roughly 60% of the slide scale.** Padding, font sizes, and gaps all come down.
It costs thirty seconds while the object is fresh in your head, and it removes an
export cycle.

This is a specific instance of §6, but it earns its own entry because §6 tells you
what to do *after* the endnote is already cropped, and this tells you how not to
crop it.

---

## Adding a rule

A defect earns a rule when it has appeared **twice**. Once is bad luck; twice is a pattern the next run will hit too.

Write it in the same shape as the rules above: what broke, what it looked like, the rule, what it cost. Then delete the corresponding line from the run log — it has been promoted from anecdote to rule and does not need to live in both places.
