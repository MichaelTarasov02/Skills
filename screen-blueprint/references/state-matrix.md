# State matrix

Read before phase 2. Seven states. Each is answered or marked not applicable **with a
reason**. Systematic enumeration adapted from `deliver-edge-cases`, narrowed from
"what can go wrong with the feature" to "what is on the screen right now".

## The seven

| State | Occurs when | Answer these |
|---|---|---|
| **Success** | data arrived, user has access | what is shown; what the primary action is |
| **Loading** | request in flight, nothing to show yet | skeleton or spinner; is the layout preserved; is any action available |
| **Partial** | some data arrived, some failed or is still coming | what renders now; how the missing part is marked; can the user act on what is there |
| **Empty** | request succeeded, result set is zero | **which of the three** (below); what the user does next |
| **Error** | request failed | is it on the screen or a toast; is there retry; is input preserved |
| **Offline** | no connection | what is cached; what is blocked; how the user learns it is back |
| **No access** | authenticated but not permitted | what is shown instead; who grants access; where the user goes |

## Empty is three states, not one

The most common blueprint defect. Each needs a different screen.

| Kind | Cause | Screen shows |
|---|---|---|
| Nothing created yet | the collection has never had members | what the collection is for, and the creating action |
| Filter matched nothing | filters exclude everything | which filter is responsible, and a way to clear it |
| Nothing visible to you | scope or permission limits the result | that access is the cause, and who grants it |

A single "No data" covers all three and helps in none. Component kits supply exactly that
by default — `a-table` renders `No Data` with no configuration, which is how a screen
ships all three states unanswered while looking finished.

## Error deserves a screen, not only a toast

A toast disappears and leaves an empty region behind. Decide explicitly:

| Failure scope | Placement |
|---|---|
| the screen's main data failed | in-screen error state, with retry |
| one action failed, screen still valid | toast or inline, with retry |
| the failure is terminal (no access, gone, version too old) | dead-end state with a way out |

Retry is part of the state. An error message with no retry affordance hands the problem
back to the user without a tool.

## Dead ends

No access, account suspended, resource deleted, client too old. Each needs: what is
shown, why, and the one action that leads somewhere. A dead end without an exit is where
sessions end.

## Optimistic updates

Only when the operation almost always succeeds and the rollback is visible. Answer:

- what appears immediately
- what marks the pending state
- what happens on failure — and where the user's input is while that happens
- whether a retry is automatic or offered

Input loss on rollback is the failure that makes users distrust an interface permanently.

## Long and background operations

| Duration | Requires |
|---|---|
| over 5s | progress, and what is happening |
| over 30s | whether the user may leave the screen |
| leaves the screen | how completion is announced |

## Concurrency

Double submit, stale response arriving after a newer one, two people editing the same
record, data changing between load and save. Each either has an answer or is stated as
accepted risk.

## Marking a state not applicable

Legitimate: a screen with no remote data has no offline state; a screen everyone may see
has no no-access state. The reason is written down. An unmarked state is an unanswered
one, and unanswered states are what this skill exists to prevent.
