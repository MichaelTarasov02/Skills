---
name: apply-edits
description: This skill should be used when a scriptwriter or editor has returned a marked-up review document and their changes must go back into the Interacta novel — "примени правки редактора", "внеси правки из docx", "редактор вернул документ", "обнови новеллу по замечаниям", "apply the editor's edits", "merge the review back". It reads the edited DOCX together with its review map JSON, applies copy changes to the localized JSON and Specification.md, rejects anything that would break the story graph or the schema, re-runs the QA gate, and reports every change as applied, rejected or unresolved.
---

# Apply editorial changes back into a novel

Take a marked-up review document and fold the editor's wording back into the package — safely, without letting a copy edit silently rewrite the story graph.

## Non-goals

- Do **not** restructure the graph. Adding, removing or rerouting screens, answers or scenarios is a regeneration task, not a copy-apply pass.
- Do **not** apply anything you cannot map with confidence. Unmapped goes to the report, not into the files.
- Do **not** write display labels into content. `(Kind)`, `sympathy +25`, `Шаг 4` and partner names are review aids, never part of answer `text`.

## Phase 0 — Inputs

Required: the edited `.docx`. The review map is inferred by replacing `Presentation Review - {LOCALE}.docx` with `Presentation Review Map - {LOCALE}.json` in the same folder.

**Without the review map, stop and ask.** The visible document deliberately carries no IDs; the map is the only safe bridge back to them. Guessing by position corrupts novels.

Follow `Prompts/Novel Editorial DOCX Revision Applicator Prompt.md` for the full contract.

## Phase 1 — Read the changes

Read, in priority order: tracked insertions and deletions, then comments attached to story fields, then plain visible text compared against the map's `sourceText`.

If the DOCX library cannot read tracked changes or comments, unpack the file and read the Word XML directly rather than silently falling back to visible text only.

## Phase 2 — Classify every change

| Class | Handling |
| --- | --- |
| Copy edit to a mapped field (title, description, step text, question text, answer text, ending text) | Apply to the localized JSON and to `Specification.md` |
| Structural request (add/remove/reorder screens, answers, routes, endings) | **Reject.** Record it with the reason; it needs regeneration |
| Change to a display label or a technical value | **Reject.** Those are review aids, not content |
| Comment that is a question or a note, not an instruction | Record as unresolved for the human |
| Change that would break the schema or safety rules | **Reject** with the reason |

Preserve `[Name]` literally. Keep en-US and ru-RU structurally identical — only user-facing strings may differ.

## Phase 3 — Apply

Write the localized `Technical Specification.{LOCALE}.json` and the matching sections of `Specification.md`. If the locale is `en-US`, update `Technical Specification.json` too so the alias stays byte-identical.

Regenerate `Database Insert.sql` whenever `content_json`, the title or the description changed.

Never touch IDs, order, weights, answer types, routes, `answeredBy`, `nextForA`/`nextForB`, `requiredSympathy`, `sympathyWeights`, or `endings` ranges.

## Phase 4 — QA gate (mandatory, blocking)

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/validate_novel.py" "Novels/Library/{Novel Title}"
```

Paste the real output. **Exit code 1 means stop** — revert or fix, then re-run. A copy edit must never leave the package invalid.

## Phase 5 — Refresh the review materials

When edits were applied, invoke **`to-editor`** on the folder so the DOCX, graph and review map match the updated novel. A stale review document is how the next round of edits gets applied to the wrong text.

## Phase 6 — Report

A table of every change: `applied` / `rejected` / `unresolved`, what it touched, and for rejections the reason. Then the QA gate output, and the refreshed editorial artifacts.

Be explicit about rejections. A silently dropped editor request is worse than a refused one — they will assume it shipped.
