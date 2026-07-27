---
name: visualize
description: This skill should be used when an existing Interacta novel needs its visual assets — "сделай визуал для новеллы", "сгенерируй картинки к новелле", "нужны изображения для новеллы", "визуализируй новеллу", "generate the visuals", "make the images for this novel". It reads the novel's reserved image URLs and visual brief, builds a continuity-locked shot list with a ready-to-run generation prompt for every asset, writes them to the novel's Visual/ folder, and generates the WebP files when an image-generation tool is available. Without such a tool it stops at the prompt pack and says so plainly rather than pretending images were produced.
---

# Produce the visual set for a novel

Turn a finished novel into a continuity-consistent set of images, one per unique visual beat.

## Honest capability note — read first

This skill needs an **image-generation tool** to produce `.webp` files. Check what is available in the current environment before promising output.

- **Tool available** → run the full pipeline, Phases 0-5.
- **No tool** → run Phases 0-3, write the prompt pack, and report clearly that no images were generated and why. Do not describe a prompt pack as if it were a delivered image set.

## Non-goals

- Do **not** modify the novel's JSON, `Specification.md` or SQL. The image URLs are already reserved there.
- Do **not** invent filenames. Generate exactly the assets the reserved URLs name.
- Do **not** produce one image per question. One image per **unique visual beat**; reused URLs get one file.

## Phase 0 — Locate and load

Walk up until `Schemas/novel.schema.json` exists. Then read:

| File | Governs |
| --- | --- |
| `Prompts/Visual Asset Generator Prompt.md` | **the full visual contract — follow it verbatim** |
| `Knowledge/Interacta Novel Visual Style Guide.md` + `Knowledge/example.png` | the house look |
| `{novel}/Specification.md` | `Visual Diversity Seed`, `Story Continuity Ledger`, `Visual Asset Brief`, `Image Reuse Map` |
| `{novel}/Technical Specification.en-US.json` | the reserved `imageUrl` values and `endings[].imageUrl` |

## Phase 1 — Derive the shot list

Collect every distinct `imageUrl` in the novel, plus one per `endings[]` entry. For each, record from the spec: the scene, what must appear, what must not, and its continuity anchors.

The list is ordered, because continuity is sequential: `header` first, then `step-01`, `step-02`, and so on, then the ending screens.

## Phase 2 — Lock continuity

Before writing any prompt, fix the things that must not drift across the set: the two leads' identity and wardrobe, the location's layout, recurring props, the light and the time of day.

The hard rule from the style guide: if `step-02` puts a table beside a window, later same-location images keep that table beside that window. The camera may move; the furniture may not, unless the story says they moved.

Both leads are adults 21+. Diversity is respectful and never a personality shortcut. No celebrity or real-person likenesses.

## Phase 3 — Write the prompt pack

Write `{novel}/Visual/prompts.md`: one entry per asset, in generation order, each carrying the full generation prompt, the aspect ratio, the continuity anchors it must honour, and which previously generated asset to use as a reference.

This file is the deliverable when no image tool is available, and the working script when one is.

## Phase 4 — Generate (only with an image tool)

Generate sequentially, never in parallel — each image uses the previous approved one as its continuity reference.

After each image, check it against its brief: right characters, right location, anchors intact, no text baked into the picture, no drift from the established look. Regenerate rather than accept a near miss; one drifted image breaks the set.

Save as WebP into `{novel}/Visual/` under the exact filename from the reserved URL.

## Phase 5 — Report

- the shot list, and for each asset whether it was generated, skipped or failed;
- where the files were written;
- **if no image tool was available: say so first**, state that `prompts.md` is the deliverable, and name what would be needed to finish;
- the reminder that generated files still need uploading to the CDN paths already reserved in the novel's `imageUrl` values.
