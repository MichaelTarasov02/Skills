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

No grid. No brackets. A cold glow from the upper left plus grain at `0.05` — the surface reads as distance, not paper.

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

The invented object should look like **a single object in the dark**: a balance that tips, a price tag with a hidden line, one lit element among unlit ones, a ladder with a missing rung. Physical, singular, metaphor-first. If it looks like a form or a schematic, it belongs to another type. It must not repeat any object from a previous post — check every existing `Visual/README.md` first.

## Single page

`.page` display drops to `78px` (still the largest of any type). Keep the air: a graphite single page with six packed blocks has failed before it exports — carry the hook, the object, two beats, the rule, the question, and nothing else.
