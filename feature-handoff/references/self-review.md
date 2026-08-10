# Self-review checklist

Read before phase 3. What tasks of each shape typically forget. Each item is answered or
marked not applicable **with a reason**.

## Any change

- [ ] Every acceptance criterion from intake traced to code
- [ ] Errors handled where the happy path was written
- [ ] Nothing left behind: debug logs, commented code, hard-coded test values
- [ ] New strings extracted, not inline — and on mobile, added to **all seven** locale files
- [ ] Feature flag or config: default value correct for production
- [ ] Migration written and reversible, if the schema moved

## New screen

- [ ] All states from the blueprint implemented — check against
      `.dev-agent/screens/<slug>.blueprint.md`, do not recall them
- [ ] Route guarded by permission
- [ ] Back path leads somewhere sensible
- [ ] Interactive elements have accessible names
- [ ] Analytics events fire where the plan says

## Changed API

- [ ] Older clients still work — mobile releases stay in the wild for weeks
- [ ] Response shape change is additive, or versioned
- [ ] Errors returned in the shape the client already parses
- [ ] Timeouts and retries on the client side match the new latency

## New data field

- [ ] Deletion path: what happens when the account is deleted
- [ ] Export path: does it belong in the data export
- [ ] Not logged, not attached to crash or analytics context
- [ ] Nullable for existing rows, or backfilled

## Touching time or location

This product records when and where work happened; both carry more weight here than in a
typical CRUD feature.

- [ ] Stored in UTC, displayed in a stated zone
- [ ] Device clock not trusted for anything authoritative
- [ ] Location absence handled — denied, indoors, hardware off
- [ ] Daylight-saving transitions do not shift a recorded shift

## Touching payroll or compliance

- [ ] Numbers reconcile with the existing calculation, not just with themselves
- [ ] Rounding rule matches what payroll already does
- [ ] The record is auditable: who changed what, and when
- [ ] Legal review flagged if the change alters what is reported about a person

## Before writing the report

Run the diff once more and ask a single question of each changed file: **why is this file
in the diff?** A file nobody can justify is either dead work or an unintended change, and
both are cheaper to find now.
