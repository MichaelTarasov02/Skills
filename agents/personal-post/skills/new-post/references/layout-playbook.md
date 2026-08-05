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

## 12. A new content type needs its own scale, or every slide reads thin

**Cost: one smoke deck plus one real run, both measured before anyone looked.**

The component library is tuned for the dense theme. The sparse theme compensates
with a much larger display and h1, which is why it holds the artboard on 18–40
words. A newly added type inherits the components and inherits no compensation,
so it lands in the void the whole time.

Cobalt showed this twice. The smoke deck built when the type was introduced
measured 34–44% fill on every body slide. The first real cobalt post measured
37–52% before a single word was changed. Same cause both times.

**Rule: when you add a content type, give it a scale block in the same pass as
its palette.** Headings, body, list items, and component padding all come up a
notch relative to the dense theme's defaults. The fix belongs in
`visual-system.css`, not in a post's `styles.css` — a per-post fix leaves the
next post to rediscover it.

**Exclude the nowrap pipeline.** `.strip.nowrap` sizes itself to hold one line;
enlarging its nodes threw a frame overflow once already (§4's counter-rule).

The cobalt block lifted a real deck from 37–52% to 49–66% with no added words.

**Amendment, after the first graphite deck since the theme was rebuilt.** This rule
says to give a *new* type a scale block, which quietly assumes the existing types
already have one. Graphite predates the rule and never received it, so a ten-slide
deck came in at 24–51% and the cause looked like the post rather than the system.
It needed a larger lift than the coloured family, for the same reason its word
budget is lower: fewer words are doing the same job on the artboard. With the block
it reads 30–75%.

**Before you adjust a post that reads thin, check whether its type has a scale
block at all.** Grep `visual-system.css` for the type name. A missing block is a
system defect wearing a post's clothes, and fixing it in the post leaves every
future deck in that type to rediscover the same thing.

---

## 13. A centred single-object slide fills lower than a top-flow slide, and that is correct

**Cost: three chased warnings across two decks before anyone noticed they were the same shape.**

The checker warns below roughly 50% fill. That threshold is calibrated for a slide
carrying several blocks down the artboard. A slide carrying **one** centred object
— a statement `.pull`, a lone panel, a caveat `.callout` — reaches a lower number
honestly, because the air around a single object is the design rather than a gap
in it.

Measured, after each was already fixed as far as it should be fixed:

- a statement `.pull` in an ivory deck: 42%
- a statement `.pull` in a cobalt deck: 44%
- a `.strip` in a panel: 45%
- a caveat `.callout`: 43%

**Rule: when a centred single-object slide warns, apply §8 once — scale the object
up — and then stop.** Do not add a sentence, do not add a second block, do not
reach for `.hero`. A statement slide that has been padded to clear the threshold
has been made worse to satisfy a number.

The warning is still worth reading. It is how you notice a slide that genuinely
holds nothing. Look at the render and decide which of the two you have.

**Amendment, after three coloured decks.** "Scale once and stop" assumes the
starting size is right. Three coloured posts in a row put a lone statement
`.pull` in the low thirties at the family's 48px and each one worked around it
in its own `styles.css`. That is not three unlucky posts; that is a system size
that is wrong. The family's `.pull` is now 56px at a 24ch measure, and the next
deck should need no override at all. **When you find yourself writing the same
per-post override for the third time, the fix belongs upstream** — the per-post
version is invisible to every future run.

---

## 14. Overlapping elements are invisible to every check in this system

**Cost: one run, and the deck exported with two words printed on top of each other.**

Three tick labels on a measure were laid out as flex children, the last of them at
`flex: 0 0 0` with a translated label. A zero-basis flex item reserves no width, so
its neighbour ran straight through it and the exported slide read `SomebodyFixed.`
as one word.

Every gate passed. That is the part worth remembering: **every check in this system
measures elements against the frame, and none measures elements against each other.**
Overflow, cropping, fill ratio, word count, dangling separators — all of them are
element-versus-artboard. Two elements occupying the same pixels is a defect class
the scripts cannot see at all.

**Rule: never position a label with a zero-basis flex item or a bare `transform`
against a neighbour. Use absolute positioning inside a positioned parent**, where
the coordinates are stated rather than negotiated. And when a bespoke object places
text near other text, open the PNG and read the words. That is the only check there is.

---

## 15. Never hand-write an SVG arc flag

**Cost: one run. The arrow exported with two thirds of it missing and every gate green.**

A looping arrow was written as `A26 26 0 1 1` with hand-picked endpoints. An SVG arc
does not take a centre; it solves for one from the radii and the two flags, there are
two valid solutions, and the wrong flag order put the centre above the viewBox. What
rendered was a third of the intended curve. Nothing overflowed, nothing was cropped,
so nothing complained.

**Rule: generate curved geometry as explicit points, and assert the extents before
you paste it in.** A few lines of Python producing a polyline is faster than one
round of guessing at flags, and the assertion is what turns a silent geometry bug
into a failed script:

```python
pts = [(cx + r*cos(t), cy + r*sin(t)) for t in steps]
assert all(0 <= x <= W and 0 <= y <= H for x, y in pts), "the curve leaves the viewBox"
```

This sits beside §14 for a reason. **Geometry inside a bespoke object is the one
thing no script in this system checks**, so an invented drawing is the first place
to look when a deck passes and still looks wrong.

---

## 16. An object that carries a claim through one variable holds every other variable still

**Cost: one run, and the object argued the opposite of the post it illustrated.**

The claim was that a team's work is connected when seen from inside and disconnected
when seen from outside. The object faded link opacity from left to right, which was
exactly right. It rendered arguing the reverse: sparse on the left, a dense web on
the right, reading as *more* connected from outside.

The links were correct. The **node density** was not held still. The generator
dropped nodes at random, the left end came out sparse, the right end came out
crowded, and crowding overwhelmed the fade. Two variables were moving and only one
of them was the argument. A second cause sat underneath: an asymptotic fade
(`1 - (x/W)^1.55`) never reaches zero, so faint links survived all the way to the
right edge.

**Rule: when an object encodes a claim through one visual variable, every other
variable is held constant, and the generator asserts it.** Even spacing, uniform
sizes, a hard cutoff rather than a fade that never quite lands. Write the assertion
in the same breath as the geometry:

```python
assert right_side_links == 0, "links survive past the cutoff"
```

Then look at the render and ask one question: **if I read only the drawing, what
does it say?** If that is not the thesis, the object is wrong no matter how the
code looks.

---

## Adding to this file

A defect earns a rule when it has appeared **twice**. Once is bad luck; twice is a pattern the next run will hit too.

Write it in the same shape as the rules above: what broke, what it looked like, the rule, what it cost.

**Then verify the rule is in this file before you report it as promoted.** Three
rules — §14, §15 and §16 — were announced in the run log and in commit messages and
were never written here. For three runs the playbook silently lagged the system that
depends on it, and every one of those runs began without rules that had already been
paid for. Open the file and read the new section. A rule that lives only in a run-log
entry is an anecdote wearing a rule's number.
