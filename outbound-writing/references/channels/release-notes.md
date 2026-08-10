# Release notes and store listings

> **Examples below are shapes, not facts about your codebase.** Field names, counts and
> paths in them are illustrative and were true of one repository at one moment. Measure
> before you quote any of them. A reference file that hands you a number is handing you a
> hypothesis.


## Two versions, produced together

| Version | Reader | Contains |
|---|---|---|
| **User** | someone deciding whether to update | what they can now do that they could not before |
| **Internal** | the team | what shipped, what to watch, what rolled back |

The internal version may name tickets, files and risks. The user version may not.

## Deriving from commits

```bash
git log --oneline <previous-build>..<this-build>
```

Category per commit, from Conventional Commits where the repo uses it:

| Prefix | User-facing? | Category |
|---|---|---|
| `feat:` | usually | Added |
| `fix:` | usually | Fixed |
| `EPEOPLE-NNNN` | read the diff — the ticket id says nothing about visibility | depends |
| `build:`, `chore:`, `refactor:` | no | internal only |

This repository tags most work with a bare ticket id, so the prefix cannot classify it.
**Read the diff.** A change touching `lib/features/*/pages/` is user-visible; one touching
`lib/data_sources/` usually is not.

## The failure this file exists to prevent

The current default store text reads:

> "This update brings a bunch of behind-the-scenes fixes and tweaks… Nothing flashy to
> call out, just lots of little upgrades working together…"

It survives every release because it fits every release. It also tells the reader nothing,
in seven languages. A user deciding whether to update learns exactly as much as from a
blank field.

The replacement rule: **name one thing that changed for the user, or say plainly that this
build is fixes only and name what area they touch.** "Fixes to shift signing and project
loading" is short, true, and worth reading. "Lots of little upgrades" is neither.

## Store listing constraints

Store notes live in `DEFAULT_RELEASE_NOTES.md` / `RELEASE_NOTES.md`, split `# ANDROID` and
`# iOS`, with one block per locale.

| | |
|---|---|
| Google Play | 500 characters per locale |
| App Store | 4000 characters, but only ~3 lines visible before "more" |
| Locales | seven, and **the codes differ from the ARB files** |

| ARB file | Store tag |
|---|---|
| `intl_he.arb` | `<iw-IL>` |
| `intl_tl.arb` | `<fil>` |
| `intl_es.arb` | `<es-ES>` |
| `intl_fr.arb` | `<fr-FR>` |
| `intl_ru.arb` | `<ru-RU>` |
| `intl_zh.arb` | `<zh-CN>` |
| `intl_en.arb` | `<en-US>` |

`he` → `iw-IL` and `tl` → `fil` are the two that get mistyped; both are legacy codes the
stores still require. A wrong tag means that locale silently falls back to English.

Put the most important line first — on both stores the rest is behind a tap.

## Structure

```markdown
## What's new — 4.46.0

Shift signing now completes without returning to the project list.

Also fixed: project data loading on slow connections.
```

Two or three lines. Categories only when there is more than one item per category —
a heading over a single bullet is scaffolding.

## Internal version

```markdown
## 4.46.0 (287)

EPEOPLE-8815 — complete sequence flow
- complete_sequence_cubit.dart +91; sequence_repository.dart +50
- also touched: constants.dart, environment.dart — shared, regression risk
- watch: document signing from an alert, resignation flow

feat: project_data_source — full project fetch
```
