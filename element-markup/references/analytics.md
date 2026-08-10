# Analytics layer

Read before phase 5.

## First: is there a plan?

Look for `PRODUCT_REPO/.telemetry/tracking-plan.yaml`.

| State | Behaviour |
|---|---|
| Plan exists | follow its naming scheme and its entity model. Inventing a name beside an existing scheme is the failure this check prevents |
| No plan | say so, name the SDK that is present, propose the event **as a proposal**, and point at `product-tracking-design-tracking-plan` |
| No plan and no SDK | the layer is not applicable. Say that and skip it |

**Current state of this product:** no `.telemetry/` in either repository. The Flutter app
carries `firebase_analytics`; the Vue app carries only Sentry, which is error monitoring,
not product analytics. So the layer is applicable on mobile as a proposal, and not
applicable on web.

That asymmetry is worth stating every time it comes up: any funnel spanning both
platforms is currently unmeasurable on the web half.

## Does this element need an event at all?

Three questions, in order. A `no` at any of them ends it.

1. **Is someone asking a question this would answer?** Not "might we want this later" —
   a question somebody has actually asked. Events added speculatively are never queried
   and never removed.
2. **Is the answer already derivable?** From an existing event, a screen view, or the
   backend. A click that always precedes a request the server already logs adds nothing.
3. **Would the answer change a decision?** If the number goes either way and nothing
   happens differently, the event is decoration.

Record the reason for a `no`. The next person to look at this element should not have to
re-derive it.

## Extend before you create

Before adding an event, check whether an existing one can carry a property instead.

`report_exported` with `format: xlsx | csv` beats `report_exported_xlsx` and
`report_exported_csv`. One event with a dimension stays analysable as formats are added;
two events fragment the same question into two queries and a union.

Create a new event only when the action is genuinely different in kind, not different in
parameter.

## Naming

With no plan in place, propose against these rules and mark the proposal as such:

| Rule | |
|---|---|
| `object_action`, past tense | `shift_started`, `report_exported` |
| snake_case, lowercase | Firebase requires it |
| the object comes from `lexicon.md` | `associate_`, never `employee_` or `user_` where the lexicon says Associate |
| no screen names in the event | screens get renamed; the action does not |
| ≤ 40 characters | Firebase limit |

The lexicon rule matters most. An event named `employee_shift_started` fossilises a
forbidden synonym into the analytics warehouse, where it outlives every UI rename.

## Properties

Enough to answer the question the event exists for, and nothing beyond.

| Include | Exclude |
|---|---|
| the dimensions the question slices by | anything identifying a person beyond the id already in scope |
| the outcome, when the action can fail | free-text the user typed |
| the entity id the action targeted | values already attached at user or session level |

Firebase caps parameters at 25 per event, names at 40 characters. Names, not just values,
are part of the schema — renaming one later splits the history.

## Never log

Personal data beyond the identifier already carried by the session: names, phone numbers,
addresses, document contents, location coordinates. In a product recording where and when
people work, this is not a formality — the analytics warehouse has a different access
model from the application database, and data crossing that line has left its original
consent context.

Flag anything doubtful for `feature-handoff`, which checks PII systematically.
