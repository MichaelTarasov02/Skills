# Skill specification template

Fill this in phase A3, show it, wait for an answer. Frame borrowed from
`deliver-edge-cases` (When to Use / When NOT to Use / Instructions / Output / Checklist),
extended with the fields Dev Agent needs.

---

## 1. Identity

```yaml
name: <kebab-case, matches directory>
description: <third person; key use case first; English and Russian triggers;
              names the artifacts involved; under 1536 characters>
```

Invocation: model-invoked for all nine working skills — the developer should not have to
remember names.

## 2. Leading word

One compact concept from the model's pretraining that the agent thinks with while
running this skill. Repeat it in the body so it accumulates meaning.

## 3. Subject

- Does:
- Deliberately does not:

## 4. Boundaries — one row per sibling

| Sibling | Seam |
|---|---|
| `setup` | |
| `spec` | |
| `copy` | |
| `craft` | |
| `review` | |
| `debug` | |
| `handoff` | |
| `resolve-bug` | |
| `enhance` | |
| `improve` | |
| `refactor` | |
| `ship-feature` | |

Fill every row. Skills with blurred seams is `duplication` — the likeliest way the agent
falls apart. For a pipeline, the seam against a tool is always the same sentence: the
pipeline routes and carries, the tool does the work. Write which work.

## 5. Trigger moment

When in the developer's work this fires. Be concrete about the state of the work, not
about phrasing.

## 6. Covered use cases

| ID | Case | What counts as closed |
|---|---|---|

Copy the IDs verbatim from the build prompt. These become the coverage report.

## 7. Inputs

| Artifact | Required | Behaviour when absent |
|---|---|---|

Every row needs the third column filled. See `artifact-contract.md`.

## 8. Output

- Path:
- Format:
- Who reads it next:

If another skill greps this artifact, state the grep-stable shape here.

## 9. Phases

| # | Phase | Completion criterion |
|---|---|---|

Criteria must let the agent tell done from not-done.

## 10. Platform split

- Shared procedure (body):
- `references/react.md`:
- `references/flutter.md`:
- Pointer wording from the body:

See `platform-split.md`.

## 11. Non-goals

Phrase as target behaviour with the alternative named, not as bare prohibition.

## 12. Verification

The runs from the build prompt, listed. Each produces output in phase A6.
