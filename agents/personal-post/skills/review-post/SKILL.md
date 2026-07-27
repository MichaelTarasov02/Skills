---
name: review-post
description: Runs the full quality check on an existing post — specification completeness, caption length and watchlist, then visual QA for frame overflow, dangling arrows, theme mismatch, fill ratio, and a cropped sign-off. Use this when the user asks to review, check, QA, or verify a post they already have, when a post looks wrong after export, when they want to know if a draft is publishable, or before publishing anything from this pipeline.
argument-hint: <path to a post folder>
allowed-tools: Read, Bash, Glob, Grep, Edit
---

# Review Post

Check an existing post without rebuilding it. Useful before publishing, after hand-editing, or when a deck looks off and the reason is not obvious.

## Run the scripts first

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/skills/new-post/scripts/verify_spec.py" "<post folder>"

cd "<post folder>/Visual" 2>/dev/null && \
  node "${CLAUDE_PLUGIN_ROOT}/skills/new-post/scripts/verify_visual.mjs"
```

The first checks the twenty required sections, caption length against the profile's band, the watchlist, banned constructions, placeholders, and invented engagement numbers. The second measures every artboard.

If the visual has not been exported yet, run `node "${CLAUDE_PLUGIN_ROOT}/skills/new-post/scripts/export.mjs"` from inside `Visual/` first — the measurements read the rendered DOM, and the PDF page count is checked against the slide count.

## Then look at the renders

The scripts measure geometry. They cannot see the defect that matters most: a component stretched so its content floats in a hollow middle. That reports 100% fill precisely because it touches both edges of the band.

Open `exports/*.png` and check each slide against `${CLAUDE_PLUGIN_ROOT}/skills/new-post/references/layout-playbook.md`. Give priority to:

- any slide the script flagged at 99%+ fill, which is where hollow stretches hide
- any slide under 40%, which reads as a small block in a void
- the single page, where a cropped `.endnote` removes the post's ending while the export still succeeds

## Report

Lead with the verdict, then the evidence. Separate what you fixed from what needs a human decision — those are different asks, and merging them buries the second.

When a defect matches a playbook rule, name the rule. When it does not and you have now seen it twice, add it to the playbook. That is how the next post starts ahead of this one.

Report failures plainly, including ones you could not fix. A review that reports "looks good" after silently skipping the visual is worse than no review, because it transfers false confidence.
