# Push and in-app notifications

## Budget

| | Title | Body |
|---|---|---|
| iOS | ~40 chars visible | ~110 chars on the lock screen |
| Android | ~50 chars | ~100 chars collapsed |

Beyond that it truncates without warning. Write to the smaller of the two and stop.

## Structure

Subject, verb, and the reason it is worth interrupting someone. The notification says what
happened and what waits; the app says the rest.

```
Meal break starts in 5 minutes
Sign in to record it before the window closes.
```

Not `Reminder` and not `You have a new notification` — both spend the interruption on
nothing.

## Frequency and grouping

Every notification needs an answer to: **what if five arrive at once?**

| Situation | Behaviour |
|---|---|
| Several of the same kind | collapse into a count, not five lines |
| Several kinds at once | one per kind, with a cap |
| The user has not opened the previous one | do not send the next of the same kind |

Grouping is part of the copy, not a platform detail. A grouped notification needs its own
text (`3 shifts need signing`), and if it has not been written, the app will show the last
one and hide the rest.

## Timing

A work-tracking product sends into people's actual shifts. Anything not tied to a moment
that matters to the recipient waits for working hours in **their** timezone — which this
product knows, and should use.

Never send during a meal break to say a meal break is happening.

## What a push may never carry

The lock screen is visible to anyone near the phone. Never in a notification: amounts,
document contents, health or compliance detail, disciplinary matters, another person's
name.

`A document needs your signature` is right. `Your disciplinary notice is ready` is a
disclosure to whoever is standing nearby.

## In-app

Same text, different constraints: more room, no lock-screen exposure, and the user is
already present — so an in-app message must justify interrupting what they came to do.
If the information can wait for the screen they are heading to, it is not a notification.
