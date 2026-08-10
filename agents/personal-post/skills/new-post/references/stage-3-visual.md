# Stage 3 — Visual

Build from the design system, not from scratch. The system already decided the palette, the components, the type floors, and the export contract. Your job is the slide set, the copy, and one bespoke object.

**Read, in order, before you build:** the resolved type's passport — `content-types/ivory.md`, `graphite.md`, or `colored.md` for cobalt, green and cherry — (the visual identity this deck must express), then `components.md` (the markup), then `layout-playbook.md` (the defect rules). `visual-system.md` explains why the system is shaped this way; read it when extending the system rather than using it. Every rule in it was paid for by a failed run, and the same four defects recur in every deck that skips it.

The passport's component bias, density, structure, cover/close character and emoji register are constraints, not suggestions — a coloured deck built like a graphite statement is a routing defect that survived into production.

## Gate

Read the spec's `Visual decision`.

- `none` → produce nothing. Report why the post is text-first and offer one or two future visual ideas. This is a complete outcome.
- `optional` / `recommended` / `required` → build.

Do not build when the visual would need unapproved screenshots, client data, or a named person, or when it would be decoration rather than argument.

## Decide four things, and write them down first

```
Theme:          <from the spec's Visual theme line — do not re-decide>
Depth:          B=<n> → <n> slides
Objects:        <n> = min(4, max(2, ceil(slides / 3)))
                signature: <the one that carries the thesis>
                support:   <the others, one line each>
Archetypes:     cover · … · close
Caption role:   short overview; the carousel carries the argument
```

## The object budget — one drawn object per three slides

A deck of ten slides carrying one drawing and nine walls of type is a document,
not a carousel. **Every deck carries several invented objects, and the count is
derived, never chosen by mood:**

```
objects = min(4, max(2, ceil(slides / 3)))
```

| Slides | Objects |
|---|---|
| 6 | 2 |
| 7–9 | 3 |
| 10–12 | 4 |

Two is the floor even on the shortest deck. Four is the ceiling, because a fifth
object stops being a drawing and starts being a pattern the reader scrolls past.

**Objects come in two tiers, and the difference is what may repeat.**

**The signature object.** One per post. It carries the thesis, it is the one that
would survive if the deck lost every other slide, and it is **globally unique
across every post ever published** — not the same object re-skinned, not the same
metaphor with new labels. This is the brand promise and it does not bend. It is
also the object that goes on the single page.

**Supporting objects.** The rest. Each is still invented in this post's
`styles.css`, still specified in the Visual Brief, still built to the same
standard. What they are allowed to do that the signature cannot: share a *family*
of shapes with an earlier post — a second ledger-with-a-strike, another two-track
comparison — as long as it is not a re-skin of some other post's **signature**.
Without that allowance the uniqueness rule would demand three never-before-seen
structures per post forever, and the fiftieth post would be inventing shapes to
satisfy a counter rather than an argument.

**Every object is marked in the markup**, on its root element:

```html
<div class="tether" data-object="tether">…</div>
```

`verify_visual.mjs` counts these. An unmarked object does not exist as far as the
gate is concerned, and a deck under its budget fails rather than warns. That is
deliberate: a rule about how many drawings a deck carries is exactly the kind of
rule that quietly decays into "one, like last time" unless something counts.

**Before choosing any of them, list what is taken.** Run:

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/skills/new-post/scripts/list_objects.py" "<output_dir>"
```

It prints every object every post has used, with its tier. Reading thirty-seven
`README.md` files by hand is how a repeat gets shipped.

**Archetype variety.** No archetype more than twice in one deck, and vary the set from the previous two or three decks — check their `Visual/README.md` first. A feed where every post is the same component sequence reads as a template, which undoes the point of a personal visual.

**Spread them.** Objects do not cluster at the front. One near the top where the
argument is set up, one in the middle where it turns, one near the proof. A deck
with three drawings on slides 2, 3 and 4 and nothing after slide 5 reads as a
deck that ran out of ideas.

Cover and close are fixed. Everything between is chosen to fit the argument.

## Build the folder

```
Visual/
  system.css          cp "${CLAUDE_PLUGIN_ROOT}/skills/new-post/assets/visual-system.css"
                      → never edit it here; it is a copy
  styles.css          this post's bespoke grammar only
  carousel.html       6–12 × section.slide[data-theme]
  single-page.html    1 × section.page[data-theme]
  README.md
  exports/
```

Both HTML files link, in order: the font stylesheet, `system.css`, then `styles.css`.

**Do not reinvent what the system provides.** Tokens, artboard sizing, grid, grain, cards, strips, stacks, pairs, ledgers, checks, chips, scales and fans all exist. Per-post CSS is only for the objects this post invents. If a rule would help three posts, it belongs in the system file instead.

## Fill discipline — the part that decides whether it looks finished

A slide must look **composed**. Two failure modes both fail review, and the second is far more common:

1. An empty half-slide.
2. A stretched component with its content floating in a hollow middle.

**Route B — right-size and centre — is the default.** Size the component to its content, centre the group. Use it for contrast pairs, card groups, short lists, framed panels, anything with a handful of rows.

**Route A — stretch with `.hero` — needs six or more rows that stay tight when sharing the height.** Five or fewer is Route B. See playbook §1; this rule cost three runs.

Either route, each item carries a title **plus** a supporting sub-line. One short line per card is the hollow defect at any size.

When a sparse-theme slide reads thin, the fix is **fewer words at a larger size** — never smaller type to fit more, never a stretch.

## Both modes are required, and the single page is not a summary

- `carousel.html` — the full argument across 6–12 slides.
- `single-page.html` — **a digest of that same argument on one artboard.**

### The single page carries the post, not a taste of it

This is the part that was wrong for a long time. A single page that runs a hook,
one drawing and a question against a ten-slide deck is a cover with extra steps.
A reader who never swipes should finish the page having received the argument,
the evidence and the limit — everything except the elaboration.

**Coverage rule, and it is a gate rather than an aspiration:** the single page
carries **at least 55% of the deck's body words**. `verify_visual.mjs` computes
the ratio and fails below it. Two lines against twenty is the defect this exists
to stop.

**What it must contain, in order:**

| Block | What it carries |
|---|---|
| Hook | eyebrow, display, lede — same claim as the cover, no softer |
| Signature object | the one object that best explains the thesis, at page scale |
| Beat grid | **4–6 beats** from the middle of the deck, in `.beatgrid`: a label and one tight line each |
| Evidence | the borrowed figure with its attribution, when the deck has one |
| Turn | the deck's `pull` line, compressed to one sentence |
| Endnote | the closing question |

**Only one object goes on the page** — the signature one. The others do not fit,
and choosing the most explanatory one is a real editorial decision worth making
deliberately rather than by slide order.

**The formatting is different from the carousel and that is the point.** A slide
gives one idea room to breathe. The page gives six ideas a structure to sit in.
The page's type scale is already a notch tighter than the slides';
use `.beatgrid` to run beats two-up. Do not simply shrink slide markup: a slide's
generous `.body` at page scale still eats the artboard, while a beat written as a
label plus one line fits six times over.

**Structural rules, each the result of a specific failure:** wrap the body in `.sheet` · the author name appears **once**, in the top meta · close with
an `.endnote`, never a footer line glued under the name · the endnote must land
inside the frame, and the crop is silent.

## Slide copy

No em dashes. No "not X, it's Y" — state Y. One `.pull` per deck, two at most: if every line is quotable, none is. Name the actor rather than letting things act. Break metronomic rhythm. Slides never restate the caption.

Emoji are functional scan markers: one per slide title, five to twelve per deck, from the verified-safe set only. Some glyphs render as garbage in the headless export — the system spec names them.

Density comes from the profile's per-theme word budget. A checklist or ledger slide may exceed it where the words are scannable rows rather than prose.

## Export and verify

```bash
cd "<post>/Visual"
node "${CLAUDE_PLUGIN_ROOT}/skills/new-post/scripts/export.mjs"
node "${CLAUDE_PLUGIN_ROOT}/skills/new-post/scripts/verify_visual.mjs"
```

Three export gates throw rather than warn: fonts, exact artboard size, slide count. Then `verify_visual.mjs` measures overflow, dangling separators, theme match, fill ratio, word budget, and whether the single page cropped its sign-off.

**Then open the PNGs.** The scripts measure geometry. They cannot see a hollow stretch — which reports 100% fill precisely because it touches both edges. Fix and re-export until scripts and eyes both pass.

Upload `exports/carousel.pdf` as a document post. The PNGs are for review.

## Report

Created files · theme and reason · depth · archetypes · export count and dimensions · gates · what you fixed · what still needs a human eye.

Name the defects you hit. A run that reports "QA passed" after three silent fixes teaches the next run nothing; a run that names them feeds the playbook.
