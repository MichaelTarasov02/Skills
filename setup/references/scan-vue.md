# Scanning a Vue repository

> **Examples below are shapes, not facts about your codebase.** Field names, counts and
> paths are illustrative. Measure before you quote any of them.

The recipe generalises to any Vue project; the same questions apply to React with
different filenames.

## Find the app first

A front-end is not always where it looks:

```bash
find . -maxdepth 3 -name package.json -not -path "*/node_modules/*"
```

A `web/` or `dist/` directory can be a **compiled build** rather than source — a bundler
runtime file, a `canvaskit` folder, hashed asset names. Recording this distinction stops
the agent reviewing generated files forever after.

## Pin the version before anything else

**This step is load-bearing.** Vue 2 and Vue 3 differ in template syntax, and the
component kits differ with them. Advice written for the wrong major produces code that
does not compile — and it looks plausible enough to be pasted.

```bash
grep -E '"(vue|vue-router|vuex|pinia)"' package.json
grep -rl 'setup(' src | wc -l      # Composition API
grep -rl 'data()'  src | wc -l     # Options API
grep -ro 'v-model:[a-z]' src | wc -l   # Vue 3 only: v-model with an argument
```

The dependency answers which major. The greps answer which style is **actually written**,
which is the one to follow — a project can be on Vue 3 and hold every component in
Options API.

Measured on one repository: `vue ^2.6.14`, kit at `1.7.8`, 342 files with `data()`, zero
with `setup()`, zero `v-model:arg`, and 146 uses of the kit's Vue-2 modal prop. Anything
written in Vue 3 syntax for that codebase is wrong in every file.

Record the major, the kit's major, and the dominant API style in `config.yaml`. Every
skill that emits markup reads them.

## `package.json` — the rest of the stack

| Look for | Fills | How to read it |
|---|---|---|
| router and store packages | state approach | their majors track the framework major — a mismatch means a partial migration |
| an i18n package | where strings live | **absent means strings are inline in templates** — a finding, not a detail |
| a component kit | design system | an external kit means the components are the kit's, and only wrappers are local |
| error monitoring | **not** product analytics | record the difference explicitly |
| product analytics | analytics SDK | its absence beside a mobile app that has one is an asymmetry worth reporting |
| `storybook` | design-system maturity | present → a real system; absent → probably a component folder |

## `src/` structure

| Look for | Fills |
|---|---|
| `src/views/*.vue` | the screens, and the navigation vocabulary |
| `src/components/*.vue` | the local component set |
| grouping such as `components/entities/` | which concepts the team treats as first-class |
| `src/router/` | routes and guards — needed for the permission question |
| `src/api/` or service modules | the code-side vocabulary for entities |

## State modelling

There is rarely a declared convention. Read two or three views and record what is done:

```bash
grep -l "loading" src/views/*.vue | head -3
```

Boolean flags in `data()` are the common case. Record it as flags rather than as a state
machine — `spec` needs to know which it is designing for.

**The flag trap:** two booleans give four combinations, three meaningless and one
unreachable. `!loading && !error && items.length === 0` — is that empty, or never
loaded? The code cannot say; the spec must.

## Where strings live when there is no i18n

Inline in templates, plus attributes, which an audit reading only tag content misses.
Three groups, and they are not equally present in every project:

| Group | What to grep |
|---|---|
| Plain HTML attributes | `placeholder`, `title`, `alt` — usually the largest group by far |
| The kit's own text surface | **find out how this kit's version exposes text before grepping for it** |
| Validation rule messages | inside form rule objects, invisible to any template scan |

**Count literals and bindings separately.** `placeholder="Enter name"` is debt.
`:placeholder="labelFromStore"` is not — its text lives elsewhere or is already dynamic.
A grep that does not split them inflates the figure:

```bash
grep -roE '[^:v-]placeholder="[^"{]' src | wc -l    # literal — this is the debt
grep -roE '(:|v-bind:)placeholder=' src | wc -l     # bound — not debt
```

Measured on one repository the split was 553 literal against 25 bound for one attribute,
228 against 50 for another. Reporting the sum would overstate the work by the bound share
and point the team at strings that need nothing.

The literal count is the localisation debt if the app is ever translated.

## Component-kit defaults are unanswered decisions

Kits ship English defaults — `No Data` for empty tables, `OK` and `Cancel` in modals.
These are user-visible strings nobody wrote. A screen using them without overrides has not
answered its empty state, it has inherited one.

**Grep the surface this kit version actually uses, not the one you expect.** A kit can
expose the same text through a direct prop in one major and through a config object in
another. Getting this wrong produces a confident zero.

That happened here: an earlier pass grepped `emptyText=` as a prop, found nothing, and
concluded the team never overrides kit text. The real form was
`:locale="{ emptyText: '...' }"` — a config object — with 28 uses.

The number worth reporting is the **ratio**, not the count:

```bash
grep -rl 'a-table'   src | wc -l    # screens using the component
grep -rl 'emptyText' src | wc -l    # screens that answered its empty state
```

Measured on one repository: 70 against 27. The other 43 show the kit's default. That is
not "the team does not know how" — 27 files prove they do — it is 43 screens where the
decision was skipped, and that is a finding `review` can act on.

## Cross-platform asymmetries — record every one

A monorepo with two front-ends almost always has them, and each matters to a different
skill:

| Asymmetry | Who needs to know |
|---|---|
| One platform localised, the other not | `copy`, `review` |
| One has product analytics, the other only error monitoring | `craft`, `review` |
| One has a dark theme, the other does not | `review` |
| Different design systems | `spec` |

These belong in `config.yaml` per platform, never averaged into one project-level answer.
