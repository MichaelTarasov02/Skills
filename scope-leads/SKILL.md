---
name: scope-leads
description: This skill should be used when someone asks for leads, prospects, or a contact list and the ask is still vague — "find me leads", "build a lead list", "who are the decision makers at X", "I need contacts for a campaign", "найди лидов", "собери контакты", "нужна база по", "кто принимает решения". It interrogates one question at a time until eight brief fields are locked, then hands the brief to find-sources. Start every lead-generation run here; a run that skips the brief collects the wrong people.
---

# Scope leads

This skill produces the **brief**: eight locked fields that every later stage reads.

## How to ask

One question at a time. Wait for the answer before asking the next.

Recommend an answer with each question — a proposal gets corrected faster than a blank gets
filled.

Look up what the environment can tell you. Ask only what lives in the user's head: the
decisions, the constraints, the definition of a good lead.

## The eight fields

Fill each one. A field the user genuinely cannot answer gets written down as `open` with the
consequence spelled out, so the gap is visible rather than silently guessed.

| # | Field | What it decides | Ask it like |
|---|---|---|---|
| 1 | **Who buys** | the organisation type | "What kind of organisation writes the cheque?" |
| 2 | **Who decides** | which roles to collect | "Which job titles sign off, and who blocks it?" |
| 3 | **Where** | geography and jurisdiction | "Which countries, states, or metros?" |
| 4 | **How many** | whether a sample or a census | "Do you need 50 good ones or everyone who qualifies?" |
| 5 | **Signal** | what makes them a lead now | "What must be true about them today for this to land?" |
| 6 | **Exclusions** | who to drop | "Who is already a customer, competitor, or out of scope?" |
| 7 | **Channel** | which contact fields matter | "Email, phone, LinkedIn, or a mailing address?" |
| 8 | **Freshness** | rebuild cadence | "How stale can this be before it hurts?" |

### Field 5 carries the most weight

**Signal** is what separates a directory dump from a lead list. It is the observable fact that
makes someone worth contacting today: a lawsuit, a funding round, a hiring surge, an
enforcement action, an expiring licence, a new location, a leadership change.

When the user names a signal, push until it is **observable in a source**, not a mood.
"Companies struggling with payroll" is a mood. "Companies with a wage-and-hour claim filed
since 2023" is a signal — something a record either shows or does not.

A signal-driven run continues into `find-signal-leads` after the contact book exists. A run
with no signal stops at `build-contact-book`.

## Guardrails to settle inside the brief

Raise these while scoping, not after the data is collected:

- **Jurisdiction.** Contact data on EU residents falls under GDPR; California's B2B exemption
  under CCPA/CPRA expired 1 January 2023, so work email and direct phone are personal data
  there. Record which regime applies in field 3.
- **Consent-gated channels.** Cold calling faces TCPA and Do-Not-Call in the US; email faces
  CAN-SPAM. Record in field 7 which channels the user is actually cleared to use.

Write the answer into the brief. The user owns the risk decision; the brief owns the record
of what was decided.

## Output

Write `leads/<slug>/brief.md`, where `<slug>` is a kebab-case name for this run.

```markdown
# Brief: <name>
Created: <ISO date>

| Field | Answer |
|---|---|
| Who buys | |
| Who decides | |
| Where | |
| How many | |
| Signal | |
| Exclusions | |
| Channel | |
| Freshness | |

## Definition of a good lead
<one sentence the user agreed to>

## Open questions
<field name — what was assumed instead, and what breaks if the assumption is wrong>

## Legal notes
<jurisdiction, channels cleared>
```

**Done when** `leads/<slug>/brief.md` exists with all eight rows filled — `open` counts as
filled only when the consequence is written beside it — and the user has confirmed the
one-sentence definition of a good lead verbatim.

Then read `find-sources`.
