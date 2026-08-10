# Scanning a Vue repository

Read before phase 1. This project's web app is **Vue 3 + ant-design-vue**, not React.

## Strings

Vue apps frequently carry no i18n layer at all, in which case strings sit inline in
`<template>` blocks. Establish which case applies before extracting.

| Read | Extract |
|---|---|
| `package.json` dependencies | presence of `vue-i18n` decides everything below |
| `src/locales/*.json` or `src/i18n/` | the key–value map, when i18n exists |
| `src/**/*.vue` `<template>` blocks | literal text between tags, and `placeholder=` / `title=` / `label=` attributes, when it does not |

Inline literals are a finding in themselves: report the count in phase 1. A repository
where the mobile app has full i18n and the web app has none will drift by construction,
because only one side is ever reviewed for wording.

## Components

| Read | Extract |
|---|---|
| `src/components/*.vue` | the local component set — file name is the component name |
| `src/components/entities/`, `src/components/layout/` | grouping reveals which concepts the team treats as first-class |
| `src/views/*.vue` | screens, and therefore the navigation vocabulary |
| `ant-design-vue` imports | which parts of the external kit are actually used — these are components nobody should reimplement |

Report local components and external-kit components separately. `screen-blueprint` needs
to know which of the two it is reusing.

## Entities

API calls under `src/api/` or axios service modules, plus Vuex/Pinia store modules. Store
module names and API field names are the code-side vocabulary for the web half; compare
them against the Flutter side to find cross-platform synonym sets.

## Cross-platform comparison

The highest-value output of this file. The same entity named differently on the two
platforms is invisible to anyone working on one of them. Compare by counting mentions per
term in each codebase and reporting the split:

```bash
grep -ril "associate" src | wc -l
grep -ril "employee" src | wc -l
```

A term that dominates on one platform and is absent on the other is a synonym set, not a
coincidence.
