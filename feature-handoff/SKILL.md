---
name: feature-handoff
description: Accepts your own work before the PR — traces every requirement to where it is implemented and what proves it, runs the self-review checklist, builds a manual test plan, enumerates ways to break the feature, finds regression risk, checks PII in logs and analytics integrity, and states plainly what is not done. Use when work feels finished but the PR is not open. Writes .dev-agent/features/<slug>.handoff.md. Триггеры — "готово ли", "приёмка перед PR", "что я забыл", "чем это можно сломать", "регресс", "PII в логах", "чек-лист проверки".
---

# Feature Handoff

Answers the question a developer answers "yes" to and is wrong: **did I actually finish?**

## Language

Answer in the language the request was written in. Findings, explanations, questions,
reports and section headings you produce for a developer follow their language — Russian
request, Russian answer.

**Text destined for the product's users is exempt.** Interface strings, release notes,
store listings and email stay in the product's interface language, taken from
`.dev-agent/config.yaml` → `interface.language`, whatever language the request used.
Mixing the two — an English report about Russian button labels, or the reverse — is the
failure this rule prevents.

## Answer in the conversation, not only in the file

The developer reads the chat. The artifact is for the skills downstream. Lead with what
was asked, in this order:

1. **The answer** — what to do, as a recommendation, not a menu
2. **What blocks it** — decisions only they can make, each carrying your recommended
   option and the reason for it
3. **The cost of being wrong** — for anything decided on their behalf
4. **Where the detail lives** — one line naming the artifact

Never open with what you verified, which reference files you read, or how you reconciled
your own numbers. That is the record of your process, not the answer to their question.
Evidence belongs attached to the claim it supports, never in the headline.

A developer who reads only the first ten lines must be able to act.

**Headline for this skill:** what is not done, then what to test before the PR.

## Evidence before claims

Inherited whole from `verification-before-completion`, and no softer here:

```
NO LINE IN THIS REPORT SAYS "CHECKED" WITHOUT EVIDENCE ATTACHED
```

Evidence is command output, a file path with a line number, or a screenshot. Not "I
looked at it", not "it should work", not "the tests cover this".

| Excuse | Answer |
|---|---|
| "obviously covered" | show the line |
| "tests pass" | which test, and what it asserts about this requirement |
| "I checked earlier" | paste that output |
| "it's a small change" | small changes ship the regressions |
| "the agent said it was done" | check the diff yourself |

## The not-done section is mandatory

The report carries a **Not done** heading and may not leave it empty by default. An empty
one is allowed only with a sentence explaining why coverage is genuinely complete.

Silence about a gap reads as absence of a gap. Every reviewer downstream then assumes the
gap was considered and dismissed, which is exactly the misunderstanding this section
exists to prevent.

## Automation before manual

Before writing a line into the manual checklist, ask whether a command could assert it.
If it could, give the command instead. A manual checklist is what remains after
automation has been exhausted — not the first place to put a check.

## Phases

### 1. Load the requirements
Read `.dev-agent/features/<slug>.intake.md`. Absent — say so, work from the task
description, and mark the traceability **incomplete** rather than inventing what was
asked.

*Done when:* every acceptance criterion from intake is listed, or the absence of intake is
stated.

### 2. Trace
One row per requirement: **requirement → where implemented → what proves it**. Anything
without an implementation or without proof goes in its own list.

*Done when:* no row has an empty third column. An empty third column is an uncovered
requirement wearing a checkmark.

### 3. Self-review
**Read `references/self-review.md` before this phase** — what tasks of this shape
typically forget.

*Done when:* every checklist item is answered or marked not applicable with a reason.

### 4. Break it
**Read `references/breaking.md` before this phase.** Concrete scenarios with steps, not a
generic list.

*Done when:* at least eight scenarios exist, each naming inputs and the expected
behaviour.

### 5. Regression
What else depends on what changed. Start from the diff, follow imports and shared state.

*Done when:* each changed shared file has its dependants listed, with the command that
found them.

### 6. Analytics
Compare against `.telemetry/tracking-plan.yaml`: did existing events break, are new ones
recorded. No plan — say so and name what that costs.

*Done when:* the state of the plan is stated and the diff's effect on events is answered.

### 7. Privacy
**Read `references/pii-patterns.md` before this phase.** Run the searches. Paste the
output — including empty output, which is a result.

*Done when:* every pattern has been run and its output shown, and deletion and export
behaviour for new data is answered.

### 8. Write
`.dev-agent/features/<slug>.handoff.md`, ending with **Not done**.

*Done when:* the report contains no claim without evidence and the not-done section
exists.

## Non-goals

- Code quality, architecture, performance — other tools do that.
- Opening the PR or writing its description: `outbound-writing`.
- Visual and UX quality: `screen-review`.
- **Fixing.** The skill produces the list; the developer edits — unless asked otherwise.
- Legal conclusions about data: raise the flag, phrase the question.
