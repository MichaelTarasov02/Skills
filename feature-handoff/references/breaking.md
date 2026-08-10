# Breaking the feature

Read before phase 4. Systematics adapted from `deliver-edge-cases`, narrowed from
cataloguing a feature's failure surface to attacking a finished implementation.

A scenario names **inputs, steps, and the expected behaviour**. "Test error handling" is
not a scenario.

## The eight that pay off most

| # | Attack | Steps | Usually broken because |
|---|---|---|---|
| 1 | Double submit | click the action twice within 300ms | the guard is on the button's visual state, not on the request |
| 2 | Stale response | start a request, change the filter, let the first response arrive last | responses are applied in arrival order, not request order |
| 3 | Mid-flight disconnect | begin the action, drop the network before the response | the UI stays in the pending state forever |
| 4 | Back after submit | submit, then navigate back | the form re-renders populated and resubmits |
| 5 | Session expiry | let the token die, then act | the failure is indistinguishable from a server error, and input is lost |
| 6 | Concurrent edit | two sessions edit the same record | last write wins silently |
| 7 | Boundary volume | zero rows, then ten thousand | pagination absent; the empty case falls into a default |
| 8 | Permission change under foot | revoke the right while the screen is open | the screen keeps working from stale state |

## Platform additions

**Web**
- reload mid-flow — what survives
- two tabs on the same record
- browser back with unsaved input
- deep link straight into a mid-flow state

**Mobile**
- backgrounded mid-action, then resumed
- killed by the OS, then reopened
- offline action, then reconnect — what syncs and who wins the conflict
- OS permission revoked in settings while the app runs
- device clock wrong or manually changed — this product records **when** work happened,
  so a wrong clock is a data-integrity attack, not a curiosity

## Ranking the scenarios

| Rank | Meaning |
|---|---|
| Must test | data loss, wrong data written, a state with no way out |
| Should test | recoverable but visible failure |
| Note | theoretically reachable, low impact |

Data corruption outranks a broken screen. A screen that fails visibly is annoying; a
silent wrong write is discovered weeks later by someone who trusted it.

## What the developer will resist

The scenarios most likely to be dismissed as unrealistic are 2 and 6 — stale responses
and concurrent edits. Both are invisible in single-user testing and both corrupt data in
production. Keep them, and state what they cost rather than arguing about likelihood.
