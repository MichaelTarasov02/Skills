# Performance

> **Examples below are shapes, not facts about your codebase.** Counts and paths are
> illustrative. Measure before you quote any of them.

Read in `perf` mode. Every recommendation here is preceded by the measurement that earns
it. An optimisation without a before-and-after is a refactor with a story attached.

## The order is fixed

1. **Reproduce** — with data of realistic size. A list is fast at ten rows and every
   product is fast in development.
2. **Measure** — get a number: queries, milliseconds, bytes, rebuilds.
3. **Locate** — find what dominates that number, not what you recognise.
4. **Fix** — the dominant cost only.
5. **Measure again** — same method, same data. Without this you do not know it worked.

The most common outcome of an unmeasured optimisation is code that reads worse and runs
the same.

## Backend — where the time usually is

### N+1 is the default failure

One query for the list, one more per row. Invisible at ten rows, fatal at a thousand, and
it does not look like a loop over queries — it looks like a loop over objects.

```python
# every access to a related object is a query
for shift in shifts:
    print(shift.associate.name)          # N queries

# one join, or one extra query
shifts = Shift.objects.select_related('associate')      # FK, one join
shifts = Shift.objects.prefetch_related('documents')    # reverse/M2M, one extra query
```

### Where to look, in yield order

Grep is a lead, a query count is proof. But grep first, because it tells you *where* to
count. Measured on one repository:

```
SerializerMethodField          458   ← the dominant shape; each one runs per row
for x in ....all()             360   ← a loop that may or may not touch relations
select_related                 143   ┐ the team knows the technique —
prefetch_related                91   ┘ the question is coverage, not knowledge
```

**A serializer method field is the highest-yield place to look**, and the easiest to miss,
because it reads as a computed value rather than as a query. One that touches a related
object runs once per row of the response, and nothing in the view suggests it.

The ratio is the finding, not the count: roughly two method fields for every optimisation
call means most of them are either free or unprotected, and only counting queries tells
you which.

Do not report "458 potential N+1s" — that is a grep pretending to be an analysis. Report
the endpoint you measured, the query count it produced, and which method field accounted
for it.

Confirm by counting queries: 

```python
from django.test.utils import CaptureQueriesContext
from django.db import connection
with CaptureQueriesContext(connection) as ctx:
    build_the_response()
print(len(ctx))
```

### Derived properties are the invisible N+1

A property recomputed on every access costs nothing in isolation and everything in a loop
— and it never appears in a query log, because it is not a query. Where a model exposes
many properties and caches none, any list rendering them pays the full cost per row.

Count them before assuming the queries are the problem:

```bash
grep -rc '@property'        --include='models.py' . | awk -F: '{s+=$2} END {print s+0}'
grep -rc '@cached_property' --include='models.py' . | awk -F: '{s+=$2} END {print s+0}'
```

### Missing indexes

Propose an index only against a query you can name. The two that pay off almost always:
the foreign key every list filters by, and the timestamp every report ranges over. The one
that surprises: a composite index whose column order does not match the query's — it will
not be used, and it will look like it should be.

An index on a column nobody filters by costs write throughput and buys nothing.

### Pagination

A list endpoint with no limit is a time bomb that goes off when the biggest customer
arrives. Ask what the largest realistic result set is; if nobody knows, that is the
finding.

## Frontend — where the jank usually is

### Rendering the whole list

A table rendering every row is fine at fifty and unusable at ten thousand. Before reaching
for virtualisation, ask whether the screen should be paginating instead — virtualising a
list nobody should be scrolling is solving the wrong problem.

**Narrow before reporting.** The raw count of eager containers is alarming and almost
entirely wrong: most of them hold a fixed number of children, where eager is correct.

```bash
# web: tables that opted out of pagination
grep -ro ':pagination="false"' src | wc -l

# mobile: eager scroll containers, then the ones that actually build a variable list
grep -rl 'SingleChildScrollView' --include='*.dart' lib | wc -l
for f in $(grep -rl 'SingleChildScrollView' --include='*.dart' lib); do
  grep -q 'Column(' "$f" && grep -qE '\.map\(|\bfor \(' "$f" && echo "$f"
done | wc -l
```

Measured on one repository:

```
web:    70 tables, 63 paginate, 8 opted out          ← 8 is the risk set
mobile: 151 scroll views → 134 with a column → 11 building a variable list
```

Eleven files, not a hundred and fifty. The other 123 are forms and detail screens with a
known number of children — eager is the right choice there, and proposing lazy builders
for them adds indirection and buys nothing.

Report the narrowed number and the narrowing steps. A reader who sees 151 stops reading;
a reader who sees 11 opens them.

### Rebuilds and re-renders

Both frameworks re-render more than authors expect. The measurement comes first: a
profiler or a rebuild counter, not a guess about which component is expensive.

Memoising without measuring is the classic waste — it adds a dependency array to maintain
and usually saves nothing.

### Images

Frequently the largest single win and the least interesting to find. Check the bytes
actually shipped against the pixels actually displayed. A photo scaled down in CSS is
downloaded at full size.

### Bundle

Measure before splitting. One heavy dependency usually dominates, and finding it is a
report, not a refactor.

## Mobile — what web does not have

| Concern | Why it differs |
|---|---|
| Main-thread work | jank is visible at 16ms, not at 100ms |
| Image decode | large images decode on the main thread and drop frames |
| Startup | cold start is measured by users, not by profilers |
| Battery and network | a polling loop is a performance problem the profiler will not show |
| List builders | building all children eagerly defeats laziness — check the builder actually is lazy |

## One number is not a measurement

**Three runs minimum, and report the range.** A single timing cannot be compared with
another single timing: a call that varies between 180 and 240 ms and now reads 200 ms has
not improved, and no one reading two bare numbers can tell.

| Metric | Runs | Report |
|---|---|---|
| Wall time | ≥3 | min–max, and the median |
| Query or call count | 1 | it is deterministic; a varying count is itself the finding |
| Memory, frame time | ≥3 | min–max |

**An improvement inside the spread is not an improvement.** Say so plainly when that is
what the numbers show — it is a useful result, and reporting it as a win is how an
unnecessary change becomes permanent.

Where the fix changes a count rather than a time, the count is the stronger evidence:
47 queries to 3 needs no statistics.

## What to report

```
Measurement:  <min–max over N runs, method, data size>
Dominates:    <what accounts for most of it>
Fix:          <the change>
After:        <min–max over N runs, same method, same data size>
Verdict:      улучшение | внутри разброса | хуже
Not the cause: <what you checked and ruled out>
```

**`After` is a measurement, not a prediction.** The fixed order ends with *measure again*,
and a template offering only an expected number is how that step disappears. Where the
change cannot be measured in this session — it needs production data, a device, a load
generator — write `After: не измерено, нужно <what>` rather than a guess. An unverified
optimisation stated as verified is worse than an unfixed bottleneck, because nobody looks
again.

**Same method, same data size.** Different conditions produce a number that means nothing,
and it will be quoted as though it did.

The last line matters more than it looks. Without it the next person re-checks everything
you already eliminated.
