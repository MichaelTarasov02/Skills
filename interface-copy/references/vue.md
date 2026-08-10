# Strings in Vue

Read before phase 3. This project's web app is Vue 3 + ant-design-vue.

## Establish the state first

Check `package.json` for `vue-i18n` before writing anything.

| Found | Then |
|---|---|
| `vue-i18n` present | write keys into the locale files, mirroring their existing structure |
| absent | strings sit inline in `<template>`; write them inline and **say so in the artifact** |

In this repository `vue-i18n` is absent while the Flutter app carries seven locales. That
asymmetry is worth stating every time: the web app is single-language by construction, so
any wording agreed for both platforms exists in translated form on one side only.

Do not introduce an i18n layer as a side effect of writing copy. Report the gap, name what
it costs, and let the team decide — that is a change to the build, not a string edit.

## Where strings appear inline

Beyond text between tags, these attributes carry user-visible words and are missed most
often:

- `placeholder`, `title`, `alt`
- ant-design-vue props: `okText`, `cancelText`, `description`, `message`, `emptyText`
- validation rule `message` fields
- `a-modal` titles, `a-popconfirm` text, `a-empty` description

An audit that only reads tag content misses most of the error and confirmation copy.

## Component-supplied defaults

ant-design-vue ships English defaults — `No Data` for empty tables, `OK` and `Cancel` in
modals. These are user-visible strings nobody wrote, and they violate the style rules:
`OK` is not an outcome verb, and `No Data` is the generic empty state that fails to
distinguish "nothing created" from "filter matched nothing".

Override them explicitly. List every component in the artifact whose default is still in
place, so the choice is visible rather than accidental.

## Plurals

With no i18n layer there is no plural mechanism. Write the count into the string with an
explicit branch in the template rather than concatenating a fragment, and flag every such
string — it is the first thing that breaks if the web app is ever localised.
