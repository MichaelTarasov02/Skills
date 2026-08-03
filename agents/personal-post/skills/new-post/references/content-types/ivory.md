# Ivory — the management memo

**Purpose:** company management, team management, processes, hiring mechanics, operating information. The reader is running something — a team, a review cycle, a hiring loop — and this post is a document they could act on.

**Character in one line:** an annotated internal memo on a clean white sheet — dense, structured, quietly authoritative. Not a keynote, not a drawing: a working document.

## Palette and colour roles

| Token | Value | Role |
|---|---|---|
| `--bg` | `#FFFFFF` | pure white sheet |
| `--surface` | `#F5F7FA` | card elevation, faint cool tint |
| `--ink` | `#10243F` | navigator navy, primary text |
| `--accent` | `#1E6B52` | **deep ledger green** — the approval stamp, the key row, the marked line |
| `--warn` | `#A6371B` | oxide red — the editor's pencil, risk and cost |

Navy ink on white is the whole identity: a printed working document rather than a designed page. Green stays the management register — sign-off, ledger, "this is the working rule" — and it is the only accent, so navy never has to compete with a second blue.

**A card cannot be white here.** On a pure white sheet a white surface is invisible, which is why `--surface` carries a faint cool tint and every card also takes a hairline. Grain drops to `0.028` for the same reason: texture that reads as considered on cream reads as dirt on white.

## Typography treatment

- Serif carries headings, as everywhere — but at the **default scale** (`106px` display), never graphite's oversized statements. A memo asserts with structure, not volume.
- Sans carries body; mono carries labels, row keys, and meta — the "form field" voice.
- Sentence case throughout headings. Uppercase lives only in mono labels.

## Structure and flow

**Top-flow is the default** (`.fill`, not `.fill.centre`). Content reads down the page like a document. Centring is reserved for the cover and at most one statement slide.

Dense: this is the type with the largest element count per slide. Word budget **35–70 per slide** (the profile's `ivory_words` governs).

## Texture and framing

**Texture** — a fine woven hatch at 10px pitch, the grain of a sheet of paper — plus **corner brackets** in navy. Grain drops to `0.028`: on pure white, texture that reads as considered on cream reads as dirt.

Every type carries a pattern and no two carry the same one. Ivory's is the quietest of the five, because a memo is the one field where the surface must never compete with the copy.

## Component bias

- **Preferred:** `ledger`, `checks`, `pair`, `stack`, `callout` — document-shaped structures with rows and labels.
- **Allowed:** `strip`, `chips`, `card`, `scale`, `pull`.
- **Avoid:** `fan` (schematic — the coloured family's home ground) and any composition that reads as a poster rather than a page.

## Cover and close

- **Cover:** eyebrow pill + display + lede, top-flowed or centred — but always with the meta line present, like a document header. The hook names the operational tension.
- **Close:** the question is procedural — "what does your form/process/cycle reward?" — set in an `.endnote` (single page) or a `card` (carousel). A memo ends with the action item, not a mic drop.

## Emoji register

From the verified-safe set only, biased to the operational: 📋 ✅ 👥 🧭 ⚖️ ⚠️ 💬 ❓ — five to twelve per deck, one per slide title.

## Bespoke object tone

The invented object should look like **a working artifact**: a form with a hidden column, an org table, a review grid, a calendar strip, a policy diff. If the object would look at home in a keynote or on a schematic, it belongs to another type. It must not repeat any object from a previous post — check every existing `Visual/README.md` first.

## Single page

Standard `.page` reductions apply (`74px` display). The memo character helps here: the single page genuinely is one document, top to bottom, closed by an `.endnote`.
