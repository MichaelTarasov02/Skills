# Entity matching

How `scripts/match_entities.py` decides, why it decides that way, and what to change when it
is wrong.

## The failure this rule exists to prevent

Organisation names are built from a small pool of generic words. Strip the generic ones and
two unrelated companies can look identical:

| Signal record | Contact book | Distinctive tokens |
|---|---|---|
| Palo Alto Networks, Inc. | Palo Alto Post-Acute | `PALO`, `ALTO` — identical |
| City of Los Angeles | Los Angeles Post Acute | `LOS`, `ANGELES` — identical |
| Global IT Resources, Inc. | Nursing Resources | `RESOURCES` — identical |

A subset rule over distinctive tokens accepts all three. Those are real matches produced by a
first-pass implementation, and they only surfaced because a sample was read by hand.

## The rule that works

Three stages, and the split between them is the point:

1. **Normalise.** Uppercase, drop punctuation, strip corporate suffixes (`LLC`, `INC`,
   `GMBH`, `LTD`). Suffixes carry no identity.
2. **Find candidates by distinctive tokens.** A token in more than `GENERIC_DF` of all names
   is generic and used only for lookup.
3. **Decide on the full token set.** Jaccard similarity over *every* token, generic included,
   must reach `JACCARD_MIN`.

Stage 3 rejects all three failures above: `{PALO, ALTO, NETWORKS}` against
`{PALO, ALTO, POST, ACUTE}` scores 0.4 against a 0.75 threshold.

An exact match on the normalised string skips straight to `high` confidence.

## Thresholds

| Constant | Default | Raise it when | Lower it when |
|---|---|---|---|
| `GENERIC_DF` | 0.015 | industry words keep surfacing as distinctive | the universe is small and everything looks generic |
| `JACCARD_MIN` | 0.75 | the sample shows wrong matches | real matches are missed over one extra word |
| `MIN_LEN` | 6 | short names collide | legitimate short names exist in the universe |

Tune against the 20-row sample, one constant at a time, and re-read the sample after each
change.

## What no threshold fixes

**Doing-business-as names.** An entity operating under a trade name shares no tokens with its
legal name. Only an identifier bridges it — a licence number, registration number, or tax ID.
When both datasets carry one, join on that and skip name matching entirely.

**Same name, different site.** Chains reuse one name across locations. Add city or postal
code to the comparison when the universe contains several rows with identical names.

**Subsidiaries filed separately.** A parent sued under a holding company name reaches its
operating entities only through an ownership dataset. When the brief depends on that, find one
in `find-sources` before relying on names.
