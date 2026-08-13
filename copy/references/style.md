# Style rules

Read before phase 2. Decided once here so no string re-argues them. English, US.

## Detect the convention before applying one

**The product's existing convention wins over the one below.** A new string in a different
case reads as foreign next to the fifty around it, and inconsistency costs more than
either convention applied consistently.

Measure before writing:

```python
import json
d = json.load(open('lib/l10n/intl_en.arb'))
v = {k: s for k, s in d.items() if not k.startswith('@') and isinstance(s, str)}
btn = {k: s for k, s in v.items()
       if any(t in k.lower() for t in ('button', 'btn')) and len(s.split()) <= 4}
caps = lambda s: sum(w[0].isupper() for w in s.split() if w and w[0].isalpha())
print('Title Case   ', sum(1 for s in btn.values() if caps(s) >= 2))
print('sentence case', sum(1 for s in btn.values() if len(s.split()) > 1 and caps(s) == 1))
```

Measured on one repository: 11 Title Case against 1 sentence case on button keys, and
1599 Title-Case strings overall. Following the table below there would have made every
new string look like a mistake.

**When the existing convention differs from the table:** follow the existing one, say that
you are doing so, and note the deviation once. Changing it is a product decision touching
thousands of strings across every locale — never a side effect of writing one screen.

## Capitalisation — the default when no convention exists

| Element | Case | Example |
|---|---|---|
| Buttons and menu actions | Sentence case | `Start shift`, not `Start Shift` |
| Field labels | Sentence case | `Phone number` |
| Headings and titles | Sentence case | `Meal break authorization` |
| Toasts, errors, hints | Sentence case | `Shift already started` |
| Proper nouns and lexicon terms | as written in `lexicon.md` | `Meal Break` when the lexicon capitalises it |

Title Case on every button is the single most common drift in an interface with no owner.
The existing product has it in places (`Wait until After your Meal Break`) — flag such
strings during an audit.

## Punctuation

| Rule | |
|---|---|
| Full stops | none on buttons, labels, headings, single-sentence toasts. Present in multi-sentence body text |
| Exclamation marks | none. Not in success, not in errors, not in onboarding |
| Ellipsis | the character `…`, never three dots. Only for a truly in-progress state |
| Quotes | curly `“ ”`; straight quotes only inside code samples |
| Dash | em dash `—` unspaced for a break in thought; en dash `–` for ranges |
| Ampersand | never in prose; `and` |
| Colons | on labels only when the layout requires them, and then on all labels or none |

## Numbers and data

| Rule | |
|---|---|
| 0–9 | words in prose, digits in data, counts, and anything a user compares |
| Time | 12-hour with `AM`/`PM` for a US workforce product; never mix formats on one screen |
| Duration | `30 min`, `1 hr 15 min` |
| Dates | `Mar 4` / `Mar 4, 2026`; never numeric-only, it is ambiguous across locales |
| Currency | symbol before, two decimals: `$12.50` |
| Ranges | en dash, no spaces: `9:00 AM–5:00 PM` |

## Words to avoid

| Avoid | Because | Use |
|---|---|---|
| `Error`, `Failed`, `Invalid` as the opening word | names the failure before the fix | what to do |
| `Please` | pads without adding meaning | drop it |
| `Sorry` | apologises where the product should act | state the fact and the next step |
| `Oops`, `Uh-oh` | jokes at the user's expense during failure | plain statement |
| `Simply`, `just`, `easy` | tells the user their difficulty is their fault | drop |
| `Are you sure?` | asks about certainty instead of stating consequence | name what will happen |
| `Submit`, `OK` | technical operation, not a result | the verb of the outcome |

## Person and voice

Second person for the user (`your shift`), active voice, present tense. The product does
not refer to itself as `we` in interface text — that voice belongs to this skill's outbound channels.

## Length

| Element | Budget |
|---|---|
| Button | 1–3 words |
| Label | 1–4 words |
| Error | one sentence |
| Empty state heading | up to 6 words |
| Empty state body | up to 2 sentences |

### Budget against the worst string, not the average one

"Other languages run about 30% longer" is the **median**, and layout does not break on the
median string. Measure the project's own catalogue instead of quoting a rule of thumb —
it takes one command and the answer is specific to the locales actually shipped:

```python
import json, glob, os, statistics
en = json.load(open('<source catalogue>'))
base = {k: v for k, v in en.items()
        if not k.startswith('@') and isinstance(v, str) and 0 < len(v) <= 40}
for f in sorted(glob.glob('<catalogue glob>')):
    d = json.load(open(f))
    r = [len(d[k]) / len(base[k]) for k in base if isinstance(d.get(k), str) and d[k]]
    if r:
        print(os.path.basename(f), f"median x{statistics.median(r):.2f}",
              f"p90 x{sorted(r)[int(len(r)*.9)]:.2f}")
```

Measured on one catalogue, 2764 short strings, six target locales: median expansion 1.17
to 1.32, **p90 expansion 1.75 to 1.86**, and one locale that *contracts* to a third of the
source length. Budgeting at the median there under-reserves by half; budgeting at the p90
is the number that holds.

Three consequences:

| | |
|---|---|
| **Size layouts at the p90, not the median** | the string that breaks the screen is the long one, and there are always some |
| **A contracting locale is also a finding** | a control sized for an expanding language looks empty in one that contracts, and centred single words look like a mistake |
| **A right-to-left locale mirrors** | directional wording — "on the left", a leading symbol carrying meaning — breaks; describe by name, never by position |

A button at the top of its budget in the source language will break the layout in
translation. Where a string is near its limit, say so with the measured multiplier rather
than as a caution.
