# String patterns

Read before phase 2. Each entry gives the **shape** of a string. Filling it is the work;
copying the example is not.

## Actions

`<verb of the outcome> <object>` — name what the user gets, not what the system does.

| Situation | Shape | Example |
|---|---|---|
| Primary action | outcome verb + object | `Start shift` |
| Destructive | the destructive verb, never softened | `Delete document` |
| Cancel out of a form | `Cancel` alone; never `No` | `Cancel` |
| Dismiss information | `Close`, `Got it` | |

Always offer 2–3 alternatives with one recommended. The recommendation names its reason:
which is shorter, which matches the lexicon, which survives translation.

## Field labels, hints, placeholders

Three different things:

| Slot | Holds | Never |
|---|---|---|
| Label | what the field is, always visible | disappears on focus |
| Hint | the constraint, shown before the user types | repeats the label |
| Placeholder | an example value only | replaces the label |

`Phone number` (label) · `10 digits, US numbers only` (hint) · `555 123 4567`
(placeholder).

## Validation errors

`<what is wrong> + <how to fix it>`. Never open with `Error` or `Invalid`. Never blame.

| Wrong | Right |
|---|---|
| `Invalid phone number` | `Phone number must be 10 digits` |
| `Error: field required` | `Enter your phone number` |
| `You entered a bad date` | `Choose a date after today` |

One string per rule, not one string per field — a field with three rules needs three
messages, or the user fixes one thing and fails again.

## Server and network errors

`<what happened in user terms> + <what they can do now>`. Never surface a status code.

| Situation | Shape |
|---|---|
| 401/403 | what they lack access to + who grants it |
| 404 | what is gone + where to go instead |
| 5xx | that it is the product's side + retry affordance |
| Timeout | that it is taking too long + retry |
| Offline | that the device has no connection + what is saved |

Never state when it will be fixed. That is a red line.

## Empty states — three different texts

| Cause | Heading names | Body | Action |
|---|---|---|---|
| Nothing created yet | the opportunity | what this list is for | the creating action |
| Filter matched nothing | that the filter is the cause | which filter to relax | clear the filter |
| No permission | that access is the cause | who can grant it | none, or contact |

Using one text for all three is the most common empty-state defect: the user who filtered
too narrowly gets told to create their first item.

## Confirmation dialogs

Title states the consequence, not the question. Body names what is lost and whether it
returns. Buttons name actions.

```
Delete this document?
The document and its signatures are removed permanently. This cannot be undone.
[Delete document]  [Cancel]
```

Never `Are you sure?`. Never `Yes` / `No`.

## Success and toasts

First decide whether a message is needed at all. If the result is visible on screen, it
is not. When it is needed: state what happened, in the past tense, without exclamation.
Add an undo affordance where the action is reversible.

## Loading and long operations

| Duration | Text |
|---|---|
| under 1s | none |
| 1–5s | none, or the noun of what is loading |
| over 5s | what is happening and why it takes time |
| over 30s | progress, plus whether the user may leave the screen |

## Permission prompts

Shown before the system dialog, never after. Names the feature that needs the permission,
what happens with it, and what still works without it. A pre-permission screen that only
says "we need location access" wastes the one chance the OS gives.

## Limits and paywalls

State the boundary as fact, name the current usage, name the way forward. No urgency, no
pressure, no countdown.

## Legally sensitive text

Write the human sentence, then flag it. The flag is part of the deliverable:

```
⚖️ Needs legal review — states a statutory requirement about meal breaks
```

Quote the requirement rather than asserting compliance on the product's behalf.
