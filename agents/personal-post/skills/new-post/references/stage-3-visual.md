# Stage 3 — Visual

Build from the design system, not from scratch. The system already decided the palette, the components, the type floors, and the export contract. Your job is the slide set, the copy, and one bespoke object.

**Read, in order, before you build:** the resolved type's passport — `content-types/ivory.md`, `graphite.md`, or `colored.md` for cobalt, green and cherry — (the visual identity this deck must express), then `components.md` (the markup), then `layout-playbook.md` (the defect rules). `visual-system.md` explains why the system is shaped this way; read it when extending the system rather than using it. Every rule in it was paid for by a failed run, and the same four defects recur in every deck that skips it.

The passport's component bias, density, structure, cover/close character and emoji register are constraints, not suggestions — a coloured deck built like a graphite statement is a routing defect that survived into production.

## Gate

Read the spec's `Visual decision`.

- `none` → produce nothing. Report why the post is text-first and offer one or two future visual ideas. This is a complete outcome.
- `optional` / `recommended` / `required` → build.

Do not build when the visual would need unapproved screenshots, client data, or a named person, or when it would be decoration rather than argument.

## Decide three things, and write them down first

```
Theme:          <from the spec's Visual theme line — do not re-decide>
Depth:          B=<n> → <n> slides
Archetypes:     cover · … · close
Bespoke object: <the one thing this post's styles.css invents>
Caption role:   short overview; the carousel carries the argument
```

**Archetype variety.** No archetype more than twice in one deck, and vary the set from the previous two or three decks — check their `Visual/README.md` first. A feed where every post is the same component sequence reads as a template, which undoes the point of a personal visual.

**Bespoke uniqueness — every post, no exceptions.** Before choosing the bespoke object, list the bespoke objects of **all** previous posts (each `Visual/README.md` names its own). The new object must not repeat any of them — not the same object re-skinned, not the same metaphor with new labels. Two posts may share a *source* (playbook §9) but never a *structural object*. If the natural object is taken, invent the next one; the passport's "bespoke object tone" section says what kind of object fits the type.

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

**Do not reinvent what the system provides.** Tokens, artboard sizing, grid, grain, cards, strips, stacks, pairs, ledgers, checks, chips, scales and fans all exist. Per-post CSS is only for the one object this post invents. If a rule would help three posts, it belongs in the system file instead.

## Fill discipline — the part that decides whether it looks finished

A slide must look **composed**. Two failure modes both fail review, and the second is far more common:

1. An empty half-slide.
2. A stretched component with its content floating in a hollow middle.

**Route B — right-size and centre — is the default.** Size the component to its content, centre the group. Use it for contrast pairs, card groups, short lists, framed panels, anything with a handful of rows.

**Route A — stretch with `.hero` — needs six or more rows that stay tight when sharing the height.** Five or fewer is Route B. See playbook §1; this rule cost three runs.

Either route, each item carries a title **plus** a supporting sub-line. One short line per card is the hollow defect at any size.

When a sparse-theme slide reads thin, the fix is **fewer words at a larger size** — never smaller type to fit more, never a stretch.

## Both modes are required

- `carousel.html` — the full argument across 6–12 slides.
- `single-page.html` — **the whole post on one artboard**: hook, the structural object, two or three proof beats, the rule, the closing question. Not a cover. A reader who never swipes still gets the argument.

Single-page structure, each rule the result of a specific failure: wrap the body in `.sheet` so blocks distribute down the page · the author name appears **once**, in the top meta · close with an `.endnote`, never a footer line glued under the name.

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
