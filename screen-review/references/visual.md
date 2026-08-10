# Visual review

Read before phase 2. Adapted from `refactoring-ui`, narrowed to reviewing one built
screen rather than designing one.

"Looks amateurish" is always a measurable cause. Find it and name the number.

## Spacing

| Symptom | Cause | Edit |
|---|---|---|
| the screen feels noisy | values off the scale — 13px beside 16px beside 20px | snap every value to one scale (4/8/12/16/24/32/48) |
| groups do not read as groups | equal gaps between related and unrelated items | related items closer than the gap that separates groups; that ratio *is* the grouping |
| elements crowd the edge | padding smaller than the internal gaps | outer padding at least equal to the largest inner gap |

Start with the largest offender. One spacing scale applied consistently fixes more
perceived quality than any other single edit.

## Typographic hierarchy

Hierarchy comes from **contrast between levels**, not from size alone.

| Symptom | Cause | Edit |
|---|---|---|
| everything shouts | too many sizes, or too many bold weights | at most three sizes on a screen; one bold |
| the heading is invisible | heading only slightly larger than body | raise the step, or lower the body's weight and colour instead |
| dense text is unreadable | line length beyond ~75 characters, or line height under 1.5 | cap the measure, raise the leading |
| numbers do not line up in a table | proportional figures | tabular numerals |

Lowering the secondary is usually better than raising the primary — it keeps the page
calm.

## Colour

| Symptom | Cause | Edit |
|---|---|---|
| the palette looks flat | one shade per hue | a light shade, a mid, and a dark for each |
| status colour carries the whole meaning | colour used alone | add an icon or a word; colour is never the only channel |
| the primary action does not stand out | too many saturated colours competing | one accent; everything else neutral |
| grey text is unreadable | mid grey on white | measure it — see phase 4 |

## Depth

| Symptom | Cause | Edit |
|---|---|---|
| shadows look pasted on | uniform blur, pure black at high opacity | shadow scales with elevation; low opacity, tinted toward the background |
| everything floats | shadow on every surface | elevation only where something genuinely overlays |
| flat looks broken | no boundary at all between surfaces | one border, or one soft shadow — not both |

## Alignment and density

Every edge either aligns with another or is deliberately offset. Accidental
near-alignment — off by two or three pixels — reads as sloppiness before anyone can say
why. Scan the left edges first; they carry most of the perceived order.

Density: a comfortable screen and a data-dense table need different scales. Choose one
per region and hold it, rather than drifting between them within a single view.

## Icons

| Check | |
|---|---|
| Meaning | readable without its label; if not, keep the label |
| Origin | from the set already in use, not mixed from a second family |
| Weight | optical weight matching the text beside it |
| Alone | an icon-only control needs an accessible name — route that to `element-markup` |

## Motion

| Purpose | Duration | Note |
|---|---|---|
| state change on one element | 100–200ms | anything slower feels laggy |
| entering or leaving | 200–300ms | ease-out entering, ease-in leaving |
| large layout shift | 300–400ms | rare; usually a sign the layout should not shift |

Motion earns its place by explaining a change — where something came from, where it went.
Motion that only decorates costs time on every repetition. Respect
`prefers-reduced-motion`; its absence is a finding.
