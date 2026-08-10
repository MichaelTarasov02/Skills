# Scanning a Flutter repository

Read before phase 1.

## Strings

| Read | Extract |
|---|---|
| `lib/l10n/*.arb` | the whole key–value map. `intl_en.arb` is the source of truth for wording; the other locales reveal how many languages a change costs |
| `@@locale` in each file | the locale set |
| `pubspec.yaml` → `flutter: generate: true`, `l10n.yaml` | confirms `intl` codegen and where generated accessors land |

Key–value drift lives here and nowhere else: the identifier is written by developers, the
value by whoever last edited the copy. They diverge silently because nothing checks them.

Detect it by comparing the words inside the key against the words inside its value:

```python
[k for k, v in arb.items() if 'lunch' in k.lower() and 'meal' in v.lower()]
```

## Components

| Read | Extract |
|---|---|
| `lib/features/*/` | one directory per feature — the strongest signal of domain vocabulary in the repo |
| `lib/common/`, shared widget directories | reusable widgets, the actual design system |
| `ThemeData`, theme extensions | tokens: colours, typography, spacing |

## Entities

Model classes, API clients under `lib/api/` and `lib/data_sources/`, and generated
serialisation code. Field names here are the code-side vocabulary; compare them against
the ARB values to find synonym sets across layers.

## Locale cost

Every string change multiplies by the number of ARB files. Report that number in phase 1
— it turns "rename this label" from a trivial edit into a decision with a price.
