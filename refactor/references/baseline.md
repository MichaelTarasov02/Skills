# Baseline

> **Examples below are shapes, not facts about your codebase.** Measure before you quote
> any of them.

Read before phase 2. The phase everything else rests on.

**No baseline, no refactor.** Without a way to tell whether behaviour changed, the work is
rewriting and hoping — and the pull request will say "no functional changes" either way.

## Two snapshots, both needed

| Snapshot | Captures | Used to prove |
|---|---|---|
| **Behaviour** | what the code does, for a set of inputs | nothing changed |
| **Metric** | how long, how many queries, how much memory | something improved |

In `clean` mode the metric is still worth taking — a tidy-up that accidentally triples the
query count is a common and invisible outcome.

## Capturing behaviour, in order of strength

| Method | Strength | When it applies |
|---|---|---|
| Existing tests that cover the block | strongest — run them, record the result | a suite exists |
| **Characterisation tests written now** | strong — and they outlive the refactor | no coverage, behaviour is pinnable |
| Recorded input → output pairs | medium — a table of what it returns today | pure-ish functions |
| A written description of every branch | weak — but better than nothing | side-effect-heavy code |
| Nothing | **stop** | — |

**Characterisation tests are the tool this phase exists to recommend.** They are not tests
of what the code *should* do — they are tests of what it *does*, written without judgement,
including the parts that look wrong. Their only job is to fail if behaviour moves.

Where the current behaviour is visibly wrong, capture it anyway and note it. Fixing it here
mixes a behaviour change into a refactor; the note becomes a separate ticket.

## Capture the behaviour nobody counts as behaviour

The happy path is the easy part. Pin these too:

```
входы:      обычный, пустой, ноль, один, много, отсутствующий, некорректный
выходы:     значение, null или пустое — какое именно
ошибки:     какой тип, какое сообщение, при каком входе
порядок:    в каком порядке приходит список, даже если никто не сортировал
побочные:   что пишется, что отправляется, что логируется — и сколько раз
количество: сколько запросов, сколько вызовов наружу
```

The last two lines are where refactors break things quietly. A side effect that fired once
per call and now fires once per row is a behaviour change no test asserts and no reviewer
sees.

## Structural refactors need a different baseline entirely

Everything above pins **what the code returns**. A structural refactor — splitting a file,
moving a class, renaming a module, extracting a package — usually does not change that at
all, and passes every characterisation test while breaking the system.

**What it changes is identity**, and identity is referenced from places that never import
the code:

| Identity | Referenced from | What breaks silently |
|---|---|---|
| Module path | migrations, serialised task payloads, dynamic imports, config strings | an old record deserialises into nothing |
| Registry or app label | ORM table names, permissions, content types | the table a model maps to |
| Class name | pickled data, stored type discriminators, API `type` fields | historical rows stop loading |
| Route or view name | reverse lookups, deep links, redirects | a URL that used to resolve |
| Translation key | string catalogues, in every locale | text falls back to the key |
| Test id, accessible name | end-to-end tests | a suite that goes red for no reason |

Measured on one repository: 1487 migration files, 16 of them naming a model by its full
module path, and **not one explicit table name** — every table derived from the app label.
Moving a model between apps there renames its table. No characterisation test can see it.

**The baseline for a structural change is an inventory, not a snapshot:**

```bash
# who names this thing as a string, rather than importing it
grep -rn "<module.path>\|'<ClassName>'\|\"<ClassName>\"" <every root> | grep -v "^<the file>"
# framework-level identity the framework derives rather than you declaring it
grep -c "db_table\|app_label\|table_name" <models file>
```

Then, before and after, run the **framework's own consistency check** and diff the output:

| Stack | Check |
|---|---|
| Django | `manage.py check` and `makemigrations --dry-run` — **any** proposed migration after a pure move is a rename you did not intend |
| Any ORM | the migration generator, in dry-run |
| TypeScript | `tsc --noEmit` before and after |
| Any | the full import graph — a module that only fails on first import fails in production, not in tests |

**A structural refactor is verified by identity, not by behaviour.** Where the identity
inventory cannot be produced — dynamic imports built from strings, reflection, config
naming classes — say so at the gate. That is the case where the honest answer is to narrow
the scope to something whose references can be enumerated.

## Capturing the metric

Measure the thing the task complains about, with data of realistic size:

```
что мерим:   <the endpoint, the call, the render>
данные:      <realistic size — not the dev fixture>
метод:       <query count, wall time, profiler — name it>
результат:   <numbers, at least three runs>
разброс:     <min–max — an improvement inside the spread is not an improvement>
```

**The spread is the field that gets skipped and decides everything.** A call taking
180–240ms that becomes 200ms has not improved; without the range nobody can tell.

Where the task brought analytics — how slow it is for users, how often it is hit — record
that as the target. An optimisation with no target succeeds by definition.

## Where the baseline lives

`.dev-agent/refactors/<slug>/baseline.md`, committed with the work. Phase 6 compares
against it, and a reviewer can check the comparison without rerunning anything.

## The gate

```
Вид:        поведенческий | структурный | оба
Поведение:  <how it is pinned — tests, characterisation tests, recorded pairs>
Идентичность: <for a structural change: who names this by string, and the
               framework check whose output is recorded — or "не применимо">
Не закреплено: <what could not be pinned, and what that risks>
Метрика:    <numbers and spread — or "не мерили, потому что <…>">
Цель:       <what improvement would count>

Базы достаточно, чтобы менять код безопасно? Или сначала пишем тесты?
```

**`Вид` is the first line because it decides which of the two baselines above applies.**
A structural change baselined only on behaviour passes its gate and breaks the system;
that is the specific failure this line exists to prevent.

`Не закреплено` non-empty is common and is not a blocker by itself — it is a risk the
engineer accepts or removes. Empty on a complex block usually means the capture was
shallow.
