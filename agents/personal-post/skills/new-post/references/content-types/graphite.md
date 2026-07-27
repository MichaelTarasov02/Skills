# Graphite — the lit stage

**Purpose:** founder lessons, selling, marketing, positioning, business judgment. The reader is deciding whether to trust a point of view — yours. This is the persuading register: the post carries a conviction, not a procedure.

**Character in one line:** a late-night keynote — one idea per screen, surrounded by air, lit warm. The sparseness *is* the authority.

## Palette and colour roles

| Token | Value | Role |
|---|---|---|
| `--bg` | `#15130F` | espresso-asphalt — warm near-black, never pure black (cold black reads cheap) |
| `--surface` | `#1E1B15` | raised panel |
| `--ink` | `#F3EEE4` | warm off-white text |
| `--accent` | `#CBA35A` | **brass** — judgment, premium, the line that sells |
| `--warn` | `#D2694C` | terracotta — the cost, the trap |

## Typography treatment

- Serif speaks **louder here than anywhere**: display `116px`, h1 `84px`, tighter letter-spacing. The statement is the design.
- `<em>` inside the display renders brass — that is the selling emphasis; use it once per hook.
- Mono stays small and rare: meta, slide numbers, one label at most per slide.

## Structure and flow

**Centred is the default** (`.fill.centre`). Content floats in air; air is the structure. No grid, no brackets — a warm spotlight vignette from the upper left instead.

Sparse: the smallest element count of the three types. Word budget **18–40 per slide** (`graphite_words`). When a slide reads thin, the fix is **fewer words at a larger size** — never more text, never a stretch.

## Texture and framing

No grid. No brackets. Spotlight gradient + heavier grain (`0.055`) — the surface reads as lit matter, not paper.

## Component bias

- **Preferred:** `pull`, `card`, `scale`, `callout` — statement-first structures that hold one thought.
- **Allowed:** `pair`, `chips`, `checks` (short), `ledger` (short).
- **Avoid:** dense multi-row `ledger`/`checks` walls and anything diagram-shaped (`fan`, long `strip` pipelines) — schematics break the stage illusion; they belong to cobalt.

## Cover and close

- **Cover:** centred display statement with one brass `<em>`, minimal furniture. The hook is a conviction, stated flat.
- **Close:** one question, alone in a `card` or as a `pull` — the ask that converts attention into a reply. Nothing else on the slide competes with it.

## Emoji register

Sparser than the other types — five to eight per deck: 💰 📈 🧭 💬 ⚡ ⚖️ — one per slide title, never inside body copy.

## Bespoke object tone

The invented object should look like **a staged scene**: a balance that tips, a price tag with a hidden line, a spotlight that moves between two actors, a ladder with a missing rung. Physical, singular, metaphor-first. If it looks like a form or a schematic, it belongs to another type. It must not repeat any object from a previous post — check every existing `Visual/README.md` first.

## Single page

`.page` display drops to `78px` (still the largest of the three types). Keep the air: a graphite single page with six packed blocks has failed before it exports — carry the hook, the object, two beats, the rule, the question, and nothing else.
