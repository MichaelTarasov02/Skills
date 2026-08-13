---
name: verify-contact-book
description: This skill should be used before handing a lead list to anyone, to run integrity checks against the contact book and produce a coverage report that states what was found, what is missing, and what no open source can supply. Triggers on "is this list any good", "check the contact book", "how complete is this", "coverage report", "проверь базу", "насколько полная база", "отчёт о покрытии". It reports per-role percentages with the SQL that produced them, so the numbers can be re-derived.
---

# Verify contact book

Two outputs, and the second is the one that gets skipped. **Integrity** answers whether the
book is internally sound. **Coverage** answers what fraction of the target it reaches, and
which part no open source reaches at all.

An honest gap tells the user where to spend money instead of where to waste calls.

## Integrity checks

Run every check. Each returns a count that should be zero unless noted.

| Check | Query shape |
|---|---|
| Organisation ID unique | `COUNT(*) - COUNT(DISTINCT org_id)` on `organization` |
| Every person carries a source | `person WHERE source_id IS NULL OR source_id = ''` |
| Every person carries confidence | `person WHERE confidence NOT IN ('high','medium','low')` |
| No orphan people | `person LEFT JOIN organization` where the org is missing |
| Gap table complete | `COUNT(*)` on `field_status` equals organisations × target roles |
| `found` is backed by a person | `field_status` rows marked found with no matching `person` |
| `not_found` hides nobody | `field_status` rows marked not_found with a matching `person` |
| Signals carry a match level | `signal WHERE match_level IS NULL` |

A failing check gets fixed in the loader and re-run. Reporting a known-broken book as
delivered is the one outcome this skill exists to prevent.

## Idempotence

Run the whole pipeline a second time and compare table counts before and after. Equal counts
mean the loaders upsert correctly; growing counts mean a natural key is missing somewhere and
the book will duplicate on every refresh.

Paste both count sets into the report.

## Manual spot check

Pick five organisations and trace every person on them back to the source record. Automated
checks confirm the book is consistent; only reading the source confirms it is true.

Cross-source agreement is the strongest evidence available here — when two unrelated
registers name the same person for the same role, that row is solid.

## Coverage report

Write `leads/<slug>/COVERAGE.md`:

```markdown
# Coverage: <name>
Generated: <ISO date>
Organisations: N · people: N · unique people: N

## Sources
| Source | Tier | Data date | Retrieved | Records |

## Coverage by role
| Role | Named | % | Mailbox only | No data |

## Coverage by segment
| Segment | Orgs | one column per role |

## Contactability
| Cut | Orgs |
| Named decision-maker + email | |
| Named decision-maker + phone | |
| Any high or medium confidence name | |

## Integrity
| Check | Result | Pass/Fail |

## Idempotence
Before: ... After: ...

## Out of reach from open sources
<role or segment — which register would hold it, and what access costs>
```

The last section is the deliverable most worth writing. Name the role, the register that
would hold it, and the price of access — a public-records request, a paid licence, or manual
lookup. That paragraph is what turns a disappointing number into a decision.

**Done when** every integrity check appears in the report with its result, the before/after
idempotence counts are pasted, the five-organisation spot check is reported with its error
count, and every role below 20 percent coverage has a named route in the out-of-reach
section.
