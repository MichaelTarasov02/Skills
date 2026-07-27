# Content Types — the orchestrator

A **content type** is the full visual identity of a post, not a palette. Palette, typography treatment, component bias, text density, structure, texture, emoji register, cover and close character — all of it is decided by the type. Each type has a **passport** in this folder; the passport is the single source of truth for how that type looks. Read the resolved type's passport before building any artboard.

The goal the system serves: **three consecutive posts in three different types must read as three different designs by the same author.** Shared brand constants hold them together; everything else is allowed — required — to differ.

## What is shared across all types (the brand constants)

These never vary per type. If a passport contradicts this list, the list wins.

- **Faces:** Newsreader (display serif) + Geist (sans) + Geist Mono. The export gate throws on any other family. Types differ in how the faces are *used* — size, weight, case, which face carries which role — never in the faces themselves.
- **Artboard:** 1080×1350, safe pad 90px, type floors (meaning-carrying text ≥ 24px on a carousel slide).
- **Film grain** as a physical surface (opacity varies per type).
- **Colour is ink and edge, not fill** — see `visual-system.md`.
- **Export gates** (fonts / size / count) and both modes (carousel + single page).
- **Risk rules on the artboard** — no logos, no CTA bands, no screenshots, no invented measurements.
- **Bespoke uniqueness:** every post invents one structural object that has never appeared in any previous post. The type shapes *what kind* of object fits; it never excuses a repeat.

## The three types

| Type | Register | Purpose — route here when the post is about | Character |
|---|---|---|---|
| `ivory` | light | Company management, team management, processes, hiring mechanics, operating information | The management memo — annotated paper, dense, green-stamped |
| `graphite` | dark | Founder lessons, selling, marketing, positioning, business judgment | The lit stage — keynote air, sparse, brass |
| `cobalt` | blue | Technical topics, AI, engineering, tools, new technology, product mechanics | The blueprint — white ink on cobalt, drafting grid, diagram-first |

Passports: `ivory.md` · `graphite.md` · `cobalt.md` — same folder as this file.

## Routing procedure

Run these steps in order; the first one that decides, decides. Log the result: `theme = <type> · source = forced | auto (<step and reason>)`.

1. **Forced override wins, always.** `--theme light|dark|blue`, a `Theme:` line, or a phrase in the user's own words. Honor it exactly and never re-route or "correct" it — even when topic routing disagrees.
2. **Route by purpose** using the table above (the profile's `theme_routing` holds the author's wording of the same map).
3. **Straddling topics route on the reader's job**, not the subject matter. Ask: who acts on this post, and what are they doing when they act? A post about AI tooling read by someone restructuring a team routes `ivory`; the same subject read by an engineer choosing a stack routes `cobalt`; read by a buyer deciding whether to trust a vendor, `graphite`.
4. **A genuine coin flip — and only then — goes to the least-used type.** Count existing posts per type (`data-theme` of each `Posts/*/Visual/carousel.html`; text-only posts do not count) and pick the smallest tally. This keeps the feed visually varied without letting the counter override meaning: if steps 2–3 produced an answer, the counter is never consulted.

## After routing

Read `content-types/<resolved type>.md` in full before Stage 3 decides archetypes or writes a line of markup. The passport constrains the build; `components.md` supplies the markup; `layout-playbook.md` supplies the defect rules. All three apply, in that order.
