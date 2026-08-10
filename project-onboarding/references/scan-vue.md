# Scanning a Vue repository

Read before phase 2. This product's web app is Vue 3 + ant-design-vue; the recipe
generalises to any Vue project.

## Finding the app first

A Vue app is not always where it looks. Check for `package.json` anywhere below the repo
root, excluding `node_modules`:

```bash
find . -maxdepth 3 -name package.json -not -path "*/node_modules/*"
```

A `web/` directory can be a **compiled build** rather than source — `flutter.js`,
`canvaskit`, or a `dist`-shaped tree means it is output, not an app to review. Recording
this distinction prevents the agent reviewing generated files for the rest of its life.

## `package.json` — the stack

| Look for | Fills | How to read it |
|---|---|---|
| `vue`, `vue-router`, `pinia` / `vuex` | platform, state approach | major version of `vue` decides Options vs Composition conventions |
| `vue-i18n` | where strings live | **absent means strings are inline in templates** — a finding, not a detail |
| `ant-design-vue`, `element-plus`, `vuetify`, `primevue` | design system | an external kit means the components are the kit's, and only wrappers are local |
| `@sentry/vue` | error monitoring, **not** product analytics | record the difference explicitly |
| analytics packages | analytics SDK | their absence beside a mobile app that has one is an asymmetry worth reporting |
| `storybook` | design system maturity | present → a real system; absent → probably a component folder |

## `src/` structure

| Look for | Fills |
|---|---|
| `src/views/*.vue` | the screens, and the navigation vocabulary |
| `src/components/*.vue` | the local component set |
| `src/components/entities/` and similar grouping | which concepts the team treats as first-class |
| `src/router/` | routes and guards — needed for the permission question |
| `src/api/` or axios service modules | the code-side vocabulary for entities |

## State modelling

There is rarely a declared convention. Read two or three views and record what is actually
done:

```bash
grep -l "loading" src/views/*.vue | head -3
```

Boolean flags in `data()` are the common case. Record it as flags rather than as a state
machine — `screen-blueprint` needs to know which it is writing for.

## Where strings live when there is no i18n

Inline in templates, plus these attributes, which an audit that reads only tag content
will miss:

- `placeholder`, `title`, `alt`
- kit props: `okText`, `cancelText`, `description`, `message`, `emptyText`
- validation rule `message` fields

Count them and record the number. It is the size of the localisation debt if the web app
is ever translated.

## Cross-platform asymmetries — record every one

A monorepo with two front-ends almost always has them, and each one matters to a different
skill:

| Asymmetry | Who needs to know |
|---|---|
| Mobile localised, web not | `interface-copy`, `screen-review` |
| Mobile has product analytics, web only error monitoring | `element-markup`, `feature-handoff` |
| Mobile has a dark theme, web does not | `screen-review` |
| Different design systems on the two platforms | `screen-blueprint` |

These belong in `config.yaml` per platform, never averaged into one project-level answer.
