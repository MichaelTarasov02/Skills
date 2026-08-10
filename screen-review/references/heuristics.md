# Usability heuristics

Read before phase 1.

**Provenance:** `dembrandt/dembrandt-skills@nielsen-usability-heuristics` (323 installs)
was recommended for this and is **not installed** — installing needs the user's explicit
consent. This checklist was written instead, from Nielsen's ten heuristics as published,
narrowed to what applies to a single screen. If that skill is installed later, compare
and keep one source rather than two.

The purpose is to convert "this feels unclear" into a named violation. An impression
cannot be argued with or prioritised; a violation can.

| # | Heuristic | Ask of this screen |
|---|---|---|
| 1 | **Visibility of system status** | after any action, does the user know what happened? Is a request in flight visible? Is a saved change confirmed? |
| 2 | **Match to the real world** | do the words match what the user calls these things — checked against `lexicon.md`, not against the code |
| 3 | **User control and freedom** | is there a way out of every state? Can a destructive action be undone or, failing that, confirmed with its consequence named? |
| 4 | **Consistency and standards** | does the same thing look and behave the same as on neighbouring screens? Is the primary action in the usual place? |
| 5 | **Error prevention** | is the invalid state reachable at all? Preventing it beats reporting it |
| 6 | **Recognition over recall** | must the user remember something from a previous screen to use this one? |
| 7 | **Flexibility and efficiency** | can a frequent user move faster — keyboard, defaults, remembered filters? |
| 8 | **Aesthetic and minimalist design** | does anything on the screen compete with the primary action without earning it? |
| 9 | **Help users recover from errors** | does each error say what happened and what to do, in the user's words, with the action available? |
| 10 | **Help and documentation** | where explanation is needed, is it at the point of need rather than in a manual? |

## Using it

Walk the screen once per heuristic. Most yield nothing on most screens — that is expected.
A finding cites its number: *"violates 1 — the export button gives no indication the file
is being generated"* is reviewable; *"unclear feedback"* is not.

## Text or a simpler screen

Heuristics 8 and 10 pull against each other, and the tension is where the most valuable
finding usually sits.

When explanation accumulates around one control, the control is the problem. Three
sentences telling the user what a toggle does means the toggle is named wrong, placed
wrong, or should not be a decision they make. Adding the text hides the defect and makes
it permanent — every later reader assumes the explanation was always necessary.

State it as: *the copy is compensating for X; the cheaper fix is Y*.

## Two ranking questions

Neither is a heuristic, both decide rank:

- **Can the user still finish?** No — blocking.
- **Will they be wrong about what happened?** Yes — blocking, even if the screen renders
  fine. A silent failure that looks like success outranks anything cosmetic.
