---
name: to-editor
description: This skill should be used when an existing Interacta novel must be turned into materials a non-technical scriptwriter or editor can read and mark up — "отдай новеллу редактору", "сделай документ для редактуры", "подготовь новеллу на ревью", "нужен граф ветвлений", "prepare this novel for review", "make the editor DOCX". It produces three files in the novel's Editorial/ folder, namely a printable Word review document, a standalone HTML branch graph, and an internal review map JSON used later to apply the editor's changes back safely. It is also called automatically at the end of generate and generate-by-script.
---

# Prepare a novel for editorial review

Render an existing novel as something a person can read on paper and correct with a pen, plus a branch graph they can follow at a glance.

## Non-goals

- Do **not** modify the novel. This skill is read-only on `Specification.md`, the JSON files and the SQL.
- Do **not** expose implementation. No scenario/question/answer IDs, no routes, no engine `weight`, no JSON field names, no file paths, no CDN URLs, no SQL.
- Do **not** put the review map's contents inside the DOCX or the graph.

## Phase 0 — Inputs

Required: the novel folder. Optional: locale (`ru-RU` default, or `en-US`), image mode (`embed-best-effort` default).

Locate the repo root by walking up until `Schemas/novel.schema.json` exists. Read the localized `Technical Specification.{LOCALE}.json` as the source of truth for text, and `Specification.md` for title, description, length and roles.

Follow `Prompts/Novel Editorial DOCX Generator Prompt.md` for the full contract. It owns the detailed rules; this skill owns the procedure and the gates.

The branch graph has one approved format, `interacta.branch-graph.v2`, specified in `Specifications/Editorial Branch Graph Format.md`. Every novel gets it. Do not redesign it for a particular novel and do not hand-author a graph — improving the format means changing the generator, which then applies to every novel at once.

## Phase 1 — Build the three artifacts

Run the generators. They derive the review model once and all three artifacts read visible step numbers from it, so the DOCX, the graph and the map can never disagree.

```bash
python3 ~/.claude/skills/interacta-novels/scripts/build_review_model.py "{novel folder}"
node     ~/.claude/skills/interacta-novels/scripts/build_review_docx.js "{novel folder}"
python3 ~/.claude/skills/interacta-novels/scripts/build_branch_graph.py "{novel folder}"
```

The graph script self-checks and **exits 1** on an orphan step, a backwards-pointing step number, a leaked engine ID, a network dependency, or a warmest ending the best playthrough cannot reach. Exit 1 means stop and fix the novel — never the document. The DOCX script needs `docx-js` (`npm install -g docx`).

What the model derives, and what to verify if you ever build these by hand:

- **visible step numbers** for every Choice question, ordered by longest-path rank so they only ever go forward. A breadth-first ordering numbers convergence hubs before the branches feeding them and makes the editor read `Шаг 6 ведёт к Шагу 5`;
- **ownership**: `answeredBy` is authoritative — `A` → Partner 1, `B` → Partner 2. Text screens are `Оба партнёра` / `Both partners`, except screens inside a role's own branch, which belong to that role;
- **narrative blocks** between Choices, kept as real screens with both role versions;
- **destinations**: an answer's destination is its *immediate* next screen. When narrative screens sit between two Choices, show them on the way;
- **playthrough facts**: every complete route walked once, giving the best and worst reachable score and the share of routes landing in each ending band.

## Phase 2 — The three artifacts

Written into `{novel folder}/Editorial/`:

```
{Title} - Presentation Review - {LOCALE}.docx
{Title} - Branch Graph - {LOCALE}.html
{Title} - Presentation Review Map - {LOCALE}.json
```

`.review-model.json` is the build intermediate the three share. It is hidden, internal, and not for the editor.

**DOCX** — cover (title, description, length, roles, sympathy legend naming the 100-point maximum), a short editor note, a branch overview table, the story step by step with both role versions, the endings section, and blank editor-note lines throughout. US Letter, Arial, page numbers. Images embed from `Visual/` when present; otherwise a clean named placeholder.

**HTML graph** — one self-contained file, inline CSS and JS, no network dependencies, opens from disk. Two views: a small SVG overview showing the whole novel on one screen, and below it a single vertical column read top to bottom like the printed document — Choice cards with destination links, narrative collapsed to one-liners that expand into a side-by-side Partner 1 / Partner 2 comparison. Plus a trial-playthrough panel that scores exactly as the engine does.

A graph that needs horizontal scrolling to read has failed, however correct its connectors are. `Prompts/Novel Editorial DOCX Generator Prompt.md` carries the full contract and the history behind it.

**Review map JSON** — the technical sidecar that makes reverse-application safe. It carries the IDs, ownership, `answeredBy`, per-answer types, sympathy values, thresholds, destinations, roles, `sympathyWeights` and `endings`. Editors never see it; `apply-edits` depends on it.

## Phase 3 — Units coherence (the check that matters most)

Per-answer values and ending thresholds must be the **same unit**, the 0-100 scale where a perfect playthrough totals 100.

Summing the best visible answer values across a playthrough must reach the warmest visible threshold. If it does not, the novel is wrong — say so and stop. Never adjust the document to hide it. An editor who adds up the visible numbers and cannot reach the ending has found a real defect, and that is exactly how one was found before.

## Phase 4 — Verify by measuring, not by reading

Confirm and report:

- **DOCX validates** — `python3 ~/.claude/skills/docx/scripts/office/validate.py "<file>"` prints `All validations PASSED!`;
- **Graph self-check passes** — `build_branch_graph.py` exits 0 and prints its destination-link count;
- **Graph carries the approved format stamp** — `data-format="interacta.branch-graph.v2"` on `<html>`. A graph without it did not come from the generator and must not be sent to an editor;
- **Graph has no orphan nodes** — every step except the first is some answer's destination, and every overview node touches an edge. Measure the rendered DOM in a browser; do not infer it from the source;
- **Step numbers only go forward** — no destination number is less than or equal to its source;
- **No sideways scrolling** — no horizontal overflow at 336px, 760px and 1360px viewport widths, measured in a browser;
- **No connector skips a screen** — a Choice never connects straight to the next Choice when narrative screens exist between them;
- **No answer connects to an ending** — endings hang off a single terminal node, each connector labelled with a sympathy band, never with an answer letter;
- **Cleanliness** — grep all three files for IDs, routes, JSON field names, SQL, file paths and CDN URLs. AnswerType values are allowed only as `(Kind)` labels before answer text;
- **Coverage** — every Choice question in the JSON has a node in the graph and a step in the DOCX; counts match the review map.

An orphan node or an answer-to-ending connector is a defect, not a cosmetic issue: both previously made an editor report that the branching ignored their answers.

## Phase 5 — Report

List the three files with real paths, the QA results above with their evidence, the embedded-image and placeholder counts, and remind the user to send only the DOCX and HTML to the editor while keeping the review map in `Editorial/`.
