---
name: generate
description: This skill should be used when the user wants to create a new Interacta interactive novel from an idea, a scenario seed, a theme or a one-line premise — "сгенерируй новеллу", "создай новеллу про", "новая новелла", "generate a novel", "make an Interacta novel about". It produces the full package under Novels/Library/{Title}/ (Specification.md, three Technical Specification JSON files, Database Insert.sql), runs the QA gate, and then automatically produces the editorial review materials (DOCX, branch graph, review map) so the result is ready to hand to a scriptwriter or editor. Not for implementing a scriptwriter's finished script — that is generate-by-script.
---

# Generate a novel from an idea

Turn a scenario seed into a complete, engine-valid, editor-ready Interacta novel.

## Non-goals

- Do **not** implement a finished scriptwriter's script here. That is `generate-by-script`.
- Do **not** generate images. That is `visualize`.
- Do **not** invent engine fields. The schema is the contract.

## Phase 0 — Locate the repo

Find the repo root by walking up from the working directory until `Schemas/novel.schema.json` exists. If it is not found, ask the user for the path to the Novels repository and stop until they answer. Every path below is relative to that root.

## Phase 1 — Load the contracts

These files are the source of truth. Read them; do not work from memory, and do not copy their rules into this skill.

| File | Governs |
| --- | --- |
| `Prompts/Novel Generator Prompt.md` | the full generation contract — follow it verbatim |
| `Specifications/Novel Production Specification.md` | output folder, `Specification.md` sections, SQL contract, QA |
| `Source/Spec 4/Генерация новых новелл *.md` | engine truth: roles, `answeredBy`, `nextForA/B`, `sympathyWeights`, `endings`, `requiredSympathy` |
| `Knowledge/Interacta Novel Voice Guide.md` | voice for all user-facing copy, en-US and ru-RU |
| `Knowledge/Interacta Novel Branching Guide.md` | branching, route families, ending lanes |
| `Knowledge/Interacta Novel Categories.json`, `Interacta Backend Category Catalog.json` | category keys |
| `Schemas/novel.schema.json` | machine-checkable JSON contract |

If the user supplied only a thin seed, apply the defaults from `Novel Generator Prompt.md`. Ask a question only when the request is unsafe or genuinely ambiguous.

## Phase 2 — Build the package

Create `Novels/Library/{Novel Title en-US}/` containing exactly:

```
Specification.md
Technical Specification.json          # byte-identical copy of the en-US file
Technical Specification.en-US.json
Technical Specification.ru-RU.json
Database Insert.sql
```

Reserve CDN image URLs; do not create image files.

### Sympathy — the rule that most often ships broken

A perfect playthrough must total **exactly 100**.

1. Assign each answer a delta from its behaviour: warm answers positive, cold and neutral answers `0`.
2. Let `R` be the sum, over every Choice on the route to the ending, of that Choice's largest positive delta.
3. Scale every delta by `100 / R` and carry the result in `sympathyWeights`, with uniform `weight: 1`.
4. Split `0..100` evenly by ending count: two endings → `0-50` / `51-100`; three → `0-33` / `34-66` / `67-100`.

The number an editor reads next to an answer and the number in an ending threshold are then the same unit, and summing the best answers reaches the warmest band. Mixing scales here is what makes a reachable ending look impossible.

## Phase 3 — QA gate (mandatory, blocking)

Run the validator and paste its real output into your reply:

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/validate_novel.py" "Novels/Library/{Novel Title}"
```

It checks: JSON parse, schema, alias equality, route integrity, reachability, question shape, `answeredBy` alternation, the 100-point sympathy scale, ending-band coverage and reachability, en/ru parity, image URLs, and the presence of the SQL and spec files.

**Exit code 1 means stop.** Fix the novel and re-run. Never edit the report, never explain a failure away, and never proceed to Phase 4 on a failing gate.

## Phase 4 — Editorial handoff (automatic)

When the gate passes, invoke the **`to-editor`** skill on the folder you just created, with locale `ru-RU` unless the user asked otherwise. It writes `Editorial/` with the review DOCX, the standalone HTML branch graph, and the review map JSON.

Do not reimplement the DOCX or graph rules here. `to-editor` owns them, so a fix there reaches every novel.

## Phase 5 — Report

State plainly:

- the folder created and the five files in it;
- the QA gate result, as the validator printed it;
- the editorial artifacts produced by `to-editor`;
- graph size: scenarios, Choice questions, answers, endings, unique images;
- that visual assets still need generating (`visualize`), since this skill only reserves URLs;
- any open question for the editor.
