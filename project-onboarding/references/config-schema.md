# config.yaml schema

> **Examples below are shapes, not facts about your codebase.** Field names, counts and
> paths in them are illustrative and were true of one repository at one moment. Measure
> before you quote any of them. A reference file that hands you a number is handing you a
> hypothesis.


Read before phase 5. Eight skills read this file. Its shape is a contract, not a
preference.

## Rules

- Every value carries `source:` — one of `code` / `file` / `user` / `assumption`
- Platform sections are per platform. Never average two platforms into one answer
- A field that could not be determined is present with `null` and a `source: unknown`,
  not omitted. An absent key is indistinguishable from a forgotten one

## Full example — this product

```yaml
version: 1
generated: 2026-07-28

product:
  name: WhereAmI
  what: { value: "Workforce time, location and compliance tracking", source: code }
  users: { value: "Associates who record shifts; Managers who review", source: code }
  type: { value: B2B, source: assumption }
  industry: { value: null, source: unknown }

interface:
  language: { value: en, source: code }
  locales:
    value: [en, es, fr, he, ru, tl, zh]
    source: code
    note: "he is RTL; store tags differ — he→iw-IL, tl→fil"

platforms:
  - id: mobile
    framework: { value: flutter, source: code }
    root: { value: whereami-flutter-2, source: code }
    strings:
      where: { value: lib/l10n/*.arb, source: code }
      library: { value: intl, source: code }
      key_count: { value: 3994, source: code }
      plural: { value: icu, source: code }
    design_system:
      kind: { value: own, source: code }
      evidence: { value: "lib/theme/ + app_colors.dart + theme extensions", source: code }
      dark_theme: { value: true, source: code }
    state_approach:
      value: { primary: cubit, packages: [flutter_bloc, provider, get_it] }
      source: code
    analytics:
      product: { value: firebase_analytics, source: code }
      errors: { value: [sentry, firebase_crashlytics], source: code }
      plan: { value: null, source: code, note: ".telemetry/ absent" }

  - id: web
    framework: { value: vue3, source: code }
    root: { value: whereami-server/whereami, source: code }
    strings:
      where: { value: "inline in <template>", source: code }
      library: { value: null, source: code, note: "vue-i18n absent" }
      plural: { value: null, source: code }
    design_system:
      kind: { value: external_kit, source: code }
      evidence: { value: ant-design-vue, source: code }
      dark_theme: { value: false, source: code }
    state_approach:
      value: { primary: boolean_flags, packages: [vuex] }
      source: code
    analytics:
      product: { value: null, source: code }
      errors: { value: ["@sentry/vue"], source: code }
      plan: { value: null, source: code }

backend:
  framework: { value: django, source: code }
  root: { value: whereami-server, source: code }

red_lines:
  - { rule: "Never state a restoration or fix date", source: assumption }
  - { rule: "Never assert legal compliance on the product's behalf; quote the requirement", source: code }
  - { rule: "Meal break and payroll wording needs legal review", source: code }

asymmetries:
  - { note: "mobile localised (7 locales), web single-language", affects: [interface-copy, screen-review] }
  - { note: "mobile has product analytics, web has none", affects: [element-markup, feature-handoff] }
  - { note: "mobile has dark theme, web does not", affects: [screen-review] }
```

## Grep contract

Every consumer retrieves what it needs without parsing YAML:

```bash
# platforms
grep -A1 "framework:" .dev-agent/config.yaml

# where strings live
grep -A3 "strings:" .dev-agent/config.yaml

# analytics SDK
grep -A2 "analytics:" .dev-agent/config.yaml

# what must never be said
grep -A5 "red_lines:" .dev-agent/config.yaml
```

Consequences for the writer: two-space indentation, no tabs, `value` always on the same
line as its key in inline maps, one blank line between top-level sections.

Phase 5 is not complete until these commands have been run against the produced file and
their output pasted.

## Changing the schema

A new key touches every reader. Add it here first, then update the consumers, then re-run
the greps. Editing the writer alone is how the contract quietly breaks.
