# Content Types — the orchestrator

A **content type** is the full visual identity of a post, not a palette. Palette, typography treatment, component bias, text density, structure, texture, emoji register, cover and close character — all of it is decided by the type. Each type has a **passport** in this folder; the passport is the single source of truth for how that type looks. Read the resolved type's passport before building any artboard.

The goal the system serves: **three consecutive posts must read as different designs by the same author.** Shared brand constants hold them together; everything else is allowed — required — to differ.

## What is shared across all types (the brand constants)

These never vary per type. If a passport contradicts this list, the list wins.

- **Faces:** Newsreader (display serif) + Geist (sans) + Geist Mono. The export gate throws on any other family. Types differ in how the faces are *used* — size, weight, case, which face carries which role — never in the faces themselves.
- **Artboard:** 1080×1350, safe pad 90px, type floors (meaning-carrying text ≥ 24px on a carousel slide).
- **Film grain** as a physical surface (opacity varies per type).
- **Colour is ink and edge, not fill** — see `visual-system.md`.
- **Export gates** (fonts / size / count) and both modes (carousel + single page).
- **Risk rules on the artboard** — no logos, no CTA bands, no screenshots, no invented measurements.
- **Bespoke uniqueness:** every post invents one structural object that has never appeared in any previous post. The type shapes *what kind* of object fits; it never excuses a repeat.

## Three purposes, five fields

| Purpose — route here when the post is about | Type | Field | Passport |
|---|---|---|---|
| Company management, team management, processes, hiring mechanics, operating information | `ivory` | white sheet, navy ink | `ivory.md` |
| Founder lessons, selling, marketing, positioning, business judgment | `graphite` | deep space, near-white ink | `graphite.md` |
| Technical topics, AI, engineering, tools, new technology, product mechanics | `cobalt` · `green` · `cherry` | saturated field, light ink | `colored.md` |

The third row is **one type wearing three colours**. Purpose, character, texture, components and word budget are identical across cobalt, green and cherry; only the hue changes. That is why they share a passport.

## Routing procedure

Run these steps in order; the first one that decides, decides. Log the result: `theme = <type> · source = forced | auto (<step and reason>)`.

1. **Forced override wins, always.** `--theme light|dark|blue|green|cherry`, a `Theme:` line, or a phrase in the user's own words. Honor it exactly and never re-route or "correct" it — even when topic routing disagrees.
2. **Route by purpose** using the table above (the profile's `theme_routing` holds the author's wording of the same map).
3. **Straddling topics route on the reader's job**, not the subject matter. Ask: who acts on this post, and what are they doing when they act? A post about AI tooling read by someone restructuring a team routes `ivory`; the same subject read by an engineer choosing a stack routes to the coloured family; read by a buyer deciding whether to trust a vendor, `graphite`.
4. **A genuine coin flip between the three purposes — and only then — goes to the least-used type.** Count existing posts per type and pick the smallest tally. If steps 2–3 produced an answer, this is never consulted.

## Choosing the colour, once the coloured family is resolved

Only runs when step 2, 3 or 4 landed on the coloured family and no colour was forced.

1. **Count the three colours across existing visual posts.** Read `data-theme` from each `Posts/*/Visual/carousel.html`. Text-only posts do not count.
2. **Take the least-used colour.** On a tie, take the one whose most recent use is furthest back. This is what stops two coloured posts running back to back in the same hue.
3. **Apply the cherry caveat.** A red field says "something is wrong here" before a word is read. If the rotation offers cherry to a post whose argument is calm and operational, say so in the run log and take the next colour instead. Variety is the reason the rotation exists; it is not permission to ignore what a colour means.

Log the colour with its reason, the same way the type is logged: `theme = green · source = auto (rotation, least used: cobalt 4 / green 0 / cherry 1)`.

## After routing

Read the resolved type's passport in full before Stage 3 decides archetypes or writes a line of markup — `ivory.md`, `graphite.md`, or `colored.md` for any of the three colours. The passport constrains the build; `components.md` supplies the markup; `layout-playbook.md` supplies the defect rules. All three apply, in that order.
