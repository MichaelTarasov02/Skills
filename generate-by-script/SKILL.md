---
name: generate-by-script
description: This skill should be used when a scriptwriter has already written a novel scenario as a Markdown file and it must be turned into a production Interacta novel package — "новелла по скрипту", "сгенерируй новеллу по сценарию", "вот скрипт от сценариста", "реализуй сценарий", "implement this script", "turn this script into a novel". It parses the [SCENARIO]/[QUESTION]/[ANSWER] notation, carries every screen, branch, answer and sympathy delta into engine-valid JSON, proves one-to-one coverage, runs the QA gate, and then produces the editorial review materials. Use generate instead when starting from an idea rather than a written scenario.
---

# Implement a scriptwriter's scenario

**The scenario is the product.** Your job is to carry it into engine-valid JSON, not to redesign it. A run that "improves" the story has failed.

## Non-goals

- Do **not** rewrite, soften or drop the scriptwriter's content. See `Content Authority` in the prompt.
- Do **not** invent screens, answers, scenarios or sympathy gates that the scenario does not contain.
- Do **not** pad the graph to reach a length tier. The scenario's own size is the length.

## Phase 0 — Locate the repo

Walk up from the working directory until `Schemas/novel.schema.json` exists. If not found, ask for the Novels repository path and stop until answered.

## Phase 1 — Load the contracts

| File | Governs |
| --- | --- |
| `Prompts/Novel Script Implementation Prompt.md` | **the full implementation contract — follow it verbatim** |
| `Source/Spec 4/How to read Editor Novel.md` | the scriptwriter's own legend for their notation — authoritative reading key |
| `Source/Spec 4/Генерация новых новелл *.md` | engine truth: navigation priority, roles, re-forks, sympathy, endings |
| `Specifications/Novel Production Specification.md` | output contract and QA |
| `Knowledge/Interacta Novel Voice Guide.md` | voice for copy **you** author (ru-RU, ending titles); never for the scriptwriter's own lines |
| `Schemas/novel.schema.json` | machine-checkable JSON contract |

Read the legend before the scenario. It defines how each screen has a Player 1 and a Player 2 version.

## Phase 2 — Parse before writing anything

Build a complete inventory first: every `[SCENARIO]`, every `[QUESTION]`, every `[ANSWER]`, its delta, its arrow target, and which player answers it. Count them. Verify every arrow resolves to a screen that exists.

Parsing a large scenario by hand is unreliable — a 119-screen scenario has too many routes to track by eye. Parse mechanically and check that every route resolves before authoring a single line of JSON.

## Phase 3 — Map onto the engine

Follow the prompt's mapping rules. The four that were historically lost, and must not be lost again:

| Scenario mechanic | Correct mapping |
| --- | --- |
| Each screen has a P1 and a P2 version | Author both; route them with `nextForA` / `nextForB`; converge at the next shared Choice |
| `[SCENARIO Y]` entered by sympathy | Map onto `requiredSympathy`; never collapse the bands |
| Text screen ends `→[SCENARIO Y]` | One engine scenario per script `[SCENARIO]`; route across |
| Text screen ends `→[THE END]` | The ending is a no-choice screen: fold it into `endings[]`; never invent a terminal Choice |

Meeting a fifth mechanic with no engine equivalent: implement the closest faithful mapping and record it in the `Engine Gap Register`. Never degrade it silently.

### Sympathy

Points come from the scriptwriter's own deltas. Negative and untagged answers score `0`. Compute `R` (the sum of each Choice's largest positive delta on the route to the ending), scale everything by `100 / R` so a perfect playthrough totals exactly **100**, and split `0..100` evenly by ending count unless the scenario names a threshold.

## Phase 4 — Prove coverage

`Specification.md` must contain a `Script Coverage Audit` accounting for **every** source `[QUESTION]` and `[ANSWER]`, with counts that reconcile arithmetically. Status is one of `Carried`, `Mirrored pair`, `Merged (justified)`, `Emitted, unreachable`, `Not carried`.

Any `Not carried` without explicit human approval blocks delivery. Coverage below 100% blocks delivery.

Also produce the `Engine Gap Register` (where the scenario exceeds engine capability) and the `Content Risk Register` (real-world risks, preserved as written and flagged — never silently edited).

## Phase 5 — QA gate (mandatory, blocking)

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/validate_novel.py" "Novels/Library/{Novel Title}"
```

Paste the real output. **Exit code 1 means stop**: fix the novel and re-run. Never edit the audit to make a check pass.

The gate does not check fidelity. Verify separately, and say so explicitly in your report:

- source scenarios = engine scenarios; source Choices = engine Choice screens; source answers = engine answers;
- scene order preserved;
- every role-specific Text run has both an A and a B version;
- negative-delta answers score exactly `0`.

## Phase 6 — Editorial handoff (automatic)

When the gate passes, invoke the **`to-editor`** skill on the folder, locale `ru-RU` unless told otherwise. It owns the DOCX, branch graph and review map. Do not reimplement those rules here.

## Phase 7 — Report

- source counts vs emitted counts, and the coverage percentage;
- the QA gate output as printed;
- the editorial artifacts;
- the `Engine Gap Register` and `Content Risk Register` entries, if any;
- that visual assets still need generating (`visualize`).
