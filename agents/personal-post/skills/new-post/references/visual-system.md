# Visual System

The authority for every artboard. Implementation lives in `assets/visual-system.css` and `scripts/export.mjs` — this file explains the decisions behind them so you can extend the system without breaking it.

The rule underneath everything:

> A theme is a **visual type**, not a palette. Changing the colour is not changing the theme.

## Why types exist

Before the system existed, every post reinvented its CSS. That produced decent one-offs and three problems: the look drifted post to post, every run paid to rebuild primitives, and there was no way to signal topic by appearance.

Content types fix all three. Consecutive posts in different types make a feed read as a person with several registers rather than one template.

**Each type's full identity — purpose, palette, typography treatment, structure, texture, component bias, density, cover/close character, emoji register, bespoke tone — lives in its passport under `content-types/`.** `content-types/index.md` is the orchestrator: the type table, the shared brand constants, and the routing procedure including the straddle rule and the least-used tiebreak. Nothing about an individual type is duplicated here; the passport is the single source of truth.

## Modes — every post ships both

**Carousel** — 6 to 12 artboards. The PDF is what gets uploaded; PNGs are for review.

**Single page** — one artboard carrying the whole post: hook, structural object, two or three proof beats, the rule, the closing question. It is not a cover. A reader who never swipes must still get the argument.

## Slide count is derived

Count load-bearing beats **B** in the spec, then `slides = clamp(B + 2, 6, 12)`. Deeper treatment earns more slides and more dwell. Padding a thin idea to 12 is the failure this prevents.

## Type floors

Nothing carrying meaning renders below 24px on a carousel slide. Display and heading floors are set per type in the CSS. The reduced single-page sizes apply only to that mode — never borrow them for the carousel.

If slide type looks small at phone scale, the fix is **fewer words at a larger size**, not smaller type to fit more.

Three faces only: a display serif, a sans, and a mono — shared by every type. The export gate throws if anything else renders, which is how a silently failed webfont gets caught instead of shipping.

## Export contract

Three gates that throw rather than warn:

1. **Fonts** — only the three system faces may render. Checks leaf text *and* display elements explicitly, because display elements carry child nodes and a naive leaf-only walk skips them.
2. **Size** — every artboard measures exactly the target dimensions.
3. **Count** — the carousel holds 6 to 12 slides.

The PDF is produced via print emulation so each slide is exactly one page at native size.

## Colour is ink and edge, not fill

Semantic colour marks a component through text, markers, and a thin edge — a coloured tag, a marker, a 3px top rule, a left border. It does not flood a box with a translucent wash. Wash-filled cards read dated; a neutral card with a coloured edge keeps contrast instant and looks modern.

Reserve a filled colour block for one deliberate emphasis, never as a default card background.

## Per-post bespoke grammar

The shared library gives primitives. It does not give a post its idea.

Every post keeps a thin `styles.css` for the one object it invents. Keep it small: if a rule would help three posts, it belongs in the system file instead.

The bar is that **the composition carries the claim before a word is read** — a chip that physically moves position across two strips, two tracks that visibly diverge at one step, a ladder with its bottom rung struck out. And the object must be new: no previous post may already own it (see stage-3's bespoke-uniqueness rule).

## Risk rules on the artboard

No logo, wordmark, QR, contact band, or hard CTA — those make a personal post read as a company ad. No client names, private product UI, or real screenshots. Any illustrative figure carries an explicit qualifier; never present an illustration as a measurement. Security and compliance claims stay as "needs review", never "is secure". No robots, AI brains, circuit boards, or stock gradients.

## Known limits

Fonts load over the network; the gate catches a failure loudly rather than shipping a silent fallback. Vendoring the faces locally is the obvious next improvement.

Slide-count derivation depends on an honest beat count. It is a discipline, not a computation.
