# The coloured family — cobalt · green · cherry

**This one passport covers all three.** They share a purpose, a character, a component bias and a word budget. The hue changes, and so does the background pattern — each colour carries its own.

**Purpose:** technical topics, AI, engineering, tools, new technology, product mechanics. The reader builds or chooses systems; this post shows them how something works or where it breaks.

**Character in one line:** a drafting sheet — light ink on a saturated field, a worked surface under it, diagrams doing the arguing. The post *is* a technical drawing of the idea.

## The three fields

| Type | Field | Ink | Accent | Risk tone | Temperature |
|---|---|---|---|---|---|
| `cobalt` | `#0E2F74` deep blue | `#F2F6FF` white | `#9CD2FF` ice cyan | `#FFB38A` copper | cool, analytical |
| `green` | `#013E37` deep green | `#FFEFB3` butter | `#FFFFFF` white | `#FFAE8F` coral | considered, calm |
| `cherry` | `#9A0002` deep red | `#EFE6DD` cream | `#FFFFFF` white | `#FFC24D` amber | urgent, loud |

Green and cherry are two-colour palettes by design, so their accent is pure white rather than a third hue. White is the only mark that reads louder than the body text without inventing a colour the palette does not contain.

Cherry's risk tone is a saturated amber rather than a cream-gold. The first attempt sat a few points off the cream ink and rendered as "slightly warmer cream" — legible side by side, identical at feed thumbnail size. On a red field the separation has to come from saturation, because hue has nowhere to go.

**Cherry carries a warning connotation the other two do not.** A red field says "something is wrong here" before a word is read. That suits a post about a failure, a risk or a hard limit, and works against a calm operational post. When the rotation offers cherry to a piece whose argument is measured, say so and take the next colour instead — the rotation exists for variety, not as an instruction to ignore what a colour means.

## Which one a post gets

The rotation rule lives in `index.md`. Short version: a forced `--theme` flag wins; otherwise take the least-used of the three across existing visual posts, then apply the cherry caveat above.

Never re-decide the hue in Stage 3. It is resolved in Step 1 and threaded through unchanged.

## Typography treatment

- **Mono works hardest here** — annotations, node labels, callout keys, measurements. The drawing voice is monospaced.
- Serif still carries the hook (default `106px` display) but yields the middle slides to sans and mono structures.
- Uppercase mono labels are welcome mid-slide, like stampings on a drawing.

## Structure and flow

**Top-flow default** (`.fill`), like a drawing sheet read from its title block down. Centre only the cover and at most one schematic that earns the isolation.

Medium density between ivory and graphite: word budget **28–55 per slide** (`cobalt_words`, `green_words`, `cherry_words` — keep them equal unless you have a reason). Diagrams replace prose: when a slide creeps past budget, convert sentences into labelled nodes, not smaller type.

## Texture and framing

**Each colour carries its own pattern.** The family used to share one ruled grid, which made three saturated fields look like one theme in three tints and read as graph paper rather than as surface.

| Type | Pattern | Reads as |
|---|---|---|
| `cobalt` | topography — nested irregular contours | a survey drawing |
| `green` | hideout — small crosses on a regular beat | quiet marking |
| `cherry` | jupiter — an ornamental lattice | the loudest field |

Corner brackets render in the ink colour like registration marks. Grain at `0.05`.

Cobalt's contours were rebuilt once: the first version used regular sine chains, which rendered as smooth waves and gave the tile repeat away. A contour map is mostly closed loops of uneven radius, and that is what it is now.

## Component bias

- **Preferred:** `strip` (pipelines), `fan` (node maps), `stack` (layers), `ledger` (spec rows) — the schematic family.
- **Allowed:** `checks`, `pair`, `chips`, `card`, `callout`.
- **Avoid:** `pull`-led slides beyond the mandatory one — a blueprint asserts with structure, not aphorism.

## Cover and close

- **Cover:** reads like a title block — meta line prominent, mono eyebrow, display hook naming the mechanism.
- **Close:** the question sits next to the smallest possible schematic fragment — a two-node strip, a single measured arm — so even the ask looks drawn, not typed.

## Emoji register

Biased to the instrumental: 🛠️ ⚙️ 🧪 🧩 🔎 ⚡ 🧠 📈 — five to twelve per deck, one per slide title.

## Bespoke object tone

The invented object should look like **a schematic**: a pipeline with a bypass valve, a layer diagram with one layer hatched out, a node graph where one edge is severed, a gauge with a marked red zone. Line-work, labels, arrows. If it looks like a memo form or a staged scene, it belongs to another type. It must not repeat any object from a previous post — check every existing `Visual/README.md` first.

## Scale compensation

The family carries a scale block in `visual-system.css` that lifts headings, body, list items and component padding a notch above the dense theme's defaults. Without it a coloured deck measures 34–52% fill on every body slide, because the components are tuned for ivory and this family runs a lower word budget. See playbook §12. `.strip.nowrap` is deliberately excluded.

If a slide still reads thin, scale the component up or give it a second genuine beat. Never add prose, and never stretch.

## Single page

Standard `.page` reductions apply and deliberately win over the scale block, because they sit later in the stylesheet. The pattern keeps a dense single page coherent — but the endnote must still land inside the frame; verify it, the crop is silent.
