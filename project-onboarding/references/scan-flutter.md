# Scanning a Flutter repository

Read before phase 2. An executable recipe: file → what to look for → how to read it.

## `pubspec.yaml` — the stack in one file

| Look for | Fills | How to read it |
|---|---|---|
| `flutter_localizations`, `intl` | strings, i18n | present → localised; absent → literals in code |
| `flutter_bloc`, `provider`, `riverpod`, `get_it` | state approach | the one with the most usages wins; several present means several conventions coexist |
| `firebase_analytics`, `amplitude`, `mixpanel`, `posthog` | analytics SDK | this is the SDK; whether a plan exists is a separate check |
| `sentry_flutter`, `firebase_crashlytics` | error monitoring — **not** product analytics | recording this distinction prevents `element-markup` proposing events into a crash reporter |
| `flutter_secure_storage`, `shared_preferences` | what persists on device | matters for the deletion question in `feature-handoff` |

Read the comments beside dependencies — teams often note which platform each is for.

## `l10n.yaml` and `lib/l10n/`

| Look for | Fills |
|---|---|
| `lib/l10n/*.arb` | where strings live; the locale set |
| `@@locale` in each file | locale codes — needed by `outbound-writing`, whose store tags differ |
| count of keys in the source ARB | the cost multiplier of any string change |
| `@key` siblings with `description` | whether translator context is a habit or an exception |

An empty or missing `l10n.yaml` with ARB files present means generation is configured
elsewhere — check `pubspec.yaml` under `flutter: generate:`.

## `lib/` structure

| Look for | Fills |
|---|---|
| `lib/features/*/` | the domain vocabulary — directory names are the strongest signal of what the product is about |
| `lib/theme/`, `app_colors.dart`, theme extensions | design system: a theme layer means one exists |
| `ThemeType` / `ThemeMode` / `darkTheme` | whether dark theme exists — a yes/no `screen-review` needs |
| `lib/common/`, shared widget directories | the reusable component set |
| cubit / bloc / notifier files inside a feature | how states are actually modelled, versus what `pubspec.yaml` allows |

Open one feature's state file rather than trusting the dependency list. A project can
depend on `flutter_bloc` and still hold half its screens on boolean flags.

## What Flutter cannot tell you

Record these as not determinable from code, so they become questions rather than silent
gaps:

- who the users are, beyond what feature names imply
- which regulation the product falls under
- what may never be promised
- whether the product is B2B or B2C

## Reading the domain from strings

Where a README says little — and most do — the source ARB file is the richest description
of the product available. Word frequency across string values gives the domain vocabulary
in one pass, and it is evidence rather than inference.

```python
import json, re, collections
d = json.load(open('lib/l10n/intl_en.arb'))
words = collections.Counter()
for k, v in d.items():
    if not k.startswith('@') and isinstance(v, str):
        for w in re.findall(r"\b[A-Za-z][a-z]{3,}\b", v):
            words[w.lower()] += 1
print(words.most_common(40))
```

Filter stop words, and the top of the list is what the product is about.
