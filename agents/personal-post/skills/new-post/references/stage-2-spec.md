# Stage 2 — Specification

Produce exactly one file: `<output_dir>/<Post Name>/Post Specification.md`. It carries the strategy, the publish-ready caption, and the two fields Stage 3 depends on.

## Required sections, in this order

```
# Personal LinkedIn Post Specification: <post name>
Source folder: · Final post language: · Working notes language:

## Source Idea              ← include source-fidelity notes
## Assumptions
## Personal Brand Fit
## Strategic Interpretation ← include source-fidelity notes
## Post Metadata
## Reader Psychology
## Narrative Angle
## Post Structure
## Discussion Strategy
## LinkedIn Optimization Notes
## Copy-Ready LinkedIn Post ← the publishing source of truth
## Alternate Hooks
## Post Copy Notes          ← include source-fidelity notes
## Visual Specification
### Optional Visual Decision
### Optional Visual Brief
## CTA / Closing Move
## Risk Notes
## Human Voice QA           ← include source-fidelity notes
## Acceptance Criteria
```

`verify_spec.py` checks all twenty are present. Run it before Stage 3.

## Post Metadata — the fields Stage 3 reads

```
Post type: · Primary reader: · Post goal: · Funnel role: · Brand pillar:
Archetype: · Recommended length: · CTA type: · Languages:
Visual decision:  none | optional | recommended | required
Visual theme:     <resolved in Step 1 — never re-decided here>
Carousel depth:   <depth> (B=<n>) → <n> slides
```

**Carousel depth is derived, never chosen by habit.** Count the load-bearing beats **B** in `Post Structure` — a beat is one idea that can hold a slide alone. Then `slides = clamp(B + 2, 6, 12)`, where the +2 is cover and close.

| Beats | Slides |
|---|---|
| 3–4 | 6–7 |
| 5–6 | 8–9 |
| 7–8 | 10–11 |
| 9+ | 12 |

Padding a thin idea to 12 slides is the failure this rule prevents. Seven honest slides beat twelve padded ones. If Stage 3 merges or drops beats, come back and correct this line — a spec that disagrees with its own deck is worse than either alone.

## The caption

When the visual decision is `recommended` or `required`, the caption is a **short overview**, not a compressed carousel. It introduces the tension, says what the carousel covers, and asks one specific question. It must not enumerate what the slides already show — a reader who sees the same list twice learns the post has nothing more to give.

When the decision is `none`, the caption carries the whole argument.

Length comes from the profile (`caption_min`/`caption_max`). Formatting: no markdown headings, no labels like "Hook:", blank lines between paragraphs, most paragraphs one sentence, pasteable straight into the platform.

## Discussion strategy

Every post needs one deliberate mechanism, chosen for the idea rather than by default: contrarian POV · two-sided trade-off · open operational question · "this works until" · myth vs production reality · personal change of mind · line-drawing question.

Record all six fields: chosen strategy · why it fits · expected side A · expected side B · safety guardrail · final question.

**Create disagreement around trade-offs, incentives, and assumptions — never hostility toward people.** Criticize a decision, a habit, a calculus. Never a group. The final question must be specific enough that "agree" is not an answer.

## Optimization notes

Cover: topic lane · reader signal in the first two lines · semantic anchors · dwell and save mechanism · AI-slop cleanup required · watchlist phrases to remove · external link policy · first-hour reply plan · analytics to watch · confidence caveat.

Two honesty rules that matter more than they look:

- Engagement-timing habits are **operating habits, not confirmed platform rules**. Say so.
- No platform publishes an official banned-word list. The watchlist is risk control, not compliance. Never present it as policy.

Never state invented reach percentages, impressions, or follower numbers anywhere.

## Humanization

Avoid, because they read as generated regardless of vocabulary: trend openings · "not X, it's Y" · rhetorical setups you answer yourself · em dashes · negative triads · staged one-line drama · inanimate actors ("the workflow decides") · vague declaratives ("the implications are significant") · fake vulnerability · inflated closings.

Prefer: a specific opening · one real moment · concrete nouns from the work · varied sentence rhythm · a stated constraint or trade-off · one practical implication.

The draft needs at least three of: concrete context · a real constraint · a trade-off · what was underestimated · a before and after · a technical detail · a business consequence · a practical takeaway.

## Collision check

The spec must name any neighbouring post and state how this angle differs. Same source with a different thesis is fine. Same thesis to the same reader is not — and it costs the author credibility, not just time.

## Gate

`verify_spec.py` passes → read `Visual decision` and proceed to Stage 3's gate.
