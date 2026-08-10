# Strings in Flutter

Read before phase 3.

## Where they live

`lib/l10n/intl_<locale>.arb`. `intl_en.arb` is the source; a new key must be added there
first, then to every other locale file or the build reports it missing.

This project carries **seven locales**: en, es, fr, he, ru, tl, zh. `he` is right-to-left.

## Key naming

Follow the convention already in the file rather than importing one. The existing
convention is `<subject><Detail><Type>` in lower camel case, with the type suffix naming
the slot:

```
enterPhoneNumberText
invalidPhoneNumberErrorMessage
estimatedLunchTimeText
```

Suffixes in use: `Text`, `ErrorMessage`, `Title`, `Description`, `Hint`.

**The key must agree with the value.** A key named `*Lunch*` holding the string
`Meal break` is a defect that outlives everyone who remembers it — this repository has
140 of them. When adding a key near an existing drift, use the canonical term from
`lexicon.md` and report the drift rather than extending it.

## Translator context

ARB carries it in the `@key` sibling. Fill `description`, and `placeholders` for every
interpolation:

```json
{
  "mealBreakRemainingText": "You have {minutes} left in your meal break",
  "@mealBreakRemainingText": {
    "description": "Countdown shown on the active shift screen during a meal break",
    "placeholders": { "minutes": { "type": "int", "format": "compact" } }
  }
}
```

Without `description` the translator sees a bare sentence and guesses the context.

## Plurals

ICU `plural`, never string concatenation and never an `if` in Dart:

```json
{
  "shiftsCompletedText": "{count, plural, =0{No shifts completed} =1{1 shift completed} other{{count} shifts completed}}"
}
```

`=0` earns its own branch whenever the zero case reads badly as a plural.

## Concatenation

Assembling a sentence from fragments at runtime is untranslatable — word order differs by
language, and in Hebrew the direction differs too. One idea, one key, with placeholders.

## RTL

Hebrew mirrors the layout. Text written for a left-to-right reading order — anything that
says "on the left" or relies on a leading symbol — breaks. Keep directional language out
of strings entirely; describe by name, not by position.
