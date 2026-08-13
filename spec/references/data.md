# Data and API design

> **Examples below are shapes, not facts about your codebase.** Field names, counts and
> paths are illustrative. Measure before you quote any of them.

Read in `data` mode. The schema outlives every screen built on it, so a wrong shape here
is the most expensive wrong shape in the project.

## Three shapes, and they use different halves of this file

`data` is not one job. Say which shape you are in — the pipelines route by this name, and
running the wrong one produces either a migration nobody asked for or a screen promising
values the query cannot deliver.

| Shape | The request is | Sections that apply | Sections that do not |
|---|---|---|---|
| **`read`** | a report, a list, a screen over columns that already exist | schema, API contract, access, indexes | table?, migrations, retention |
| **`write`** | a settings screen, an editor, a form over columns that already exist | API contract, **validation**, access, frozen | table?, migrations |
| **`schema`** | something is stored that is not stored now | all of them |

**`write` is the shape that gets mistaken for `read`.** Nothing new is stored, so it looks
like nothing needs designing. Three things do, and none of them exists yet just because
the column does:

| | Why it is not already answered |
|---|---|
| **Who may write it** | reading a field and changing it are different permissions, and the write audience is almost always narrower |
| **What values are allowed** | a column that nothing wrote had no validator; the bounds are a product decision, not a database constraint |
| **What happens to what was already computed under the old value** | see `## Frozen` — and where the field feeds money, hours or compliance, this is a blocker, not a note |

Where the third has no answer, route the design of it to `improve` — an effective date or a
snapshot is a design task, not a field on a form.

## Read the existing schema first — always

```bash
find . -name models.py -not -path "*/migrations/*" | head -20
git log --oneline --since='6 months ago' --name-only -- ':(glob)**/migrations/**' \
  | grep -ci '<table>'
```

**The pathspec matters.** `'*/migrations/'` quoted returns nothing — git does not expand
the single star across directory levels, and it fails silently rather than erroring.
Measured on one repository: `'*/migrations/'` gave 0 while `'**/migrations/**'` gave 1256,
with 1555 migration files on disk. A recipe that returns zero reads exactly like a clean
schema.

**Ask per table, not per repository.** A mature project has thousands of migrations; the
repo-wide count says nothing. What decides the design is which *table* is moving:

```
associate   51 migration files in 6 months   ← contested, a proposal here will collide
shift       34
payroll     13
document     8                               ← stable, safe to extend
```

Three things to establish before proposing anything:

| Question | Why it decides the design |
|---|---|
| Does this entity already exist under another name? | half the "new table" requests are a column on an existing one |
| Is this table stable or contested? | recency per table, not per repo — a contested table means coordinate first |
| What already reads it? | every reader constrains what you may change |

A proposal written without reading the schema is a guess wearing a diagram.

## The first question is always: does this need a table?

| Signal | Answer |
|---|---|
| The thing has its own lifecycle, is queried on its own, or is referenced by others | a table |
| It only ever exists as an attribute of one row | a column |
| It is a fixed, small, rarely-changing set | an enum or choices, not a lookup table |
| It is derived from other columns and never edited | a computed property, not a column |

**Derived-but-stored is the defect that hides longest.** A stored column recomputed from
others drifts the first time someone updates one side, and nothing complains. Store it
only when there is a reason it must be frozen — an audit record, a payroll snapshot, a
price at time of purchase — and then say in the design that it is deliberately frozen.

Find the candidates, then read each one — the grep proposes, it does not decide:

```bash
grep -rnE "^\s+(total|duration|count|amount|sum|subtotal)(_\w+)? = models\." \
  --include=models.py .
```

**Anchor the alternation with `(_\w+)?`, not `_?\w*`.** The loose form matches any word
*starting* with one of the stems — `country` matches on `count` — and sends the reader
chasing a field that has nothing to do with the question. Measured on one repository: 19
hits loose, 18 anchored, and the extra one was a country code.

## Derived values that are recomputed on every access

The mirror image of the same question. Count them:

```bash
grep -rc '@property'        --include=models.py . | awk -F: '{s+=$2} END {print s+0}'
grep -rc '@cached_property' --include=models.py . | awk -F: '{s+=$2} END {print s+0}'
```

A large `@property` count with a zero `@cached_property` count means every derived value
is recomputed on each access. Read alone that is fine; read in a loop over a list it is
the same shape as an N+1, and it will not show up in any query log because it is not a
query.

Measured on one repository: 46 against 0. Flag it in the design when the new feature
reads such a property in a list, and hand the measurement to `craft`.

## Naming

Field and table names come from `.dev-agent/lexicon.md`. A column named with a `forbidden`
synonym fossilises it in a place nobody renames: migrations, historical records, reports,
and every integration that reads the database directly.

Renaming a column is not a rename. It is a migration, a deploy window, and every consumer
you did not know about.

## What must never be renamed

Anything referenced by records that must stay reproducible — payroll snapshots, signed
documents, audit trails, financial history. If recomputing an old record must give the
same answer it gave then, the columns it read are frozen regardless of how badly they are
named. Say this explicitly in the design rather than discovering it in review.

## Migrations

Every migration answers four questions:

| Question | If unanswered |
|---|---|
| Is it reversible? | a bad deploy has no way back |
| What happens to existing rows? | a `NOT NULL` column on a populated table fails at deploy |
| How long does it lock? | a table rewrite on a large table is an outage |
| Does old code still run against the new schema? | the deploy window breaks, because both versions run at once |

The fourth is the one teams skip. During any rolling deploy, old and new code run at the
same time. That makes the safe shape **additive first**: add the column nullable, backfill,
switch readers, then make it required in a later migration. Three deploys instead of one,
and no outage.

## API contracts

| Change | Safe? | Why |
|---|---|---|
| Add an optional response field | yes | old clients ignore it |
| Add a required request field | **no** | old clients do not send it |
| Remove or rename a response field | **no** | old clients read it |
| Narrow a type or an enum | **no** | old clients send the old values |
| Add a new endpoint | yes | nothing depends on it |

**Mobile makes this sharper than web.** A web client updates on reload; a mobile release
stays in the wild for weeks and cannot be forced. A breaking change needs a version, a
compatibility window, or a forced-update floor — and the floor is a product decision, not
a technical one.

### When none of the three exists

Check before advising, because the common answer in an internal product is *none*:

```bash
grep -rhoE 'api/v[0-9]+' --include='*.py' . | sort -u        # versioned paths
grep -rniE 'min_app_version|minimum_version' --include='*.py' .   # a floor
```

Measured on one repository: zero versioned paths, no floor. Telling that team to "add a
version" is a quarter of work they did not ask for, attached to a two-day feature.

What to recommend instead, in this order:

| Option | Cost | When it fits |
|---|---|---|
| **Make the change additive** — new field beside the old, both served | one release of duplication | almost always; this is the answer unless the old shape is actively harmful |
| **New endpoint beside the old** | two code paths until the old one is dead | the shape changes too much to add to |
| **Introduce versioning for this endpoint only** | a routing change | the endpoint will keep changing |
| **Version the whole API** | a project | never as part of a feature; propose separately |

Additive wins because it needs no coordination: old clients keep reading the old field,
new clients read the new one, and the old field is removed in a later release once
telemetry shows nobody reads it. Say when that removal becomes possible, and on what
evidence — otherwise the duplication is permanent.

## Access and scoping

Before the shape, answer who may see which rows. Scoping is usually a foreign key, and
choosing the wrong one is a data leak, not a bug:

- scoped to the user who created it
- scoped to an organisational unit — company, project, team
- scoped by an explicit permission record
- visible to everyone

Say which, and say what happens to rows whose scope changes after the fact.

## Indexes

Propose an index only against a query you can name. An index on a column nobody filters by
costs write throughput and buys nothing.

The two that pay off almost always: the foreign key that every list filters by, and the
timestamp every report ranges over. The one that surprises: a composite index whose column
order does not match the query's — it will not be used, and it will look like it should be.

## Retention and deletion

Answer both, for every new field:

| Question | Consequence of skipping it |
|---|---|
| What happens when the account is deleted? | the field outlives the account silently |
| Does it belong in the data export? | a field missing from export is as much a defect as one wrongly included |

Local device storage counts. Cached data on a phone after logout is still retained data.

## The design document

```markdown
# Data design: <name>

## What already exists
<tables read, with paths; what is stable, what is moving>

## Proposal
<tables and columns, with the reason for each; what is a column rather than a table>

## Migration
<steps, reversibility, behaviour on existing rows, deploy-window safety>

## API
<endpoints, request and response shapes, what breaks for old clients>

## Access
<who sees which rows, and the key that scopes them>

## Indexes
<each one against a named query>

## Frozen
<what may never be renamed, and which records depend on it>

## Open questions
<one per line, each naming who decides>
```
