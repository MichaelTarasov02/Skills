# Scanning a Flutter repository

> **Examples below are shapes, not facts about your codebase.** Field names, counts and
> paths are illustrative. Measure before you quote any of them.

One pass answers both questions: what the stack is, and what the product's vocabulary is.

## `pubspec.yaml` — the stack in one file

| Look for | Fills | How to read it |
|---|---|---|
| `flutter_localizations`, `intl` | strings, i18n | present → localised; absent → literals in code |
| `flutter_bloc`, `provider`, `riverpod`, `get_it` | state approach | the one with most usages wins; several present means several conventions coexist |
| product analytics packages | analytics SDK | this is the SDK; whether a plan exists is a separate check |
| crash reporters | error monitoring — **not** product analytics | recording the difference stops `craft` proposing events into a crash reporter |
| secure storage, shared preferences | what persists on device | matters for the deletion question in `review` |

Read the comments beside dependencies — teams often note which platform each is for.

## `l10n.yaml` and `lib/l10n/`

| Look for | Fills |
|---|---|
| `lib/l10n/*.arb` | where strings live; the locale set |
| `@@locale` in each file | locale codes — store tags differ from these, `copy` needs both |
| key count in the source ARB | the cost multiplier of any string change |
| `@key` siblings with `description` | whether translator context is a habit or an exception |

Empty or missing `l10n.yaml` with ARB files present means generation is configured
elsewhere — check `pubspec.yaml` under `flutter: generate:`.

## Key–value drift lives here and nowhere else

The identifier is written by developers, the value by whoever last edited the copy. They
diverge silently because nothing checks them. Compare the words inside each key against
the words inside its value:

```python
[k for k, v in arb.items() if 'x' in k.lower() and 'y' in v.lower()]
```

## `lib/` structure

| Look for | Fills |
|---|---|
| `lib/features/*/` | the domain vocabulary — directory names are the strongest signal of what the product is about |
| `lib/theme/`, colour files, theme extensions | design system: a theme layer means one exists |
| `ThemeType` / `ThemeMode` / `darkTheme` | whether dark theme exists — a yes/no `review` needs |
| `lib/common/`, shared widget directories | the reusable component set |
| cubit / bloc / notifier files inside a feature | how states are **actually** modelled, versus what `pubspec.yaml` allows |

Open one feature's state file rather than trusting the dependency list. A project can
depend on `flutter_bloc` and still hold half its screens on boolean flags.

## Entities

Model classes, API clients, generated serialisation. Field names here are the code-side
vocabulary; compare them against the ARB values to find synonym sets across layers.

## Reading the domain from strings

Where a README says little — and most do — the source ARB file is the richest description
of the product available. Word frequency across string values gives the domain vocabulary
in one pass, and it is evidence rather than inference.

```python
import json, re, collections
d = json.load(open('lib/l10n/intl_en.arb'))
STOP = set("this that with your have will from please there when been they into more than "
           "then only some such were which about other after before their would could "
           "should cannot again also make need want does done here over same used using "
           "while being because without between the and for you are not can all any has "
           "was its our may but".split())
VERBS = set("select start create take complete required scheduled enter open close save "
            "send confirm cancel continue submit choose view edit delete update".split())

raw = collections.Counter()
for k, v in d.items():
    if not k.startswith('@') and isinstance(v, str):
        for w in re.findall(r"\b[A-Za-z][a-z]{3,}\b", v):
            lw = w.lower()
            if lw not in STOP:
                raw[lw] += 1

merged = collections.Counter()                       # collapse simple plurals
for w, c in raw.items():
    base = w[:-1] if w.endswith('s') and not w.endswith('ss') and w[:-1] in raw else w
    merged[base] += c

print([(w, c) for w, c in merged.most_common(30) if w not in VERBS][:15])
```

**Both filters are load-bearing, and skipping either changes the ranking.**

*Plurals split the count.* Without the merge, a term appearing as both singular and plural
is counted twice and ranks below terms that are not. Measured on one repository: the
dominant entity sat at 258 uncollapsed and 351 collapsed, which moved it from third place
to second — a wrong answer to "what is this product about".

*Interface verbs outrank domain nouns.* `select`, `create`, `start` are frequent in any
product and describe none. Filter them, and extend `VERBS` with whatever else surfaces
that is an action rather than a thing.

The top of the filtered list is what the product is about. Terms below a handful of
occurrences are noise, not vocabulary.

## Locale cost

Every string change multiplies by the number of ARB files. Report that number — it turns
"rename this label" from a trivial edit into a decision with a price.

## What Flutter cannot tell you

Record as not determinable from code, so it becomes a question rather than a silent gap:
who the users are beyond what feature names imply, which regulation applies, what may
never be promised, whether the product is B2B or B2C.
