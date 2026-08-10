# Style rules

Read before phase 2. Decided once here so no string re-argues them. English, US.

## Capitalisation

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
not refer to itself as `we` in interface text — that voice belongs to `outbound-writing`.

## Length

| Element | Budget |
|---|---|
| Button | 1–3 words |
| Label | 1–4 words |
| Error | one sentence |
| Empty state heading | up to 6 words |
| Empty state body | up to 2 sentences |

German and French run roughly 30% longer than English, and Hebrew reverses direction.
A button at the top of its budget in English will break the layout in translation.
