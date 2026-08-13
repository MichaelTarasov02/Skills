# Inward-facing documents

## Feature documentation

Written for the person who gets paged at 3am and has never seen this code.

```markdown
## Complete sequence flow

## What it does
Finishes a document sequence and marks the project step complete.

## How to turn it off
`environment.dart` → `sequenceCompletionV2` — false restores the previous flow.

## Configuration
`constants.dart` → `sequenceCompleteTimeout` (ms)

## Limits
- one sequence completes at a time per device
- offline completion queues; conflicts resolve server-side, last write wins

## When it breaks
| Symptom | Likely cause | First check |
|---|---|---|
| completion hangs | repository never confirms | server logs for POST /sequence/complete |
| page bounces to project list | the pre-fix behaviour | which build the user is on |
```

The order matters: **how to turn it off comes second**, before configuration and before
explanation. At 3am the reader wants the switch, not the design.

## Demo script

Two minutes, and the hard part is the starting state.

```markdown
## Setup (do this before the call)
Account: demo-manager · Project: "Warehouse 4" with one incomplete sequence

## Script
1. Open the project → the sequence shows two unsigned documents (5s)
   Say: "before, finishing here dropped you back to the project list"
2. Sign both → completion runs (30s)
   Say: "the app waits for confirmation before moving on"
3. Land on the completed sequence (10s)
   Say: "you stay where you were, and the state is confirmed"

## If it fails
Fall back to the staging recording — the completion call needs the server up.
```

Three things people forget and the script must carry: the starting state, what to say
while something loads, and what to do when it fails live.

Wall-clock timings per step, not "briefly". A demo overruns because two steps quietly took
forty seconds each.

## Both documents

Facts only. Neither is a place for a date, a promise, or an assessment of whether the
feature was a good idea.
