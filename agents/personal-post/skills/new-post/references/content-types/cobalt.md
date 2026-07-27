# Cobalt — the blueprint

**Purpose:** technical topics, AI, engineering, tools, new technology, product mechanics. The reader builds or chooses systems; this post shows them how something works or where it breaks.

**Character in one line:** a drafting sheet — white ink on deep cobalt, a fine ruled grid, diagrams doing the arguing. The post *is* a technical drawing of the idea.

## Palette and colour roles

| Token | Value | Role |
|---|---|---|
| `--bg` | `#0E2F74` | deep drafting cobalt — unmistakably blue, dark enough for white text |
| `--surface` | `#17398C` | raised panel, one step lighter |
| `--ink` | `#F2F6FF` | white ink with a faint cold cast |
| `--accent` | `#9CD2FF` | **ice cyan** — the highlighted line on the drawing, the active node |
| `--warn` | `#FFB38A` | heated copper — the failure path, legible on cobalt |

White-on-blue is the whole identity: no other type may use a blue surface, and cobalt never borrows brass or ledger green.

## Typography treatment

- **Mono works hardest here** — annotations, node labels, callout keys, measurements. The drawing voice is monospaced.
- Serif still carries the hook (default `106px` display) but yields the middle slides to sans/mono structures.
- Uppercase mono labels are welcome mid-slide, like stampings on a drawing.

## Structure and flow

**Top-flow default** (`.fill`), like a drawing sheet read from its title block down. Centre only the cover and at most one schematic that earns the isolation.

Medium density between ivory and graphite: word budget **28–55 per slide** (`cobalt_words`). Diagrams replace prose — when a slide creeps past budget, convert sentences into labelled nodes, not smaller type.

## Texture and framing

Fine **ruled grid** — thin white lines at low opacity, 90px pitch (this is the one type where ruled lines are correct; they *are* the surface). Corner brackets render in white ink like registration marks. Grain at `0.05`.

## Component bias

- **Preferred:** `strip` (pipelines), `fan` (node maps), `stack` (layers), `ledger` (spec rows) — the schematic family.
- **Allowed:** `checks`, `pair`, `chips`, `card`, `callout`.
- **Avoid:** `pull`-led slides beyond the mandatory one — a blueprint asserts with structure, not aphorism.

## Cover and close

- **Cover:** reads like a title block — meta line prominent, mono eyebrow, display hook naming the mechanism ("X doesn't do Y. It does Z.").
- **Close:** the question sits next to the smallest possible schematic fragment — a two-node strip, a single measured arm — so even the ask looks drawn, not typed.

## Emoji register

Biased to the instrumental: 🛠️ ⚙️ 🧪 🧩 🔎 ⚡ 🧠 📈 — five to twelve per deck, one per slide title.

## Bespoke object tone

The invented object should look like **a schematic**: a pipeline with a bypass valve, a layer diagram with one layer hatched out, a node graph where one edge is severed, a gauge with a marked red zone. Line-work, labels, arrows. If it looks like a memo form or a staged scene, it belongs to another type. It must not repeat any object from a previous post — check every existing `Visual/README.md` first.

## Scale compensation

Cobalt carries a scale block in `visual-system.css` that lifts headings, body, list items and component padding a notch above the dense theme's defaults. Without it a cobalt deck measures 34–52% fill on every body slide, because the components are tuned for ivory and cobalt runs a lower word budget. See playbook §12. `.strip.nowrap` is deliberately excluded from the block.

If a cobalt slide still reads thin, scale the component up or give it a second genuine beat. Never add prose, and never stretch.

## Single page

Standard `.page` reductions apply and deliberately win over the scale block, because they sit later in the stylesheet. The grid keeps a dense single page coherent — but the endnote must still land inside the frame; verify it, the crop is silent.
