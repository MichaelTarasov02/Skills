# Artifact contract

Read before phases A1 and B2. The nine skills are wired together by files, not by calls.
This file is what makes them an agent rather than nine separate tools.

Everything lives in `PRODUCT_REPO/.dev-agent/`, never inside the plugin. The plugin is
the tool; the repository holds the knowledge.

| File | Written by | Read by |
|---|---|---|
| `project.md` | `project-onboarding` | all |
| `config.yaml` | `project-onboarding` | all — platforms, paths, i18n, analytics |
| `onboarding.md` | `project-onboarding` | a human: known / assumed / unknown |
| `lexicon.md` | `product-lexicon` | `interface-copy`, `screen-blueprint`, `element-markup`, `outbound-writing` |
| `tone-of-voice.md` | `product-lexicon` | `interface-copy`, `outbound-writing` |
| `red-lines.md` | `product-lexicon` | `interface-copy`, `outbound-writing` |
| `component-inventory.md` | `product-lexicon` | `screen-blueprint`, `screen-review` |
| `features/<slug>.intake.md` | `feature-intake` | `screen-blueprint`, `feature-handoff` |
| `features/<slug>.handoff.md` | `feature-handoff` | `outbound-writing` |
| `screens/<slug>.blueprint.md` | `screen-blueprint` | `interface-copy`, `element-markup`, `screen-review`, `feature-handoff` |
| `screens/<slug>.strings.md` | `interface-copy` | `screen-review`, `outbound-writing` |
| `reviews/<slug>.review.md` | `screen-review` | `feature-handoff` |
| `.telemetry/tracking-plan.yaml` | plugin `product-tracking-skills` | `element-markup`, `feature-handoff` |

## Absence is a supported state

A reader that stops because a file is missing has failed. Every reader handles absence in
three moves: name what is missing, offer the skill that produces it, continue on
assumptions marked as such in its own output.

This is checked in B2 by opening each reader and citing the line where it does this.

## Grep stability

Several artifacts are consumed by other skills rather than by people. Their shape is part
of the contract: a term in `lexicon.md` must be findable by its canonical name; a
blueprint must yield its list of text slots and its list of interactive elements. Any
skill producing such an artifact states its grep-stable shape in specification field 8,
and proves it in phase A6 with the output of an actual search.

## Changing the contract

A new file or a changed shape touches every reader. Add the row here first, then update
the readers, then re-run B2. Editing a producer without touching this table is how the
chain quietly breaks.
