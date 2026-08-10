# Graphite — deep space

**Purpose:** founder lessons, selling, marketing, positioning, business judgment. The reader is deciding whether to trust a point of view — yours. This is the persuading register: the post carries a conviction, not a procedure.

**Character in one line:** deep space — one idea per screen, surrounded by air, lit cold. The sparseness *is* the authority.

This theme used to be a warm espresso field with a brass accent, a "lit stage". The ground went cool, and brass dies on a cold ground, so the accent went cool with it. The register is now distance and quiet rather than late-night warmth, and the rest of this file has been brought in line with that.

## Palette and colour roles

| Token | Value | Role |
|---|---|---|
| `--bg` | `#151721` | cool near-black with a blue-violet cast, never pure black |
| `--surface` | `#1E2130` | raised panel |
| `--ink` | `#E9EBF2` | near-white text, faint cold cast |
| `--accent` | `#A9B4FF` | **periwinkle** — reads as light rather than metal |
| `--warn` | `#F2947C` | coral — the one warm note, so risk still reads as risk |

## Typography treatment

- Serif speaks **louder here than anywhere**: display `116px`, h1 `84px`, tighter letter-spacing. The statement is the design.
- `<em>` inside the display renders periwinkle — that is the selling emphasis; use it once per hook.
- Mono stays small and rare: meta, slide numbers, one label at most per slide.

## Structure and flow

**Centred is the default** (`.fill.centre`). Content floats in air; air is the structure. No grid, no brackets — a cold glow from the upper left instead.

Sparse: the smallest element count of any type. Word budget **18–40 per slide** (`graphite_words`). When a slide reads thin, the fix is **fewer words at a larger size** — never more text, never a stretch.

## Texture and framing

**Bubbles** — twenty-six discs of uneven radius on a 74px tile, over a cold glow from the upper left, plus film grain at `0.05`. On a near-black field a dense field of small discs reads as stars, which is the register the whole theme is named for. An earlier version used fourteen larger discs and read as blobs. No brackets.

**The pattern rule, shared by every type.** A background is something the reader *can* notice and like, never something they have to read past. Opacity stays in the 0.045–0.055 band for all five types, and density does the other half of the work: a sparse motif at low opacity reads as unfinished, while a dense one at the same opacity reads as a worked surface. **When a pattern looks badly drawn, add detail and shrink the tile before touching opacity.** Several patterns are drawn in a larger coordinate space than they are displayed in, because the reduction is what makes detail fine rather than merely small.


The cast is deliberate and it is close to the coloured family's territory. It was checked on a rendered artboard: cobalt is far lighter and far more saturated, so the two do not blur at feed size. If a future palette change moves either one, re-check that pair before shipping.

## Component bias

- **Preferred:** `pull`, `card`, `scale`, `callout` — statement-first structures that hold one thought.
- **Allowed:** `pair`, `chips`, `checks` (short), `ledger` (short).
- **Avoid:** dense multi-row `ledger`/`checks` walls and anything diagram-shaped (`fan`, long `strip` pipelines) — schematics break the sense of distance; they belong to the coloured family.

## Cover and close

- **Cover:** centred display statement with one brass `<em>`, minimal furniture. The hook is a conviction, stated flat.
- **Close:** one question, alone in a `card` or as a `pull` — the ask that converts attention into a reply. Nothing else on the slide competes with it.

## Emoji register

Sparser than the other types — five to eight per deck: 💰 📈 🧭 💬 ⚡ ⚖️ — one per slide title, never inside body copy.

## Bespoke object tone

Every graphite deck carries two to four objects (`min(4, max(2, ceil(slides/3)))`), and each should look like **a single object in the dark**: a balance that tips, a price tag with a hidden line, one lit element among unlit ones, a ladder with a missing rung, a row where only one mark differs. Physical, singular, metaphor-first. If an object looks like a form or a schematic, it belongs to another type.

**This is the type where the budget is hardest, and the answer is not to compromise the type.** Graphite objects are singular by nature, so three of them means three separate physical metaphors, each alone on its artboard with air around it. That is more demanding than three panels of a schematic and it is the right cost: a graphite deck of ten slides with one drawing and nine statements is exactly the deck this rule was written against. Keep each object simple enough to read in a second — a graphite object with six labelled parts has become a schematic and belongs to the coloured family.

The **signature** object must not repeat any previous post's signature. Supporting objects may share a family with earlier work. Run `list_objects.py` rather than trusting memory.

## Single page

`.page` display drops to `78px` (still the largest of any type),.

**This section used to say the opposite, and it was wrong.** It read: keep the air, carry two beats and nothing else. That produced a page holding a fifth of what the deck held, and a reader who never swiped got a cover. Air is the authority *on a slide*, where one idea has a whole artboard. The single page is a different artefact with a different job: it is the only thing some readers will see.

Carry the hook, the signature object, a `.beatgrid` of four to six beats, the evidence line if the deck has one, the turn, and the question. Coverage gate: 55% of the deck's words, same as every other type.

What graphite keeps from its character is **restraint per element**, not fewer elements: shorter beat lines, more space between blocks than the other types, no second object. The page is dense in coverage and calm in texture.
